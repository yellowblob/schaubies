import io
import os
import sys
import json

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.cloud.vision_v1 import enums

from google.protobuf.json_format import MessageToDict

def request_annotations(source):
	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	#get all files from the given folder
	if(os.path.isdir(source)):
		
		files = []
		# r=root, d=directories, f = files
		for r, d, f in os.walk(source):
			for file in f:
					if not '.DS_Store' in file and not '.json' in file and not '.localized' in file:
						files.append(os.path.join(r, file))

	#if only one img is given save it in the same array structure when many are given
	else :

		files = [source]

	#define features to retrieve from the API
	features = [
		{"type": enums.Feature.Type.LABEL_DETECTION},
		{"type": enums.Feature.Type.OBJECT_LOCALIZATION},
	]

	#build requests
	requests = []
	for f in files:
		with io.open(f, 'rb') as image_file:
			content = image_file.read()
		requests.append({"image": types.Image(content=content), "features": features})

	#make request
	response = client.batch_annotate_images(requests)

	#transform request to dict
	response = MessageToDict(response)

	#output response as json
	for i, f in enumerate(files):

		#write full response json to path where img is located
		filename = os.path.splitext(f)[0]
		with open(filename + '-origin.json', 'w') as outfile:
			json.dump(response['responses'][i], outfile, indent=4)

		#write simplifide response json to path where img is located
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

		with open(filename + '-readable.json', 'w') as outfile:
			json.dump(output, outfile, indent=4)

if __name__ == "__main__":
	# The name of the image file to annotate or the path to the folder with the images to batch annotate
	source = os.path.abspath(sys.argv[1])
	request_annotations(source)

