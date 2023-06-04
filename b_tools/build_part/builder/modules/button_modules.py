from builder.models.base_modules.base_modules_models import *

class ButtonModule(BaseModuleModel):
    def __init__(self, moduleId: str, jsonOptions, projectUid) -> None:
        super().__init__(moduleId, 'button_module', jsonOptions, projectUid)

    def addDefParams(self):
        self.moduleDefParamsMap = {
            '<button_margin>': 'left: 0.0, top: 0.0, right: 0.0, bottom: 0.0',
            '<press_function>': ' ',
            '<background_color>' : '0xffffffff',
            '<border_color>': '0xff000000',
            '<button_text_color>': '0xff000000',
            '<button_height>': '50',
            '<button_width>': '50',
            '<button_text_aligment>': 'Alignment.center',
            '<button_text>': '"button"',
            '<font_size>': '16'
        }

    def addCssToDartOptionsMap(self):
        self.moduleCssToDartOptionsMap = {
            'backgroundColor' : '<background_color>',
            'height': '<button_height>',
            'width': '<button_width>',
            'name': '<button_text>',
            'fontSize': '<font_size>',
            'color': '<button_text_color>',
            'actions' : '<press_function>'
        }

    def clearCssName(self, nameToClear):
        return '"'+nameToClear+'"'

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

    def clearButtonAction(self, data):
        if data['name'] == '':
            return ' '
        if data['name'] == 'leed_to_screen':
            return f"leedToScreen(context, {self.transformId(data['options']['screenId'], bracelets=True)});"

    def addCssClearDataMap(self):
        self.moduleClearCssDataMap['name'] = self.clearCssName
        self.moduleClearCssDataMap['color'] = self.createDartHexColorFromCssColor
        self.moduleClearCssDataMap['actions'] = self.clearButtonAction