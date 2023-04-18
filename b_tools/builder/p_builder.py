import os
import argparse
import os.path
import sys
import shutil

from commons import *

def createProject(projectName:str, projectPath:str) -> int:
    projectsFullPath = projectPath + projectName
    return os.system(f'flutter create --platforms android --project-name {projectName} {projectsFullPath}')

if __file__ == 'p_builder':
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', nargs='?', default='def_name')

    namespace = parser.parse_args(sys.argv[1:])

    if createProject(namespace.name, projectsPath) == 0:
        os.remove(projectsPath+namespace.name+'/lib/main.dart')
        shutil.rmtree(projectsPath+namespace.name+'/test')