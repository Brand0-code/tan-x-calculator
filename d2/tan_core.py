"""
tan(x) core computation module - implemented FROM SCRATCH.

SOEN 6011 - Deliverable 2 - Problem 5
Function assigned: F2 = tan(x)

"From scratch" per the project constraint means: apart from functions
related to input, output, arithmetic, and user interface design, no
built-in or library functions provided by Python are used.

Explicit assumptions about the "from scratch" boundary:
  1. A hardcoded numeric literal (PI, below) is NOT a function call,
     so it does not violate the constraint.
  2. Core arithmetic operators (+ - * / % **) are language mechanics,
     not library functions, and are permitted.
  3. Core language control-flow built-ins (range(), used only as a
     loop counter, and float()/int(), used only to parse text input)
     are treated as language mechanics rather than mathematical
     library functions, and are permitted as part of "input" handling.
  4. Built-in exception classes are explicitly permitted by Problem 5
     ("either by using built-in exception classes ... or writing your
     own").

Functions replaced from D1 (which used the math module):
  math.pi        -> PI (hardcoded constant, not a function call)
  math.factorial -> my_factorial()
  math.radians   -> degrees_to_radians()
  abs()          -> my_abs()
"""


class UndefinedTangentError(Exception):
    """Raised when tan(x) is undefined (x is an odd multiple of pi/2)."""
    pass


# Hardcoded constant: not a function call, so this does not use a
# library function to obtain the value of pi.
PI = 3.14159265358979323846


def my_abs(x):
    """Absolute value, built from scratch (no built-in abs())."""
    if x >= 0:
        return x
    return -x


def my_factorial(n):
    """Factorial computed iteratively from scratch (no math.factorial)."""
    result = 1
    for i in range(2, n + 1):
        result = result * i
    return result


def degrees_to_radians(degrees):
    """Convert degrees to radians using only arithmetic (no math.radians)."""
    return degrees * PI / 180


def reduce_range(x):
    """Reduce x into [-pi, pi] using only arithmetic (no math.pi call)."""
    two_pi = 2 * PI
    x = x % two_pi
    if x > PI:
        x = x - two_pi
    return x


def taylor_sin(x, n_terms=20):
    """Compute sin(x) using its Maclaurin (Taylor) series expansion."""
    result = 0.0
    for k in range(n_terms):
        term = ((-1) ** k) * (x ** (2 * k + 1)) / my_factorial(2 * k + 1)
        result = result + term
    return result


def taylor_cos(x, n_terms=20):
    """Compute cos(x) using its Maclaurin (Taylor) series expansion."""
    result = 0.0
    for k in range(n_terms):
        term = ((-1) ** k) * (x ** (2 * k)) / my_factorial(2 * k)
        result = result + term
    return result


def tan_taylor(x, epsilon=1e-10, n_terms=20):
    """
    Compute tan(x) = sin(x) / cos(x) using Taylor series for sin and cos,
    entirely from scratch.

    Raises:
        UndefinedTangentError: if x is within `epsilon` of an odd
            multiple of pi/2, where tan(x) is mathematically undefined.
    """
    x_reduced = reduce_range(x)
    cos_x = taylor_cos(x_reduced, n_terms)

    if my_abs(cos_x) < epsilon:
        raise UndefinedTangentError(
            "tan(x) is undefined here because the angle is too close to "
            "90 degrees (pi/2 radians), where cosine is zero."
        )

    sin_x = taylor_sin(x_reduced, n_terms)
    return sin_x / cos_x