### Script for setting up transforms, the global transform dictionary, and the transform handler pipeline

from abc import ABC, abstractmethod
import bpy

class Transform(ABC):
    """
    Abstract base class for all transforms.
    """

    def __init__(self, args: dict = None):
        self.args = args or {}

    @abstractmethod
    def do(self):
        """
        Apply the transform to the asset.
        """
        pass

    def apply(self):
        """
        Apply the transform using the stored arguments and update the scene.
        """
        self.do(**self.args)
        # Update the scene after applying the transform
        bpy.context.view_layer.update()


