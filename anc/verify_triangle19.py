#!/usr/bin/env python3
"""Exact arithmetic audit for the refutation of the 19-triangle tiling.

The accompanying proof uses published classification/rationality theorems and
then reduces the remaining 120-degree cases to elementary arithmetic.  This
script independently checks the algebra in that new arithmetic reduction:

  * the trigonometric side identities, symbolically;
  * the four area-ratio formulas, symbolically modulo c^2=a^2+ab+b^2;
  * the factorization a+b=s(s+2t) from the complete primitive
    parametrization, giving an independent route to the prime obstruction;
  * the primitive gcd claims on 41,112 exact parametrized triples;
  * the finite p=19 exceptional candidates, as an extra audit.

All arithmetic is exact.  There is no floating-point computation.
This script does not re-prove the cited geometric classification theorems.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import sympy as sp


def assert_zero_mod_relation(
    expr: sp.Expr,
    relation: sp.Expr,
    variable: sp.Symbol,
    label: str,
) -> None:
    """Assert that a rational expression vanishes modulo a monic relation."""
    numerator = sp.together(expr).as_numer_denom()[0]
    remainder = sp.rem(sp.expand(numerator), relation, variable)
    if sp.simplify(remainder) != 0:
        raise AssertionError(f"{label}: nonzero remainder {sp.factor(remainder)}")


def symbolic_checks() -> None:
    a, b, c, m = sp.symbols("a b c m", positive=True)
    relation = c**2 - a**2 - a*b - b**2
    sqrt3 = sp.sqrt(3)
    K = 2*c/sqrt3

    # Sine-law and cosine-law data for tile angles
    # (alpha, beta, gamma=2*pi/3), opposite sides (a,b,c).
    sin_a = a/K
    sin_b = b/K
    sin_g = sqrt3/2
    cos_a = (a + 2*b)/(2*c)
    cos_b = (2*a + b)/(2*c)

    sin_ab = sin_a*cos_b + cos_a*sin_b
    cos_ab = cos_a*cos_b - sin_a*sin_b
    sin_2a = 2*sin_a*cos_a
    sin_2b = 2*sin_b*cos_b
    sin_a2b = sin_ab*cos_b + cos_ab*sin_b
    sin_2ab = sin_ab*cos_a + cos_ab*sin_a
    sin_3b = 3*sin_b - 4*sin_b**3

    identities = {
        "K sin(alpha+beta)=c": K*sin_ab - c,
        "K sin(2 alpha)=a(a+2b)/c": K*sin_2a - a*(a+2*b)/c,
        "K sin(2 beta)=b(b+2a)/c": K*sin_2b - b*(b+2*a)/c,
        "K sin(alpha+2 beta)=a+b": K*sin_a2b - (a+b),
        "K sin(2 alpha+beta)=a+b": K*sin_2ab - (a+b),
        "K sin(3 beta)=3ab(a+b)/c^2": K*sin_3b - 3*a*b*(a+b)/c**2,
    }
    for label, expr in identities.items():
        assert_zero_mod_relation(expr, relation, c, label)

    tile_sine_product = sin_a*sin_b*sin_g
    # (case label, K_T/K, outer sine product, claimed area ratio N)
    area_cases = [
        (
            "C: (alpha, alpha+beta, alpha+2beta)",
            m,
            sin_a*sin_ab*sin_a2b,
            m**2*(a+b)/b,
        ),
        (
            "B: (alpha, 2beta, 2alpha+beta)",
            m*c,
            sin_a*sin_2b*sin_2ab,
            m**2*(b+2*a)*(a+b),
        ),
        (
            "D: (2alpha, 2beta, alpha+beta)",
            m*c,
            sin_2a*sin_2b*sin_ab,
            m**2*(a+2*b)*(b+2*a),
        ),
        (
            "A: (alpha, 2alpha, 3beta)",
            m*c**2/a,
            sin_a*sin_2a*sin_3b,
            3*m**2*(a+2*b)*(a+b),
        ),
    ]
    for label, scale_ratio, outer_product, target in area_cases:
        computed = scale_ratio**2 * outer_product / tile_sine_product
        assert_zero_mod_relation(computed - target, relation, c, f"area formula {label}")

    # Independent symbolic route for the only non-obviously-composite case.
    # The complete primitive parametrization (Beeson, arXiv:2607.19572v1,
    # Theorem 6) has either (a,b)=(s^2-t^2,t(2s+t)) or the swapped pair.
    # In both branches:
    s, t = sp.symbols("s t", integer=True, positive=True)
    param_a = s**2 - t**2
    param_b = t*(2*s+t)
    assert sp.expand(param_a + param_b - s*(s+2*t)) == 0
    assert sp.expand(param_b + param_a - s*(s+2*t)) == 0

    print("symbolic trigonometric identities: PASS")
    print("symbolic area-ratio formulas:       PASS")
    print("symbolic prime-obstruction factor:  PASS")


def primitive_triples(limit: int) -> Iterable[tuple[int, int, int]]:
    """Generate primitive solutions via the two-branch parametrization.

    Branches per Beeson, arXiv:2607.19572v1, Theorem 6, over
    2 <= s <= limit, 1 <= t < s, gcd(s, t) = 1, s != t (mod 3);
    both labelings (a, b) and (b, a) are emitted (they never coincide,
    since a = b would force c^2 = 3a^2).
    """
    seen: set[tuple[int, int, int]] = set()
    for s in range(2, limit + 1):
        for t in range(1, s):
            if math.gcd(s, t) != 1 or (s - t) % 3 == 0:
                continue
            a = s*s - t*t
            b = t*(2*s + t)
            c = s*s + s*t + t*t
            for triple in ((a, b, c), (b, a, c)):
                if triple not in seen:
                    seen.add(triple)
                    yield triple


def gcd_sanity_checks(limit: int = 300) -> None:
    count = 0
    for a, b, c in primitive_triples(limit):
        count += 1
        assert c*c == a*a + a*b + b*b
        assert math.gcd(math.gcd(a, b), c) == 1
        assert math.gcd(a, b) == math.gcd(a, c) == math.gcd(b, c) == 1
        assert c % 3 != 0
        assert a + b > 1

        # Integer side-ratio vectors for cases C, B, D, A respectively.
        vectors = [
            (a, c, a+b),
            (a*c, b*(b+2*a), c*(a+b)),
            (a*(a+2*b), b*(b+2*a), c*c),
            (c*c, c*(a+2*b), 3*b*(a+b)),
        ]
        for vector in vectors:
            g = math.gcd(math.gcd(vector[0], vector[1]), vector[2])
            assert g == 1, (a, b, c, vector, g)

    print(f"primitive gcd sanity check ({count:,} triples): PASS")


@dataclass(frozen=True)
class ExceptionalCandidate:
    m: int
    b: int
    a: int
    c_squared: int
    lower_square: int
    upper_square: int


def finite_nineteen_check() -> list[ExceptionalCandidate]:
    """Extra direct audit of case C after setting N=19."""
    candidates: list[ExceptionalCandidate] = []
    for m in range(1, math.isqrt(18) + 1):
        b = m*m
        a = 19 - b
        c_squared = a*a + a*b + b*b
        c_floor = math.isqrt(c_squared)
        if c_floor*c_floor == c_squared:
            raise AssertionError(f"unexpected integral c for a={a}, b={b}, c^2={c_squared}")
        candidates.append(
            ExceptionalCandidate(
                m=m,
                b=b,
                a=a,
                c_squared=c_squared,
                lower_square=c_floor*c_floor,
                upper_square=(c_floor+1)*(c_floor+1),
            )
        )

    expected = [
        (1, 1, 18, 343),
        (2, 4, 15, 301),
        (3, 9, 10, 271),
        (4, 16, 3, 313),
    ]
    actual = [(x.m, x.b, x.a, x.c_squared) for x in candidates]
    assert actual == expected

    print("finite N=19 cross-check:")
    for x in candidates:
        print(
            f"  m={x.m}: (a,b)=({x.a},{x.b}), c^2={x.c_squared}, "
            f"{x.lower_square} < c^2 < {x.upper_square}"
        )
    print("finite N=19 cross-check:            PASS")
    return candidates


def main() -> None:
    symbolic_checks()
    gcd_sanity_checks()
    finite_nineteen_check()
    print(
        "\nARITHMETIC CORE VERIFIED: no remaining 120-degree branch "
        "can have a prime tile count; in particular N=19 is impossible."
    )


if __name__ == "__main__":
    main()
