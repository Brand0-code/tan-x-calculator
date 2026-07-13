"""
tan(x) implementation using Taylor series expansion of sin(x) and cos(x).

SOEN 6011 - Deliverable 1 - Problem 4
Function assigned: F2 = tan(x)

Algorithm: Taylor series via sin/cos decomposition (Algorithm A from
Problem 3), selected via mind map analysis in Problem 4.

Note: built-in functions (math.factorial, math.pi, etc.) are used here
since the "from scratch" restriction only applies starting in D2/Problem 5.
"""

import math

EPSILON = 1e-10        # threshold below which cos(x) is treated as zero
DEFAULT_TERMS = 20     # number of Taylor series terms to compute


def reduce_range(x):
    """Reduce x into the range [-pi, pi] for faster series convergence."""
    two_pi = 2 * math.pi
    x = x % two_pi
    if x > math.pi:
        x -= two_pi
    return x


def taylor_sin(x, n_terms=DEFAULT_TERMS):
    """Compute sin(x) using its Maclaurin (Taylor) series expansion."""
    result = 0.0
    for k in range(n_terms):
        term = ((-1) ** k) * (x ** (2 * k + 1)) / math.factorial(2 * k + 1)
        result += term
    return result


def taylor_cos(x, n_terms=DEFAULT_TERMS):
    """Compute cos(x) using its Maclaurin (Taylor) series expansion."""
    result = 0.0
    for k in range(n_terms):
        term = ((-1) ** k) * (x ** (2 * k)) / math.factorial(2 * k)
        result += term
    return result


def tan_taylor(x, epsilon=EPSILON, n_terms=DEFAULT_TERMS):
    """
    Compute tan(x) = sin(x) / cos(x) using Taylor series for sin and cos.

    Raises:
        ValueError: if x is within `epsilon` of an odd multiple of pi/2,
                    where tan(x) is mathematically undefined (REQ-002).
    """
    x_reduced = reduce_range(x)
    cos_x = taylor_cos(x_reduced, n_terms)

    if abs(cos_x) < epsilon:
        raise ValueError(
            "tan(x) is undefined here because the angle is too close to "
            "90 degrees (pi/2 radians), where cosine is zero."
        )

    sin_x = taylor_sin(x_reduced, n_terms)
    return sin_x / cos_x


def get_float_input(prompt):
    """Prompt the user for a float, re-prompting on invalid input."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("  -> Please enter a valid number (e.g., 0.5, 1.2, -3.14).")


def main():
    """Textual (command-line) user interface for tan(x). Satisfies REQ-004."""
    print("=" * 50)
    print("  tan(x) Calculator  (SOEN 6011 - F2)")
    print("=" * 50)
    print("Computes tan(x) using a Taylor series implementation.")
    print("Type 'q' at any prompt to quit.\n")

    while True:
        unit = input("Enter unit for x - 'r' for radians, 'd' for degrees "
                      "(or 'q' to quit): ").strip().lower()
        if unit == 'q':
            print("Goodbye!")
            break
        if unit not in ('r', 'd'):
            print("  -> Please enter 'r', 'd', or 'q'.\n")
            continue

        label = 'radians' if unit == 'r' else 'degrees'
        x_input = get_float_input(f"Enter x in {label}: ")

        # REQ-005 / REQ-006: default to radians, convert if degrees given
        x_radians = math.radians(x_input) if unit == 'd' else x_input

        try:
            result = tan_taylor(x_radians)
            unit_label = "deg" if unit == 'd' else "rad"
            print(f"  tan({x_input} {unit_label}) = {result:.6f}\n")
        except ValueError as e:
            print(f"  Error: {e}\n")


if __name__ == "__main__":
    main()