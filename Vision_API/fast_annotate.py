import os
import sys

from heic2jpeg import heic2jpeg
from vision_request import request_annotations

source = os.path.abspath(sys.argv[1])

heic2jpeg(source)

source = os.path.splitext(source)[0] + '.jpg'

request_annotations(source)