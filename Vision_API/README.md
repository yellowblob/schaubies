# gcloud Vision API Example

## Prerequisites

As a start it is a good practise to create a project folder and create a virtual environment.

Create the environment like this:

	python3 -m virtualenv your-virtual-env

activate it with:

	source your-virtual-env/bin/activate

## Option 1 - REST API

Follow this guide to get started and try the vision API using the command line.
<a href="https://cloud.google.com/vision/docs/quickstart-cli" target="_blank">https://cloud.google.com/vision/docs/quickstart-cli</a>

Use [image2request_json.py](image2request_json.py) to get a request json you can send to the Vision API.

You can use the script like this:

	python image2request_json.py path/to/your/img

Make the request:

	curl -X POST \
	-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
	-H "Content-Type: application/json; charset=utf-8" \
	https://vision.googleapis.com/v1/images:annotate -d @your-request.json > your-response.json

## Option 2 - Client Libraries

The Quickstart guide for using the client libraries can be found here:  
<a href="https://cloud.google.com/vision/docs/quickstart-client-libraries" target="_blank">https://cloud.google.com/vision/docs/quickstart-client-libraries</a>

Use [vision_request.py](vision_request.py) to directly request the data via python and get a reduced json, that only includes recognized labels/objects and the scores they have.

	python vision_request.py path/to/your/img

<i class="far fa-circle" style="color:gold"></i> Robert, July 16<sup>th</sup>, 2020