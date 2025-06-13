### Script for setting up transforms, the global transform dictionary, and the transform handler pipeline

from abc import ABC, abstractmethod

class Transform(ABC):
    """
    Abstract base class for all transforms.
    """

    def __init__(self, args: dict = None):
        self.args = args or {}

    @abstractmethod
    def apply(self):
        """
        Apply the transform to the asset.
        """
        pass




