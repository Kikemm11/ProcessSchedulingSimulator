"""
Authors:
- Iván Maldonado (Kikemaldonado11@gmail.com)
- Maria José Vera (nandadevi97816@gmail.com)
- Sergio Fernández (sergiofnzg@gmail.com)

Developed at: September 2024
"""


import tkinter as tk
from tkinter import Toplevel

import settings
import time
from statistics import mean
import random


class SimulationWindow(Toplevel):
    def __init__(self, parent, _processes, _selected_algorithm):
        super().__init__(parent)
        self.title("Process Simulation")
        self.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        self.processes = _processes
        self.selected_algorithm = _selected_algorithm
        self.total_processes = len(self.processes)
        
        # Special variables to handle the logic during the simulation 
        
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
        self.blocked_time = []
        self.blocked_processes = []
        
        self.current_process = None
        
        
        
        # Configure Window Grid
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)# Resources and utils for simulation
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
        
        
    # ---------------------------- Non Preemptive Algorithms -----------------------------------------
    
    
    # FIFO ALGORITHM

    def fifo(self):
        """Under the FIFO logic schedules the process in arrival order in wich
        the first process to reach the ready queue will be the first to executes"""
        
        if self.total_processes == len(self.finished_processes): return
        
        start_timestamp = time.time()
        
        self.update_ready_queue()
        
        
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
            
            
        self.check_finish_execution()
                
        self.update_blocked_processes() 
            
        self.cpu_to_none()
            
        self.update_statistics()

        end_timestamp = time.time()
        
        self.dt = end_timestamp - start_timestamp  
        
        self.update_timers()
                
        self.after(1, self.fifo)
        
        
        
    # RANDOM SELECTION ALGORITHM
        
    def random_selection(self):
        """Given n number of processes in the ready queue the algorithm
        will schedule any process randomly to be executed, in the cases
        where there is only one process at the queue this will be executed
        right away"""
        
        if self.total_processes == len(self.finished_processes):
            return
        
        start_timestamp = time.time()
        
        self.update_ready_queue()
        
        
        # Randomly select a process if the CPU is available
        
        if self.ready_processes and self.cpu_available:
            self.cpu_available = False
            self.burst_time = 0
            self.cpu_usage_time = 0
            self.current_process = random.choice(self.ready_processes)
            self.ready_processes.remove(self.current_process)
            self.processes.remove(self.current_process)
            self.process_waiting_times.append(self.current_process.waiting_time)
            self.current_process_value.config(text=f"PID: {self.current_process.pid}")
            
            
        self.check_finish_execution()
        
        self.update_blocked_processes()
        
        self.cpu_to_none()
        
        self.update_statistics()
        
        end_timestamp = time.time()
        
        self.dt = end_timestamp - start_timestamp
        
        self.update_timers()
        
        self.after(1, self.random_selection)
        
        

    # PRIORITY SELECTION ALGORITHM     
            
    def priority_selection_non_preemptive(self):
        """All the processes will be rearranged in the ready queue
        based on their priority value and then the one with the
        higher value will be executed and so on in every iteration.
        Once a process it's being executed it will stay until finished"""
        
        if self.total_processes == len(self.finished_processes): return
        
        start_timestamp = time.time()
        
        self.update_ready_queue()
                    
        
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
            
        
        self.check_finish_execution()
        
        self.update_blocked_processes()  
            
        self.cpu_to_none()
            
        self.update_statistics()
        
        end_timestamp = time.time()  
        
        self.dt = end_timestamp - start_timestamp
        
        self.update_timers()
                
        self.after(1, self.priority_selection_non_preemptive)   
        
        
    
    
    # ---------------------------- Preemptive Algorithms --------------------------------------------
    
    
    
    # SRTF ALGORITHM
    
    def srtf(self):
        """This algorithm will rearrange the processes in the ready
        queue based on its reamining burst time value and the next
        to be executed will be the one with the minor value. In the
        cases when a process it's being executed and another arrives
        with minor burst time it inmediatly will be placed at the cpu
        and the other one will be remitted to the ready queue again"""
        
        if self.total_processes == len(self.finished_processes): return
        
        start_timestamp = time.time()
        
        self.update_ready_queue()
        
        # Manage the logic when the cpu is available to accept a process
        
        if self.ready_processes and self.cpu_available:
            
            self.cpu_available = False
            self.burst_time = 0
            self.cpu_usage_time = 0
            
            if self.processes: self.processes.remove(self.ready_processes[0])
            
            self.current_process = self.ready_processes.pop(0)
            self.process_waiting_times.append(self.current_process.waiting_time)
            self.current_process_value.config(text=f"PID: {self.current_process.pid}")
            self.queue_listbox.delete(0)
            

        self.check_finish_execution()
        
        self.update_blocked_processes()
            
        
        # Check if there is a process with minor remaining burst time to reach the cpu first
        
        possible_next_process = min(self.ready_processes, key=lambda p: p.remaining_burst_time) if self.ready_processes else None
        
        if possible_next_process and self.current_process and possible_next_process.remaining_burst_time < self.current_process.remaining_burst_time:
            
            self.burst_time = 0
            self.cpu_usage_time = 0
            
            self.current_process.waiting_time = 0
            self.processes.append(self.current_process)
            self.ready_processes.append(self.current_process)
            
            self.current_process = possible_next_process
            self.ready_processes.remove(self.current_process)
            self.processes.remove(self.current_process)
            self.current_process_value.config(text=f"PID: {self.current_process.pid}")
        
            
        self.cpu_to_none()                     
            
        self.update_statistics()
        
        end_timestamp = time.time()  
        
        self.dt = end_timestamp - start_timestamp
        
        self.update_timers()
                
        self.after(1, self.srtf)
        
        
        
    # PRIORITY SELECTION (PREEMPTIVE)

    def priority_selection_preemptive(self):
        """All the processes will be rearranged in the ready queue
        based on their priority value and then the one with the
        higher value will be executed and so on in every iteration.
        In the cases when a process it's being executed and another
        arrives with higher priority it inmediatly will be placed at
        the cpu and the other one will be remitted to the ready queue
        again"""
        
        if self.total_processes == len(self.finished_processes):
            return
        
        start_timestamp = time.time()
        
        self.update_ready_queue()
        
        # Sort ready processes by priority (higher priority first)
        
        self.ready_processes.sort(key=lambda x: x.priority, reverse=True)
        
        # Preempt the current process if a higher priority process arrives
        
        if self.ready_processes:
            if self.current_process:
                
                if self.ready_processes[0].priority > self.current_process.priority:            # Preempt if the new process has higher priority than the current process and
                    self.ready_processes.append(self.current_process)                           # put the current process back into the ready queue
                    self.processes.append(self.current_process)   
                    self.current_process = None
                    
            if not self.current_process or self.cpu_available:
                self.cpu_available = False
                self.burst_time = 0
                self.cpu_usage_time = 0
                
                if self.processes: self.processes.remove(self.ready_processes[0])
                self.current_process = self.ready_processes.pop(0)
                
                self.process_waiting_times.append(self.current_process.waiting_time)
                self.current_process_value.config(text=f"PID: {self.current_process.pid}")
                self.queue_listbox.delete(0)
            
                
        self.check_finish_execution()
        
        self.update_blocked_processes()
    
        self.cpu_to_none()
        
        self.update_statistics()
        
        end_timestamp = time.time()
        
        self.dt = end_timestamp - start_timestamp
        
        self.update_timers()
        
        self.after(1, self.priority_selection_preemptive)
        
        
        
    # Resources and utils for simulation


    def run_simulation(self):
        """Determines wich algorithm to use and executes its logic"""
        
        if self.selected_algorithm == "FIFO":
                      
            self.processes.sort(key=lambda x: x.arrival_time)
            self.fifo()
            
        elif self.selected_algorithm == "SJF":
            pass
        elif self.selected_algorithm == "RandomSelection":
            
            self.random_selection()
            
        elif self.selected_algorithm == "PrioritySelection (Non-Preemptive)":
            
            self.processes.sort(key=lambda x: x.priority, reverse=True)
            self.priority_selection_non_preemptive()
            
        
        elif self.selected_algorithm == "RoundRobin":
            pass
        elif self.selected_algorithm == "SRTF":
              
            self.processes.sort(key=lambda x: x.remaining_burst_time)
            self.srtf()
            
        elif self.selected_algorithm == "PrioritySelection (Preemptive)":
        
            self.processes.sort(key=lambda x: x.priority, reverse=True)
            self.priority_selection_preemptive()
            
    
    def update_ready_queue(self):
        """Update the value of the ready queue based on the available processes in the list"""
        
        self.queue_listbox.delete(0, tk.END)
        for process in self.processes:
            if  self.arrival_time >= process.arrival_time:    
                self.queue_listbox.insert(tk.END, f"PID: {process.pid}, AT: {process.arrival_time}, Remaining BT: {process.remaining_burst_time}, PR: {process.priority}")
                if process not in self.ready_processes:
                    self.ready_processes.append(process)
                    
                    
    def check_finish_execution(self):
        """Check if the current process in execution has reached its burst time to update its state"""
        
        if self.current_process and self.burst_time >= self.current_process.remaining_burst_time:
            self.finished_listbox.insert(tk.END, f"PID: {self.current_process.pid}, AT: {self.current_process.arrival_time}, BT: {self.current_process.burst_time}, PR: {self.current_process.priority}")
            self.cpu_available = True
            self.cpu_usage.append(self.cpu_usage_time)
            self.execution_time.append(self.current_process.waiting_time + self.current_process.burst_time)
            self.finished_processes.append(self.current_process)
            self.current_process = None
            
            
    def update_blocked_processes(self):
        """Update the blocked list based on the available process in the blocked list"""
        
        self.block_listbox.delete(0, tk.END)    
        for process in self.blocked_processes:
            self.block_listbox.insert(tk.END, f"PID: {process.pid}, AT: {process.arrival_time}, Remaining BT: {process.remaining_burst_time}, PR: {process.priority}")
            
            
    def cpu_to_none(self):
        """Set the CPU label to None in case it's not currently executing a process"""
        
        if not self.current_process:
            self.current_process_value.config(text="None")
            
            
    def update_statistics(self):
        """Manage all the logic and calcules to show the required statistics"""
        
        self.stats_text.delete(1.0, tk.END)
    
        avrg_cpu_usage = (sum(self.cpu_usage) / self.simulation_time ) * 100
        self.stats_text.insert(tk.END, f"CPU usage %: {round(avrg_cpu_usage,2)}%\n")
        avrg_execution_time = mean(self.execution_time) if self.execution_time else 0
        self.stats_text.insert(tk.END, f"Average Execution Time: {round(avrg_execution_time, 2)}\n")
        avrg_waiting_time = mean(self.process_waiting_times) if self.process_waiting_times else 0
        self.stats_text.insert(tk.END, f"Average Waiting Time: {round(avrg_waiting_time, 2)}\n")
        avrg_blocked_time = mean(self.blocked_time) if self.blocked_time else 0
        self.stats_text.insert(tk.END, f"Average Blocked Time: {round(avrg_blocked_time, 2)}\n")
        self.stats_text.insert(tk.END, f"Total processes completed: {len(self.finished_processes)}\n")
        self.stats_text.insert(tk.END, f"Simulation time: {round(self.simulation_time, 2)} seconds\n")
        self.update_idletasks()
        
        
    def update_timers(self):
        """Update all the timers involved in the simulation"""
        
        self.arrival_time += self.dt
        self.burst_time += self.dt
        
        for process in self.ready_processes:
            process.waiting_time += self.dt
            
            
        for process in self.blocked_processes:
            if not process.still_bloked(self.dt):
                self.blocked_processes.remove(process)
                self.processes.append(process)
                self.ready_processes.append(process)
            
            
        if not self.cpu_available:
            self.cpu_usage_time += self.dt
            self.current_process.remaining_burst_time -= (self.dt)
            
            rand = random.randint(0,3000)
            
            if  rand == 11:
                
                self.current_process.bloked = True
                self.current_process.blocked_time = 0
                blocked_time = random.randint(1,7)
                self.current_process.blocked_max_time = blocked_time
                self.blocked_time.append(blocked_time)
                self.blocked_processes.append(self.current_process)
                
                self.cpu_available = True
                self.current_process = None
            
        self.simulation_time += self.dt