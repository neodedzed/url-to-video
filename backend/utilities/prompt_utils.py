import json
import os
from pathlib import Path
import re
from dotenv import load_dotenv
from google import genai

def get_scripts_from_LLM(product_folder):

    raw_llm_response = get_LLM_response(product_folder)
    # print(raw_llm_response)
    # print('='*50)
    try:
        cleaned_llm_response=re.search(
            r'(\{.*\})',
            raw_llm_response, 
            re.DOTALL
            ).group(1)
        
        #COnvert to Json
        cleaned_llm_response_json = json.loads(cleaned_llm_response)
        print(cleaned_llm_response_json)
        print(type(cleaned_llm_response_json))
        print(list(cleaned_llm_response_json.values()))

    except Exception as e:
        print('Response not in json format', e)
    
    #The values are the scripts
    return list(cleaned_llm_response_json.values())

def get_LLM_response(product_folder):

    load_dotenv()
    client = genai.Client(api_key=os.environ.get('API_KEY'))
    
    prompt = generate_prompt(product_folder)
    response = client.models.generate_content(
        model='gemini-2.0-flash-lite',
        contents=prompt
    )
    return response.text
    

def generate_prompt(product_folder):

    path_to_product = f'./{product_folder}/' 
    prompt_template = Path('./assets/prompt_template.md').read_text()

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

# get_scripts_from_LLM()

   