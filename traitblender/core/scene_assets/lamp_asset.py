from .scene_asset import SceneAsset
import bpy

class LampAsset(SceneAsset):
    """
    Specialized SceneAsset for managing lamp (spot light) objects in Blender.
    Provides convenient access to common spot light settings.
    """
    @property
    def lamp(self):
        obj = self.object
        if obj and obj.type == 'LIGHT' and obj.data.type == 'SPOT':
            return obj.data
        raise TypeError(f"Object '{self.name}' is not a Spot light.")

    @property
    def color(self):
        return self.lamp.color

    @color.setter
    def color(self, value):
        self.lamp.color = value

    @property
    def power(self):
        return self.lamp.energy

    @power.setter
    def power(self, value):
        self.lamp.energy = value

    @property
    def use_soft_falloff(self):
        return self.lamp.use_soft_falloff

    @use_soft_falloff.setter
    def use_soft_falloff(self, value):
        self.lamp.use_soft_falloff = value

    @property
    def radius(self):
        return self.lamp.shadow_soft_size

    @radius.setter
    def radius(self, value):
        self.lamp.shadow_soft_size = value

    @property
    def size(self):
        return self.lamp.spot_size

    @size.setter
    def size(self, value):
        self.lamp.spot_size = value

    @property
    def blend(self):
        return self.lamp.spot_blend

    @blend.setter
    def blend(self, value):
        self.lamp.spot_blend = value

    @property
    def show_cone(self):
        return self.lamp.show_cone

    @show_cone.setter
    def show_cone(self, value):
        self.lamp.show_cone = value

    pass 