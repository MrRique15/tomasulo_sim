from tools.mem_inst import Instruction_Memory
from tools.instruction_utils import Utils
from tools.processor import Processor
from pprint import pprint
data_set_path = 'data_sets/teste2.txt'

def tomasulo() -> None:
    instruction_memory = Instruction_Memory() # memoria de instruções para guardar instruções de entrada
    utils = Utils()
    main_processor = Processor()
    
    with open(data_set_path) as raw_data:        # abertura e leitura de cada linha do arquivo
        for line in raw_data:                
            list_instruction = utils.instruction_to_list(instruction=line)
            instruction_memory.insert_item(
                utils.Instruction(instruction=list_instruction)
            )                                    # formata e insere a instrução na memória de instruções
    
    print("-----------------------------------------[ Instruction memory ]-----------------------------------------")
    for item in instruction_memory.inst_mem:
        print(item.__dict__)
    print("--------------------------------------------------------------------------------------------------------")
        
    main_processor.set_instruction_memory(instructions_memory=instruction_memory.inst_mem) # seta a memória de instruções no processador
    main_processor.start_processing() # inicia o processamento das instruções

    print("End of processing achieved! Exiting...")

if __name__ == '__main__':
    tomasulo()