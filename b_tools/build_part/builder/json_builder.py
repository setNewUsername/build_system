import json, os
from flashtext.keyword import KeywordProcessor

from models.screen_model import *
from models.base_modules.base_modules_models import *

from modules.footer_modules import *
from modules.button_modules import *
from modules.header_modules import *
from modules.body_dummie import *
from modules.scroll_modules import *
from modules.wrapper_modules import *

from tools.tools import *
from tools.module_factory import *

class Builder:
    projectFilesFolderPath:str = './test'

    commonHeader:BaseModuleWithChildren = None
    commonFooter:BaseModuleWithChildren = None

    jsonProjectData:dict = None
    screensAmount:int = None

    moduleFactory: ModuleFactory = ModuleFactory()

    def __init__(self, jsonData) -> None:
        self.jsonProjectData = jsonData

    #common objects
    def createCommonHeader(self):
        self.commonHeader = HeaderModule(transformId(self.jsonProjectData['header']['id']), self.jsonProjectData['header']['options'])

        for child in self.jsonProjectData['header']['modules']:
            self.commonHeader.addChild(self.moduleFactory.getModuleByName(child['namePrivate'], requiredData={
                'id': transformId(child['id']),
                'options': child['options']
            }))

        self.commonHeader.appendChildrenLines(',')
        self.commonHeader.processChildrenLines()
        self.commonHeader.writeDataToDartFile('./test/commons')

    def createCommonFooter(self):
        self.commonFooter = FooterModule(transformId(self.jsonProjectData['footer']['id']), self.jsonProjectData['footer']['options'])

        for child in self.jsonProjectData['footer']['modules']:
            self.commonFooter.addChild(self.moduleFactory.getModuleByName(child['namePrivate'], requiredData={
                'id': transformId(child['id']),
                'options': child['options']
            }))

        self.commonFooter.appendChildrenLines(',')
        self.commonFooter.processChildrenLines()
        self.commonFooter.writeDataToDartFile('./test/commons')
    #common objects

    #objects by screen
    def createScreenHeader(self, headerData, screenId):
        if(headerData != {}):
            head = HeaderModule(transformId(headerData['id']), headerData['options'])

            for child in headerData['modules']:
                head.addChild(
                    self.moduleFactory.getModuleByName(child['namePrivate'], requiredData={
                        'id': transformId(child['id']),
                        'options': child['options']
                    })
                )

            head.appendChildrenLines(',')
            head.processChildrenLines()
            head.writeDataToDartFile(f'./test/modules_by_screens/{screenId}')

    def createScreenFooter(self, footerData, screenId):
        foot = FooterModule(transformId(footerData['id']), footerData['options'])

        for child in footerData['modules']:
            foot.addChild(
                self.moduleFactory.getModuleByName(child['namePrivate'], requiredData={
                    'id': transformId(child['id']),
                    'options': child['options']
                })
            )

        foot.appendChildrenLines(',')
        foot.processChildrenLines()
        foot.writeDataToDartFile(f'./test/modules_by_screens/{screenId}')

    def checkScrollable(self, bodyData:dict):
        if 'scrollable' in bodyData.keys():
            return bodyData['scrollable']
        else:
            return 'false'

    def createScreenBody(self, bodyData, screenId):
        body = self.moduleFactory.getModuleByName(bodyData['namePrivate'], requiredData={
            'scrollable': self.checkScrollable(bodyData),
            'id': transformId(bodyData['id']),
            'children': bodyData['modules'],
            'options': bodyData['options']
        })
        body.processChildrenLines()
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
                transformId(screen['id']),
                transformId(headerId),
                transformId(screen['modules'][0]['id']),
                transformId(footerId),
                'screen')
            scr.writeLinesToDart()

    def createScreensModules(self):
        for screen in self.jsonProjectData['screens']:
            os.mkdir(f"./test/modules_by_screens/{transformId(screen['id'])}")
            self.createScreenFooter(self.jsonProjectData['footer'], transformId(screen['id']))
            self.createScreenHeader(screen['uncommonHeader'], transformId(screen['id']))
            self.createScreenBody(screen['modules'][0], transformId(screen['id']))

    def createScreenHandler(self):
        file = open('./controls_templates/screen_handler.templ', 'r')
        lines = file.readlines()
        file.close()
        importLines = []
        getLines = []
        output = open('./test/controls/screen_handler.dart', 'w')

        for screen in self.jsonProjectData['screens']:
            importLines.append(f"import 'package:test/screens/{transformId(screen['id'])}.dart';\n")
            getLines.append("Widget get"+transformId(screen['id'])+"Screen(){\n")
            getLines.append(f"return const {transformId(screen['id'])}();\n")
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
        kw.add_keyword('<start_screen_id>',  '"'+transformId(self.jsonProjectData['screens'][0]['id'])+'"')
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
            addScreensLines.append(f"ScreenRootInheritedWidget.of(context).scrnNav.addScreen({transformId(screen['id'], bracelets=True)}, scrHand.get{transformId(screen['id'])}Screen);\n")

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

file = open('./project2.json', 'r')
data = json.load(file)
file.close()

bui = Builder(data)
bui.createCommonHeader()
bui.createCommonFooter()
bui.createScreens()
bui.createScreensModules()
bui.createScreenHandler()
bui.createScreenNavigator()
bui.createMainFile()

# bod = ScrollableWrapper('test_scroll', data['screens'][0]['modules'][0])
# bod.processChildren(ButtonModule('fefwew', data['footer']['modules'][0]))
# bod.processChildrenLines()
# bod.writeDataToDartFile('./test/')

# bod = NotScrollableWrapper('efwe', data['screens'][1]['modules'][0]['options'])
# bod.addChild(ButtonModule('fefwew', data['screens'][1]['modules'][0]['modules'][0]))
# bod.addChild(ButtonModule('fefwew', data['screens'][1]['modules'][0]['modules'][1]))
# bod.addChild(ButtonModule('fefwew', data['screens'][1]['modules'][0]['modules'][2]))
# bod.addChild(ButtonModule('fefwew', data['screens'][1]['modules'][0]['modules'][3]))
# bod.processChildrenColumns()
# bod.processChildrenLines()
# bod.writeDataToDartFile('./test')