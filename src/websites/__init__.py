from typing import List, Type

from .magalu import Magalu
from .pichau import Pichau
from .website import Website

WEBSITE_CLASSES: List[Type[Website]] = [Magalu, Pichau]
