class Process():
    
    def __init__(self, _pid, _arrival_time, _burst_time, _priority):
        self.pid = _pid
        self.arrival_time = _arrival_time
        self.burst_time = _burst_time
        self.priority = _priority
        self.waiting_time = 0
        self.remaining_burst_time = self.burst_time