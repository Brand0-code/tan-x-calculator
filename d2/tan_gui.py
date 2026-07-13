"""
tan(x) Tkinter GUI - built on top of the from-scratch core.

SOEN 6011 - Deliverable 2 - Problem 5
Function assigned: F2 = tan(x)

Run with: python3 tan_gui.py
No IDE required to compile or run.

"From scratch" boundary note: str.strip() (used on the raw entry-box
text before parsing) is treated as input handling, same category as
float() in tan_core.py's documented assumptions - not a computation
on the mathematical value itself.
"""

import tkinter as tk
from tan_core import tan_taylor, degrees_to_radians, UndefinedTangentError


class TanCalculatorGUI:
    def __init__(self, root):
        self.root = root
        root.title("tan(x) Calculator - SOEN 6011 F2")
        root.geometry("440x280")
        root.resizable(False, False)

        # --- Input row ---
        tk.Label(root, text="Enter x:", font=("Arial", 11)).grid(
            row=0, column=0, padx=12, pady=(15, 5), sticky="w")
        self.entry_x = tk.Entry(root, font=("Arial", 11), width=20)
        self.entry_x.grid(row=0, column=1, padx=12, pady=(15, 5))
        self.entry_x.focus()

        # --- Unit selection ---
        tk.Label(root, text="Unit:", font=("Arial", 11)).grid(
            row=1, column=0, padx=12, sticky="w")
        self.unit_var = tk.StringVar(value="radians")
        unit_frame = tk.Frame(root)
        unit_frame.grid(row=1, column=1, sticky="w")
        tk.Radiobutton(unit_frame, text="Radians", variable=self.unit_var,
                        value="radians", font=("Arial", 10)).pack(side="left")
        tk.Radiobutton(unit_frame, text="Degrees", variable=self.unit_var,
                        value="degrees", font=("Arial", 10)).pack(side="left")

        # --- Compute button ---
        self.compute_btn = tk.Button(
            root, text="Compute tan(x)", command=self.on_compute,
            font=("Arial", 11, "bold"), bg="#4a7abc", fg="white",
            activebackground="#3a6aac", padx=10, pady=5)
        self.compute_btn.grid(row=2, column=0, columnspan=2, pady=18)

        # --- Result / error display ---
        self.result_var = tk.StringVar(value="Result will appear here.")
        self.result_label = tk.Label(
            root, textvariable=self.result_var, font=("Arial", 11),
            wraplength=400, fg="black", justify="left", anchor="w")
        self.result_label.grid(row=3, column=0, columnspan=2, padx=12,
                                pady=5, sticky="w")

        # Allow pressing Enter in the entry field to trigger compute
        self.entry_x.bind("<Return>", lambda event: self.on_compute())

    def on_compute(self):
        raw_input = self.entry_x.get().strip()

        # --- Exception handling: invalid (non-numeric) input ---
        try:
            x_value = float(raw_input)
        except ValueError:
            self.result_var.set(
                f"Error: '{raw_input}' is not a valid number. "
                f"Please enter a numeric value, e.g. 0.5, 45, or -1.2."
            )
            self.result_label.config(fg="#c0392b")
            return

        # Unit conversion (REQ-005 / REQ-006 equivalent from D1)
        if self.unit_var.get() == "degrees":
            x_radians = degrees_to_radians(x_value)
        else:
            x_radians = x_value

        # --- Exception handling: undefined tan(x) ---
        try:
            result = tan_taylor(x_radians)
            unit_label = "deg" if self.unit_var.get() == "degrees" else "rad"
            self.result_var.set(f"tan({x_value} {unit_label}) = {result:.6f}")
            self.result_label.config(fg="black")
        except UndefinedTangentError as e:
            self.result_var.set(f"Error: {e}")
            self.result_label.config(fg="#c0392b")


def main():
    root = tk.Tk()
    TanCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()