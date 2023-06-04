from builder.models.base_modules.base_modules_models import *

class BodyDummie(BaseModuleWithChildren):
    def __init__(self, moduleId: str, jsonOptions, projectUid) -> None:
        super().__init__(moduleId, 'body_dummie', jsonOptions, projectUid)

    def addDefParams(self):
        self.moduleDefParamsMap = {}

    def addCssToDartOptionsMap(self):
        self.moduleCssToDartOptionsMap = {}

    def addCssClearDataMap(self):
        pass