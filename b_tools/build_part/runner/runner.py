import json, sys, os, psycopg2, shutil
from psycopg2 import Error
from b_tools.build_part.builder.json_builder import *

BUILD_SYSTEM_FULL_PATH = os.path.abspath(__file__).removesuffix('\\b_tools\\build_part\\runner\\runner.py')
BUILD_SYSTEM_PROJECTS_DIR = 'projects'
PROJECT_FILES_ROOT_DIR_NAME = 'lib'

class Runner:
    projectUid = None
    projectLocalName = None
    currentProjectFilesFullPath = None
    currentProjectFullPath = None

    def __init__(self, projectId) -> None:
        self.projectUid = projectId
        self.projectLocalName = 'a'+self.projectUid.replace('-', '')
        self.currentProjectFilesFullPath = f'{BUILD_SYSTEM_FULL_PATH}\{BUILD_SYSTEM_PROJECTS_DIR}\{self.projectLocalName}\{PROJECT_FILES_ROOT_DIR_NAME}'
        self.currentProjectFullPath = f'{BUILD_SYSTEM_FULL_PATH}\{BUILD_SYSTEM_PROJECTS_DIR}\{self.projectLocalName}'

    def prepProjectFolders(self) -> None:
        os.mkdir(f'{self.currentProjectFilesFullPath}\\commons')
        os.mkdir(f'{self.currentProjectFilesFullPath}\\controls')
        os.mkdir(f'{self.currentProjectFilesFullPath}\\modules_by_screens')
        os.mkdir(f'{self.currentProjectFilesFullPath}\\screens')

    def createProjectDir(self):
        pass

    def createProjectFromJson(self):
        #file = open(os.path.abspath(__file__).removesuffix('\\runner.py')+'/jsonProject.json', 'r')
        data = json.loads(self.getLayout())
        #file.close()

        bui = Builder(data, self.currentProjectFilesFullPath, self.projectLocalName)
        bui.createCommonHeader()
        bui.createCommonFooter()
        bui.createScreens()
        bui.createScreensModules()
        bui.createScreenHandler()
        bui.createScreenNavigator()
        bui.createMainFile()
        bui.createRootWidget()
        bui.createBaseModuleFile()

    def initFlutterProject(self):
        if not self.checkProjectCreated():
            os.system(f'flutter create  --platforms android --project-name {self.projectLocalName} {BUILD_SYSTEM_FULL_PATH}\{BUILD_SYSTEM_PROJECTS_DIR}\{self.projectLocalName}')
        self.clearProject()

    def checkProjectCreated(self):
        pass

    def checkProjectCreated(self) -> bool:
        return os.path.exists(f'{self.currentProjectFullPath}')

    def clearProject(self):
        for files in os.listdir(self.currentProjectFilesFullPath):
            path = os.path.join(self.currentProjectFilesFullPath, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)

    def startBuild(self):
        if os.name == 'posix':
            os.system(f'cd {BUILD_SYSTEM_FULL_PATH}/{BUILD_SYSTEM_PROJECTS_DIR} && cp -r {self.projectLocalName} ~/flutter_tmp && cd ~/flutter_tmp/{self.projectLocalName} && flutter build apk')
            if not os.path.exists(f'{BUILD_SYSTEM_FULL_PATH}/outputs/{self.projectLocalName}'):
                os.system(f'mkdir {BUILD_SYSTEM_FULL_PATH}/outputs/{self.projectLocalName}')
            os.system(f'mv ~/flutter_tmp/{self.projectLocalName}/build/app/outputs/apk/release/app-release.apk {BUILD_SYSTEM_FULL_PATH}/outputs/{self.projectLocalName}')
            os.system(f'rm -r ~/flutter_tmp/{self.projectLocalName}')
        else:
            os.system(f'cd {self.currentProjectFullPath} && flutter build apk')
        pass

    def getLayout(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="root",
                                          host="192.168.0.107",
                                          port="5432",
                                          database="frankenstein")
        
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                postgreSQL_select_Query = f"select * from projects where uid='{self.projectUid}'"
                curs = connection.cursor()
                curs.execute(postgreSQL_select_Query)

                project = curs.fetchall()

                if len(project) == 0:
                    print("no such project")
                    return None

                curs.close()

                for row in project:
                    return row[5]

                connection.close()
                print("Соединение с PostgreSQL закрыто")
        pass

def start(projectUid):
    run = Runner(projectUid)
    run.initFlutterProject()
    run.prepProjectFolders()
    run.createProjectFromJson()
    run.startBuild()