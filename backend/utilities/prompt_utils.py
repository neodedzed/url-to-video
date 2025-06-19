import json
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

def get_LLM_response():

    load_dotenv()
    client = genai.Client(api_key=os.environ.get('API_KEY'))
    
    prompt = generate_prompt()
    response = client.models.generate_content(
        model='gemini-2.0-flash-lite',
        contents=prompt
    )
    print('='*50)
    print(response.text)
    

def generate_prompt(
    product = 'HP_OmniBook_X_Laptop_Snapdragon_X_Elite_X1E_78_100_20250619_102246'
):
    path_to_product = f'../scraped_products/{product}/' 
    prompt_template = Path('../assets/prompt_template.md').read_text()

    product_summary = Path(path_to_product + 'product_summary.txt').read_text()
    product_info = json.loads(
        Path(path_to_product + 'product_info.json').read_text()
        )

    prompt = prompt_template.format(
        product_summary=product_summary.strip(),
        features='\n'.join(f"- {f}" for f in product_info["features"]),
        price=product_info["price"],
        rating=product_info["rating"],
        availability=product_info["availability"] 
    )
    print(prompt)
    return prompt

get_LLM_response()

   