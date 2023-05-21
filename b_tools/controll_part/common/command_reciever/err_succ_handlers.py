class BaseCodesHandlers:
    messagesList: dict = None

    def __init__(self) -> None:
        self.messagesList = {}

    def addMesageInList(self, messageCode:int, message:str) -> None:
        self.messagesList[messageCode] = message

    def processMessage(self, code) -> str:
        return self.messagesList[code]

class SuccessHandler(BaseCodesHandlers):

    def __init__(self) -> None:
        super().__init__()

    def processSuccess(self, successCode) -> str:
        return super().processMessage(successCode)

class ErrorHandler(BaseCodesHandlers):

    def __init__(self) -> None:
        super().__init__()

    def processError(self, errorCode:int) -> str:
        return super().processMessage(errorCode)

succHandler = SuccessHandler()
succHandler.addMesageInList(201, 'request completed')
succHandler.addMesageInList(202, 'build started')
succHandler.addMesageInList(203, 'build stopped')
succHandler.addMesageInList(204, 'build planned')
succHandler.addMesageInList(205, 'project files removed')
succHandler.addMesageInList(206, 'build machines amount checked')
succHandler.addMesageInList(207, 'machine registered')
succHandler.addMesageInList(208, 'machine unregistered')
succHandler.addMesageInList(209, 'project remove from queue')

errHandler = ErrorHandler()
errHandler.addMesageInList(100, 'unhandler error')
errHandler.addMesageInList(101, 'no purpose field')
errHandler.addMesageInList(102, 'not supported purpose')
errHandler.addMesageInList(103, 'purpose wrong data')
errHandler.addMesageInList(104, 'host not in white list')
errHandler.addMesageInList(105, 'no purpose handlers')
errHandler.addMesageInList(106, 'project already marked as candidate to remove from build queue')