import os
import sys


def close_program():
    sys.exit(1)


def menu_bar_exit_click(ui):
    ui.menuFile.triggered.connect(close_program)
