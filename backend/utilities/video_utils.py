from moviepy import AudioFileClip, ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips
from pathlib import Path

def create_video(text_overlay: str ='Test', product_folder:str = None,audio_clip: AudioFileClip = None):
    if not product_folder: product_folder = 'scraped_products/test'
    images = list(Path(f'./{product_folder}/images/').iterdir())
    
    duration = 3
    if audio_clip:
        duration = audio_clip.duration / len(images)

    print(images, duration)
    # clips = [ken_burns_effect(img,1.1, duration) for img in images]
    clips = [ImageClip(img).with_duration(duration) for img in images]

    video = concatenate_videoclips(clips, method='compose')

    text_clip = TextClip(
        text=text_overlay, 
        color='white',
        bg_color='black', 
        font_size=10,
        vertical_align='bottom',
        horizontal_align='center',
        duration=video.duration,
        method='label'
        )
    # text_clip = text_clip.with_position(('center', 'bottom')).with_duration(video.duration)

    video.write_videofile(f'./{product_folder}/output.mp4', fps=30)

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

