from django.shortcuts import render
from django.http import JsonResponse
from .integrations import search_all_stores

def index(request):
    """
    Renders the main search interface.
    """
    return render(request, 'search_engine/index.html')

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
