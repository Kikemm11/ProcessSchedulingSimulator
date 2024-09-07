import tkinter as tk
from tkinter import Toplevel

import settings
import time
from statistics import mean

class SimulationWindow(Toplevel):
    def __init__(self, parent, _processes, _selected_algorithm):
        super().__init__(parent)
        self.title("Process Simulation")
        self.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        self.processes = _processes
        self.selected_algorithm = _selected_algorithm
        self.total_processes = len(self.processes)
        
        
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
            
            self.simulation_time = 0.1
            
            self.arrival_time = 0
            self.burst_time = 0
            self.cpu_usage_time = 0
            
            self.cpu_available = True
            
            self.ready_processes = []
            self.process_waiting_times = []
            self.finished_processes = []
            self.cpu_usage = []
            self.execution_time = []
            
            self.current_process = None
            self.processes.sort(key=lambda x: x.arrival_time)
            
            # Function call
            
            self.fifo()
            
        elif self.selected_algorithm == "SJF":
            pass
        elif self.selected_algorithm == "RandomSelection":
            pass
        elif self.selected_algorithm == "PrioritySelection (Non-Preemptive)":
            
            # Special variables for PrioritySelection (Non-Preemptive) algorithm
            
            self.simulation_time = 0.1
            
            self.arrival_time = 0
            self.burst_time = 0
            self.cpu_usage_time = 0
            
            self.cpu_available = True
            
            self.ready_processes = []
            self.process_waiting_times = []
            self.finished_processes = []
            self.cpu_usage = []
            self.execution_time = []
            
            self.current_process = None
            self.processes.sort(key=lambda x: x.priority, reverse=True)
            
            # Function call
            
            self.priority_selection_non_preemptive()
            
        
        elif self.selected_algorithm == "RoundRobin":
            pass
        elif self.selected_algorithm == "SRTF":
            pass
        elif self.selected_algorithm == "PrioritySelection (Preemptive)":
            pass



# ------------------------------- Non-Preemptive algorithms -------------------------------------------




    # FIFO ALGORITHM


    def fifo(self):
        
        if self.total_processes == len(self.finished_processes): return
        
        start_timestamp = time.time()
        
        # Update process queue and add process to the ready_process list
        
        self.queue_listbox.delete(0, tk.END)
        for process in self.processes:
            if  self.arrival_time >= process.arrival_time:    
                self.queue_listbox.insert(tk.END, f"PID: {process.pid}, AT: {process.arrival_time}, BT: {process.burst_time}, PR: {process.priority}")
                if process not in self.ready_processes:
                    self.ready_processes.append(process)


        # Manage the logic when the cpu is available to accept a process
        

        if self.ready_processes and self.cpu_available:
            
            self.cpu_available = False
            self.burst_time = 0
            self.cpu_usage_time = 0
            if self.processes: self.processes.pop(0)
            
            self.current_process = self.ready_processes.pop(0)
            self.process_waiting_times.append(self.current_process.waiting_time)
            self.current_process_value.config(text=f"PID: {self.current_process.pid}")
            self.queue_listbox.delete(0)
            
            
        # Check if there is a current process in the cpu and if it has completed its burst time
        
        if self.current_process and self.burst_time >= self.current_process.burst_time:
            self.finished_listbox.insert(tk.END, f"PID: {self.current_process.pid}, AT: {self.current_process.arrival_time}, BT: {self.current_process.burst_time}, PR: {self.current_process.priority}")
            self.cpu_available = True
            self.cpu_usage.append(self.cpu_usage_time)
            self.execution_time.append(self.current_process.waiting_time + self.current_process.burst_time)
            self.finished_processes.append(self.current_process)
            self.current_process = None
            
        # Set the cpu label to None if it has no process    
            
        if not self.current_process:
            self.current_process_value.config(text="None")
            
        # Update the statistics    
            
        self.stats_text.delete(1.0, tk.END)
        
        avrg_cpu_usage = (sum(self.cpu_usage) / self.simulation_time ) * 100
        self.stats_text.insert(tk.END, f"CPU usage %: {round(avrg_cpu_usage,2)}%\n")
        
        avrg_execution_time = mean(self.execution_time) if self.execution_time else 0
        self.stats_text.insert(tk.END, f"Average Execution Time: {round(avrg_execution_time, 2)}\n")
        
        
        avrg_waiting_time = mean(self.process_waiting_times) if self.process_waiting_times else 0
        self.stats_text.insert(tk.END, f"Average Waiting Time: {round(avrg_waiting_time, 2)}\n")
        
        self.stats_text.insert(tk.END, f"Total processes completed: {len(self.finished_processes)}\n")
        
        self.stats_text.insert(tk.END, f"Simulation time: {round(self.simulation_time, 2)} seconds\n")
        
        self.update_idletasks()
        
        # Update the timers
        
        end_timestamp = time.time()  
        
        self.arrival_time += end_timestamp - start_timestamp
        self.burst_time += end_timestamp - start_timestamp
        
        for process in self.ready_processes:
            process.waiting_time += end_timestamp - start_timestamp
            
        if not self.cpu_available:
            self.cpu_usage_time += end_timestamp - start_timestamp
            
        self.simulation_time += end_timestamp - start_timestamp
                
        self.after(1, self.fifo)
        
        
        
    # PRIORITY SELECTION ALGORITHM     
        
        
    def priority_selection_non_preemptive(self):
        
        if self.total_processes == len(self.finished_processes): return
        
        start_timestamp = time.time()
        
        # Update process queue and add process to the ready_process list
        
        self.queue_listbox.delete(0, tk.END)
        for process in self.processes:
            if  self.arrival_time >= process.arrival_time:    
                self.queue_listbox.insert(tk.END, f"PID: {process.pid}, AT: {process.arrival_time}, BT: {process.burst_time}, PR: {process.priority}")
                if process not in self.ready_processes:
                    self.ready_processes.append(process)
                    
        
        # Manage the logic when the cpu is available to accept a process
        
        self.ready_processes.sort(key=lambda x: x.priority, reverse=True)

        if self.ready_processes and self.cpu_available:
            
            self.cpu_available = False
            self.burst_time = 0
            self.cpu_usage_time = 0
            if self.processes: self.processes.remove(self.ready_processes[0])
            
            self.current_process = self.ready_processes.pop(0)
            self.process_waiting_times.append(self.current_process.waiting_time)
            self.current_process_value.config(text=f"PID: {self.current_process.pid}")
            self.queue_listbox.delete(0)
            
        
        # Check if there is a current process in the cpu and if it has completed its burst time
        
        if self.current_process and self.burst_time >= self.current_process.burst_time:
            self.finished_listbox.insert(tk.END, f"PID: {self.current_process.pid}, AT: {self.current_process.arrival_time}, BT: {self.current_process.burst_time}, PR: {self.current_process.priority}")
            self.cpu_available = True
            self.cpu_usage.append(self.cpu_usage_time)
            self.execution_time.append(self.current_process.waiting_time + self.current_process.burst_time)
            self.finished_processes.append(self.current_process)
            self.current_process = None
            
        # Set the cpu label to None if it has no process    
            
        if not self.current_process:
            self.current_process_value.config(text="None")
            
        
        # Update the statistics    
            
        self.stats_text.delete(1.0, tk.END)
        
        avrg_cpu_usage = (sum(self.cpu_usage) / self.simulation_time ) * 100
        self.stats_text.insert(tk.END, f"CPU usage %: {round(avrg_cpu_usage,2)}%\n")
        
        avrg_execution_time = mean(self.execution_time) if self.execution_time else 0
        self.stats_text.insert(tk.END, f"Average Execution Time: {round(avrg_execution_time, 2)}\n")
        
        
        avrg_waiting_time = mean(self.process_waiting_times) if self.process_waiting_times else 0
        self.stats_text.insert(tk.END, f"Average Waiting Time: {round(avrg_waiting_time, 2)}\n")
        
        self.stats_text.insert(tk.END, f"Total processes completed: {len(self.finished_processes)}\n")
        
        self.stats_text.insert(tk.END, f"Simulation time: {round(self.simulation_time, 2)} seconds\n")
        
        self.update_idletasks()
        
        # Update the timers
        
        end_timestamp = time.time()  
        
        self.arrival_time += end_timestamp - start_timestamp
        self.burst_time += end_timestamp - start_timestamp
        
        for process in self.ready_processes:
            process.waiting_time += end_timestamp - start_timestamp
            
        if not self.cpu_available:
            self.cpu_usage_time += end_timestamp - start_timestamp
            
        self.simulation_time += end_timestamp - start_timestamp
                
        self.after(1, self.priority_selection_non_preemptive)