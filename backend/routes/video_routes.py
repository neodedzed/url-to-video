from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

video_router = APIRouter()

@video_router.get('/')
def get_video(product: str=None):
    # video_path = Path(f'./scraped_products/{product}/output.mp4')

    BASE_DIR = Path(__file__).resolve().parent.parent  # → backend/
    video_path = BASE_DIR / 'scraped_products' / product / 'output.mp4'
    def stream_video():
        with open(video_path, 'rb') as video:
            yield from video
    
    return StreamingResponse(stream_video(), media_type='video/mp4')