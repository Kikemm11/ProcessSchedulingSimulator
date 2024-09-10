"""
Authors:
- Iván Maldonado (Kikemaldonado11@gmail.com)
- Maria José Vera (nandadevi97816@gmail.com)
- Sergio Fernández (sergiofnzg@gmail.com)

Developed at: September 2024
"""


import tkinter as tk
from tkinter import ttk, simpledialog, Toplevel

import settings
from windows.SimulationWindow import SimulationWindow
from src.Process import Process


class MainWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Process Schedule Simulator")
        self.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        # Window grid configurations
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        
        
        # Dropdown for selecting the scheduling algorithm
        
        self.algorithm_label = tk.Label(self, text="Algorithm:")
        self.algorithm_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.algorithm_var = tk.StringVar()
        self.algorithm_combobox = ttk.Combobox(
            self, 
            textvariable=self.algorithm_var, 
            values=[
                "FIFO", 
                "SJF", 
                "RandomSelection", 
                "PrioritySelection (Non-Preemptive)", 
                "RoundRobin", 
                "SRTF",
                "PrioritySelection (Preemptive)"
            ],
            state="readonly"
        )
        self.algorithm_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        self.algorithm_combobox.current(0)
        
        
        # Treeview widget to display the list of processes
        
        self.tree = ttk.Treeview(self, columns=("PID", "Arrival Time", "Burst Time", "Priority"), show="headings", height=8)
        self.tree.heading("PID", text="PID")
        self.tree.heading("Arrival Time", text="Arrival Time")
        self.tree.heading("Burst Time", text="Burst Time")
        self.tree.heading("Priority", text="Priority")
        self.tree.grid(row=1, column=1, padx=10, pady=10, sticky="n")
        
        self.tree.grid_propagate(False)
        self.tree.grid_columnconfigure(0, weight=1)
        self.tree.grid_rowconfigure(1, weight=1)
        
        
        # Window Buttons
        
        self.add_button = tk.Button(self, text="+ Add Process", command=self.add_process)
        self.add_button.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        self.remove_button = tk.Button(self, text="- Remove Selected", command=self.remove_process)
        self.remove_button.grid(row=0, column=2, padx=10, pady=10, sticky="se")

        self.simulate_button = tk.Button(self, text="Simulate", command=self.simulate)
        self.simulate_button.grid(row=2, column=1, padx=10, pady=10, sticky="n")
        
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()
     
     
                
    def add_process(self):
        
        pid = simpledialog.askstring("Input", "Enter Process ID (PID):", parent=self)
        arrival_time = simpledialog.askstring("Input", "Enter Arrival Time:", parent=self)
        burst_time = simpledialog.askstring("Input", "Enter Burst Time:", parent=self)
        priority = simpledialog.askstring("Input", "Enter Priority:", parent=self)
        
        if pid and arrival_time and burst_time and priority:
            self.tree.insert("", "end", values=(pid, arrival_time, burst_time, priority))


    def remove_process(self):
        selected_item = self.tree.selection() 
        if selected_item:
            self.tree.delete(selected_item)
    
    
    def get_processes(self):
        processes = []
        for child in self.tree.get_children():
            process_data = self.tree.item(child)["values"]
            process = Process(process_data[0], int(process_data[1]), int(process_data[2]), int(process_data[3]))
            processes.append(process)
        
        return processes


    def simulate(self):
        processes = self.get_processes()
        selected_algorithm = self.algorithm_var.get()
        
        if processes:
            self.simulation_window = SimulationWindow(self, processes, selected_algorithm)


    def on_closing(self):
        self.destroy()