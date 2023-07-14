from Song.emotion import get_max_emotion
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_audioclips
import os
from moviepy.editor import AudioFileClip
from moviepy.video import fx


from moviepy.video.compositing.concatenate import concatenate_videoclips

from PIL import Image, ImageDraw, ImageFont




def generatevideo(lyrics,language):
    if language=='en' or language=='es':
        font_path = "static/Courgette-Regular.ttf"
    elif language=='hi':
        font_path = "static/TiroDevanagariHindi-Italic.ttf"
    else:
        font_path = "static/Orbit-Regular.ttf"
        
        
    emotion_index=get_max_emotion(lyrics)
    if emotion_index in [3,4,5,9]:
        background_music_path = f"soft.mp3"
        
    else:
        background_music_path = f"hard.mp3"    
        
    
    output_fps = 30
    output_duration = 4  # in seconds
    background_image_path = f"static/videoimage/bg{emotion_index}.png"
    background_image = cv2.imread(background_image_path)

    # Get the dimensions of the background image
    output_height, output_width, _ = background_image.shape

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter('lyrical2_video.mp4', fourcc, output_fps, (output_width, output_height))
    
   
      # Replace with your Hindi font path
    font_size = 60
    font = ImageFont.truetype(font_path, font_size)

    # Create PIL draw object
    
    

    # Generate video frames with lyrics
    lyrics_duration = len(lyrics) * output_duration
  
 
    for row in lyrics:
        # Create a black background image
        frame = np.zeros((output_height, output_width, 3), dtype=np.uint8)
        pil_image = Image.fromarray(cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        # Add the text to the frame for each column in the row
        for i, line in enumerate(row):
            # Calculate the position to center the text
            
            text_size = draw.textsize(line, font=font)
            text_x = int((output_width - text_size[0]) / 2)
            text_y = int((output_height - text_size[1]) / 3) +i*100
            
            draw.text((text_x, text_y), line, font=font, fill=(255, 255, 255))

        # Convert PIL image back to OpenCV format
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            # Add the text to the frame
        
        #  Write the frame to the output video
        for _ in range(output_duration * output_fps):  # Repeat the frame for a certain duration
            output_video.write(frame)
        
       

    # Release the video writer
    output_video.release()

    # Repeat the background music to match the duration of the lyrics
    background_music = AudioFileClip(background_music_path)
    if background_music.duration < lyrics_duration:
        num_repeats = int(np.ceil(lyrics_duration / background_music.duration))
        repeated_music = [background_music] * num_repeats

# Concatenate the repeated background music clips
        background_music = concatenate_audioclips(repeated_music)

    lyrical_video = VideoFileClip('lyrical2_video.mp4')
    lyrical_video = lyrical_video.set_duration(lyrics_duration)
    lyrical_video = lyrical_video.set_fps(output_fps)
    lyrical_video = lyrical_video.set_audio(background_music)
    output_video_path_final = 'static/final2_lyrical_video.mp4'
    lyrical_video.write_videofile(output_video_path_final, codec='libx264', audio_codec='aac')
    
    os.remove('lyrical2_video.mp4')
    
    






