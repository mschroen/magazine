import importlib.metadata

__version__ = importlib.metadata.version("magazine")

from .magazine import Magazine
from .publish import Publish
