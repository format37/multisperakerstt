import sys
import os
from scripts.converter import convert_audio
from scripts.transcribator import transcribation
from scripts.gpt_proxy import gpt
import time
import datetime
import pandas as pd
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def merge_speakers(df):
    # Create a 'group' column that increments every time 'speaker_name' changes
    df['group'] = (df['speaker_name'] != df['speaker_name'].shift()).cumsum()

    # Group by 'group', join the 'transcription' strings, and get the first 'start_time' and 'speaker_name' and last 'end_time' in each group
    df = df.groupby('group').agg({
        'start_time': 'first',
        'end_time': 'last',
        'speaker_name': 'first',
        'transcription': ' '.join,
    }).reset_index(drop=True)
    return df


def main():
    time_start = time.time()
    # Define a pandas dataframe to contain the start_time, end_time speaker_name and transcription
    df = pd.DataFrame(columns=['start_time', 'end_time', 'speaker_name', 'transcription'])
    # Iterate files in path 'in'
    for filename in os.listdir('in'):
        if filename.endswith('.md'):
            continue
        in_path = os.path.join('in', filename)
        filename_wav = filename.split('.')[0] + '.wav'
        out_path = os.path.join('out', filename_wav)
        
        # Convert audio
        print('#', filename, 'convert_audio')
        convert_audio(in_path, out_path)

        # Transcribe
        print('#', filename, 'transcribation')
        pattern = "audio(.*?)\d+\.m4a"  # This pattern looks for any character(s) between "audio" and a series of numbers followed by ".m4a"
        match = re.search(pattern, filename)
        if match:
            speaker_name = match.group(1)
        else:
            speaker_name = filename
        transcribation(out_path, out_path + '.csv', speaker_name)
        # Append the transcribed data to the dataframe
        df = df.append(pd.read_csv(out_path + '.csv'))
    
    # Sort by start_time
    df = df.sort_values(by=['start_time'])
    # Merge speakers
    df = merge_speakers(df)
    # Save as text in format: start_time speaker_name transcription
    transcription = ''
    with open('out/transcription.txt', 'w') as f:
        for index, row in df.iterrows():
            new_line = row['speaker_name'] + ': ' + row['transcription'] + '\n'
            transcription += new_line
            f.write(new_line)
    
    # Restoring the dialog
    if not os.path.exists("openai_api_key.txt"):
        logger.info("openai_api_key.txt not found")
        sys.exit(1)
    with open("openai_api_key.txt", "r") as f:
        openai_key = f.read().splitlines()[0]
    # read with utf-8-sig encoding to remove BOM
    # with open('out/transcription.txt', 'r', encoding='utf-8-sig') as f:
    with open('out/transcription.txt', 'r') as f:
        transcription = f.read()
    system_prompt = """You are the secretary. Your job is reading the text which was recognized from audio recordings obtained as a result of Zoom video meetings. And then you need to write a short Russian overview about meeting:
* Agenda
* Discussion topics
* Resume of this meeting"""
    transctiption_restored = gpt(transcription, openai_key, system_prompt)
    with open('out/transcription_restored.txt', 'w') as f:
        f.write(transctiption_restored)    
            
    time_end = time.time()
    time_passed_formatted = str(datetime.timedelta(seconds=time_end - time_start))
    print('#', 'Done in', time_passed_formatted)


if __name__ == "__main__":
    main()
