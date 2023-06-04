from builder.models.base_modules.base_modules_models import *

class ScrollableWrapper(BaseModuleWithChildren):
    childrenAmount:str = None

    def __init__(self, moduleId: str, jsonData, projectUid) -> None:
        super().__init__(moduleId, 'scrollable_wrapper', jsonData, projectUid)

    def addDefParams(self):
        self.moduleDefParamsMap = {
            '<children_amount>': ' ',
            '<columns_amount>': '2',
            '<grid_columns_gap>': '5',
            '<grid_row_gap>': '5'
        }

    def addCssToDartOptionsMap(self):
        self.moduleCssToDartOptionsMap = {
        }

    def processChildren(self, children:BaseModuleModel) -> None:
        self.moduleChildrenFileLines = children.replaceDataWithJsonData()
        self.moduleChildrenFileLines.append(';')

    def addCssClearDataMap(self):
        pass

    def getChildrenAmount(self, jsonData) -> int:
        return 20

    def appendChildrenLines():
        pass

    def addChild():
        pass
