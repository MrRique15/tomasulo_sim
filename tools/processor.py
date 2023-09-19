from tools.stations_and_units import Reserv_Station, Functional_Unit, Registers
from tools.instruction_utils import Utils
import os

debug = False

class Processor():
    def __init__(self):
        self.instructions_memory = []
        self.out_put_path = ''
        self.dispatch_queue = [None for i in range(5)]
        self.data_memory = [0 for i in range(512)]
        self.registers = [Registers(number=i,qi=0,value=0) for i in range(32)]
        self.pc = 0
        self.is_branching = False
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
        
    def start_processing(self, out_put_path: str) -> None:
        self.clocks_to_finish = len(self.instructions_memory)
        self.out_put_path = out_put_path
               
        while(self.clocks_to_finish != 0):
            self.process_clock()
            self.clock += 1
            
            with open(self.out_put_path, 'a') as output_file:
                output_file.write("----==========================================================================================================----\n")
                output_file.write(f"----==============================================[ CLOCK: {self.clock:{3}} ]==============================================----\n")
                output_file.write("----==========================================================================================================----\n")
                
            print("----==========================================================================================================----")
            print(f"----==============================================[ CLOCK: {self.clock:{3}} ]==============================================----")
            print("----==========================================================================================================----")
            self.print_reserv_stations_status()
            self.print_functional_units_status()
            self.print_registers_status()
            
            self.clocks_to_finish = self.verify_remaining_clocks()
            
            # print_memory = input("Print memory? (y/n): ")
            # if print_memory == 'y':
            #     self.print_memory_status()
            
            with open(self.out_put_path, 'a') as output_file:
                output_file.write("----==========================================================================================================----\n")
            print("----==========================================================================================================----")
            
            next_clock = input("Next clock? (y/n): ")
            if next_clock == 'n':
                break
            
            clear_output = input("Clear Output? (y/n): ")
            if clear_output == 'y':
                os.system('cls' if os.name == 'nt' else 'clear')
        
        print("End of processing achieved! Exiting...")
        self.clear_processor()
        
    def process_clock(self) -> None:
        self.process_functional_units()   # processa as unidades funcionais
        self.process_reserv_stations()    # processa as estações de reserva
        self.dispatch_instruction()       # tenta despachar novas instruções se possível
        
        # travando busca e despacho quando um branch está em andamento.
        if not self.is_branching:
            self.populete_dispatch_queue()    # popula a fila de despacho
            
        return None
        
    def process_functional_units(self) -> None:
        for load_unit in self.load_functional_units:
            if load_unit.busy and load_unit.operation_clocks > 0:
                load_result = load_unit.operate()
                if load_result != "still operating":
                    load_station_index = int(load_unit.reserv_station_name[4:]) - 1
                    
                    if load_result == 'lw':
                        address = self.load_stations[load_station_index].A + self.load_stations[load_station_index].Vj
                        self.load_stations[load_station_index].A = address
                        self.load_stations[load_station_index].Vj = None
                        self.load_stations[load_station_index].result = self.data_memory[address]
                        
                    elif load_result == 'sw':
                        address = self.load_stations[load_station_index].A + self.load_stations[load_station_index].Vk
                        self.load_stations[load_station_index].A = address
                        self.load_stations[load_station_index].result = self.load_stations[load_station_index].Vj
                        self.load_stations[load_station_index].Vk = None
                        
                    self.load_stations[load_station_index].clock_cycles = 2
                    load_unit.clear_unit()
            
        for add_unit in self.add_functional_units:
            if add_unit.busy and add_unit.operation_clocks > 0:
                add_result = add_unit.operate()
                if add_result != "still operating":
                    add_station_index = int(add_unit.reserv_station_name[3:]) - 1
                    
                    if add_result in ['add', 'addi']:
                        sum_result = self.add_stations[add_station_index].Vj + self.add_stations[add_station_index].Vk
                        self.add_stations[add_station_index].result = sum_result
                        
                    elif add_result in ['sub', 'subi']:
                        sub_result = self.add_stations[add_station_index].Vj - self.add_stations[add_station_index].Vk
                        self.add_stations[add_station_index].result = sub_result
                        
                    elif add_result in ['blt', 'bgt', 'beq', 'bne']:
                        if add_result == 'blt':
                            if self.add_stations[add_station_index].Vj < self.add_stations[add_station_index].Vk:
                                self.add_stations[add_station_index].result = self.add_stations[add_station_index].A
                            else:
                                self.add_stations[add_station_index].result = None
                                
                        elif add_result == 'bgt':
                            if self.add_stations[add_station_index].Vj > self.add_stations[add_station_index].Vk:
                                self.add_stations[add_station_index].result = self.add_stations[add_station_index].A
                            else:
                                self.add_stations[add_station_index].result = None
                                
                        elif add_result == 'beq':
                            if self.add_stations[add_station_index].Vj == self.add_stations[add_station_index].Vk:
                                self.add_stations[add_station_index].result = self.add_stations[add_station_index].A
                            else:
                                self.add_stations[add_station_index].result = None
                                
                        elif add_result == 'bne':
                            if self.add_stations[add_station_index].Vj != self.add_stations[add_station_index].Vk:
                                self.add_stations[add_station_index].result = self.add_stations[add_station_index].A
                            else:
                                self.add_stations[add_station_index].result = None
                    
                    elif add_result == 'not':
                        not_result = ~self.add_stations[add_station_index].Vj
                        self.add_stations[add_station_index].result = not_result
                        
                    elif add_result == 'and':
                        and_result = self.add_stations[add_station_index].Vj & self.add_stations[add_station_index].Vk
                        self.add_stations[add_station_index].result = and_result
                        
                    elif add_result == 'or':
                        or_result = self.add_stations[add_station_index].Vj | self.add_stations[add_station_index].Vk
                        self.add_stations[add_station_index].result = or_result
                        
                    self.add_stations[add_station_index].clock_cycles = 2
                    add_unit.clear_unit()
            
        for mult_unit in self.mult_functional_units:
            if mult_unit.busy and mult_unit.operation_clocks > 0:
                mult_result = mult_unit.operate()
                if mult_result != "still operating":
                    mult_station_index = int(mult_unit.reserv_station_name[4:]) - 1
                    
                    if mult_result == 'mul':
                        mult_result = self.mult_stations[mult_station_index].Vj * self.mult_stations[mult_station_index].Vk
                        self.mult_stations[mult_station_index].result = mult_result
                    
                    elif mult_result == 'div':
                        div_result = self.mult_stations[mult_station_index].Vj / self.mult_stations[mult_station_index].Vk
                        self.mult_stations[mult_station_index].result = div_result
                        
                    self.mult_stations[mult_station_index].clock_cycles = 2
                    mult_unit.clear_unit()
                    
        return None
            
    def process_reserv_stations(self) -> None:
        # escrevendo resultados de instruções que finalizaram execução há 1 ciclo atrás
        for load_station in self.load_stations:
            if load_station.busy and load_station.clock_cycles == 2:
                load_station.clock_cycles -= 1
                
            elif load_station.busy and load_station.clock_cycles == 1:
                load_station.clock_cycles -= 1
                self.propagate_result(load_station)
                
                if load_station.operand == 'lw':
                    for register in self.registers:
                        if register.Qi == load_station.name:
                            register.value = load_station.result
                            register.Qi = 0
                            break
                    
                elif load_station.operand == 'sw':
                    self.data_memory[load_station.A] = load_station.result
                
                load_station.clear_station()
                
        for add_station in self.add_stations:
            if add_station.busy and add_station.clock_cycles == 2:
                add_station.clock_cycles -= 1
                
            elif add_station.busy and add_station.clock_cycles == 1:
                add_station.clock_cycles -= 1
                self.propagate_result(add_station)
                
                if add_station.operand in ['add', 'sub', 'addi', 'subi', 'not', 'and', 'or']:
                    for register in self.registers:
                        if register.Qi == add_station.name:
                            register.value = add_station.result
                            register.Qi = 0
                            break
                
                elif add_station.operand in ['blt', 'bgt', 'beq', 'bne']:
                    if add_station.result != None:
                        self.pc = add_station.result
                        
                    # com a escrita do branch, destrava busca e despacho de instruções
                    self.is_branching = False
                
                add_station.clear_station()
            
        for mult_station in self.mult_stations:
            if mult_station.busy and mult_station.clock_cycles == 2:
                mult_station.clock_cycles -= 1
                
            elif mult_station.busy and mult_station.clock_cycles == 1:
                mult_station.clock_cycles -= 1
                self.propagate_result(mult_station)
                
                if mult_station.operand in ['mul', 'div']:
                    for register in self.registers:
                        if register.Qi == mult_station.name:
                            register.value = mult_station.result
                            register.Qi = 0
                            break
                
                mult_station.clear_station()
    
        # iniciando execução de instruções que estavam aguardando resultados
        for load_station in self.load_stations:
            if not load_station.busy:
                continue
            if load_station.clock_cycles != 5:
                continue
            
            if load_station.Qj == None and load_station.Qk == None:
                for load_unit in self.load_functional_units:
                    if load_unit.busy:
                        continue
                    
                    load_unit.popule_unit(
                        operand=load_station.operand,
                        operation_clocks=4,
                        reserv_station_name=load_station.name
                    )
                    load_station.clock_cycles -= 1
                    break
        
        for add_station in self.add_stations:
            if not add_station.busy:
                continue
            if add_station.clock_cycles != 5:
                continue
            
            if add_station.Qj == None and add_station.Qk == None:
                for add_unit in self.add_functional_units:
                    if add_unit.busy:
                        continue
                    
                    add_unit.popule_unit(
                        operand=add_station.operand,
                        operation_clocks=4,
                        reserv_station_name=add_station.name
                    )
                    add_station.clock_cycles -= 1
                    break
                
        for mult_station in self.mult_stations:
            if not mult_station.busy:
                continue
            if mult_station.clock_cycles != 15 and mult_station.operand == 'mul':
                continue
            if mult_station.clock_cycles != 25 and mult_station.operand == 'div':
                continue
            
            if mult_station.Qj == None and mult_station.Qk == None:
                for mult_unit in self.mult_functional_units:
                    if mult_unit.busy:
                        continue
                    
                    mult_unit.popule_unit(
                        operand=mult_station.operand,
                        operation_clocks=14 if mult_station.operand == 'mul' else 24,
                        reserv_station_name=mult_station.name
                    )
                    mult_station.clock_cycles -= 1
                    break
                
        return None
    
    def propagate_result(self, station) -> None:
        for add_station in self.add_stations:
            if add_station.busy and add_station.Qj == station.name:
                add_station.Vj = station.result
                add_station.Qj = None
            if add_station.busy and add_station.Qk == station.name:
                add_station.Vk = station.result
                add_station.Qk = None
        
        for mult_station in self.mult_stations:
            if mult_station.busy and mult_station.Qj == station.name:
                mult_station.Vj = station.result
                mult_station.Qj = None
            if mult_station.busy and mult_station.Qk == station.name:
                mult_station.Vk = station.result
                mult_station.Qk = None
        
        for load_station in self.load_stations:
            if load_station.busy and load_station.Qj == station.name:
                load_station.Vj = station.result
                load_station.Qj = None
            if load_station.busy and load_station.Qk == station.name:
                load_station.Vk = station.result
                load_station.Qk = None
        return None
    
    def dispatch_instruction(self) -> None:
        if self.dispatch_queue[0] != None:
            dispatching_instruction = self.dispatch_queue.pop(0)
            self.dispatch_queue.append(None)
            self.dispatch_instruction_to_station(dispatching_instruction)
            return None
            
    def dispatch_instruction_to_station(self, instruction) -> None:
        op = instruction.op
        
        if op in ['add', 'sub', 'and', 'or']:
            for add_station in self.add_stations:
                if not add_station.busy:
                    add_station.popule_station(
                        operand=op,
                        Vj=self.registers[instruction.rs].value if self.registers[instruction.rs].Qi == 0 else None,
                        Vk=self.registers[instruction.rt].value if self.registers[instruction.rt].Qi == 0 else None,
                        Qj=self.registers[instruction.rs].Qi if self.registers[instruction.rs].Qi != 0 else None,
                        Qk=self.registers[instruction.rt].Qi if self.registers[instruction.rt].Qi != 0 else None,
                        A=None,
                        clock_cycles=instruction.cycles
                    )
                    self.registers[instruction.rd].Qi = add_station.name
                    return None
        elif op in ['addi', 'subi']:
            for add_station in self.add_stations:
                if not add_station.busy:
                    add_station.popule_station(
                        operand=op,
                        Vj=self.registers[instruction.rs].value if self.registers[instruction.rs].Qi == 0 else None,
                        Vk=instruction.imm,
                        Qj=self.registers[instruction.rs].Qi if self.registers[instruction.rs].Qi != 0 else None,
                        Qk=None,
                        A=None,
                        clock_cycles=instruction.cycles
                    )
                    self.registers[instruction.rd].Qi = add_station.name
                    return None
        elif op in ['mul', 'div']:
            for mult_station in self.mult_stations:
                if not mult_station.busy:
                    mult_station.popule_station(
                        operand=op,
                        Vj=self.registers[instruction.rs].value if self.registers[instruction.rs].Qi == 0 else None,
                        Vk=self.registers[instruction.rt].value if self.registers[instruction.rt].Qi == 0 else None,
                        Qj=self.registers[instruction.rs].Qi if self.registers[instruction.rs].Qi != 0 else None,
                        Qk=self.registers[instruction.rt].Qi if self.registers[instruction.rt].Qi != 0 else None,
                        A=None,
                        clock_cycles=instruction.cycles
                    )
                    self.registers[instruction.rd].Qi = mult_station.name
                    return None
        elif op in ['blt', 'bgt', 'beq', 'bne']:
            for add_station in self.add_stations:
                if not add_station.busy:
                    add_station.popule_station(
                        operand=op,
                        Vj=self.registers[instruction.rs].value if self.registers[instruction.rs].Qi == 0 else None,
                        Vk=self.registers[instruction.rt].value if self.registers[instruction.rt].Qi == 0 else None,
                        Qj=self.registers[instruction.rs].Qi if self.registers[instruction.rs].Qi != 0 else None,
                        Qk=self.registers[instruction.rt].Qi if self.registers[instruction.rt].Qi != 0 else None,
                        A=instruction.imm,
                        clock_cycles=instruction.cycles
                    )
                    return None
        elif op in ['not']:
            for add_station in self.add_stations:
                if not add_station.busy:
                    add_station.popule_station(
                        operand=op,
                        Vj=self.registers[instruction.rs].value if self.registers[instruction.rs].Qi == 0 else None,
                        Vk=None,
                        Qj=self.registers[instruction.rs].Qi if self.registers[instruction.rs].Qi != 0 else None,
                        Qk=None,
                        A=None,
                        clock_cycles=instruction.cycles
                    )
                    self.registers[instruction.rd].Qi = add_station.name
                    return None
        elif op == "lw":
            for load_station in self.load_stations:
                if not load_station.busy:
                    load_station.popule_station(
                        operand=op,
                        Vj=self.registers[instruction.rs].value if self.registers[instruction.rs].Qi == 0 else None,
                        Vk=None,
                        Qj=self.registers[instruction.rs].Qi if self.registers[instruction.rs].Qi != 0 else None,
                        Qk=None,
                        A=instruction.imm,
                        clock_cycles=instruction.cycles
                    )
                    self.registers[instruction.rd].Qi = load_station.name
                    return None
        elif op == "sw":
            for load_station in self.load_stations:
                if not load_station.busy:
                    load_station.popule_station(
                        operand=op,
                        Vj=self.registers[instruction.rs].value if self.registers[instruction.rs].Qi == 0 else None,
                        Vk=self.registers[instruction.rt].value if self.registers[instruction.rt].Qi == 0 else None,
                        Qj=self.registers[instruction.rs].Qi if self.registers[instruction.rs].Qi != 0 else None,
                        Qk=self.registers[instruction.rt].Qi if self.registers[instruction.rt].Qi != 0 else None,
                        A=instruction.imm,
                        clock_cycles=instruction.cycles
                    )
                    return None
    
    def populete_dispatch_queue(self) -> None:
        for i in range(len(self.dispatch_queue)):
            if self.dispatch_queue[i] == None:
                if self.pc < len(self.instructions_memory):
                    
                    # encontrada instrução de desvio, trava novas buscas até resolver
                    if self.instructions_memory[self.pc].op in ['blt', 'bgt', 'beq', 'bne']:
                        self.is_branching = True
                        
                    self.dispatch_queue[i] = self.instructions_memory[self.pc]
                    self.pc += 1
                    return None
                else:
                    print("No more instructions to put in dispatch queue")
                    return None
        return None
    
    def print_reserv_stations_status(self) -> None:
        print("---------------------------------------------------[ Reserv Stations Status ]---------------------------------------------------")
        print("=====================================================")
        print("LOAD Stations:")
        for load_station in self.load_stations:
            print(load_station.__str__())
        print("=====================================================")
        print("ADD Stations:")
        for add_station in self.add_stations:
            print(add_station.__str__())
        print("=====================================================")
        print("MULT Stations:")
        for mult_station in self.mult_stations:
            print(mult_station.__str__())
        print("=====================================================")
        print("--------------------------------------------------------------------------------------------------------------------------------")
        
        with open(self.out_put_path, 'a') as output_file:
            output_file.write("---------------------------------------------------[ Reserv Stations Status ]---------------------------------------------------\n")
            output_file.write("=====================================================\n")
            output_file.write("LOAD Stations:\n")
            for load_station in self.load_stations:
                output_file.write(load_station.__str__())
                output_file.write('\n')
            output_file.write("=====================================================\n")
            output_file.write("ADD Stations:\n")
            for add_station in self.add_stations:
                output_file.write(add_station.__str__())
                output_file.write('\n')
            output_file.write("=====================================================\n")
            output_file.write("MULT Stations:\n")
            for mult_station in self.mult_stations:
                output_file.write(mult_station.__str__())
                output_file.write('\n')
            output_file.write("=====================================================\n")
            output_file.write("--------------------------------------------------------------------------------------------------------------------------------\n")
        
        return None
    
    def print_functional_units_status(self) -> None:
        print("---------------------------------------------------[ Functional Units Status ]--------------------------------------------------")
        print("=====================================================")
        print("LOAD Units:")
        for load_unit in self.load_functional_units:
            print(load_unit.__str__())
        print("=====================================================")
        print("ADD Units:")
        for add_unit in self.add_functional_units:
            print(add_unit.__str__())
        print("=====================================================")
        print("MULT Units:")
        for mult_unit in self.mult_functional_units:
            print(mult_unit.__str__())
        print("=====================================================")
        print("--------------------------------------------------------------------------------------------------------------------------------")
        
        with open(self.out_put_path, 'a') as output_file:
            output_file.write("---------------------------------------------------[ Functional Units Status ]---------------------------------------------------\n")
            output_file.write("=====================================================\n")
            output_file.write("LOAD Units:\n")
            for load_unit in self.load_functional_units:
                output_file.write(load_unit.__str__())
                output_file.write('\n')
            output_file.write("=====================================================\n")
            output_file.write("ADD Units:\n")
            for add_unit in self.add_functional_units:
                output_file.write(add_unit.__str__())
                output_file.write('\n')
            output_file.write("=====================================================\n")
            output_file.write("MULT Units:\n")
            for mult_unit in self.mult_functional_units:
                output_file.write(mult_unit.__str__())
                output_file.write('\n')
            output_file.write("=====================================================\n")
            output_file.write("--------------------------------------------------------------------------------------------------------------------------------\n")
        
            
        return None
    
    def print_registers_status(self) -> None:
        print("---------------------------------------------------[ Registers Status ]---------------------------------------------------------")
        print("=====================================================")
        for register in self.registers:
            print(register.__str__())
        print("=====================================================")
        print("--------------------------------------------------------------------------------------------------------------------------------")
        
        with open(self.out_put_path, 'a') as output_file:
            output_file.write("---------------------------------------------------[ Registers Status ]---------------------------------------------------------\n")
            output_file.write("=====================================================\n")
            for register in self.registers:
                output_file.write(register.__str__())
                output_file.write('\n')
            output_file.write("=====================================================\n")
            output_file.write("--------------------------------------------------------------------------------------------------------------------------------\n")
        return None
    
    def print_memory_status(self) -> None:
        print("---------------------------------------------------[ Memory Status ]------------------------------------------------------------")
        print("=====================================================")
        for i in range(len(self.data_memory)):
            print(f"Data Memory [{i:{3}}] = {self.data_memory[i]}")
        print("=====================================================")
        print("--------------------------------------------------------------------------------------------------------------------------------")
        
        with open(self.out_put_path, 'a') as output_file:
            output_file.write("---------------------------------------------------[ Memory Status ]---------------------------------------------------------\n")
            output_file.write("=====================================================\n")
            for i in range(len(self.data_memory)):
                output_file.write(f"Data Memory [{i:{3}}] = {self.data_memory[i]}\n")
            output_file.write("=====================================================\n")
            output_file.write("--------------------------------------------------------------------------------------------------------------------------------\n")
        
        return None
    
    def verify_remaining_clocks(self):
        for load_station in self.load_stations:
            if load_station.busy and load_station.clock_cycles > 0:
                return 1
            
        for add_station in self.add_stations:
            if add_station.busy and add_station.clock_cycles > 0:
                return 1
            
        for mult_station in self.mult_stations:
            if mult_station.busy and mult_station.clock_cycles > 0:
                return 1
            
        for instruction in self.dispatch_queue:
            if instruction != None:
                return 1
        
        return 0
    
    def clear_processor(self):
        self.instructions_memory = []
        self.dispatch_queue = [None for i in range(5)]
        self.data_memory = [0 for i in range(512)]
        self.registers = [Registers(number=i,qi=0,value=0) for i in range(32)]
        self.pc = 0
        self.clock = 0
        self.clocks_to_finish = 0
        self.load_stations = [Reserv_Station(name=f"LOAD{i+1}") for i in range(16)]
        self.add_stations = [Reserv_Station(name=f"ADD{i+1}") for i in range(16)]
        self.mult_stations = [Reserv_Station(name=f"MULT{i+1}") for i in range(16)]
        self.load_functional_units = [Functional_Unit(name=f"LOAD{i+1}") for i in range(3)]
        self.add_functional_units = [Functional_Unit(name=f"ADD{i+1}") for i in range(3)]
        self.mult_functional_units = [Functional_Unit(name=f"MULT{i+1}") for i in range(3)]
        return None