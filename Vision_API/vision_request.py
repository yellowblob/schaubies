import io
import os
import sys
import json

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath(sys.argv[1])

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image,max_results=100)
labels = response.label_annotations
response = client.object_localization(image=image,max_results=100)
objects = response.localized_object_annotations

label_output = []
object_output = []

for label in labels:
	label_output.append({
		'description': label.description,
		'score': label.score
		})

for localized_object in objects:
	object_output.append({
		'description': localized_object.name,
		'score': localized_object.score
		})

#construct json
output = {
	'labels' : label_output,
	'objects': object_output
}

# remove file extension from image file path
filename = os.path.splitext(sys.argv[1])[0]

#write request json to path where img is located
with open(filename + '.json', 'w') as outfile:
    json.dump(output, outfile, indent=2)