from .client import GSTLAClient  # registered by AutoBizHawkClientRegister
from .world import GSTLAWorld  # registered by AutoWorldRegister

__all__ = ['GSTLAClient', 'GSTLAWorld']  # for now only cosmetic
