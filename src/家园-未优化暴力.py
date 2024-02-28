import logging
import re
import pyautogui
import numpy as np
from models.utils.gameOCR import *
from airtest.core.api import *

logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

image = 