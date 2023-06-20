# Multiple speakers speech to text and summarization

## Dependencies

- Python 3.5+
- FFmpeg
- [openai api key](https://openai.com/)
- [vosk speech to text](https://github.com/format37/stt/tree/main/vosk_cpu)

## Installation
```
git clone 
cd 
python3 -m pip install -r requirements.txt
```
Obtain your openai key at https://openai.com/
and put it to a new file 'openai.key'
```
echo "your-openai-key" > openai_api_key.txt
```

## Package run
1. Put your video into 'in' folder  
2. Run:
```
python3 transcribe.py
```
3. Wait for the result
4. Get your transcribation and summarization from 'out' folder
