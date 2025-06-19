This prompt is in markdown format

# Ad Script Prompt for Product
## Context:
We are creating a video ad script for a product listed on Amazon.

## Product Summary:
{product_summary}

## Features:
{features}

## Price:
{price}

## Rating:
{rating} stars

## Availability:
{availability}

## Request:
Please generate two a 15-30 second persuasive script for a audio-only ad. The tone should be friendly, informative, and energetic. Use plain language. Mention the most important features naturally in the flow. End with a light call to action.

## Format:
Keep all the parts to be of a the script in a single flow. The narration should be in the JSON format:
    {{
        'Narration 1' : (Script 1) 
        'Narration 2' : (Sctipt 2) 
    }}

The (Script) part of the JSON object above should only contain the monologue that is to be spoken and nothing else. Below is an example output. The example is solely present to show the format of the output. Do not use the content of the example to generate the script.  

## Example Output
    {{
        'Narration' : "Hey there, tech enthusiasts! Ready to experience the future of laptops? Introducing the HP OmniBook X, now available on Amazon! This sleek laptop is packed with power. Imagine blazing-fast performance thanks to the Qualcomm Snapdragon X Elite processor. You get a stunning 14-inch 2.2K touchscreen display with anti-glare and Gorilla Glass, making everything look incredible. Multitasking is a breeze with 16GB of super-speedy memory and a massive 1TB solid-state drive. Plus, enjoy all-day productivity with its long battery life and get a 50% charge in just 45 minutes! It's got all the latest connectivity options including Wi-Fi 7, and a comfy, backlit keyboard. The HP OmniBook X is in stock now on Amazon and is rated 5.0 stars! Don't miss out! Visit Amazon today and get yours!",
        'Narration 2' : "Hey tech lovers! Get ready to level up your laptop game with the brand-new HP OmniBook X, available now on Amazon! This powerhouse is built for speed, featuring the cutting-edge Qualcomm Snapdragon X Elite processor for lightning-fast performance. The gorgeous 14-inch 2.2K touchscreen is protected by Gorilla Glass and designed with anti-glare tech—perfect for work or play. With 16GB of ultra-fast memory and a spacious 1TB SSD, multitasking and storage are effortless. Stay unplugged longer with impressive all-day battery life, and when you need a boost, you’ll get 50% charge in just 45 minutes. Equipped with Wi-Fi 7, a backlit keyboard, and top-tier reviews—this laptop is rated 5.0 stars on Amazon! Don’t wait—grab the HP OmniBook X today and experience the future of computing.",
        }}