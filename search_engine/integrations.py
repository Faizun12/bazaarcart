import httpx
import asyncio

async def fetch_fakestore_api(query: str) -> list:
    url = "https://fakestoreapi.com/products"
    results = []
    try:
        async with httpx.AsyncClient() as client:
            # FakeStore API doesn't have a direct search endpoint, so we fetch all and filter in memory
            # For a real store, we would use their search endpoint.
            response = await client.get(url, timeout=3.0)
            response.raise_for_status()
            products = response.json()
            
            for item in products:
                if query.lower() in item.get('title', '').lower() or query.lower() in item.get('description', '').lower():
                    results.append({
                        'id': f"fs_{item['id']}",
                        'title': item['title'],
                        'price': item['price'],
                        'currency': '$',
                        'store_name': 'FakeStore',
                        'image_url': item['image'],
                        'product_url': '#',
                        'rating': item.get('rating', {}).get('rate', 0.0)
                    })
    except Exception as e:
        print(f"FakeStoreAPI error: {e}")
    return results

async def fetch_dummyjson_api(query: str) -> list:
    url = f"https://dummyjson.com/products/search?q={query}"
    results = []
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=3.0)
            response.raise_for_status()
            data = response.json()
            products = data.get('products', [])
            
            for item in products:
                results.append({
                    'id': f"dj_{item['id']}",
                    'title': item['title'],
                    'price': item['price'],
                    'currency': '$',
                    'store_name': 'DummyJSON',
                    'image_url': item['thumbnail'],
                    'product_url': '#',
                    'rating': item.get('rating', 0.0)
                })
    except Exception as e:
        print(f"DummyJSON error: {e}")
    return results

async def fetch_mock_bazaar_api(query: str) -> list:
    # A mocked internal store that just simulates some delay and returns mock data
    await asyncio.sleep(0.5)
    mock_db = [
        {"id": 101, "title": "Bazaar Ultra HD TV 55 inch", "price": 450.00, "image": "https://dummyjson.com/image/400x400/282828?text=TV"},
        {"id": 102, "title": "Bazaar Wireless Headphones Pro", "price": 89.99, "image": "https://dummyjson.com/image/400x400/282828?text=Headphones"},
        {"id": 103, "title": "Bazaar Ergonomic Office Chair", "price": 120.00, "image": "https://dummyjson.com/image/400x400/282828?text=Chair"},
        {"id": 104, "title": "Bazaar Gaming Laptop RTX 4060", "price": 1099.99, "image": "https://dummyjson.com/image/400x400/282828?text=Laptop"},
    ]
    results = []
    for item in mock_db:
        if query.lower() in item['title'].lower():
            results.append({
                'id': f"bz_{item['id']}",
                'title': item['title'],
                'price': item['price'],
                'currency': '$',
                'store_name': 'Bazaar Exclusive',
                'image_url': item['image'],
                'product_url': '#',
                'rating': 4.8
            })
    return results

async def fetch_bestbuy_api(query: str) -> list:
    """
    EXAMPLE: How a real e-commerce API integration would look.
    Requires a real API Key from developer.bestbuy.com
    """
    API_KEY = "YOUR_BESTBUY_API_KEY_HERE"
    
    # If no real key is set, just return empty list so the app doesn't break
    if API_KEY == "YOUR_BESTBUY_API_KEY_HERE":
        return []
        
    url = f"https://api.bestbuy.com/v1/products((search={query}))?apiKey={API_KEY}&sort=regularPrice.asc&show=sku,name,regularPrice,image,url,customerReviewAverage&format=json"
    results = []
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=3.0)
            response.raise_for_status()
            data = response.json()
            products = data.get('products', [])
            
            for item in products:
                results.append({
                    'id': f"bb_{item['sku']}",
                    'title': item['name'],
                    'price': item['regularPrice'],
                    'currency': '$',
                    'store_name': 'BestBuy',
                    'image_url': item['image'],
                    'product_url': item['url'],
                    'rating': item.get('customerReviewAverage', 0.0)
                })
    except Exception as e:
        print(f"BestBuy error: {e}")
    return results

async def search_all_stores(query: str, min_price: str = '', max_price: str = '', brand: str = '') -> list:
    # Fan-out to all stores concurrently using asyncio.gather
    # If one store fails, the others will still complete successfully thanks to try-except blocks inside each fetch
    results = await asyncio.gather(
        fetch_fakestore_api(query),
        fetch_dummyjson_api(query),
        fetch_mock_bazaar_api(query),
        fetch_bestbuy_api(query), # <--- Just drop the new function here!
    )
    
    # Flatten the list of lists
    flat_results = [item for sublist in results for item in sublist]
    
    # Apply filters
    filtered_results = []
    
    min_p = float(min_price) if min_price else 0.0
    max_p = float(max_price) if max_price else float('inf')
    b_lower = brand.lower() if brand else ''
    
    for item in flat_results:
        price = float(item.get('price', 0))
        
        # Check price range
        if price < min_p or price > max_p:
            continue
            
        # Check brand (simplified: look for brand name in title)
        if b_lower and b_lower not in item.get('title', '').lower():
            continue
            
        filtered_results.append(item)
    
    # Sort results by price (ascending) as a default aggregation strategy
    filtered_results.sort(key=lambda x: x['price'])
    
    return filtered_results
