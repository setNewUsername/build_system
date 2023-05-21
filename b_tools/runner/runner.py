import json, sys, os, psycopg2
from psycopg2 import Error

#b_tools path
sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}\..\..\\')
#builder path
sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}\..\..\\builder\\')

from b_tools.builder.builder import *
from b_tools.builder.p_builder import *
from b_tools.builder.commons import *

filePath = os.path.dirname(os.path.abspath(__file__))

class Runner:
    objects = {}
    cursor = None
    def __init__(self, DBconnection) -> None:
        self.cursor = DBconnection.cursor()

    def checkProjectCreated(self, projName:str) -> bool:
        return os.path.exists(f'{filePath}/' + projectsPath + projName)

    def runBuild(self, projName:str):
        builder = Builder(projName)

        layout = self.getLayout(projName)

        try:
            if layout != None:
                self.createObjects(layout)

                if not self.checkProjectCreated(projName):
                    if createProject(projName, f'{filePath}/' + projectsPath) == 0:
                        os.remove(f'{filePath}/' + projectsPath + projName + '/lib/main.dart')
                        shutil.rmtree(f'{filePath}/'+ projectsPath + projName+'/test')
                    builder.prepProject()
                for objKey in self.objects.keys():
                    if 'screen' in objKey:
                        builder.createScreen(self.objects[objKey])
                    else:
                        builder.createModule(self.objects[objKey])
                
                if os.name == 'posix':
                    os.system(f'cd {filePath}/../../projects/ && cp -r {projName} ~/flutter_tmp && cd ~/flutter_tmp/{projName} && flutter build apk')
                    if not os.path.exists(f'{filePath}/../../outputs/{projName}'):
                        os.system(f'mkdir {filePath}/../../outputs/{projName}')
                    os.system(f'mv ~/flutter_tmp/{projName}/build/app/outputs/apk/release/app-release.apk {filePath}/../../outputs/{projName}')
                    os.system(f'rm -r ~/flutter_tmp/{projName}')
                else:
                    os.system(f'cd {filePath}/../../projects/{projName} && flutter build apk')
        except:
            return False
        return True

    def getLayout(self, projName:str):
        postgreSQL_select_Query = f"select * from projects where uid='{projName}'"

        self.cursor.execute(postgreSQL_select_Query)

        project = self.cursor.fetchall()

        if len(project) == 0:
            print("no such project")
            return None

        self.cursor.close()

        for row in project:
            return row[5]

    def createScreen(self, header:ModuleModel, footer:ModuleModel, rawScreenData) -> list:

        scrnBody = self.createModule(rawScreenData['modules'], 'body')
        
        return [ScreenModel(header=header, body=scrnBody, footer=footer, parentScreen='', screenName=rawScreenData['name']), scrnBody]

    def createModule(self, rawModuleData:dict, newRole:str = None) -> ModuleModel:
        if newRole == None:
            newRole = 'controlls'

        moduleName = rawModuleData['name']
        moduleOptions = rawModuleData['options']
        moduleKeyWord = rawModuleData['keyWord']
        moduleChildren = []
        
        #print(moduleOptions)

        if 'modules' in rawModuleData.keys():
            for module in rawModuleData['modules']:
                moduleChildren.append(self.createModule(module))

        return ModuleModel(moduleName=moduleName, role=newRole, keyWord=moduleKeyWord, childrenModules=moduleChildren, options=moduleOptions)

    def createObjects(self, jsonData:str):
        rawData = json.loads(jsonData)
        header = self.createModule(rawData['header'], 'header')
        footer = self.createModule(rawData['footer'], 'footer')
    
        self.objects['header'] = header
        self.objects['footer'] = footer

        for i, scrn in enumerate(rawData['screens']):
            screen = self.createScreen(header, footer, scrn)
            self.objects['screen'+str(i)] = screen[0]
            self.objects['body'+str(i)] = screen[1]

def start(name:str):
    try:
        connection = psycopg2.connect(user="psql_test_user",
                                    password="root",
                                    host="192.168.0.107",
                                    port="5432",
                                    database="frank")
        
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            run = Runner(connection)
            
            run.runBuild(name)

            connection.close()
            print("Соединение с PostgreSQL закрыто")