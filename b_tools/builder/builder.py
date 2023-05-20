import sys, os, argparse
from flashtext.keyword import KeywordProcessor
from commons import *

filePath = os.path.dirname(os.path.abspath(__file__))

class ModuleModel:
    moduleName = ''
    role=''
    keyWord = ''
    childrenModules = []
    options = {}

    def __init__(self, moduleName:str, role:str, keyWord:str, childrenModules:list, options:dict) -> None:
        self.moduleName = moduleName
        self.role = role
        self.keyWord = keyWord
        self.childrenModules = childrenModules
        self.options = options

    def formatModuleFileName(self, defParams:bool) -> str:
        result = ''
        result += self.moduleName[0].lower()
        for i in range(1, len(self.moduleName)):
            if self.moduleName[i].isupper():
                result+='_'
                result+=self.moduleName[i].lower()
            else:
                result+=self.moduleName[i]
        if defParams:
            result += '_defparams'
        return result

    def getImportLine(self, projectName:str) -> str:
        return f'import \'package:{projectName}/modules/{self.formatModuleFileName(defParams=False)}.dart\';'

    def getVarCreateLine(self) -> str:
        return self.moduleName + '()'

class ScreenModel:
    header:ModuleModel = None
    body:ModuleModel = None
    footer:ModuleModel = None

    screenName:str = ''
    parentScreen = None

    def __init__(self, header:ModuleModel, body:ModuleModel, footer:ModuleModel, parentScreen:str, screenName:str) -> None:
        self.header = header
        self.body = body
        self.footer = footer

        self.screenName = screenName
        self.parentScreen = parentScreen

    def formatScreenFileName(self):
        result = ''
        result += self.screenName[0].lower()
        for i in range(1, len(self.screenName)):
            if self.screenName[i].isupper():
                result+='_'
                result+=self.screenName[i].lower()
            else:
                result+=self.screenName[i]
        return result

class Builder:
    projectName = ''

    parser = argparse.ArgumentParser()
    keyword_processor = KeywordProcessor()
    namespace = None

    def __init__(self, projectName:str) -> None:
        self.projectName = projectName
        if __file__ == 'builder.py':
            self.parser.add_argument('--project-name', nargs='?', default='none')
            self.namespace = self.parser.parse_args(sys.argv[1:])

        self.keyword_processor.add_keyword('<proj_name>', self.projectName)
        self.keyword_processor.add_keyword('<proj_title>', '\''+self.projectName+'\'')

    def addMapToKWProcessor(self, map:dict) -> None:
        for key in map.keys():
            self.keyword_processor.add_keyword(key, map[key])

    def removeMapFromKWProcessor(self, map:dict) -> None:
        for key in map.keys():
            self.keyword_processor.remove_keyword(key)

    def readModuleDefParams(self, filePath) -> dict:
        result = {}
        file = open(filePath, 'r')

        for line in file:
            splittedLine = line.split(' = ')
            result[splittedLine[0]] = splittedLine[1].removesuffix('\n')

        file.close()

        return result

    def compareModuleOptions(self, defParams:dict, newParams:dict) -> dict:
        for nPK in newParams.keys():
            if '<'+nPK+'>' in defParams:
                #print('yes')
                defParams['<'+nPK+'>'] = str(newParams[nPK])
            else:
                pass#print('no')
        return defParams

    def createModule(self, module:ModuleModel):
        importLinesBuffer = []
        keyWords = {}
        defParamsMap = {}

        for cModule in module.childrenModules:
            importLinesBuffer.append(cModule.getImportLine(self.projectName))
            keyWords[cModule.keyWord] = cModule.getVarCreateLine()
            self.createModule(cModule)

        self.addMapToKWProcessor(keyWords)

        file = None
        if module.role == 'header':
            file = open(f'{filePath}/../resources/modules_def_params/header_modules/{module.formatModuleFileName(defParams=False)}/{module.formatModuleFileName(defParams=False)}.module', 'r')
            defParamsMap = self.readModuleDefParams(f'{filePath}/../resources/modules_def_params/header_modules/{module.formatModuleFileName(defParams=False)}/{module.formatModuleFileName(defParams=True)}.txt')
        elif module.role == 'body':
            file = open(f'{filePath}/../resources/modules_def_params/body_modules/{module.formatModuleFileName(defParams=False)}/{module.formatModuleFileName(defParams=False)}.module', 'r')
            defParamsMap = self.readModuleDefParams(f'{filePath}/../resources/modules_def_params/body_modules/{module.formatModuleFileName(defParams=False)}/{module.formatModuleFileName(defParams=True)}.txt')
        elif module.role == 'footer':
            file = open(f'{filePath}/../resources/modules_def_params/footer_modules/{module.formatModuleFileName(defParams=False)}/{module.formatModuleFileName(defParams=False)}.module', 'r')
            defParamsMap = self.readModuleDefParams(f'{filePath}/../resources/modules_def_params/footer_modules/{module.formatModuleFileName(defParams=False)}/{module.formatModuleFileName(defParams=True)}.txt')
        elif module.role == 'controlls':
            file = open(f'{filePath}/../resources/modules_def_params/controlls_modules/{module.formatModuleFileName(defParams=False)}/{module.formatModuleFileName(defParams=False)}.module', 'r')
            defParamsMap = self.readModuleDefParams(f'{filePath}/../resources/modules_def_params/controlls_modules/{module.formatModuleFileName(defParams=False)}/{module.formatModuleFileName(defParams=True)}.txt')
        else:
            pass

        #print(defParamsMap)

        comparedMap = self.compareModuleOptions(defParamsMap, module.options)

        #print(comparedMap)

        self.addMapToKWProcessor(comparedMap)

        output = open(f'{filePath}/'+getModulesPath(self.projectName)+f'/{module.formatModuleFileName(defParams=False)}.dart', 'w')

        for line in importLinesBuffer:
            output.writelines(self.keyword_processor.replace_keywords(line))

        for line in file:
            output.writelines(self.keyword_processor.replace_keywords(line))

        self.removeMapFromKWProcessor(comparedMap)
        self.removeMapFromKWProcessor(keyWords)

        file.close()
        output.close()

    def createScreen(self, screen:ScreenModel):
        file = open(f'{filePath}/../resources/screen.templ', 'r')
        output = open(f'{filePath}/'+getScreensPath(self.projectName) + f'/{screen.formatScreenFileName()}.dart', 'w')

        if screen.header != None:
            self.keyword_processor.add_keyword('<header_import>', screen.header.getImportLine(self.projectName))
            self.keyword_processor.add_keyword('<header_var_create>', f'const {screen.header.getVarCreateLine()}.createWidget(context)')
        else:
            self.keyword_processor.add_keyword('<header_import>', '/*<header_import>*/') 
            self.keyword_processor.add_keyword('<header_var_create>', 'null/*<header_var_create>*/')

        if screen.body != None:
            self.keyword_processor.add_keyword('<body_import>', screen.body.getImportLine(self.projectName))
            self.keyword_processor.add_keyword('<body_var_create>', f'const {screen.body.getVarCreateLine()}.createWidget(context)')
        else:
            self.keyword_processor.add_keyword('<body_import>', '/*<body_import>*/')
            self.keyword_processor.add_keyword('<body_var_create>', 'null/*<body_var_create>*/')

        if screen.footer != None:
            self.keyword_processor.add_keyword('<footer_import>', screen.footer.getImportLine(self.projectName))
            self.keyword_processor.add_keyword('<footer_var_create>', f'const {screen.footer.getVarCreateLine()}.createWidget(context)')
        else:
            self.keyword_processor.add_keyword('<footer_import>', '/*<footer_import>*/')
            self.keyword_processor.add_keyword('<footer_var_create>', 'null/*<footer_var_create>*/')

        self.keyword_processor.add_keyword('<screen_class_name>', screen.screenName)

        for line in file:
            output.writelines(self.keyword_processor.replace_keywords(line))

        file.close()
        output.close()

        self.keyword_processor.remove_keyword('<header_import>')
        self.keyword_processor.remove_keyword('<header_var_create>')
        self.keyword_processor.remove_keyword('<body_import>')
        self.keyword_processor.remove_keyword('<body_var_create>')
        self.keyword_processor.remove_keyword('<footer_import>')
        self.keyword_processor.remove_keyword('<footer_var_create>')

    def prepProject(self):
        #create main.dart file
        file = open(f'{filePath}/../resources/main.templ', 'r')
        output = open(f'{filePath}/{projectsPath}{self.projectName}/lib/main.dart', 'w')
        for line in file:
            output.writelines(self.keyword_processor.replace_keywords(line))
        file.close()
        output.close()
        #create main.dart file

        #create empty dirs
        os.mkdir(f'{filePath}/' + getScreensPath(self.projectName))
        os.mkdir(f'{filePath}/' + getModulesPath(self.projectName))
        os.mkdir(f'{filePath}/' + getInterfacesPath(self.projectName))
        os.mkdir(f'{filePath}/' + getInterfacesPath(self.projectName)+'/module_interfaces')
        os.mkdir(f'{filePath}/' + getInterfacesPath(self.projectName)+'/screen_interfaces')
        #create empty dirs

        #place interfaces
        for dir in ['module_interfaces', 'screen_interfaces']:
            for root, dirs, files in os.walk(f"{filePath}/../resources/interfaces/{dir}"):  
                for filename in files:
                    file = open(f'{filePath}/../resources/interfaces/{dir}/{filename}', 'r')
                    output = open(f'{filePath}/' + getInterfacesPath(self.projectName)+f'/{dir}/{filename.removesuffix(".templ")+".dart"}', 'w')
                    for line in file:
                        output.writelines(line)
                    file.close()
                    output.close()
        #place interfaces

if __file__ == 'builder':
    builder = Builder('test2')

    builder.prepProject()

    simpleTile = ModuleModel(moduleName='SimpleTileModule', role='controlls', keyWord='<tile_module>', childrenModules=[], options={})

    header = ModuleModel(moduleName='TitleButtonsAppBarHeader', role='header', keyWord='', childrenModules=[], options={})
    body = ModuleModel(moduleName='ScrollBodyModule', role='body', keyWord='', childrenModules=[simpleTile], options={
        'mainAxisSpacing': '20'
    })
    footer = ModuleModel(moduleName='ButtonsFooterModule', role='footer', keyWord='', childrenModules=[], options={})

    screen = ScreenModel(header=header, body=body, footer=footer, parentScreen='', screenName='MainScreen')
    builder.createScreen(screen)

    builder.createModule(header)
    builder.createModule(body)
    builder.createModule(footer)