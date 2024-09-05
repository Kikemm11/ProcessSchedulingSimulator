import tkinter as tk
from tkinter import Toplevel

import settings
import time

class SimulationWindow(Toplevel):
    def __init__(self, parent, _processes, _selected_algorithm):
        super().__init__(parent)
        self.title("Process Simulation")
        self.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        self.processes = _processes
        self.selected_algorithm = _selected_algorithm
        
        
        # Configure Window Grid
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        
        # Process Queue
        
        self.queue_label = tk.Label(self, text="Process Queue:")
        self.queue_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        self.queue_listbox = tk.Listbox(self, height=10, width=30)
        self.queue_listbox.grid(row=0, column=0, padx=10, pady=(30, 10), sticky="nw")
        
        
        # Block Processes
        
        self.block_label = tk.Label(self, text="Blocked Processes:")
        self.block_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        
        self.block_listbox = tk.Listbox(self, height=10, width=30)
        self.block_listbox.grid(row=1, column=0, padx=10, pady=(30, 10), sticky="nw")
        
        
        # Finished Processes
        
        self.finished_label = tk.Label(self, text="Finished Processes:")
        self.finished_label.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
        
        self.finished_listbox = tk.Listbox(self, height=10, width=30)
        self.finished_listbox.grid(row=2, column=0, padx=10, pady=(30, 10), sticky="nw")
        
        
        # CPU
        
        self.current_process_label = tk.Label(self, text="CPU:")
        self.current_process_label.grid(row=0, column=1, padx=10, pady=10, sticky="ne")
        
        self.current_process_value = tk.Label(self, text="None")
        self.current_process_value.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="ne")
        
        
        # Statistics
        
        self.stats_label = tk.Label(self, text="Statistics:")
        self.stats_label.grid(row=2, column=1, padx=10, pady=10, sticky="se")
        
        self.stats_text = tk.Text(self, height=10, width=50)
        self.stats_text.grid(row=2, column=1, padx=10, pady=(30, 10), sticky="se")
        
        self.run_simulation()



    def run_simulation(self):
        
        if self.selected_algorithm == "FIFO":
            
            # Special variables for FIFO algorithm
            
            self.arrival_time = 0
            self.burst_time = 0
            self.cpu_available = True
            self.ready_processes = []
            self.current_process = None
            self.processes.sort(key=lambda x: x["Arrival Time"])
            
            # Function call
            
            self.fifo()
            
        elif self.selected_algorithm == "SJF":
            pass
        elif self.selected_algorithm == "RandomSelection":
            pass
        elif self.selected_algorithm == "PrioritySelection":
            pass
        elif self.selected_algorithm == "RoundRobin":
            pass
        elif self.selected_algorithm == "SRTF":
            pass



    # No expulsive algorithms


    def fifo(self):
        
        start_timestamp = time.time()
        
        # Update process queue and add process to the ready_process list
        
        self.queue_listbox.delete(0, tk.END)
        for process in self.processes:
            if  self.arrival_time >= process['Arrival Time']:    
                self.queue_listbox.insert(tk.END, f"PID: {process['PID']}, AT: {process['Arrival Time']}, BT: {process['Burst Time']}, PR: {process['Priority']}")
                if process not in self.ready_processes:
                    self.ready_processes.append(process)


        # Manage the logic when the cpu is available to accept a process

        if self.ready_processes and self.cpu_available:
            
            self.cpu_available = False
            self.burst_time = 0
            if self.processes: self.processes.pop(0)
            
            self.current_process = self.ready_processes.pop(0)
            self.current_process_value.config(text=f"PID: {self.current_process['PID']}")
            self.queue_listbox.delete(0)
            
            
        # Check if there is a current process in the cpu and if it has completed its burst time
        
        if self.current_process and self.burst_time >= self.current_process['Burst Time']:
            self.finished_listbox.insert(tk.END, f"PID: {self.current_process['PID']}, AT: {self.current_process['Arrival Time']}, BT: {self.current_process['Burst Time']}, PR: {self.current_process['Priority']}")
            self.cpu_available = True
            self.current_process = None
            
        # Set the cpu label to None if it has no process    
            
        if not self.current_process:
            self.current_process_value.config(text="None")
            
        # Update the statistics (HAVEN'T DONE YET. JUST DUMMY )    
            
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"Average Waiting Time: 5.0\n")
        self.stats_text.insert(tk.END, f"Turnaround Time: 10.0\n")
        self.update_idletasks()
        
        # Update the timers
        
        end_timestamp = time.time()  
        self.arrival_time += end_timestamp - start_timestamp
        self.burst_time += end_timestamp - start_timestamp
        
        self.after(1, self.fifo)
        
