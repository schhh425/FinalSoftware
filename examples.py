import tkinter.messagebox
from tkinter import *

from PyQt5.QtWidgets import *

from project.figure import MainDialogImgBW

if __name__ == "__main__":

    tk = Tk()
    tk.withdraw()

    askyesno = tkinter.messagebox.askyesno("Hi", "Please make sure you have informed consent.")
    if askyesno:
        app = QApplication(sys.argv)
        main = MainDialogImgBW()
        main.show()
        sys.exit(app.exec_())
    else:
        tkinter.messagebox.showinfo("Bye", "Have a good day.")
        sys.exc_info()