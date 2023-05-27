import sys, os
sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}\..\\')

from common.command_reciever import command_reciever as CR

class StartBuildPurpose(CR.BasePurposeHandler):
    addProjectToQueueFunc = None

    def __init__(self, reqFields: list, addPToQFunc) -> None:
        super().__init__('start_build', reqFields, True)
        self.addProjectToQueueFunc = addPToQFunc

    def purposeProcess(self, jsonData):
        return self.addProjectToQueueFunc(jsonData['purpose_data']['project_id'])
    
class RemoveProjectFromQueuePurpose(CR.BasePurposeHandler):
    removeProjectFromQueueFunc = None

    def __init__(self, reqFields: list, remPFromQFunc) -> None:
        super().__init__('remove_project_from_queue', reqFields, True)
        self.removeProjectFromQueueFunc = remPFromQFunc

    def purposeProcess(self, jsonData):
        return self.removeProjectFromQueueFunc(jsonData['purpose_data']['project_id'])
    
class RegisterMachinePurpose(CR.BasePurposeHandler):
    registerMachineFunction = None

    def __init__(self, reqFields: list, regMachineFunc) -> None:
        super().__init__('register_machine', reqFields, True)
        self.registerMachineFunction = regMachineFunc

    def purposeProcess(self, jsonData):
        return self.registerMachineFunction(jsonData['purpose_data'])
    
class UnRegisterMachinePurpose(CR.BasePurposeHandler):
    unRegisterMachineFunction = None

    def __init__(self, reqFields: list, unregMachineFunc) -> None:
        super().__init__('unregister_machine', reqFields, True)
        self.unRegisterMachineFunction = unregMachineFunc

    def purposeProcess(self, jsonData):
        return self.unRegisterMachineFunction(jsonData['purpose_data']['machine_id'])
    
class BuildFinishedPurpose(CR.BasePurposeHandler):
    buildFinishedFunc = None

    def __init__(self, reqFields: list, buildFinFunc) -> None:
        super().__init__('build_finished', reqFields, True)
        self.buildFinishedFunc = buildFinFunc

    def purposeProcess(self, jsonData):
        return self.buildFinishedFunc(jsonData['purpose_data']['machine_id'])