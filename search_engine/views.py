from django.shortcuts import render
from django.http import JsonResponse
from .integrations import search_all_stores

def index(request):
    """
    Renders the main search interface.
    """
    return render(request, 'search_engine/index.html')

def bazaar_store(request, product_id):
    """
    Mock website for Bazaar Exclusive products.
    """
    return render(request, 'search_engine/bazaar_store.html', {'product_id': product_id})

import httpx
from bs4 import BeautifulSoup
import urllib.parse

async def web_details(request):
    """
    Scrapes an external URL and renders its text content natively inside Bazaarcart.
    """
    target_url = request.GET.get('url', '')
    if not target_url:
        return render(request, 'search_engine/web_details.html', {'error': 'No URL provided.'})
        
    try:
        # Decode URL just in case
        target_url = urllib.parse.unquote(target_url)
        
        async with httpx.AsyncClient(headers={'User-Agent': 'Mozilla/5.0'}) as client:
            response = await client.get(target_url, timeout=5.0, follow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else "External Page"
            
            # Extract main paragraphs to simulate "reading" the page natively
            paragraphs = soup.find_all('p')
            content = [p.text for p in paragraphs if len(p.text.strip()) > 20]
            
            # If no paragraphs found, just get raw text snippet
            if not content:
                raw_text = soup.get_text(separator='\n', strip=True)
                content = [raw_text[:1000] + "..."]
                
            return render(request, 'search_engine/web_details.html', {
                'title': title,
                'content': content[:15], # Limit to first 15 paragraphs
                'original_url': target_url
            })
            
    except Exception as e:
        return render(request, 'search_engine/web_details.html', {
            'error': f"Failed to load content from {target_url}. It might be protected.",
            'original_url': target_url
        })

async def api_search(request):
    """
    Async endpoint that takes a search query and returns aggregated JSON results.
    """
    query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    brand = request.GET.get('brand', '').strip()
    
    if not query:
        return JsonResponse({'results': [], 'count': 0, 'query': query})
    
    # Perform the fan-out search across multiple APIs concurrently
    results = await search_all_stores(query, min_price, max_price, brand)
    
    return JsonResponse({
        'results': results,
        'count': len(results),
        'query': query
    })
