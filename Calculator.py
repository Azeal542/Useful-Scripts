from tkinter import StringVar
import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()

# Initialize the problem variable and StringVar
problem = ""
problem_var = StringVar(value=problem)

# Function to update the problem variable
def update_problem(value):
    global problem
    if value == "=":
        try:
            # Evaluate the expression and update the problem variable
            problem = str(eval(problem))
        except Exception as e:
            problem = "Error, please press clear"
    elif value == "-1":
        try:
            # Make either positive or negative
            problem  += "*-1"
            problem = str(eval(problem))
        except Exception as e:
            problem = "Error, please press clear"
    else:
        if problem and problem[-1] in "+-*/" and value in "+-*/":
            # Replace the last operand with the new one
            problem = problem[:-1] + value
        else:
            problem += value
    problem_var.set(problem)

# Function to clear the problem variable
def clear_problem():
    global problem
    problem = ""
    problem_var.set(problem)

def keypress(event):
    key = event.char
    if key in "0123456789+-*/.=":
        update_problem(key)
    elif key == '\r':  # Enter key
        update_problem("=")
    elif key == '\x08':  # Backspace key
        clear_problem()

# Configure styles
style = ttk.Style()
style.configure("TFrame", padding=6, relief="flat", background="#0B0033")
style.configure("TButton", padding=6, relief="flat", background="#370031")

# Create frame
frm = ttk.Frame(root, padding=10)
frm.grid()
for i in range(1, 5):
    frm.grid_columnconfigure(i, weight=1, minsize=50)
for i in range(2, 6):
    frm.grid_rowconfigure(i, weight=1, minsize=50)

# Create buttons
ttk.Button(frm, text="7", command=lambda: update_problem("7")).grid(column=1, row=2, sticky="nsew")
ttk.Button(frm, text="8", command=lambda: update_problem("8")).grid(column=2, row=2, sticky="nsew")
ttk.Button(frm, text="9", command=lambda: update_problem("9")).grid(column=3, row=2, sticky="nsew")
ttk.Button(frm, text="/", command=lambda: update_problem("/")).grid(column=4, row=2, sticky="nsew")
ttk.Button(frm, text="4", command=lambda: update_problem("4")).grid(column=1, row=3, sticky="nsew")
ttk.Button(frm, text="5", command=lambda: update_problem("5")).grid(column=2, row=3, sticky="nsew")
ttk.Button(frm, text="6", command=lambda: update_problem("6")).grid(column=3, row=3, sticky="nsew")
ttk.Button(frm, text="*", command=lambda: update_problem("*")).grid(column=4, row=3, sticky="nsew")
ttk.Button(frm, text="1", command=lambda: update_problem("1")).grid(column=1, row=4, sticky="nsew")
ttk.Button(frm, text="2", command=lambda: update_problem("2")).grid(column=2, row=4, sticky="nsew")
ttk.Button(frm, text="3", command=lambda: update_problem("3")).grid(column=3, row=4, sticky="nsew")
ttk.Button(frm, text="-", command=lambda: update_problem("-")).grid(column=4, row=4, sticky="nsew")
ttk.Button(frm, text="0", command=lambda: update_problem("0")).grid(column=1, row=5, columnspan=2, sticky="nsew")  # Spans 2 columns
ttk.Button(frm, text=".", command=lambda: update_problem(".")).grid(column=3, row=5, sticky="nsew")
ttk.Button(frm, text="+", command=lambda: update_problem("+")).grid(column=4, row=5, sticky="nsew")
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=8, sticky="nsew")
ttk.Button(frm, text="Clear", command=lambda: clear_problem()).grid(column=2, row=8, sticky="nsew")
ttk.Button(frm, text="=", command=lambda: update_problem("=")).grid(column=3, row=8, sticky="nsew")  # Spans 2 columns
ttk.Button(frm, text="+/-", command=lambda: update_problem("-1")).grid(column=4, row=8, sticky="nsew")  # Spans 2 columns

# Create the label with textvariable
ttk.Label(frm, textvariable=problem_var).grid(column=1, row=0, sticky="w")

# Bind keypress events to the keypress function
root.bind("<Key>", keypress)

# Start the main event loop
root.mainloop()
