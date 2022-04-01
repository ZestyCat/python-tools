import noiseline as nl
import tkinter as tk
from tkinter import ttk

nl.test_func()

class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        
        self.type_entry = tk.Entry()
        self.type_entry.pack() # Use grid() later for better placement
        self.type = tk.StringVar()
        self.type.set("line")
        self.type_entry["textvariable"] = self.type
        # And so on for rest of input variables

        self.p1_entry = tk.Entry()
        self.p1_entry.pack()
        self.p1 = tk.StringVar()
        self.p1.set("./data/csv/Flight/")
        self.p1_entry["textvariable"] = self.p1

        self.f1_entry = tk.Entry()
        self.f1_entry.pack()
        self.f1 = tk.StringVar()
        self.f1.set("F-18EF_F414-GE-400_84NC.csv")
        self.f1_entry["textvariable"] = self.f1


        self.type_entry.bind("<Key-Return>", self.get_type)

    def get_type(self, event):
        print("You chose ", self.type.get())

root = tk.Tk()
a = App(root)
a.mainloop()
