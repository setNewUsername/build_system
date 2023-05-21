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