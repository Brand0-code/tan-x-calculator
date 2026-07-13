"""
Unit tests for d2/tan_core.py (D3/Problem 8).

math is imported here ONLY as a reference oracle for expected values -
it is never imported by tan_core.py itself, which must stay from
scratch (see d2/tan_core.py's own docstring for that constraint).
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "d2"))

from tan_core import (  # noqa: E402  (path insert must precede this import)
    PI,
    UndefinedTangentError,
    degrees_to_radians,
    my_abs,
    my_factorial,
    tan_taylor,
)


class TestKnownValues(unittest.TestCase):
    """tan(x) at well-known exact angles."""

    def test_tan_zero(self):
        self.assertAlmostEqual(tan_taylor(0), 0.0, places=9)

    def test_tan_pi_over_4(self):
        self.assertAlmostEqual(tan_taylor(PI / 4), 1.0, places=9)

    def test_tan_negative_pi_over_4(self):
        self.assertAlmostEqual(tan_taylor(-PI / 4), -1.0, places=9)

    def test_tan_pi_over_3(self):
        self.assertAlmostEqual(tan_taylor(PI / 3), math.sqrt(3), places=9)


class TestUndefinedPoints(unittest.TestCase):
    """tan(x) is undefined at odd multiples of pi/2."""

    def test_undefined_at_pi_over_2(self):
        with self.assertRaises(UndefinedTangentError):
            tan_taylor(PI / 2)

    def test_undefined_at_negative_pi_over_2(self):
        with self.assertRaises(UndefinedTangentError):
            tan_taylor(-PI / 2)

    def test_undefined_at_3pi_over_2(self):
        with self.assertRaises(UndefinedTangentError):
            tan_taylor(3 * PI / 2)


class TestPrecisionAgainstMathTan(unittest.TestCase):
    """tan_taylor() must track math.tan() closely across a value range."""

    def test_matches_math_tan_within_tolerance(self):
        test_values = [x / 10 for x in range(-30, 31) if x != 0]
        for x in test_values:
            with self.subTest(x=x):
                diff = abs(tan_taylor(x) - math.tan(x))
                self.assertLess(diff, 1e-9)


class TestSubordinateFunctions(unittest.TestCase):
    """The from-scratch helper functions tan_taylor() is built on."""

    def test_factorial_zero(self):
        self.assertEqual(my_factorial(0), 1)

    def test_factorial_five(self):
        self.assertEqual(my_factorial(5), 120)

    def test_abs_negative(self):
        self.assertEqual(my_abs(-3), 3)

    def test_abs_zero(self):
        self.assertEqual(my_abs(0), 0)

    def test_degrees_to_radians_zero(self):
        self.assertAlmostEqual(degrees_to_radians(0), 0.0, places=9)

    def test_degrees_to_radians_180(self):
        self.assertAlmostEqual(degrees_to_radians(180), PI, places=9)


if __name__ == "__main__":
    unittest.main()
