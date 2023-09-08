
class Utils:
    
    def __init__(self)->None:
        self.help_text = "utils tool to help in data formating"
    
    def instruction_to_list(self, instruction:str)->list:
        instruction = instruction.replace("\n", "")                         # limpa o \n da string recebida
        lst_instruction = instruction.split(" ")              # separa operando dos registradores e valores
        lst_instruction[1] = lst_instruction[1].split(",")    # cria uma lista com cada registrador ou valor recebido
        return lst_instruction
    
    class Instruction:
        
        def __init__(self, instruction:list)->None:
            self.op = instruction[0]
            self.rd = None 
            self.rs = None 
            self.rt = None 
            self.imm = None 
            self.cycles = None
            self.prepare(instruction=instruction)
        
        def prepare(self, instruction:list)->None:
            operands_list = instruction[1] # lista de operandos à ser tratada
            
            if self.op in ['add', 'sub', 'mul', 'div', 'and', 'or']:
                self.rd = operands_list[0]
                self.rs = operands_list[1]
                self.rt = operands_list[2]
                self.cycles = 5
                
                # definição de ciclos maiores para MUL e DIV como na tabela
                match self.op:
                    case "mul": 
                        self.cycles = 15
                    case "div":
                        self.cycles = 25
                    case _:
                        self.cycles = 5
            
            elif self.op in ['addi', 'subi']:
                self.rd = operands_list[0]
                self.rs = operands_list[1]
                self.imm = operands_list[2]
                self.cycles = 5

            elif self.op in ['blt', 'bgt', 'beq', 'bne']:
                self.rs = operands_list[0]
                self.rt = operands_list[1]
                self.imm = operands_list[2]
                self.cycles = 5
                
            else:
                match self.op:
                    case 'not':
                        self.rd = operands_list[0]
                        self.rs = operands_list[1]
                        self.cycles = 5

                    case 'j':
                        self.imm = operands_list[1]
                        self.cycles = 5

                    case 'lw':
                        self.rd = operands_list[0]
                        imm_rs = operands_list[1].replace("(", " ").replace(")", "")
                        imm, rs = imm_rs.split(" ")
                        self.rs = rs
                        self.imm = imm
                        self.cycles = 5

                    case 'sw':
                        self.rs = operands_list[0]
                        imm_rt = operands_list[1].replace("(", " ").replace(")", "")
                        imm, rt = imm_rt.split(" ")
                        self.rt = rt
                        self.imm = imm
                        self.cycles = 5

                    case "movi":
                        self.op = "addi"
                        self.rd = operands_list=[0]
                        self.rs = "r0"
                        self.imm = operands_list[1]
                        self.cycles = 5
                        
                    case "mov":
                        self.op = "add"
                        self.rd = operands_list[0]
                        self.rs = "r0"
                        self.rt = operands_list[1]
                        self.cycles = 5
                        
                    case _:
                        raise(f"invalid operation inserted {self.op}")

            self.rd = int(self.rd.replace("r", "")) if self.rd != None else None
            self.rs = int(self.rs.replace("r", "")) if self.rs != None else None
            self.rt = int(self.rt.replace("r", "")) if self.rt != None else None
            self.imm = int(self.imm) if self.imm != None else None