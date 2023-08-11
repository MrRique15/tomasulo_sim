from tools.mem_inst import Instruction_Memory
from pprint import pprint
data_set_path = 'data_sets/teste1.txt'

def tomasulo() -> None:
    instruction_memory = Instruction_Memory() # memoria de instruções para guardar instruções de entrada
    
    with open(data_set_path) as raw_data:        # abertura e leitura de cada linha do arquivo
        for line in raw_data:             
            line = line.replace("\n", "")        # limpa o '\n' de cada linha       
            instruction_memory.insert_item(line) # insere a instrução na memória de instruções
            
    pprint(instruction_memory.inst_mem)          # imprime a memória de instruções (lista de strings)
    
if __name__ == '__main__':
    tomasulo()