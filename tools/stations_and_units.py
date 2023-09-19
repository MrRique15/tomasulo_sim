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
        self.clock_cycles = 0
        self.result = None
        
    def __str__(self):
        return f"Name: {self.name:{6}} | Busy: {self.busy} | Operand: {self.operand} | Vj: {self.Vj} | Vk: {self.Vk} | Qj: {self.Qj} | Qk: {self.Qk} | A: {self.A}"
    
    def popule_station(self, operand: str, Vj: int, Vk: int, Qj: str, Qk: str, A: int, clock_cycles: int):
        self.busy = True
        self.operand = operand
        self.Vj = Vj
        self.Vk = Vk
        self.Qj = Qj
        self.Qk = Qk
        self.A = A
        self.clock_cycles = clock_cycles
        self.result = None
        
    def clear_station(self):
        self.busy = False
        self.operand = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None
        self.clock_cycles = 0
        self.result = None
        
class Functional_Unit():
    def __init__(self, name:str):
        self.name = name
        self.busy = False
        self.operand = None
        self.operation_clocks = 0
        self.reserv_station_name = None
        
    def __str__(self):
        return f"Name: {self.name:{6}} | Busy: {self.busy} | Operand: {self.operand} | Operation Clocks: {self.operation_clocks}"
    
    def popule_unit(self, operand: str, operation_clocks: int, reserv_station_name: str):
        self.busy = True
        self.operand = operand
        self.operation_clocks = operation_clocks
        self.reserv_station_name = reserv_station_name
        
    def clear_unit(self):
        self.busy = False
        self.operand = None
        self.operation_clocks = 0
        self.reserv_station_name = None
        
    def operate(self) -> str:
        if self.busy and self.operation_clocks > 0:
            self.operation_clocks -= 1
        
            if self.operation_clocks == 0:
                return self.operand
            else:
                return "still operating"
        
class Registers():
    def __init__(self, number:int, qi:int, value:int):
        self.number = number
        self.Qi = 0
        self.value = 0
        
    def set_register_qi(self, qi: int):
        self.Qi = qi
        
    def set_register_value(self, value: int):
        self.value = value
        
    def clear_register(self):
        self.Qi = 0
        self.value = 0
        
    def __str__(self):
        return f"R{self.number:{2}} --> Qi: {self.Qi:{6}} | Value: {self.value:{4}}"
