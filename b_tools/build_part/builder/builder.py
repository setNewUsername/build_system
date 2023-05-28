import json, os
from flashtext.keyword import KeywordProcessor

from screen_model import *
from base_modules_models import *
from footer_modules import *
from button_modules import *
from header_modules import *
from body_dummie import *

class Builder:
    projectFilesFolderPath:str = './test'

    commonHeader:BaseModuleWithChildren = None
    commonFooter:BaseModuleWithChildren = None

    jsonProjectData:dict = None
    screensAmount:int = None

    def __init__(self, jsonData) -> None:
        self.jsonProjectData = jsonData

    def prepFolders(self) -> None:
        os.mkdir(f'{self.projectFilesFolderPath}/commons')
        os.mkdir(f'{self.projectFilesFolderPath}/controls')
        os.mkdir(f'{self.projectFilesFolderPath}/modules_by_screens')
        os.mkdir(f'{self.projectFilesFolderPath}/screens')

    def transformId(self, idToTransform:str, bracelets:bool = False) -> str:
        res = ''.join(idToTransform.split('-'))
        try:
            int(res[0])
        except:
            pass
        else:
            print(res[0])
            res = res.replace(res[0], 'a', 1)
        if not bracelets:
            return res
        else:
            return '"'+res+'"'

    #common objects
    def createCommonHeader(self):
        pass

    def createCommonFooter(self):
        self.commonFooter = FooterModule(self.transformId(self.jsonProjectData['footer']['id']), self.jsonProjectData['footer']['options'])

        for child in self.jsonProjectData['footer']['modules']:
            self.commonFooter.addChild(ButtonModule(self.transformId(child['id']), child['options']))

        self.commonFooter.appendChildrenLines(',')
        self.commonFooter.processChildrenLines()
        self.commonFooter.writeDataToDartFile('./test/commons')
    #common objects

    #objects by screen
    def createScreenHeader(self, headerData, screenId):
        head = HeaderModule(self.transformId(headerData['id']), headerData['options'])

        for child in headerData['modules']:
            head.addChild(TextModule(self.transformId(child['id']), child['options']))

        head.appendChildrenLines(',')
        head.processChildrenLines()
        head.writeDataToDartFile(f'./test/modules_by_screens/{screenId}')

    def createScreenFooter(self, footerData, screenId):
        foot = FooterModule(self.transformId(footerData['id']), footerData['options'])

        for child in footerData['modules']:
            foot.addChild(ButtonModule(self.transformId(child['id']), child['options']))

        foot.appendChildrenLines(',')
        foot.processChildrenLines()
        foot.writeDataToDartFile(f'./test/modules_by_screens/{screenId}')

    def createScreenBody(self, bodyData, screenId):
        body = BodyDummie(self.transformId(bodyData['id']), bodyData['options'])

        body.writeDataToDartFile(f'./test/modules_by_screens/{screenId}')
    #objects by screen

    def createScreens(self):
        for screen in self.jsonProjectData['screens']:
            headerId = None
            footerId = None
            if screen['uncommonHeader'] != {}:
                headerId = screen['uncommonHeader']['id']
            else:
                headerId = self.commonHeader.moduleId
            if screen['uncommonFooter'] != {}:
                footerId = screen['uncommonFooter']['id']
            else:
                footerId = self.commonFooter.moduleId
            scr = ScreenModel(
                self.transformId(screen['id']),
                self.transformId(headerId),
                self.transformId(screen['modules'][0]['id']),
                self.transformId(footerId),
                'screen')
            scr.writeLinesToDart()

    def createScreensModules(self):
        for screen in self.jsonProjectData['screens']:
            os.mkdir(f"./test/modules_by_screens/{self.transformId(screen['id'])}")
            self.createScreenFooter(self.jsonProjectData['footer'], self.transformId(screen['id']))
            self.createScreenHeader(screen['uncommonHeader'], self.transformId(screen['id']))
            self.createScreenBody(screen['modules'][0], self.transformId(screen['id']))

    def createScreenHandler(self):
        file = open('./controls_templates/screen_handler.templ', 'r')
        lines = file.readlines()
        file.close()
        importLines = []
        getLines = []
        output = open('./test/controls/screen_handler.dart', 'w')

        for screen in self.jsonProjectData['screens']:
            importLines.append(f"import 'package:test/screens/{self.transformId(screen['id'])}.dart';\n")
            getLines.append("Widget get"+self.transformId(screen['id'])+"Screen(){\n")
            getLines.append(f"return const {self.transformId(screen['id'])}();\n")
            getLines.append('}\n')

        #insert import lines
        insertIndex = -1
        for i, line in enumerate(lines):
            if line.find('<screens_imports>') != -1:
                insertIndex = i
                lines[insertIndex] = ' '
                break
        if insertIndex != -1:
            for lineIndex in range(len(importLines)-1, -1, -1):
                lines.insert(insertIndex, importLines[lineIndex])

        #insert get lines
        insertIndex = -1
        for i, line in enumerate(lines):
            if line.find('<screens_get_functions>') != -1:
                insertIndex = i
                lines[insertIndex] = ' '
                break
        if insertIndex != -1:
            for lineIndex in range(len(getLines)-1, -1, -1):
                lines.insert(insertIndex, getLines[lineIndex])

        output.writelines(lines)

    def createScreenNavigator(self):
        file = open('./controls_templates/screen_navigator.templ', 'r')
        lines = file.readlines()
        file.close()
        output = open('./test/controls/screen_navigator.dart', 'w')
        kw = KeywordProcessor()
        kw.add_keyword('<start_screen_id>',  '"'+self.transformId(self.jsonProjectData['screens'][0]['id'])+'"')
        for lineIndex in range(len(lines)):
            lines[lineIndex] = kw.replace_keywords(lines[lineIndex])
        output.writelines(lines)

    def createMainFile(self):
        file = open('./common_templates/main.templ', 'r')
        lines = file.readlines()
        file.close()
        output = open('./main.dart', 'w')

        addScreensLines = []

        for screen in self.jsonProjectData['screens']:
            addScreensLines.append(f"ScreenRootInheritedWidget.of(context).scrnNav.addScreen({self.transformId(screen['id'], bracelets=True)}, scrHand.get{self.transformId(screen['id'])}Screen);\n")

        insertIndex = -1
        for i, line in enumerate(lines):
            if line.find('<add_screens>') != -1:
                insertIndex = i
                lines[insertIndex] = ' '
                break
        if insertIndex != -1:
            for lineIndex in range(len(addScreensLines)-1, -1, -1):
                lines.insert(insertIndex, addScreensLines[lineIndex])

        output.writelines(lines)

file = open('./jsonProject.json', 'r')
data = json.load(file)
file.close()

bui = Builder(data)
bui.createCommonFooter()
bui.createScreens()
bui.createScreensModules()
bui.createScreenHandler()
bui.createScreenNavigator()
bui.createMainFile()