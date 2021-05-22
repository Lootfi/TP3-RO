import tkinter as tk
from tkinter import DoubleVar
from tkinter.constants import END
import tkinter.font as tkFont
import numpy as np
from collections import namedtuple

from tp3 import graph_it, knapsack, Item


class App:
    text = None
    number_of_variables = None
    variables = []
    lvw = []

    def __init__(self, root):
        root.title("TP3 - Branch & Bound")

        root.resizable(width=False, height=False)

    # Labels

        number_of_variables_label = tk.Label(root)
        ft = tkFont.Font(family='Times', size=18)
        number_of_variables_label["font"] = ft
        number_of_variables_label["fg"] = "#333333"
        number_of_variables_label["justify"] = "center"
        number_of_variables_label["text"] = "Var Num"
        number_of_variables_label.grid(row=0, column=0)

        max_weight_label = tk.Label(root)
        ft = tkFont.Font(family='Times', size=18)
        max_weight_label["font"] = ft
        max_weight_label["fg"] = "#333333"
        max_weight_label["justify"] = "center"
        max_weight_label["text"] = "Max W"
        max_weight_label.grid(row=0, column=4)

    # Entries
        num_var = tk.IntVar(root)
        num_var.set(7)
        number_of_variables = tk.Entry(root, textvariable=num_var)
        number_of_variables["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        number_of_variables["font"] = ft
        number_of_variables["fg"] = "#333333"
        number_of_variables["justify"] = "center"
        number_of_variables.grid(padx=10, row=0, column=1)
        self.number_of_variables = num_var

        max_w_var = tk.IntVar(root)
        max_w_var.set(1)
        max_weight_entry = tk.Entry(root, textvariable=max_w_var)
        max_weight_entry["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        max_weight_entry["font"] = ft
        max_weight_entry["fg"] = "#333333"
        max_weight_entry["justify"] = "center"
        max_weight_entry.grid(row=0, column=5)
        self.max_weight_entry = max_w_var

        change_var_entries = tk.Button(root)
        change_var_entries["activebackground"] = "#cc0000"
        change_var_entries["activeforeground"] = "#ffffff"
        change_var_entries["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=18)
        change_var_entries["font"] = ft
        change_var_entries["fg"] = "#000"
        change_var_entries["justify"] = "center"
        change_var_entries["text"] = "Change"
        change_var_entries.grid(row=0, column=2)
        change_var_entries["command"] = self.change_num_of_variables_entries_command

        solve_button = tk.Button(root)
        solve_button["activebackground"] = "#cc0000"
        solve_button["activeforeground"] = "#ffffff"
        solve_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=18)
        solve_button["font"] = ft
        solve_button["fg"] = "#f00"
        solve_button["justify"] = "center"
        solve_button["text"] = "Search"
        solve_button.grid(row=1, column=0)
        solve_button["command"] = self.solve_button_command

        # init variable entires

        x_label = tk.Label(root)
        ft = tkFont.Font(family='Times', size=15)
        x_label["font"] = ft
        x_label["fg"] = "#000"
        x_label["justify"] = "center"
        x_label["text"] = "Values"
        x_label.grid(row=4, column=0)

        x_label = tk.Label(root)
        ft = tkFont.Font(family='Times', size=15)
        x_label["font"] = ft
        x_label["fg"] = "#000"
        x_label["justify"] = "center"
        x_label["text"] = "Weights"
        x_label.grid(row=5, column=0)

        for i in np.arange(0, int(self.number_of_variables.get()), 1):
            x_label = tk.Label(root)
            ft = tkFont.Font(family='Times', size=15)
            x_label["font"] = ft
            x_label["fg"] = "#000"
            x_label["justify"] = "center"
            x_label["text"] = "x" + str(i+1)
            x_label.grid(row=3, column=i+1)

            x_val_var = DoubleVar(root)
            x_val_var.set(0)
            x_value_entry = tk.Entry(root, textvariable=x_val_var)
            x_value_entry["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times', size=10)
            x_value_entry["font"] = ft
            x_value_entry["fg"] = "#333333"
            # x_value_entry['relief'] = "groove"
            x_value_entry["justify"] = "center"
            x_value_entry.grid(row=4, column=i+1)

            x_w_var = DoubleVar(root)
            x_w_var.set(1)
            x_weight_entry = tk.Entry(root, textvariable=x_w_var)
            x_weight_entry["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times', size=10)
            x_weight_entry["font"] = ft
            x_weight_entry["fg"] = "#333333"
            # x_weight_entry['relief'] = "groove"
            x_weight_entry["justify"] = "center"
            x_weight_entry.grid(row=5, column=i+1)

            self.variables.append(
                Item(i, x_val_var, x_w_var))
            self.lvw.append((x_label, x_value_entry, x_weight_entry))

        # default exo values buttons!

        x_label = tk.Label(root)
        ft = tkFont.Font(family='Times', size=15)
        x_label["font"] = ft
        x_label["fg"] = "#000"
        x_label["justify"] = "center"
        x_label["text"] = "Default Values of:"
        x_label.grid(row=6, column=0)

        tp3_button = tk.Button(root)
        tp3_button["activebackground"] = "#cc0000"
        tp3_button["activeforeground"] = "#ffffff"
        tp3_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=13)
        tp3_button["font"] = ft
        tp3_button["fg"] = "#000"
        tp3_button["justify"] = "center"
        tp3_button["text"] = "TP3"
        tp3_button.grid(row=6, column=1, pady=10)
        tp3_button["command"] = self.tp3_values_set

        td2_exo5_button = tk.Button(root)
        td2_exo5_button["activebackground"] = "#cc0000"
        td2_exo5_button["activeforeground"] = "#ffffff"
        td2_exo5_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=13)
        td2_exo5_button["font"] = ft
        td2_exo5_button["fg"] = "#000"
        td2_exo5_button["justify"] = "center"
        td2_exo5_button["text"] = "TD2EXO5"
        td2_exo5_button.grid(row=6, column=2, pady=10)
        td2_exo5_button["command"] = self.td2_exo5_values_set

        td2_exo7_button = tk.Button(root)
        td2_exo7_button["activebackground"] = "#cc0000"
        td2_exo7_button["activeforeground"] = "#ffffff"
        td2_exo7_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=13)
        td2_exo7_button["font"] = ft
        td2_exo7_button["fg"] = "#000"
        td2_exo7_button["justify"] = "center"
        td2_exo7_button["text"] = "TD2EXO7"
        td2_exo7_button.grid(row=6, column=3, pady=10)
        td2_exo7_button["command"] = self.td2_exo7_values_set

    def update_variables(self):
        new_variable_array = []
        new_lvw_array = []
        for i in np.arange(0, int(self.number_of_variables.get()), 1):
            x_label = tk.Label(root)
            ft = tkFont.Font(family='Times', size=15)
            x_label["font"] = ft
            x_label["fg"] = "#000"
            x_label["justify"] = "center"
            x_label["text"] = "x" + str(i+1)
            x_label.grid(row=3, column=i+1)

            x_val_var = DoubleVar(root)
            if(i < len(self.variables)):
                x_val_var.set(self.variables[i].value.get())
            x_value_entry = tk.Entry(root, textvariable=x_val_var)
            x_value_entry["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times', size=10)
            x_value_entry["font"] = ft
            x_value_entry["fg"] = "#333333"
            x_value_entry["justify"] = "center"
            x_value_entry.grid(row=4, column=i+1)

            x_w_var = DoubleVar(root)
            if(i < len(self.variables)):
                x_w_var.set(self.variables[i].weight.get())
            x_weight_entry = tk.Entry(root, textvariable=x_w_var)
            x_weight_entry["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times', size=10)
            x_weight_entry["font"] = ft
            x_weight_entry["fg"] = "#333333"
            x_weight_entry["justify"] = "center"
            x_weight_entry.grid(row=5, column=i+1)

            new_variable_array.append(Item(i, x_val_var, x_w_var))
            new_lvw_array.append((x_label, x_value_entry, x_weight_entry))

        self.variables = new_variable_array
        self.lvw = new_lvw_array
        return 0

    def change_num_of_variables_entries_command(self):
        for lvw in self.lvw:
            lvw[0].grid_remove()
            lvw[1].grid_remove()
            lvw[2].grid_remove()
        if int(self.number_of_variables.get()) < len(self.variables):
            self.lvw[0:int(
                self.number_of_variables.get())]
            self.variables = self.variables[0:int(
                self.number_of_variables.get())]

        self.update_variables()

    def solve_button_command(self):
        arr = []
        for i, item in enumerate(self.variables):
            arr.append(Item(i, item.value.get(), item.weight.get()))
        Z, N = knapsack(arr, self.max_weight_entry.get())
        print("Max Z = ", Z)
        # vous devez installer graphviz pour lancer graph_it
        # do both:
        # https://graphviz.org/download/#windows
        # and : pip install graphviz
        # make sure to add graphviz to your $PATH
        graph_it(N)

    def tp3_values_set(self):
        arr = [Item(1, 8, 3),
               Item(2, 16, 7),
               Item(3, 20, 9),
               Item(4, 12, 6),
               Item(5, 6, 3),
               Item(6, 9, 5)]
        self.set_values(arr)
        self.max_weight_entry.set(17)

    def td2_exo5_values_set(self):
        arr = [Item(1, 70, 31),
               Item(2, 20, 10),
               Item(3, 39, 20),
               Item(4, 35, 18),
               Item(5, 7, 4),
               Item(6, 5, 3),
               Item(7, 9, 6)]
        self.set_values(arr)
        self.max_weight_entry.set(50)

    def td2_exo7_values_set(self):
        arr = [Item(1, 20000, 4),
               Item(2, 18000, 6),
               Item(3, 32000, 8),
               Item(4, 45000, 10),
               Item(5, 6000, 1)]
        self.set_values(arr)
        self.max_weight_entry.set(14)

    def set_values(self, arr):
        self.number_of_variables.set(len(arr))
        self.change_num_of_variables_entries_command()
        for i, item in enumerate(self.variables):
            item.value.set(arr[i].value)
            item.weight.set(arr[i].weight)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
