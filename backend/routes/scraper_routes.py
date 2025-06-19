from fastapi import APIRouter

from routes.models.url import ScrapeUrl
from utilities.prompt_utils import get_scripts_from_LLM
from utilities.scraper_utils import scrape_page

scraper_router = APIRouter()

@scraper_router.post('/')
def post_url_for_scraping(urlData: ScrapeUrl):
   
    #Send to scraper util
    product_folder = scrape_page(urlData.url)   
  
    if not product_folder: 
        return {
            'message' : 'Could not scrap URL',
            'product_folder': product_folder 
        }
    
    #Send to AI Util
    scripts = get_scripts_from_LLM()

    #Send to movie-stitching util
      