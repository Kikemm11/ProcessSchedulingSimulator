"""
Authors:
- Iván Maldonado (Kikemaldonado11@gmail.com)
- Maria José Vera (nandadevi97816@gmail.com)
- Sergio Fernández (sergiofnzg@gmail.com)

Developed at: September 2024
"""


import os

import pandas as pd
from tkinter import messagebox


# Main properties

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600

FONT = "Poppins"


# Resources and utilities


def show_error_message(message):
        messagebox.showerror(
            title="Error",
            message=message
        )


def info_message(message):
    messagebox.showinfo(
          title="Success",
          message=message
        )