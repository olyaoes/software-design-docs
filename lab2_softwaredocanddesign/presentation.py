from abc import ABC, abstractmethod

class IOnboardingController(ABC):
    @abstractmethod
    def start_migration(self):
        pass
        
    @abstractmethod
    def get_status(self) -> str:
        pass