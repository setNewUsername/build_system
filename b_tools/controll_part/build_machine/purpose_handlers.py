import sys, os, threading
sys.path.append('..\\..\\..\\')

from b_tools.controll_part.common.command_reciever import command_reciever as CR

class StartBuildPurpose(CR.BasePurposeHandler):
    startBuildFunc = None

    def __init__(self, reqFields: list, startPFunc) -> None:
        super().__init__('start_build', reqFields, True)
        self.startBuildFunc = startPFunc

    def purposeProcess(self, jsonData) -> tuple:
        return self.startBuildFunc()
    
class setCoordInfoPurpose(CR.BasePurposeHandler):
    setCoordInfoFunc = None

    def __init__(self, reqFields: list, setInfoFunc) -> None:
        super().__init__('set_coord_info', reqFields, True)
        self.setCoordInfoFunc = setInfoFunc

    def purposeProcess(self, jsonData) -> tuple:
        return self.setCoordInfoFunc(jsonData)
    
class regMachinePurposer(CR.BasePurposeHandler):
    regMachineFunc = None

    def __init__(self, reqFields: list, regFunc) -> None:
        super().__init__('reg_machine', reqFields, True)
        self.regMachineFunc = regFunc

    def purposeProcess(self, jsonData) -> tuple:
        return self.regMachineFunc(jsonData)
    
class unregMachinePurpose(CR.BasePurposeHandler):
    unregMachineFunc = None

    def __init__(self, reqFields: list, unregFunc) -> None:
        super().__init__('unreg_machine', reqFields, True)
        self.unregMachineFunc = unregFunc

    def purposeProcess(self, jsonData) -> tuple:
        return self.unregMachineFunc(jsonData)