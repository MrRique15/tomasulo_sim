class Instruction_Memory():
    def __init__(self) -> None:
        self.inst_mem = []
        
    def insert_item(self, item:list) -> None:
        self.inst_mem.append(item)