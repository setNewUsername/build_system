from b_tools.build_part.builder.models.base_modules.base_modules_models import *

class TextModule(BaseModuleModel):
    def __init__(self, moduleId: str, jsonData, projectUid) -> None:
        super().__init__(moduleId, 'text', jsonData, projectUid)

    def addDefParams(self):
        self.moduleDefParamsMap = {
            '<text_margin>':'left: 0.0, top: 0.0, right: 0.0, bottom: 0.0',
            '<text_padding>': 'left: 0.0, top: 0.0, right: 0.0, bottom: 0.0',
            '<text_alignment>': 'Alignment.center',
            '<text>': '"Sample text"',
            '<text_font_size>': '16',
            '<text_color>': '0xffffffff'
        }

    def addCssToDartOptionsMap(self):
        self.moduleCssToDartOptionsMap = {
            'name' : '<text>',
            'fontSize': '<text_font_size>',
            'color': '<text_color>',
        }

    def clearCssName(self, nameToClear):
        return '"'+nameToClear+'"'

    def addCssClearDataMap(self):
        self.moduleClearCssDataMap['name'] = self.clearCssName
        self.moduleClearCssDataMap['color'] = self.createDartHexColorFromCssColor