from base_modules_models import *
from text_modules import *

class HeaderModule(BaseModuleWithChildren):
    def __init__(self, moduleId: str, jsonOptions) -> None:
        super().__init__(moduleId, 'header', jsonOptions)

    def addDefParams(self):
        self.moduleDefParamsMap = {
            '<backgroud_header_color>': '0xffffffff',
            '<header_text_color>': '0xff000000',
            '<header_height>': '60.0',
        }

    def addCssToDartOptionsMap(self):
        self.moduleCssToDartOptionsMap = {
            'height' : '<header_height>',
            'backgroundColor' : '<backgroud_header_color>',
        }