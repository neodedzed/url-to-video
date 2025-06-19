from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
from pathlib import Path

def create_clips(
        product='HP_OmniBook_X_Laptop_Snapdragon_X_Elite_X1E_78_100_20250619_102246',
        audio_clip: AudioFileClip = None
        ):
    images = list(Path(f'../scraped_products/{product}/images/').iterdir())
    
    duration = 3
    if audio_clip:
        duration = audio_clip.duration / len(images)

    print(images)
    clips = [ken_burns_effect(img,1.1, duration) for img in images]

    video = concatenate_videoclips(clips, method='compose')

    video.write_videofile(f'../scraped_products/{product}/output.mp4', fps=30)

def ken_burns_effect(image, zooom=1.1, duration=3):
    clip = ImageClip(image)

    width, hieght = clip.size

    zoomed_image = clip.resized(zooom*clip.size)

    animated = zoomed_image.crop(
        x1=lambda t: int((zoomed_image.w - width) * t / duration),
        y1=lambda t: int((zoomed_image.h - hieght) * t / duration),
        x2=lambda t: int((zoomed_image.w - width) * t / duration + width),
        y2=lambda t: int((zoomed_image.h - hieght) * t / duration + hieght)
    ).set_duration(duration)

    return animated
