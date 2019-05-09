from __future__ import print_function
import sys

from PIL import Image
import base64
import io
import cv2
import numpy as np

from sqlalchemy import inspect

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    
def base64_to_image_file(data):
#     data = request.get_json(silent=True)
    base64ImageString = data[23:]
    imgdata = base64.b64decode(base64ImageString)
    image = Image.open(io.BytesIO(imgdata))
#     imageRGB = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    return np.array(image)
                    
def map_row_data_to_object(data):
    inst = inspect(data)
    result = {}
    for key, x in inst.attrs.items():
        result[key] = x.value
    return result