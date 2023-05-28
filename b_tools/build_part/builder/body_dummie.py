from base_modules_models import *

class BodyDummie(BaseModuleModel):
    def __init__(self, moduleId: str, jsonOptions) -> None:
        super().__init__(moduleId, 'body_dummie', jsonOptions)

    def addDefParams(self):
        self.moduleDefParamsMap = {}

    def addCssToDartOptionsMap(self):
        self.moduleCssToDartOptionsMap = {}

    def addCssClearDataMap(self):
        pass