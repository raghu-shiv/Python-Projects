import ffmpeg
import whisper
import os
import subprocess

def inspect_video(video_path):
    """
    Inspects the video file to provide detailed information about its structure.

    Parameters:
    video_path (str): Path to the video file.
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-v", "trace", "-i", video_path],
            capture_output=True, text=True
        )
        print(result.stdout)
    except Exception as e:
        print(f"Error inspecting video: {str(e)}")
        raise

def repair_video(video_path, repaired_video_path):
    """
    Attempts to repair a video file using alternative methods.

    Parameters:
    video_path (str): Path to the original video file.
    repaired_video_path (str): Path where the repaired video will be saved.
    """
    try:
        # Attempt repair with ffmpeg
        print("Attempting to repair video with ffmpeg...")
        ffmpeg.input(video_path).output(repaired_video_path, c='copy', movflags='+faststart').run(overwrite_output=True)
        print("Video repaired successfully.")
    except ffmpeg.Error as e:
        print(f"Error repairing video by copying streams: {e.stderr.decode() if e.stderr else e}")
        # Try re-encoding as a fallback
        try:
            print("Re-encoding video as a fallback...")
            ffmpeg.input(video_path).output(repaired_video_path, vcodec='libx264', acodec='aac').run(overwrite_output=True)
            print("Video re-encoded successfully.")
        except ffmpeg.Error as e:
            print(f"Error re-encoding video: {e.stderr.decode() if e.stderr else e}")
            raise

def extract_audio(video_path, audio_path):
    """
    Extracts audio from a video file and saves it as a .wav file.

    Parameters:
    video_path (str): Path to the video file.
    audio_path (str): Path where the extracted audio will be saved.
    """
    try:
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(stream, audio_path)
        ffmpeg.run(stream, overwrite_output=True)
        print("Audio extracted successfully.")
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e.stderr.decode() if e.stderr else e}")
        raise

def transcribe_audio(audio_path):
    """
    Transcribes the audio file using OpenAI's Whisper model.

    Parameters:
    audio_path (str): Path to the audio file to be transcribed.

    Returns:
    str: The transcribed text.
    """
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        print("Transcription completed successfully.")
        return result['text']
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        raise

def append_transcription_to_file(transcription, output_path):
    """
    Appends the transcription text to an existing file.

    Parameters:
    transcription (str): The transcribed text.
    output_path (str): Path to the file where the transcription text will be appended.
    """
    try:
        with open(output_path, 'a', encoding='utf-8') as file:
            file.write(transcription + "\n\n")
        print(f"Transcription appended to {output_path} successfully.")
    except Exception as e:
        print(f"Error appending transcription to file: {str(e)}")
        raise

def main(video_path, audio_path, transcription_path):
    """
    Main function to extract audio from video, transcribe it, and append the transcription to a file.

    Parameters:
    video_path (str): Path to the video file.
    audio_path (str): Path where the extracted audio will be saved.
    transcription_path (str): Path where the transcription text will be appended.
    """
    repaired_video_path = video_path.replace(".mp4", "_fixed.mp4")
    
    # Inspect the video file
    print("Inspecting video file...")
    inspect_video(video_path)
    
    # Repair the video file if necessary
    print("Repairing video file if necessary...")
    repair_video(video_path, repaired_video_path)
    
    # Extract audio from the repaired video
    extract_audio(repaired_video_path, audio_path)
    
    # Transcribe audio
    transcription = transcribe_audio(audio_path)
    
    # Append transcription to file
    append_transcription_to_file(transcription, transcription_path)
    return transcription

if __name__ == "__main__":
    # Define paths to the video, audio, and transcription files
    video_path = 'F:/Programming/Python/Subtitle Generator/ExceptionsontheConsole.mp4'
    audio_path = 'F:/Programming/Python/Subtitle Generator/ExceptionsontheConsole.wav'
    transcription_path = 'F:/Programming/Python/Subtitle Generator/section_11.txt'
    
    # Ensure the directories for audio_path and transcription_path exist
    audio_dir = os.path.dirname(audio_path)
    if audio_dir and not os.path.exists(audio_dir):
        os.makedirs(audio_dir, exist_ok=True)

    transcription_dir = os.path.dirname(transcription_path)
    if transcription_dir and not os.path.exists(transcription_dir):
        os.makedirs(transcription_dir, exist_ok=True)
    
    # Run the main function
    try:
        transcription = main(video_path, audio_path, transcription_path)
    except Exception as e:
        print(f"An error occurred: {e}")