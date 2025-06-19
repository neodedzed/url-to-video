from fastapi import APIRouter

from routes.models.url import ScrapeUrl
from utilities.scraper import scrape_page

scraper_router = APIRouter()

@scraper_router.post('/')
def post_url_for_scraping(urlData: ScrapeUrl):
    message = 'Could not scrape page'
    product_folder = scrape_page(urlData.url)   
    if(product_folder): message = 'Page scrapped successfully'
    return {
        'message' : message,
        'product_folder': product_folder 
    }
