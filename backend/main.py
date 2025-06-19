from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.scraper_routes import scraper_router

backend = FastAPI()

backend.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_headers=['*'],
    allow_methods=['*'],
    allow_credentials=['*'],

)

backend.include_router(scraper_router, prefix='/scraper')