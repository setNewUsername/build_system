projectsPath = '../../projects/'

def getScreensPath(projectName:str) -> str:
    return projectsPath+projectName+'/lib/screens'

def getModulesPath(projectName:str) -> str:
    return projectsPath+projectName+'/lib/modules'

def getInterfacesPath(projectName:str) -> str:
    return projectsPath+projectName+'/lib/interfaces'