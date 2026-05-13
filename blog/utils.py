import requests
import os
import json

def get_country_info(country_name):
    """
    Fetch country information from restcountries.com API.
    If the input is a city or state, resolves it to the correct country using Nominatim.
    """
    if not country_name:
        return None
        
    def fetch_from_restcountries(name):
        try:
            url = f"https://restcountries.com/v3.1/name/{name}?fullText=true"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()[0]
                return {
                    'name': data.get('name', {}).get('common', name),
                    'flag_url': data.get('flags', {}).get('png', ''),
                    'capital': data.get('capital', ['N/A'])[0],
                    'population': f"{data.get('population', 0):,}",
                    'region': data.get('region', 'N/A'),
                }
            else:
                # Fallback if fullText fails, try partial match
                url = f"https://restcountries.com/v3.1/name/{name}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()[0]
                    return {
                        'name': data.get('name', {}).get('common', name),
                        'flag_url': data.get('flags', {}).get('png', ''),
                        'capital': data.get('capital', ['N/A'])[0],
                        'population': f"{data.get('population', 0):,}",
                        'region': data.get('region', 'N/A'),
                    }
        except Exception as e:
            print(f"Error fetching country info for {name}: {e}")
        return None

    # First attempt: direct search
    result = fetch_from_restcountries(country_name)
    if result:
        return result
        
    # Second attempt: Geocode the input to find the country name
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={country_name}&format=json&addressdetails=1&limit=1"
        headers = {'User-Agent': 'AIGlobalBlog/1.0'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            results = response.json()
            if results and len(results) > 0:
                resolved_country = results[0].get('address', {}).get('country')
                if resolved_country and resolved_country.lower() != country_name.lower():
                    print(f"Resolved '{country_name}' to country '{resolved_country}'. Fetching country data...")
                    return fetch_from_restcountries(resolved_country)
    except Exception as e:
        print(f"Error resolving country via Nominatim: {e}")
        
    return None

def generate_cover_image(title):
    """
    Smart AI Generation:
    1. Fetches a summary of the topic from Wikipedia.
    2. Passes the summary to Hugging Face FLUX.1-schnell model to generate a highly accurate image.
    """
    fallback_image = "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?q=80&w=1000&auto=format&fit=crop"
    
    hf_token = os.environ.get('HUGGINGFACE_API_KEY')
    if not hf_token:
        print("No HUGGINGFACE_API_KEY set. Returning placeholder.")
        return fallback_image
        
    if not title:
        return fallback_image

    headers = {'User-Agent': 'AIGlobalBlog/1.0'}
    summary = ""
    
    try:
        # Step 1: Search Wikipedia for the best matching article title
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={title}&format=json"
        search_response = requests.get(search_url, headers=headers, timeout=5)
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            search_results = search_data.get('query', {}).get('search', [])
            
            if search_results:
                wiki_title = search_results[0]['title']
                
                # Step 2: Fetch the summary (extract) of that article
                extract_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=3&exlimit=1&titles={wiki_title}&explaintext=1&formatversion=2&format=json"
                extract_response = requests.get(extract_url, headers=headers, timeout=5)
                
                if extract_response.status_code == 200:
                    pages = extract_response.json().get('query', {}).get('pages', [])
                    if pages:
                        summary = pages[0].get('extract', '').strip()
    except Exception as e:
        print(f"Error fetching Wikipedia summary: {e}")
        
    # Step 3: Generate the image using Hugging Face
    API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    hf_headers = {"Authorization": f"Bearer {hf_token}"}
    
    # We create a highly descriptive prompt using the Wikipedia summary
    prompt = f"A beautiful, high quality photograph of: {title}."
    if summary:
        # Truncate summary if too long, usually AI prompts are better < 500 chars
        prompt += f" Context: {summary[:400]}. Highly detailed, award winning photography."
    else:
        prompt += " Digital art, beautiful lighting, highly detailed."
        
    try:
        response = requests.post(API_URL, headers=hf_headers, json={"inputs": prompt}, timeout=60)
        if response.status_code == 200:
            import uuid
            from django.conf import settings
            
            filename = f"cover_{uuid.uuid4().hex[:8]}.png"
            media_dir = os.path.join(settings.BASE_DIR, 'media', 'covers')
            os.makedirs(media_dir, exist_ok=True)
            
            filepath = os.path.join(media_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            return f"{settings.MEDIA_URL}covers/{filename}"
        else:
            print(f"Hugging Face API Error: {response.text}")
    except Exception as e:
        print(f"Error generating image: {e}")
        
    return fallback_image

def analyze_sentiment(text):
    """
    Analyze comment sentiment using Hugging Face Inference API.
    Returns 'Positive', 'Neutral', or 'Negative'.
    """
    if not text:
        return 'Neutral'
        
    hf_token = os.environ.get('HUGGINGFACE_API_KEY')
    if not hf_token:
        print("No HUGGINGFACE_API_KEY set. Defaulting to Neutral.")
        return 'Neutral'

    API_URL = "https://router.huggingface.co/hf-inference/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=10)
        if response.status_code == 200:
            results = response.json()
            # API returns a list of lists, e.g., [[{'label': 'positive', 'score': 0.9}, ...]]
            if isinstance(results, list) and len(results) > 0:
                predictions = results[0]
                # Sort by score
                best_prediction = max(predictions, key=lambda x: x['score'])
                label = best_prediction['label'].lower()
                
                if 'positive' in label:
                    return 'Positive'
                elif 'negative' in label:
                    return 'Negative'
                else:
                    return 'Neutral'
        else:
            print(f"Hugging Face API Error: {response.text}")
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        
    return 'Neutral'
