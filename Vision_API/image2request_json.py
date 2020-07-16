import base64
import sys
import json
import os

# read img file and write it as base64 encoded string to variable
with open(sys.argv[1], "rb") as img_file:
    img_string = base64.b64encode(img_file.read())
    img_string = img_string.decode('utf-8') #remove starting b from string

# build request dict
request = {
  "requests": [
    {
      "image": {
        "content": img_string
        },
      "features": [
        {
          "type": "LABEL_DETECTION",
          "maxResults": 100
        },
        {
          "type": "OBJECT_LOCALIZATION",
          "maxResults": 100
        }
      ]
    }
  ]
}

# remove file extension from image file path
filename = os.path.splitext(sys.argv[1])[0]

#write request json to path where img is located
with open(filename + '.json', 'w') as outfile:
    json.dump(request, outfile)