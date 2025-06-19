from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import logging
from typing import Dict, List, Optional
import json
import re
import os


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scraper:
    #Keep in mind the delay. The server is not actually slow.
    #It isslowing down to avoid captcha and "anti-scraping" behaviour
    def __init__(self, delay_range: tuple = (2, 4)):
        self.session = requests.Session()
        self.delay_range = delay_range
        
        #MIMIC THE BROWSER TO AVOID CAPCTHA
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        self.session.headers.update(self.headers)

    def avoid_captcha_delay(self):
        """Add random delay between requests"""
        delay = random.uniform(*self.delay_range)
        logger.debug(f"Waiting {delay:.2f} seconds...")
        time.sleep(delay)
    
    def fetch_page(self, url: str, max_retries: int = 3) -> Optional[BeautifulSoup]:
        for attempt in range(max_retries):
            try:
                self.avoid_captcha_delay()
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                logger.info(f"Successfully fetched {url}")
                return soup
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                
        logger.error(f"Failed to fetch {url} after {max_retries} attempts")
        return None
    
    def extract_product_info(self, soup: BeautifulSoup) -> Dict[str, any]:
        """
        Extract product information with multiple fallback selectors
        """
        product_data = {}
        
        # Title extraction with multiple selectors
        title_selectors = [
            '#productTitle',
            '.product-title',
            'h1[data-automation-id="product-title"]',
            'h1.a-size-large'
        ]
        
        product_data['title'] = self._extract_text_by_selectors(soup, title_selectors)
        
        # Price extraction (Amazon has many price formats)
        price_selectors = [
            '.a-price-whole',
            '.a-price .a-offscreen',
            '[data-testid="price-current"]',
            '.a-price-current',
            '.a-color-price'
        ]
        
        product_data['price'] = self._extract_text_by_selectors(soup, price_selectors)
        
        # Rating
        rating_selectors = [
            '.a-icon-alt',
            '[data-hook="rating-out-of-text"]',
            '.a-star-mini .a-icon-alt'
        ]
        
        rating_text = self._extract_text_by_selectors(soup, rating_selectors)
        if rating_text:
            # Extract number from rating text
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            product_data['rating'] = rating_match.group(1) if rating_match else None
        
        # Availability
        availability_selectors = [
            '#availability span',
            '.a-color-success',
            '.a-color-state',
            '[data-testid="availability"]'
        ]
        
        product_data['availability'] = self._extract_text_by_selectors(soup, availability_selectors)
        
        # Feature bullets/highlights
        bullets = []
        bullet_selectors = [
            '#feature-bullets ul li span',
            '.a-unordered-list .a-list-item',
            '[data-testid="feature-bullets"] li'
        ]
        
        for selector in bullet_selectors:
            elements = soup.select(selector)
            if elements:
                bullets = [elem.get_text(strip=True) for elem in elements[:5]]  # Limit to 5
                break
        
        product_data['features'] = [b for b in bullets if b and len(b) > 10]
        
        # Images (this is complex and may break easily)
        try:
            product_data['images'] = self._extract_images(soup)
        except Exception as e:
            logger.warning(f"Image extraction failed: {e}")
            product_data['images'] = []
        
        return product_data
    
    def _extract_text_by_selectors(self, soup: BeautifulSoup, selectors: List[str]) -> Optional[str]:
        """Try multiple selectors and return first match"""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text:
                    return text
        return None
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract product images (fragile - Amazon changes this frequently)"""
        images = []
        
        # Method 1: JSON data in script tags
        script_tags = soup.find_all('script', string=re.compile(r'ImageBlockATF|colorImages'))
        for script in script_tags:
            try:
                # This is very fragile and Amazon-specific
                json_match = re.search(r'colorImages[\'"]:\s*(\[.*?\])', script.string)
                if json_match:
                    image_data = json.loads(json_match.group(1))
                    for img in image_data:
                        if isinstance(img, dict) and 'large' in img:
                            images.append(img['large'])
                    break
            except (json.JSONDecodeError, KeyError):
                continue
        
        # Method 2: Image tags (fallback)
        if not images:
            img_tags = soup.select('#landingImage, .a-dynamic-image, [data-testid="product-image"]')
            for img in img_tags[:5]:  # Limit results
                src = img.get('src') or img.get('data-src')
                if src and src.startswith('http'):
                    images.append(src)
        
        return list(set(images))  # Remove duplicates
    
    def save_images(self, image_urls: List[str], folder_path: str) -> List[str]:
        """Download and save product images"""
        saved_files = []
 
        if not image_urls:
            return saved_files
        
        images_folder = os.path.join(folder_path, "images")
        os.makedirs(images_folder, exist_ok=True)
        
        for i, url in enumerate(image_urls):
            try:
                self.avoid_captcha_delay()  # Be respectful when downloading images
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                # Get file extension from URL or default to jpg
                ext = url.split('.')[-1].split('?')[0] if '.' in url else 'jpg'
                if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                    ext = 'jpg'
                
                filename = f"image_{i+1:02d}.{ext}"
                filepath = os.path.join(images_folder, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                saved_files.append(filepath)
                logger.info(f"Saved image: {filename}")
                
            except Exception as e:
                logger.error(f"Failed to download image {url}: {e}")
                continue
        
        return saved_files

def save_product_data(product_info: Dict, url: str) -> str:
    # Create folder name based on product title or timestamp
    title = product_info.get('title', 'Unknown Product')
    safe_title = re.sub(r'[^\w\s-]', '', title)[:50]  # Remove special chars, limit length
    safe_title = re.sub(r'[-\s]+', '_', safe_title)  # Replace spaces/dashes with underscores
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{safe_title}" if safe_title else f"product_{timestamp}"
    
    # Create  folder
    base_folder = "scraped_products"
    product_folder = os.path.join(base_folder, folder_name)
    os.makedirs(product_folder, exist_ok=True)
    
    # Save product info as JSON
    json_path = os.path.join(product_folder, "product_info.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(product_info, f, indent=2, ensure_ascii=False)
    
    # Save product info as readable text
    txt_path = os.path.join(product_folder, "product_summary.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"Product Information Summary\n")
        f.write(f"=" * 50 + "\n")
        f.write(f"Scraped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Source URL: {url}\n\n")
        
        for key, value in product_info.items():
            if key == 'images':
                continue  # Handle images separately
            
            f.write(f"{key.upper().replace('_', ' ')}:\n")
            f.write("-" * 20 + "\n")
            
            if value:
                if isinstance(value, list):
                    for i, item in enumerate(value, 1):
                        f.write(f"{i}. {item}\n")
                else:
                    f.write(f"{value}\n")
            else:
                f.write("Not found\n")
            f.write("\n")
    
    # Save metadata
    metadata_path = os.path.join(product_folder, "metadata.txt")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write(f"Scraping Metadata\n")
        f.write(f"=" * 30 + "\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Source URL: {url}\n")
        f.write(f"Product Title: {title}\n")
        f.write(f"Images Found: {len(product_info.get('images', []))}\n")
        f.write(f"Features Count: {len(product_info.get('features', []))}\n")
        f.write(f"\nFolder Structure:\n")
        f.write(f"├── product_info.json (structured data)\n")
        f.write(f"├── product_summary.txt (human-readable)\n")
        f.write(f"├── metadata.txt (this file)\n")
        f.write(f"└── images/ (downloaded product images)\n")
    
    return product_folder


def scrape_page(url):
    
    scraper = Scraper()

    print(f"Target URL: {url}\n")
    
    # Fetch the page
    soup = scraper.fetch_page(url)
    
    if not soup:
        print("Could not to fetch the page. (Invalid URL or Captcha)")
        return
    
    # Extract product information
    product_info = scraper.extract_product_info(soup)
    
    # Save all product data to files
    print("Saving product data to folder")
    try:
        product_folder = save_product_data(product_info, url)
        print(f"Product data saved to: {product_folder}")
        
        # Download and save images
        if product_info.get('images'):
            print(f"Downloading {len(product_info['images'])} images...")
            saved_images = scraper.save_images(product_info['images'], product_folder)
            print(f"{len(saved_images)} images downloaded successfully")
            
            # Update the metadata with actual saved images
            metadata_path = os.path.join(product_folder, "metadata.txt")
            with open(metadata_path, 'a', encoding='utf-8') as f:
                f.write(f"\nActual Images Downloaded: {len(saved_images)}\n")
                for img_path in saved_images:
                    f.write(f"  • {os.path.basename(img_path)}\n")
        else:
            print("No images found to download")
        print('')
        return product_folder
            
    except Exception as e:
        print(f"Error saving data: {e}")
        logger.error(f"Failed to save product data: {e}")
        return None
