from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import scraper_routes, video_routes

backend = FastAPI()

backend.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_headers=['*'],
    allow_methods=['*'],
    allow_credentials=['*'],

)

backend.include_router(scraper_routes.scraper_router, prefix='/scraper')
backend.include_router(video_routes.video_router, prefix='/video')
