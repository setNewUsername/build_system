from .base_modules_models import *

class ScrollableWrapper(BaseModuleWithChildren):
    childrenAmount:str = None

    def __init__(self, moduleId: str) -> None:
        super().__init__(moduleId, 'scrollable_wrapper')

    def addDefParams(self):
        self.moduleDefParamsMap = {
            ' ': ['<children_amount>'],
            '2': ['<columns_amount>'],
            '5': ['<grid_columns_gap>', '<grid_row_gap>'],
        }

    def processChildren(self, children:BaseModuleModel) -> None:
        self.moduleChildrenFileLines = children.replaceDataWithJsonData()
        self.moduleChildrenFileLines.append(';')

    def getChildrenAmount(self, jsonData) -> int:
        return 20

    def appendChildrenLines():
        pass

    def addChild():
        pass
