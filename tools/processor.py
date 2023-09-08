from tools.stations_and_units import Reserv_Station, Functional_Unit

debug = False

class Processor():
    def __init__(self):
        self.instructions_memory = []
        self.data_memory = [0 for i in range(512)]
        self.registers = [0 for i in range(32)]
        self.pc = 0
        self.clock = 0
        self.clocks_to_finish = 0
        self.load_stations = [Reserv_Station(name=f"LOAD{i+1}") for i in range(16)]
        self.add_stations = [Reserv_Station(name=f"ADD{i+1}") for i in range(16)]
        self.mult_stations = [Reserv_Station(name=f"MULT{i+1}") for i in range(16)]
        self.load_functional_units = [Functional_Unit(name=f"LOAD{i+1}") for i in range(3)]
        self.add_functional_units = [Functional_Unit(name=f"ADD{i+1}") for i in range(3)]
        self.mult_functional_units = [Functional_Unit(name=f"MULT{i+1}") for i in range(3)]
    
    def set_instruction_memory(self, instructions_memory: list):
        self.instructions_memory = instructions_memory
        
    def start_processing(self):
        self.clocks_to_finish = len(self.instructions_memory)
        
        while(self.clocks_to_finish != 0):
            self.process_clock()
            self.clock += 1
            print("=====================================================")
            print(f"Clock: {self.clock}")
            print("=====================================================")
            self.print_reserv_stations_status()
            self.print_functional_units_status()
            self.print_registers_status()
            
            self.clocks_to_finish = self.verify_remaining_clocks()
            
            print_memory = input("Print memory? (y/n): ")
            if print_memory == 'y':
                self.print_memory_status()
                
            print("=====================================================")
            print("=====================================================")
            
            next_clock = input("Next clock? (y/n): ")
            if next_clock == 'n':
                break
            
            
    def process_clock(self) -> None:
        self.process_functional_units()   # processa as unidades funcionais
        self.process_reserv_stations()    # processa as estações de reserva
        self.process_instructions()       # tenta despachar novas instruções se possível
        
    def process_functional_units(self) -> None:
        for load_unit in self.load_functional_units:
            load_result = load_unit.operate()
            if load_result == "finished":
                pass
            # finish processing function
            
        for add_unit in self.add_functional_units:
            add_result = add_unit.operate()
            if add_result == "finished":
                pass
            # finish processing function
            
        for mult_unit in self.mult_functional_units:
            mult_result = mult_unit.operate()
            if mult_result == "finished":
                pass
            # finish processing function
            
    def process_reserv_stations(self) -> None:
        for load_station in self.load_stations:
            load_result = load_station.operate()
            if load_result == "finished":
                pass
            # finish processing function
            
        for add_station in self.add_stations:
            add_result = add_station.operate()
            if add_result == "finished":
                pass
            # finish processing function
            
        for mult_station in self.mult_stations:
            mult_result = mult_station.operate()
            if mult_result == "finished":
                pass
            # finish processing function
            
    def process_instructions(self) -> None:
        if self.pc < len(self.instructions_memory):
            instruction = self.instructions_memory[self.pc]
            if debug == True:
                print(f"Instruction: {instruction}")
            dispatched = self.dispatch_instruction(instruction=instruction)
            
            if dispatched:
                self.pc += 1
            
    def dispatch_instruction(instruction: list) -> bool:
        pass
        # criar despacho com possíveis verificações
    
    
    def verify_remaining_clocks(self):
        for load_station in self.load_stations:
            if load_station.busy and load_station.operation_clocks > 0:
                return 1
            
        for add_station in self.add_stations:
            if add_station.busy and add_station.operation_clocks > 0:
                return 1
            
        for mult_station in self.mult_stations:
            if mult_station.busy and mult_station.operation_clocks > 0:
                return 1
        return 0