from tools import *
from models.base_modules.base_modules_models import *
from modules.footer_modules import *
from modules.footer_modules import *
from modules.button_modules import *
from modules.header_modules import *
from modules.body_dummie import *
from modules.scroll_modules import *
from modules.wrapper_modules import *

class ModuleFactory:
    creationModuleMap:dict[str, any] = None

    def __init__(self) -> None:
        self.fillCreateMap()

    def fillCreateMap(self):
        self.creationModuleMap = {
            'Wrapper': self.createWrapper,
            'Button': self.createButton,
            'Text': self.createText
        }

    def createButton(self, data) -> BaseModuleModel:
        return ButtonModule(data['id'], data['options'])

    def createWrapper(self, data:dict) -> BaseModuleWithChildren:
        if 'children' in data.keys() and len(data['children']) > 0:
            if data['scrollable'] == 'true':
                bod = ScrollableWrapper(data['id'], data['options'])
                bod.processChildren(self.getModuleByName(data['children'][0]['namePrivate'], requiredData={
                    'id': transformId(data['children'][0]['id']),
                    'options': data['children'][0]['options']
                }))
                return bod
            if data['scrollable'] == 'false':
                bod = NotScrollableWrapper(data['id'], data['options'])
                for child in data['children']:
                    bod.addChild(self.getModuleByName(child['namePrivate'], requiredData={
                    'id': transformId(child['id']),
                    'options': child['options']
                }))
                bod.processChildrenColumns()
                return bod
        else:
            return BodyDummie(data['id'], data['options'])

    def createText(self, data) -> BaseModuleModel:
        return TextModule(data['id'], data['options'])

    def getModuleByName(self, moduleName, requiredData={}) -> BaseModuleModel:
        return self.creationModuleMap[moduleName](requiredData)