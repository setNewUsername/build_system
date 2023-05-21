class BuildMachine:
    machineAdress = None
    machinePort = None
    machineFree:bool = True

    def __init__(self, adress, port) -> None:
        self.machineAdress = adress
        self.machinePort = port