import sys
import os
from scripts.converter import convert_audio_m4a_to_wav
from scripts.transcribator import transcribation
import time
import datetime
import pandas as pd
import re

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
        
        """# Convert audio
        print('#', filename, 'convert_audio')
        convert_audio_m4a_to_wav(in_path, out_path)

        # Transcribe
        print('#', filename, 'transcribation')
        pattern = "audio(.*?)\d+\.m4a"  # This pattern looks for any character(s) between "audio" and a series of numbers followed by ".m4a"
        match = re.search(pattern, filename)
        if match:
            speaker_name = match.group(1)
        else:
            speaker_name = filename
        transcribation(out_path, out_path + '.csv', speaker_name)"""
        # Append the transcribed data to the dataframe
        df = df.append(pd.read_csv(out_path + '.csv'))
    # Sort by start_time
    df = df.sort_values(by=['start_time'])
    # Merge speakers
    df = merge_speakers(df)
    # Save as text in format: start_time speaker_name transcription
    with open('out/transcription.txt', 'w') as f:
        for index, row in df.iterrows():
            # f.write(str(row['start_time']) + ' ' + row['speaker_name'] + ' ' + row['transcription'] + '\n')
            f.write(row['speaker_name'] + ': ' + row['transcription'] + '\n')
            
    time_end = time.time()
    time_passed_formatted = str(datetime.timedelta(seconds=time_end - time_start))
    print('#', 'Done in', time_passed_formatted)


if __name__ == "__main__":
    main()
