"""Dev-only driver script used to demonstrate a pdb session (D3/Problem 7).
Not part of the graded implementation; not imported by tan_core.py/tan_gui.py."""

from tan_core import tan_taylor

if __name__ == "__main__":
    result = tan_taylor(1.0)
    print("result:", result)
