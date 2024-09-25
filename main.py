from tkinter import *
from Ventana import Ventana

def main():
    root = Tk()
    root.wm_title("Crud Python MySQL")
    app = Ventana(root)
    app.mainloop()

if __name__ == "__main__":
    main()
