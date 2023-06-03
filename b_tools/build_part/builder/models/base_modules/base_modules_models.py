from flashtext.keyword import KeywordProcessor

class BaseModuleModel:
    keywordProcessor:KeywordProcessor = None

    jsonModuleOptionsData:dict = None

    moduleFileName:str = None
    moduleFileLines:list[str] = None

    moduleId:str = None
    moduleClearCssDataMap:dict[str, any] = None
    moduleDefParamsMap:dict[str, str] = None
    moduleCssToDartOptionsMap:dict[str, str] = None

    def __init__(self, moduleId:str, moduleFileName:str, jsonOptionsData:dict) -> None:
        self.jsonModuleOptionsData = jsonOptionsData
        self.moduleFileName = moduleFileName+'.module'
        self.moduleId = moduleId
        self.keywordProcessor = KeywordProcessor()
        self.keywordProcessor.add_keyword('<module_id>', self.moduleId)

        #default clear data map
        self.moduleClearCssDataMap = {
            'backgroundColor': self.createDartHexColorFromCssColor,
            'height': self.clearAutoHeight,
            'width': self.clearAutoWidth,
            'fontSize': self.clearCssPx
        }

        self.addCssClearDataMap()
        self.loadModuleFile()
        self.addDefParams()
        self.addCssToDartOptionsMap()
        self.replaceDefParamsWithJsonParams()
        self.placeKeyWordsToKW()

    def placeKeyWordsToKW(self):
        for key in self.moduleDefParamsMap.keys():
            self.keywordProcessor.add_keyword(key, self.moduleDefParamsMap[key])

    def loadModuleFile(self):
        file = open(f'./modules_modules/{self.moduleFileName}')
        self.moduleFileLines = file.readlines()
        file.close()

    def replaceDefParamsWithJsonParams(self):
        for cssToDartMapKey in self.moduleCssToDartOptionsMap.keys():
            if cssToDartMapKey in self.jsonModuleOptionsData.keys():
                dartKeyVal = self.moduleCssToDartOptionsMap[cssToDartMapKey]
                clearData = ''
                if cssToDartMapKey in self.moduleClearCssDataMap.keys():
                    clearData = self.moduleClearCssDataMap[cssToDartMapKey](self.jsonModuleOptionsData[cssToDartMapKey])
                else:
                    clearData = self.jsonModuleOptionsData[cssToDartMapKey]
                self.moduleDefParamsMap[dartKeyVal] = clearData

    def replaceDataWithJsonData(self) -> list:
        for lineIndex in range(len(self.moduleFileLines)):
            self.moduleFileLines[lineIndex] = self.keywordProcessor.replace_keywords(self.moduleFileLines[lineIndex])
        return self.moduleFileLines

    def createDartHexColorFromCssColor(self, cssColor:str):
        return '0xff'+cssColor.removeprefix('#')

    def clearAutoWidth(self, CssWidth:str):
        if CssWidth == 'auto':
            return 'MediaQuery.of(context).size.width'
        else:
            return self.clearCssPx(CssWidth)

    def clearAutoHeight(self, CssHeight:str):
        if CssHeight == 'auto':
            return 'MediaQuery.of(context).size.height'
        else:
            return self.clearCssPx(CssHeight)

    def clearCssPx(self, CssLength:str):
        return CssLength.removesuffix('px')

    def createDataFromJson(self, jsonData):
        print('createDataFromJson method is not overrided')

    def addCssClearDataMap(self):
        print('addCssClearDataMap method is not overrided')

    def addDefParams(self):
        print('addDefParams method is not overrided')

    def addCssToDartOptionsMap(self):
        print('addCssToDartOptionsMap method is not overrided')

    def writeDataToDartFile(self, path):
        #print(self.moduleFileLines)
        file = open(f'{path}/{self.moduleId}.dart', 'w')
        for lineIndex in range(len(self.moduleFileLines)):
            self.moduleFileLines[lineIndex] = self.keywordProcessor.replace_keywords(self.moduleFileLines[lineIndex])
        file.writelines(self.moduleFileLines)
        file.close()

class BaseModuleWithChildren(BaseModuleModel):
    moduleChildren:list[BaseModuleModel] = None
    moduleChildrenFileLines:list = None

    def __init__(self, moduleId: str, moduleFileName: str, jsonData:dict) -> None:
        super().__init__(moduleId, moduleFileName, jsonData)
        self.moduleChildren = []
        self.moduleChildrenFileLines = []

    def addChild(self, newChild) -> None:
        self.moduleChildren.append(newChild)

    def appendChildrenLines(self, childrenDelimeter:str) -> None:
        for child in self.moduleChildren:
            for line in child.replaceDataWithJsonData():
                self.moduleChildrenFileLines.append(line)
            self.moduleChildrenFileLines.append(childrenDelimeter)

    def appendChildLines(self, childId:int, childrenDelimeter:str) -> None:
        for line in self.moduleChildren[childId].replaceDataWithJsonData():
            self.moduleChildrenFileLines.append(line)
        self.moduleChildrenFileLines.append(childrenDelimeter)

    #inserts children file lines to self file lines
    def processChildrenLines(self):
        insertIndex = -1
        for i, line in enumerate(self.moduleFileLines):
            if line.find('<children_lines>') != -1:
                insertIndex = i
                self.moduleFileLines[insertIndex] = ' '
                break
        if insertIndex != -1:
            for lineIndex in range(len(self.moduleChildrenFileLines)-1, -1, -1):
                self.moduleFileLines.insert(insertIndex, self.moduleChildrenFileLines[lineIndex])