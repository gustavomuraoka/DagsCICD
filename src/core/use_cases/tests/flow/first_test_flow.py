from utils.logs.logger import logger

class FirstTestFlow():
    def __init__(self):
        self.__greet__()
    
    def __greet__(self) -> None:
        for i in range(3):
            logger.info("Testando 1... 2... 3...")


      
