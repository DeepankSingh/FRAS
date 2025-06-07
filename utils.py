import tkinter as tk

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

# Helper function to create styled buttons
def create_button(parent, text, command, x, y):
    btn = tk.Button(parent, text=text, command=command, bd=0,
                    font=("Verdana", 18, "bold"),
                    bg="#2980B9", fg="#FFFFFF",
                    activebackground="#2471A3",
                    activeforeground="#FFFFFF",
                    height=3, width=30, relief="flat", cursor="hand2")
    btn.place(x=x, y=y)
    return btn
