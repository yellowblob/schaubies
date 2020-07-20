from PIL import Image
import pyheif
import os
import sys

# The name of the image file to annotate or the path to the folder with the images to batch annotate
source = os.path.abspath(sys.argv[1])

if(os.path.isdir(source)):
	
	files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(source):
		for file in f:
				if not '.DS_Store' in file and not '.json' in file and not '.localized' in file:
					files.append(os.path.join(r, file))
	
	for f in files:
		heif_file = pyheif.read(f)
		image = Image.frombytes(
    		heif_file.mode, 
    		heif_file.size, 
    		heif_file.data,
    		"raw",
    		heif_file.mode,
    		heif_file.stride,
    		)
		filename = os.path.splitext(f)[0]
		image.save(filename + ".jpg", "JPEG")