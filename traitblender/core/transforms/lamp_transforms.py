# Lamp-related transforms for TraitBlender

from .transforms import Transform
from ..scene_assets.asset_helpers import with_scene_asset
import random

# Add lamp-related transform classes here 

class GaussianLampPower(Transform):
    """
    Transform that sets the lamp's power to a value drawn from a Gaussian distribution.
    Args:
        mean (float): Mean of the Gaussian. Default is 10.
        sd (float): Standard deviation of the Gaussian. Default is 1.5.
    """
    @with_scene_asset(name="Lamp", type="LampAsset")
    def do(self, mean=10, sd=1.5, active_asset=None):
        value = random.gauss(mean, sd)
        active_asset.power = value 