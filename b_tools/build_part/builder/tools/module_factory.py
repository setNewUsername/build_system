from .tools import *
from builder.models.base_modules.base_modules_models import *
from builder.modules.footer_modules import *
from builder.modules.footer_modules import *
from builder.modules.button_modules import *
from builder.modules.header_modules import *
from builder.modules.body_dummie import *
from builder.modules.scroll_modules import *
from builder.modules.wrapper_modules import *

class ModuleFactory:
    creationModuleMap:dict[str, any] = None
    projectUid:str = None

    def __init__(self, projUid) -> None:
        self.fillCreateMap()
        self.projectUid = projUid

    def fillCreateMap(self):
        self.creationModuleMap = {
            'Wrapper': self.createWrapper,
            'Button': self.createButton,
            'Text': self.createText
        }

    def createButton(self, data) -> BaseModuleModel:
        return ButtonModule(data['id'], data['options'], self.projectUid)

    def createWrapper(self, data:dict) -> BaseModuleWithChildren:
        if 'children' in data.keys() and len(data['children']) > 0:
            if data['scrollable'] == 'true':
                bod = ScrollableWrapper(data['id'], data['options'], self.projectUid)
                bod.processChildren(self.getModuleByName(data['children'][0]['namePrivate'], requiredData={
                    'id': transformId(data['children'][0]['id']),
                    'options': data['children'][0]['options']
                }))
                return bod
            if data['scrollable'] == 'false':
                bod = NotScrollableWrapper(data['id'], data['options'], self.projectUid)
                for child in data['children']:
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