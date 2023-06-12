import sys, os
sys.path.append('..\\..\\..\\')

from b_tools.controll_part.common.command_reciever import command_reciever as CR

class StartBuildPurpose(CR.BasePurposeHandler):
    addProjectToQueueFunc = None

    def __init__(self, reqFields: list, addPToQFunc) -> None:
        super().__init__('start_build', reqFields, True)
        self.addProjectToQueueFunc = addPToQFunc

    def purposeProcess(self, jsonData):
        return self.addProjectToQueueFunc(jsonData['purpose_data']['project_id'])