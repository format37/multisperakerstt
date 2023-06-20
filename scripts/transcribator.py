import asyncio
import websockets
import wave
import json
import sys
import pandas as pd

def accept_feature_extractor(dataframe, accept, speaker_name):    
    if len(accept)>1 and accept['text'] != '':        
        accept_text = str(accept['text'])                
        accept_start = str(accept['result'][0]['start'])
        accept_end = accept['result'][-1:][0]['end']        
        conf_score = []
        for result_rec in accept['result']:
            conf_score.append(float(result_rec['conf']))
        conf_mid = str(sum(conf_score)/len(conf_score))
        dataframe.append([accept_start, accept_end, speaker_name, accept_text])


async def run_test(uri, filename, out_filepath, speaker_name):
    df_data = []
    df_columns = ['start_time', 'end_time', 'speaker_name', 'transcription']
    
    async with websockets.connect(uri) as websocket:
        wf = wave.open(filename, "rb")        
        await websocket.send('{ "config" : { "sample_rate" : %d } }' % (wf.getframerate()))
        buffer_size = int(wf.getframerate() * 0.2) # 0.2 seconds of audio
        while True:
            data = wf.readframes(buffer_size)
            if len(data) == 0:
                break

            await websocket.send(data)
            accept = json.loads(await websocket.recv())					
            accept_feature_extractor(df_data, accept, speaker_name)

        await websocket.send('{"eof" : 1}')
        accept = json.loads(await websocket.recv())		
        accept_feature_extractor(df_data, accept, speaker_name)

    # Create pandas DataFrame and save to CSV
    df = pd.DataFrame(df_data, columns=df_columns)
    df.to_csv(out_filepath, index=False)


def transcribation(filename, out_filepath, speaker_name):
    print('# transcribation', filename, out_filepath, speaker_name)
    asyncio.run(run_test('ws://localhost:2800', filename, out_filepath, speaker_name))


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} input.wav output.csv speaker_name")
        sys.exit(1)
    filename = sys.argv[1]
    out_filepath = sys.argv[2]
    speaker_name = sys.argv[3]
    transcribation(filename, out_filepath, speaker_name)


if __name__ == "__main__":
    main()