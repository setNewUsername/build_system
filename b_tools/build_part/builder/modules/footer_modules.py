from models.base_modules.base_modules_models import *

class FooterModule(BaseModuleWithChildren):

    def __init__(self, moduleId: str, jsonData) -> None:
        super().__init__(moduleId, 'footer', jsonData)

    def addDefParams(self):
        self.moduleDefParamsMap = {
            '<footer_height>' : '60',
            '<footer_padding>': 'left: 0.0, top: 0.0, right: 0.0, bottom: 0.0',
            '<footer_margin>': 'left: 0.0, top: 0.0, right: 0.0, bottom: 0.0',
            '<footer_background_color>': '0xffffffff',
            '<children_spacing>': 'MainAxisAlignment.spaceEvenly'
        }

    def addCssToDartOptionsMap(self):
        self.moduleCssToDartOptionsMap = {
            'backgroundColor' : '<footer_background_color>',
            'height': '<footer_height>'
        }

    def addCssClearDataMap(self):
        pass