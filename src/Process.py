"""
Authors:
- Iván Maldonado (Kikemaldonado11@gmail.com)
- Maria José Vera (nandadevi97816@gmail.com)
- Sergio Fernández (sergiofnzg@gmail.com)

Developed at: September 2024
"""


class Process():
    
    def __init__(self, _pid, _arrival_time, _burst_time, _priority):
        self.pid = _pid
        self.arrival_time = _arrival_time
        self.burst_time = _burst_time
        self.priority = _priority
        self.waiting_time = 0
        self.remaining_burst_time = self.burst_time
        self.blocked = False
        self.blocked_time = 0
        self.blocked_max_time = 0
        
        
    def still_bloked(self, dt):
        
        self.blocked_time += dt
        
        if self.blocked_time >= self.blocked_max_time:
            self.blocked = False
            return self.blocked
        else:
            return True           