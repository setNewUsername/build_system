import json, sys, os, psycopg2, shutil
from psycopg2 import Error
sys.path.append('../')
from builder.json_builder import *

BUILD_SYSTEM_FULL_PATH = os.path.abspath(__file__).removesuffix('\\b_tools\\build_part\\runner\\runner.py')
BUILD_SYSTEM_PROJECTS_DIR = 'projects'
PROJECT_FILES_ROOT_DIR_NAME = 'lib'

class Runner:
    projectUid = None
    currentProjectFilesFullPath = None
    currentProjectFullPath = None

    def __init__(self, projectId) -> None:
        self.projectUid = projectId
        self.currentProjectFilesFullPath = f'{BUILD_SYSTEM_FULL_PATH}\{BUILD_SYSTEM_PROJECTS_DIR}\{self.projectUid}\{PROJECT_FILES_ROOT_DIR_NAME}'
        self.currentProjectFullPath = f'{BUILD_SYSTEM_FULL_PATH}\{BUILD_SYSTEM_PROJECTS_DIR}\{self.projectUid}'

    def prepProjectFolders(self) -> None:
        os.mkdir(f'{self.currentProjectFilesFullPath}\\commons')
        os.mkdir(f'{self.currentProjectFilesFullPath}\\controls')
        os.mkdir(f'{self.currentProjectFilesFullPath}\\modules_by_screens')
        os.mkdir(f'{self.currentProjectFilesFullPath}\\screens')

    def createProjectDir(self):
        pass

    def createProjectFromJson(self):
        file = open('./jsonProject.json', 'r')
        data = json.load(file)
        file.close()

        bui = Builder(data, self.currentProjectFilesFullPath, self.projectUid)
        bui.createCommonHeader()
        bui.createCommonFooter()
        bui.createScreens()
        bui.createScreensModules()
        bui.createScreenHandler()
        bui.createScreenNavigator()
        bui.createMainFile()

    def initFlutterProject(self):
        if not self.checkProjectCreated():
            os.system(f'flutter create  --platforms android --project-name {self.projectUid} {BUILD_SYSTEM_FULL_PATH}\{BUILD_SYSTEM_PROJECTS_DIR}\{self.projectUid}')
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
            os.system(f'cd {BUILD_SYSTEM_FULL_PATH}/{BUILD_SYSTEM_PROJECTS_DIR} && cp -r {self.projectUid} ~/flutter_tmp && cd ~/flutter_tmp/{self.projectUid} && flutter build apk')
            if not os.path.exists(f'{BUILD_SYSTEM_FULL_PATH}/outputs/{self.projectUid}'):
                os.system(f'mkdir {BUILD_SYSTEM_FULL_PATH}/outputs/{self.projectUid}')
            os.system(f'mv ~/flutter_tmp/{self.projectUid}/build/app/outputs/apk/release/app-release.apk {BUILD_SYSTEM_FULL_PATH}/outputs/{self.projectUid}')
            os.system(f'rm -r ~/flutter_tmp/{self.projectUid}')
        else:
            os.system(f'cd {self.currentProjectFullPath} && flutter build apk')
        pass

    def getLayout(self):
        pass

run = Runner('test_proj')
run.initFlutterProject()
run.prepProjectFolders()
run.createProjectFromJson()