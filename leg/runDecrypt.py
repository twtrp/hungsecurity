import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from clientApp import *

recipient = sys.argv[1]

DecryptFile(recipient)