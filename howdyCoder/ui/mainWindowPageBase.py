from abc import abstractmethod, abstractclassmethod, ABC


class MainWindowPageBase(ABC):
    @abstractmethod
    def loadMainPage(self):
        pass

    @abstractclassmethod
    def leaveMainPage(self):
        pass
