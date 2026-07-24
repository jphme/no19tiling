Ancillary files for:

  "No triangle can be cut into nineteen congruent triangles:
   the prime case of Erdos Problem 634"
  Jan Philipp Harries, July 2026

Files
-----
verify_triangle19.py   Exact-arithmetic checks (SymPy) of the algebra in
                       Lemma 9 of the paper.
README.txt             This file.

Requirements
------------
Python >= 3.10 with SymPy installed.
Tested with Python 3.14.6 and SymPy 1.14.0.

Run
---
    python3 verify_triangle19.py

or, using uv:

    uv run --with sympy verify_triangle19.py

Runtime is under one second. Expected output:

    symbolic trigonometric identities: PASS
    symbolic area-ratio formulas:       PASS
    symbolic prime-obstruction factor:  PASS
    primitive gcd sanity check (41,112 triples): PASS
    finite N=19 cross-check:
      m=1: (a,b)=(18,1), c^2=343, 324 < c^2 < 361
      m=2: (a,b)=(15,4), c^2=301, 289 < c^2 < 324
      m=3: (a,b)=(10,9), c^2=271, 256 < c^2 < 289
      m=4: (a,b)=(3,16), c^2=313, 289 < c^2 < 324
    finite N=19 cross-check:            PASS

    ARITHMETIC CORE VERIFIED: no remaining 120-degree branch can have a
    prime tile count; in particular N=19 is impossible.

What is checked, and what that means
------------------------------------
The proofs in the paper are self-contained; this script provides
supplementary checks only. All arithmetic is exact (no floating point).

1. Exact symbolic checks. The six trigonometric identities (3) and the
   four area-ratio formulas of the table in Section 3 are verified with
   SymPy, modulo the relation c^2 = a^2 + ab + b^2 and in both labelings
   of the acute angles.

2. Finite stress tests. The primitivity (gcd) claims for the four side
   vectors are universal statements, proved in the paper. The script
   additionally tests them on 41,112 primitive solutions of
   c^2 = a^2 + ab + b^2, generated from the two-branch parametrization
   (Beeson, arXiv:2607.19572v1, Theorem 6):

       a = s^2 - t^2,  b = t(2s+t),  c = s^2 + st + t^2,

   and the same with a and b exchanged, over 2 <= s <= 300, 1 <= t < s,
   gcd(s,t) = 1, s != t (mod 3). The two labelings (a,b) and (b,a) are
   counted as distinct triples; they never coincide, since a = b would
   force c^2 = 3a^2. This gives 2 x 20,556 = 41,112 triples. A finite
   test is error detection, not a proof.

3. Finite N=19 cross-check. In case C the proof forces p = a + b and
   b = m^2; for p = 19 the script confirms that all four candidates
   (a,b) = (19 - m^2, m^2), 1 <= m <= 4, fail to make a^2 + ab + b^2 a
   perfect square.

4. Second route for case C. The script verifies a + b = s(s + 2t) on the
   parametrization; since s >= 2 and s + 2t >= 4, this makes a + b
   composite, independently excluding p = a + b.

The script does not re-prove the cited geometric classification theorems.
