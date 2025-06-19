import json
import os
from pathlib import Path
import re
from dotenv import load_dotenv
from google import genai

def get_scripts_from_LLM():

    raw_llm_response = get_LLM_response()
    print(raw_llm_response)
    print('='*50)
    try:
        cleaned_llm_response_json=re.search(
            r'(\{.*\})',
            raw_llm_response, 
            re.DOTALL
            ).group(1)
        print(cleaned_llm_response_json)

    except Exception as e:
        print('Response not in json format', e)
    
    #The values are the scripts
    return cleaned_llm_response_json.values()

def get_LLM_response():

    load_dotenv()
    client = genai.Client(api_key=os.environ.get('API_KEY'))
    
    prompt = generate_prompt()
    response = client.models.generate_content(
        model='gemini-2.0-flash-lite',
        contents=prompt
    )
    return response.text
    

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
    return prompt

get_scripts_from_LLM()

   