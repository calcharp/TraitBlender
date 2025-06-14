### Script for setting up transforms, the global transform dictionary, and the transform handler pipeline

from abc import ABC, abstractmethod
import bpy
import random
from PIL import ImageColor

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

class RandomWorldColor(Transform):
    """
    Transform that sets the world color to a random color, either from a provided list or randomly from the RGB spectrum.
    Args:
        colors (list of str): Optional list of hex color codes. If not provided, a random color is chosen.
    """
    def do(self, colors=None):
        # Use provided colors or self.args
        colors = colors or self.args.get('colors')
        if colors:
            hex_color = random.choice(colors)
            rgb = ImageColor.getrgb(hex_color)
            # Convert to 0-1 range and keep only RGB
            rgb = tuple(c / 255.0 for c in rgb[:3])
        else:
            rgb = (random.random(), random.random(), random.random())
        # Set the world color in Blender (node-based)
        world = bpy.context.scene.world
        if world and world.use_nodes:
            bg = world.node_tree.nodes.get('Background')
            if bg:
                bg.inputs[0].default_value = (*rgb, 1.0)
        else:
            # Fallback for non-node worlds
            world.color = rgb

# Global dictionary of available transforms
TRANSFORMS = {
    "RandomWorldColor": RandomWorldColor
}


