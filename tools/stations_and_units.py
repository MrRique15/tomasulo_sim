class Reserv_Station():
    def __init__(self, name: str):
        self.name = name
        self.busy = False
        self.operand = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None
        self.operation_clocks = 0
        
    def __str__(self):
        return f"Name: {self.name} | Busy: {self.busy} | Operand: {self.operand} | Vj: {self.Vj} | Vk: {self.Vk} | Qj: {self.Qj} | Qk: {self.Qk} | A: {self.A} | Operation Clocks: {self.operation_clocks}"
    
    def popule_station(self, operand: str, Vj: int, Vk: int, Qj: str, Qk: str, A: int, operation_clocks: int):
        self.busy = True
        self.operand = operand
        self.Vj = Vj
        self.Vk = Vk
        self.Qj = Qj
        self.Qk = Qk
        self.A = A
        self.operation_clocks = operation_clocks
        
    def clear_station(self):
        self.busy = False
        self.operand = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None
        self.operation_clocks = 0
        
    def operate(self):
        if self.busy and self.operation_clocks > 0:
            self.operation_clocks -= 1
            if self.operation_clocks == 0:
                return "finished"
            else:
                return "still operating"
        else:
            return False
        
class Functional_Unit():
    def __init__(self, name:str):
        self.name = name
        self.busy = False
        self.operand = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None
        self.operation_clocks = 0
        self.reserv_station_name = None
        
    def __str__(self):
        return f"Name: {self.name} | Busy: {self.busy} | Operand: {self.operand} | Vj: {self.Vj} | Vk: {self.Vk} | Qj: {self.Qj} | Qk: {self.Qk} | A: {self.A} | Operation Clocks: {self.operation_clocks}"
    
    def popule_unit(self, operand: str, Vj: int, Vk: int, Qj: str, Qk: str, A: int, operation_clocks: int, reserv_station_name: str):
        self.busy = True
        self.operand = operand
        self.Vj = Vj
        self.Vk = Vk
        self.Qj = Qj
        self.Qk = Qk
        self.A = A
        self.operation_clocks = operation_clocks
        self.reserv_station_name = reserv_station_name
        
    def clear_unit(self):
        self.busy = False
        self.operand = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None
        self.operation_clocks = 0
        self.reserv_station_name = None
        
    def operate(self):
        if self.busy and self.operation_clocks > 0:
            self.operation_clocks -= 1
        
            if self.operation_clocks == 0:
                # match self.operand:
                #     case 'add':
                #         return self.Vj + self.Vk
                #     case 'sub':
                #         return self.Vj - self.Vk
                #     case 'mult':
                #         return self.Vj * self.Vk
                #     case 'div':
                #         return self.Vj / self.Vk
                #     case 'addi':
                #         return self.Vj + self.Vk
                #     case 'subi':
                #         return self.Vj - self.Vk
                #     case 'not':
                #         return ~self.Vj
                #     case 'lw':
                #         return self.Vj + self.Vk
                #     case 'sw':
                #         return self.Vj + self.Vk
                #     case 'movi':
                #         return self.Vj + self.Vk
                #     case 'mov':
                #         return self.Vj + self.Vk
                #     case 'blt':
                #         return self.Vj + self.Vk
                #     case 'bgt':
                #         return self.Vj + self.Vk
                #     case 'beq':
                #         return self.Vj + self.Vk
                #     case 'bne':
                #         return self.Vj + self.Vk
                #     case 'j':
                #         return self.Vj + self.Vk
                #     case _:
                #         raise(f"invalid operation inserted {self.operand}")
                return "finished"
            else:
                return "still operating"
        