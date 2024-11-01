import importlib.metadata

__version__ = importlib.metadata.version("magazine")

from .story import Story

report = Story.report
post = Story.post
figure = Story.figure

from .publish import Publish
