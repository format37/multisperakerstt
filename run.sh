sudo docker run -it --rm \
  -v $(pwd)/scripts:/app/scripts \
  -v $(pwd)/in:/app/in \
  -v $(pwd)/out:/app/out \
  -v $(pwd)/openai_api_key.txt:/app/openai_api_key.txt \
  -v $(pwd)/start.py:/app/start.py \
  multispeakerstt