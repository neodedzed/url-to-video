from moviepy import ImageClip, concatenate_videoclips
from pathlib import Path

def create_clips(product='HP_OmniBook_X_Laptop_Snapdragon_X_Elite_X1E_78_100_20250619_102246'):
    images = list(Path(f'../scraped_products/{product}/images/').iterdir())

    print(images)
    clips = [ImageClip(img).with_duration(3) for img in images]

    video = concatenate_videoclips(clips, method='compose')

    video.write_videofile(f'../scraped_products/{product}/output.mp4', fps=30)

create_clips()