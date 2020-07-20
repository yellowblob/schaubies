import io
import os
import sys
import json

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

from google.protobuf.json_format import MessageToDict

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath(sys.argv[1])

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response_labels = client.label_detection(image=image,max_results=100)
labels = response_labels.label_annotations
response_objects = client.object_localization(image=image,max_results=100)
objects = response_objects.localized_object_annotations

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

#construct json to generate easily readable output
output = {
	'labels' : label_output,
	'objects': object_output
}

# remove file extension from image file path
filename = os.path.splitext(sys.argv[1])[0]

#write request json to path where img is located
with open(filename + '.json', 'w') as outfile:
    json.dump(output, outfile, indent=2)

#generating full output to have positions of recognized objects included

output = {
	'labelAnnotations' : MessageToDict(response_labels),
	'localizedObjectAnnotations': MessageToDict(response_objects)
}

#write request json to path where img is located
with open(filename + '-origin.json', 'w') as outfile:
    json.dump(output, outfile, indent=2)