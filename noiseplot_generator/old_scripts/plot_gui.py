import noiseline as nl
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

nl.test_func()

class Text(tk.Entry): # make TextInput class inherit from tk.Entry
    def __init__(self, master, value): 
        super().__init__(master) # Access methods of super class (ttk.Frame)
        self.var = tk.StringVar() # make a string variable
        self.var.set(value) # set var to value
        self["textvariable"] = self.var # link entry to variable
        self.bind("<Key-Return>", self.print_contents)

    def print_contents(self, event): # callback to test variable
        print("Current content is:", self.var.get())

class Save(ttk.Frame):
    def __init__(self, master, placeholder):
        super().__init__(master)
        self.entry = tk.Entry()
        self.entry.grid(column = 0, row = 0)
        self.text = tk.StringVar()
        self.entry["textvariable"] = self.text
        self.text.set(placeholder)
        self.btn = tk.Button(command = self.get_file, text = "Save as", width = 5, height = 1)
        self.btn.grid(column = 1, row = 0)

    def get_file(self):
        file = fd.asksaveasfilename()
        self.text.set(file)

class Selection(ttk.Frame):
    def __init__(self, master, placeholder):
        super().__init__(master)
        self.var = tk.StringVar()
        self.var.set(placeholder)
        self.drop = tk.OptionMenu(master, self.var, *nl.list_aircraft()).grid(column = 1, row = 1)
        self.lab = tk.Label(master, text = "Select an aircraft").grid(column = 0, row = 1)
        
class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.save = Save(self, "Save file name")
        self.power = Text(self, "Power setting")
        self.aircraft = Selection(self, "Aircraft")
        self.plot_btn = tk.Button(self, text = "Make a plot", command = self.plot).grid(column = 0, row = 2)
        self.grid()
    def plot(self):
        ac = self.aircraft.var.get()
        print(ac)
root = tk.Tk()
a = App(root)
a.mainloop()
