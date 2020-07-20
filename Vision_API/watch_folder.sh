fswatch -0 ~/Downloads -e ".DS_Store" -e ".jpg" -e ".json" --event=PlatformSpecific | while read -d "" event
do
	echo "\n"
	echo ${event}
	python fast_annotate.py ${event}
	echo "\n"

done