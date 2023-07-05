# Multiple speakers speech to text and summarization

## Dependencies

- Docker
- [openai api key](https://openai.com/)
- [vosk speech to text](https://github.com/format37/stt/tree/main/vosk_gpu)

## Installation
```
git clone https://github.com/format37/multisperakerstt.git
cd multisperakerstt
sh build.sh
```
Obtain your openai key at https://openai.com/
and put it to a new file 'openai_api_key.txt':
```
echo "your-openai-key" > openai_api_key.txt
```

## Usage
1. Put your Zoom audio files into 'in' folder  
2. Run:
```
sh run.sh
```
3. Wait for the result
4. Get your transcribation and summarization from 'out' folder
