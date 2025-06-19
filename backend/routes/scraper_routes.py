from fastapi import APIRouter

scraper_router = APIRouter()

@scraper_router.post('/')
def post_url_for_scraping(url: str):
    print(url)
    return {
        'message' : 'processing'
    }
