from flashtext.keyword import KeywordProcessor
import os, sys

class ScreenModel:
    headerId:str = None
    bodyId:str = None
    footerId:str = None
    screenId:str = None

    projectUid:str = None

    templateLines:list = None
    dartLines:list = None

    keyWordProc:KeywordProcessor = None

    def __init__(self, screenId, headerId, bodyId, footerId, screenTemplateName, projectUid) -> None:
        self.projectUid = projectUid
        self.screenId = screenId
        self.headerId = headerId
        self.bodyId = bodyId
        self.footerId = footerId
        self.keyWordProc = KeywordProcessor()
        file = open(os.path.abspath(__file__).removesuffix('\\models\\screen_model.py') + f'\\templates\\{screenTemplateName}_template.module')
        self.templateLines = file.readlines()
        file.close()
        self.dartLines = []
        self.addKeyWords()
    
    def addKeyWords(self):
        self.keyWordProc.add_keyword('<screen_body_id>', self.bodyId)
        self.keyWordProc.add_keyword('<screen_header_id>', self.headerId)
        self.keyWordProc.add_keyword('<screen_footer_id>', self.footerId)
        self.keyWordProc.add_keyword('<screen_id>', self.screenId)
        self.keyWordProc.add_keyword('<project_name>', self.projectUid)

    def writeLinesToDart(self, projectFilesFullPath):
        for lineIndex in range(len(self.templateLines)):
            self.templateLines[lineIndex] = self.keyWordProc.replace_keywords(self.templateLines[lineIndex])
        file = open(f'{projectFilesFullPath}\\screens\\{self.screenId}.dart', 'w')
        file.writelines(self.templateLines)
        file.close()