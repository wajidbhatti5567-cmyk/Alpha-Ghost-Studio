import time
import logging
from email_agent import get_latest_command, send_email_update
from story_engine import generate_script
from animation_engine import generate_scene_clip
from sound_engine import add_foley_and_music
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Setup Logging
logging.basicConfig(filename='studio_errors.log', level=logging.ERROR)

def run_with_retry(func, *args, retries=3):
    """Self-healing mechanism to retry failed operations."""
    for i in range(retries):
        try:
            return func(*args)
        except Exception as e:
            if i == retries - 1: raise e
            print(f"Attempt {i+1} failed, retrying... Error: {e}")
            time.sleep(5)

def run_production_pipeline(command_data):
    try:
        print(f"Producing: {command_data['episode_title']}")
        script = generate_script(command_data['theme'], command_data['duration'])
        
        clips = [VideoFileClip("assets/intro.mp4")]
        
        for scene in script['scenes']:
            # The agent will try to generate the scene up to 3 times if it fails
            clip = run_with_retry(generate_scene_clip, scene['prompt'])
            final_clip = add_foley_and_music(clip, scene['mood'])
            clips.append(final_clip)
            
        clips.append(VideoFileClip("assets/outro.mp4"))
        
        final_video = concatenate_videoclips(clips)
        final_video.write_videofile(f"AlphaGhost_{command_data['episode_num']}.mp4")
        return True
        
    except Exception as e:
        logging.error(f"Critical failure: {str(e)}")
        raise e

def main():
    print("Alpha Ghost Studio: System Online with Self-Healing.")
    while True:
        try:
            command = get_latest_command()
            if command:
                send_email_update("Status", "Production started automatically.")
                run_production_pipeline(command)
                send_email_update("Success", "Your episode is ready!")
        except Exception as e:
            print(f"Fatal error handled: {e}")
            send_email_update("Error", "System encountered an error but is recovering.")
        
        time.sleep(300) # Wait 5 minutes between checks

if __name__ == "__main__":
    main()
