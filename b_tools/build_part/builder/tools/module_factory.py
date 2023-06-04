from .tools import *
from  b_tools.build_part.builder.models.base_modules.base_modules_models import *
from  b_tools.build_part.builder.modules.footer_modules import *
from  b_tools.build_part.builder.modules.footer_modules import *
from  b_tools.build_part.builder.modules.button_modules import *
from  b_tools.build_part.builder.modules.header_modules import *
from  b_tools.build_part.builder.modules.body_dummie import *
from  b_tools.build_part.builder.modules.scroll_modules import *
from  b_tools.build_part.builder.modules.wrapper_modules import *

class ModuleFactory:
    creationModuleMap:dict[str, any] = None
    projectUid:str = None

    def __init__(self, projUid) -> None:
        self.fillCreateMap()
        self.projectUid = projUid

    def fillCreateMap(self):
        self.creationModuleMap = {
            'Wrapper': self.createRootWrapper,
            'Button': self.createButton,
            'Text': self.createText,
            'EWrapper': self.createEmbeddedWrapper
        }

    def createButton(self, data) -> BaseModuleModel:
        return ButtonModule(data['id'], data['options'], self.projectUid)

    def processWrapperChildrenElements(self, wrapperChildrenData):
        pass

    def createEmbeddedWrapper(self, data):
        if data['scrollable'] == 'true':
            bod = EmbeddedScrollableWrapper(data['id'], data['options'], self.projectUid)
            if data['children'][0]['namePrivate'] == 'Wrapper':
                    bod.processChildren(self.getModuleByName('EWrapper', requiredData={
                        'id': transformId(data['children'][0]['id']),
                        'options': data['children'][0]['options'],
                        'children': data['children'][0]['modules'],
                        'scrollable': data['children'][0]['scrollable']
                    }))
            else:
                bod.processChildren(self.getModuleByName(data['children'][0]['namePrivate'], requiredData={
                    'id': transformId(data['children'][0]['id']),
                    'options': data['children'][0]['options']
                }))
            bod.processChildrenLines()
            return bod
        if data['scrollable'] == 'false':
            bod = EmbeddedNotScrollableWrapper(data['id'], data['options'], self.projectUid)
            for child in data['children']:
                if child['namePrivate'] == 'Wrapper':
                    bod.addChild(self.getModuleByName('EWrapper', requiredData={
                        'id': transformId(child['id']),
                        'options': child['options'],
                        'children': child['modules'],
                        'scrollable': child['scrollable']
                    }))
                else:
                    bod.addChild(self.getModuleByName(child['namePrivate'], requiredData={
                        'id': transformId(child['id']),
                        'options': child['options']
                    }))
            
            bod.processChildrenColumns()
            bod.processChildrenLines()
            return bod

    def createRootWrapper(self, data:dict) -> BaseModuleWithChildren:
        if 'children' in data.keys() and len(data['children']) > 0:
            if data['scrollable'] == 'true':
                bod = ScrollableWrapper(data['id'], data['options'], self.projectUid)
                if data['children'][0]['namePrivate'] == 'Wrapper':
                    bod.processChildren(self.getModuleByName('EWrapper', requiredData={
                        'id': transformId(data['children'][0]['id']),
                        'options': data['children'][0]['options'],
                        'children': data['children'][0]['modules'],
                        'scrollable': data['children'][0]['scrollable']
                    }))
                else:
                    bod.processChildren(self.getModuleByName(data['children'][0]['namePrivate'], requiredData={
                        'id': transformId(data['children'][0]['id']),
                        'options': data['children'][0]['options']
                    }))
                return bod
            if data['scrollable'] == 'false':
                bod = NotScrollableWrapper(data['id'], data['options'], self.projectUid)
                for child in data['children']:
                    if child['namePrivate'] == 'Wrapper':
                        bod.addChild(self.getModuleByName('EWrapper', requiredData={
                            'id': transformId(child['id']),
                            'options': child['options'],
                            'children': child['modules'],
                            'scrollable': child['scrollable']
                        }))
                    else:
                        bod.addChild(self.getModuleByName(child['namePrivate'], requiredData={
                            'id': transformId(child['id']),
                            'options': child['options']
                        }))
                bod.processChildrenColumns()
                return bod
        else:
            return BodyDummie(data['id'], data['options'], self.projectUid)

    def createText(self, data) -> BaseModuleModel:
        return TextModule(data['id'], data['options'], self.projectUid)

    def getModuleByName(self, moduleName, requiredData={}) -> BaseModuleModel:
        return self.creationModuleMap[moduleName](requiredData)