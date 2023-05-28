from .base_modules_models import *

class NotScrollableWrapper(BaseModuleWithChildren):
    columnsAmount:int = None

    def __init__(self, moduleId: str, columnsAmount) -> None:
        super().__init__(moduleId, 'notscrollable_wrapper')
        self.columnsAmount = columnsAmount

    def addDefParams(self):
        self.moduleDefParamsMap = {}

    def processChildrenColumns(self):
        modulesPerColumn = int(len(self.moduleChildren) / self.columnsAmount)
        moduleMinIndex = 0
        moduleMaxIndex = modulesPerColumn

        for _ in range(self.columnsAmount):
            self.moduleChildrenFileLines.append('Column(\n')
            self.moduleChildrenFileLines.append('children: [\n')

            for childIndex in range(moduleMinIndex, moduleMaxIndex):
                self.appendChildLines(childIndex, ',')

            self.moduleChildrenFileLines.append('],\n')
            self.moduleChildrenFileLines.append('),\n')

            moduleMinIndex+=modulesPerColumn
            moduleMaxIndex+=modulesPerColumn
            print(moduleMinIndex)
            print(moduleMaxIndex)