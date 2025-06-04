# Before you run the code, Bash on terminal:
# pip install matplotlib

import tkinter as tk
from tkinter import messagebox
import math
import cmath
import matplotlib.pyplot as plt
import numpy as np

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Scientific Calculator")
        self.root.geometry("500x750")
        self.root.minsize(480, 750)
        self.is_dark = True
        self.memory = 0

        self.create_widgets()
        self.bind_keys()
        self.set_theme()

    def create_widgets(self):
        self.entry = tk.Entry(self.root, font="Arial 20", borderwidth=5, relief=tk.RIDGE, justify="right")
        self.entry.pack(fill=tk.BOTH, ipadx=8, ipady=15, padx=10, pady=10)

        self.history = tk.Text(self.root, height=5, font="Arial 12")
        self.history.pack(fill=tk.BOTH, padx=10, pady=5)
        self.history.insert(tk.END, "History:\n")
        self.history.config(state=tk.DISABLED)

        # Top bar
        top_row = ["M+", "MR", "MC", "Theme", "Clear Hist"]
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")
        for btn in top_row:
            b = tk.Button(frame, text=btn, font="Arial 14")
            b.pack(side="left", expand=True, fill="both", padx=2, pady=2)
            b.bind("<Button-1>", self.click)

        # Main buttons
        buttons = [
            ["7", "8", "9", "/", "sin"],
            ["4", "5", "6", "*", "cos"],
            ["1", "2", "3", "-", "tan"],
            ["0", ".", "^", "+", "log"],
            ["(", ")", "√", "=", "ln"],
            ["abs", "exp", "pi", "j", "C"],
            ["Plot", "EvalC"]
        ]

        for row in buttons:
            frame = tk.Frame(self.root)
            frame.pack(expand=True, fill="both")
            for btn in row:
                b = tk.Button(frame, text=btn, font="Arial 14")
                b.pack(side="left", expand=True, fill="both", padx=2, pady=2)
                b.bind("<Button-1>", self.click)

    def bind_keys(self):
        self.root.bind("<Return>", lambda event: self.evaluate())
        self.root.bind("<BackSpace>", lambda event: self.backspace())
        for char in "0123456789+-*/.^()j":
            self.root.bind(char, self.key_input)

    def set_theme(self):
        bg, fg, entry_bg, hist_bg, hist_fg = (
            "#1e1e1e", "#eeeeee", "#2e2e2e", "#121212", "#aaaaaa"
        ) if self.is_dark else (
            "#ffffff", "#000000", "#f0f0f0", "#e8e8e8", "#333333"
        )
        self.root.config(bg=bg)
        self.entry.config(bg=entry_bg, fg=fg)
        self.history.config(bg=hist_bg, fg=hist_fg)
        for frame in self.root.winfo_children():
            if isinstance(frame, tk.Frame):
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Button):
                        widget.config(bg=bg, fg=fg, activebackground="#555" if self.is_dark else "#ccc")

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.set_theme()

    def click(self, event):
        text = event.widget.cget("text")

        if text == "=":
            self.evaluate()
        elif text == "EvalC":
            self.evaluate_complex()
        elif text == "Plot":
            self.plot_expression()
        elif text == "C":
            self.entry.delete(0, tk.END)
        elif text == "Clear Hist":
            self.clear_history()
        elif text == "√":
            try:
                result = math.sqrt(float(self.entry.get()))
                self.show_result(f"√({self.entry.get()}) = {result}")
            except:
                self.show_error()
        elif text == "M+":
            try:
                self.memory = float(self.entry.get())
                self.save_history(f"Memory stored: {self.memory}")
            except:
                self.show_error()
        elif text == "MR":
            self.entry.insert(tk.END, str(self.memory))
        elif text == "MC":
            self.memory = 0
            self.save_history("Memory cleared")
        elif text == "Theme":
            self.toggle_theme()
        elif text == "pi":
            self.entry.insert(tk.END, str(math.pi))
        elif text in ["sin", "cos", "tan", "log", "ln", "abs", "exp"]:
            try:
                value = float(self.entry.get())
                func_map = {
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "log": math.log10,
                    "ln": math.log,
                    "abs": abs,
                    "exp": math.exp
                }
                result = func_map[text](value)
                self.show_result(f"{text}({value}) = {result}")
            except:
                self.show_error()
        else:
            self.entry.insert(tk.END, text)

    def evaluate(self):
        try:
            expr = self.entry.get().replace("^", "**")
            result = eval(expr)
            self.show_result(f"{self.entry.get()} = {result}")
        except:
            self.show_error()

    def evaluate_complex(self):
        try:
            expr = self.entry.get().replace("^", "**")
            result = eval(expr, {"__builtins__": None}, {"j": 1j, "cmath": cmath})
            self.show_result(f"{self.entry.get()} = {result}")
        except:
            self.show_error()

    def show_result(self, text):
        self.save_history(text)
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, str(text.split('=')[-1].strip()))

    def show_error(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, "Error")

    def save_history(self, text):
        self.history.config(state=tk.NORMAL)
        self.history.insert(tk.END, f"{text}\n")
        self.history.config(state=tk.DISABLED)
        with open("history.txt", "a") as f:
            f.write(f"{text}\n")

    def clear_history(self):
        self.history.config(state=tk.NORMAL)
        self.history.delete(1.0, tk.END)
        self.history.insert(tk.END, "History:\n")
        self.history.config(state=tk.DISABLED)
        with open("history.txt", "w") as f:
            f.write("")

    def plot_expression(self):
        expr = self.entry.get().replace("^", "**")
        try:
            x = np.linspace(-10, 10, 400)
            y = eval(expr, {"x": x, "sin": np.sin, "cos": np.cos, "tan": np.tan,
                            "exp": np.exp, "log": np.log10, "sqrt": np.sqrt, "pi": np.pi,
                            "abs": np.abs, "np": np, "math": math})
            plt.plot(x, y)
            plt.title(f"Graph of: {expr}")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.grid(True)
            plt.show()
        except Exception as e:
            messagebox.showerror("Plot Error", f"Could not plot expression.\n{e}")

    def key_input(self, event):
        self.entry.insert(tk.END, event.char)

    def backspace(self):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current[:-1])

# Run the calculator
if __name__ == "__main__":
    root = tk.Tk()
    calc = ScientificCalculator(root)
    root.mainloop()