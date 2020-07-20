import io
import os
import sys
import json

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.cloud.vision_v1 import enums

from google.protobuf.json_format import MessageToDict

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate or the path to the folder with the images to batch annotate
source = os.path.abspath(sys.argv[1])

if(os.path.isdir(source)):
	
	files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(source):
		for file in f:
				if not '.DS_Store' in file and not '.json' in file:
					files.append(os.path.join(r, file))

	features = [
		{"type": enums.Feature.Type.LABEL_DETECTION},
		{"type": enums.Feature.Type.OBJECT_LOCALIZATION},
	]

	requests = []
	for f in files:
		with io.open(f, 'rb') as image_file:
			content = image_file.read()
		requests.append({"image": types.Image(content=content), "features": features})

	response = client.batch_annotate_images(requests)

	response = MessageToDict(response)

	# remove file extension from image file path
	filename = os.path.splitext(sys.argv[1])[0]

	for i, f in enumerate(files):
		#write request json to path where img is located
		filename = os.path.splitext(f)[0]
		with open(filename + '-origin.json', 'w') as outfile:
			json.dump(response['responses'][i], outfile, indent=4)

		labels = []
		objects = []

		if 'labelAnnotations' in response['responses'][i]:
			for annotation in response['responses'][i]['labelAnnotations']:
				labels.append(annotation['description'] + ' (' + str(annotation['score']) + ')')
		if 'localizedObjectAnnotations' in response['responses'][i]:
			for annotation in response['responses'][i]['localizedObjectAnnotations']:
				objects.append(annotation['name'] + ' (' + str(annotation['score']) + ')')

		output = {
			'labels' : labels,
			'objects': objects
		}		

		#write request json to path where img is located
		with open(filename + '-readable.json', 'w') as outfile:
			json.dump(output, outfile, indent=4)

else :

	
	
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
	
	