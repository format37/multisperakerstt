# Retrieve the container ID of the container named vosk_cpu_vosk-cpu_1
# container_id=$(sudo docker ps -a | grep vosk_cpu_vosk-cpu_1 | awk '{print $1}')

# Check if the container is running
# if [ -z "$(sudo docker ps -q -f id=$container_id)" ]; then
#     echo "Container is not running. Starting container with id: $container_id"
#     # Start the docker container named vosk_cpu_vosk-cpu_1 if it has not been started yet
#     sudo docker start $container_id
    # wait 30 seconds for the container to start
#     sleep 30
# else
#     echo "Container with id: $container_id is already running. No action is taken."
# fi


sudo docker run -it --rm \
  --network=host \
  -v $(pwd)/scripts:/app/scripts \
  -v $(pwd)/in:/app/in \
  -v $(pwd)/out:/app/out \
  -v $(pwd)/openai_api_key.txt:/app/openai_api_key.txt \
  -v $(pwd)/start.py:/app/start.py \
  multispeakerstt
