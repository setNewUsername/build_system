from flashtext.keyword import KeywordProcessor

class ScreenModel:
    headerId:str = None
    bodyId:str = None
    footerId:str = None
    screenId:str = None

    templateLines:list = None
    dartLines:list = None

    keyWordProc:KeywordProcessor = None

    def __init__(self, screenId, headerId, bodyId, footerId, screenTemplateName) -> None:
        self.screenId = screenId
        self.headerId = headerId
        self.bodyId = bodyId
        self.footerId = footerId
        self.keyWordProc = KeywordProcessor()
        file = open(f'./{screenTemplateName}_template.module')
        self.templateLines = file.readlines()
        file.close()
        self.dartLines = []
        self.addKeyWords()
    
    def addKeyWords(self):
        self.keyWordProc.add_keyword('<screen_body_id>', self.bodyId)
        self.keyWordProc.add_keyword('<screen_header_id>', self.headerId)
        self.keyWordProc.add_keyword('<screen_footer_id>', self.footerId)
        self.keyWordProc.add_keyword('<screen_id>', self.screenId)

    def writeLinesToDart(self):
        for lineIndex in range(len(self.templateLines)):
            self.templateLines[lineIndex] = self.keyWordProc.replace_keywords(self.templateLines[lineIndex])
        file = open(f'./test/screens/{self.screenId}.dart', 'w')
        file.writelines(self.templateLines)
        file.close()