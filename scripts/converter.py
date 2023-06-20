import os
import sys
import subprocess

def convert_audio(input_audio_path, output_audio_path):
    command = ["ffmpeg", "-i", input_audio_path, "-y", "-ac", "1", "-ar", "16000", "-ab", "256k", output_audio_path]
    subprocess.run(command, check=True)

def convert_audio_m4a_to_wav(input_audio_path, output_audio_path):
    command = ["ffmpeg", "-i", input_audio_path, "-y", "-ac", "1", "-ar", "32000", "-ab", "126k", output_audio_path]
    subprocess.run(command, check=True)

def main():
    # Ensure correct number of arguments are passed
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.wav output.wav")
        sys.exit(1)

    input_audio_path = sys.argv[1]
    output_audio_path = sys.argv[2]

    # Convert the audio file
    convert_audio(input_audio_path, output_audio_path)

if __name__ == "__main__":
    main()
