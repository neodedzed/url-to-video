from fastapi import APIRouter

from routes.models.product_path import ProductPath
from routes.models.url import ScrapeUrl
from utilities.prompt_utils import get_scripts_from_LLM
from utilities.scraper_utils import scrape_page
from utilities.video_utils import create_video

scraper_router = APIRouter()

@scraper_router.post('/', response_model=ProductPath)
def post_url_for_scraping(urlData: ScrapeUrl):
   
    #Send to scraper util
    product_folder = scrape_page(urlData.url)  
    product_name = product_folder.split('/')[1]
    print(f'Product scraped', product_name)
    if not product_folder: 
        return {
            'message' : 'Could not scrap URL',
            'product_folder': product_folder 
        }
    
    #Send to AI Util
    print('Generating Scripts. Please Wait...')
    scripts = get_scripts_from_LLM(product_folder)
    print('Scripts generated')

    #Send to movie-stitching util
    create_video(product_folder)

    return ProductPath(product=product_name) 