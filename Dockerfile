FROM python:3.10-slim-buster
WORKDIR /app
# Update the system and install FFmpeg
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y ffmpeg
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python3 -m pip install --upgrade openai
# COPY start.py /app
ENTRYPOINT ["python3"]
CMD ["start.py"]

