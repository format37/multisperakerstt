FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python3 -m pip install --upgrade openai
# COPY start.py /app
ENTRYPOINT ["python3"]
CMD ["start.py"]

