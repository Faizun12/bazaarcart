import httpx
import asyncio
import urllib.parse
import re
from bs4 import BeautifulSoup

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
                        'product_url': f"https://fakestoreapi.com/products/{item['id']}",
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
                    'product_url': f"https://dummyjson.com/products/{item['id']}",
                    'rating': item.get('rating', 0.0)
                })
    except Exception as e:
        print(f"DummyJSON error: {e}")
    return results

async def get_real_image(query: str, index: int = 0) -> str:
    """Helper to fetch a real product image from DummyJSON based on the query."""
    url = f"https://dummyjson.com/products/search?q={query}"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=2.0)
            if resp.status_code == 200:
                products = resp.json().get('products', [])
                if products:
                    # Pick an image based on index, loop around if not enough products
                    return products[index % len(products)]['thumbnail']
    except Exception:
        pass
    return f"https://dummyjson.com/image/400x400/282828?text={urllib.parse.quote(query)}"

async def fetch_mock_bazaar_api(query: str) -> list:
    # A mocked internal store that just simulates some delay and returns mock data
    await asyncio.sleep(0.5)
    mock_db = [
        {"id": 101, "title": "Bazaar Ultra HD TV 55 inch", "price": 450.00, "image_query": "tv"},
        {"id": 102, "title": "Bazaar Wireless Headphones Pro", "price": 89.99, "image_query": "headphones"},
        {"id": 103, "title": "Bazaar Ergonomic Office Chair", "price": 120.00, "image_query": "chair"},
        {"id": 104, "title": "Bazaar Gaming Laptop RTX 4060", "price": 1099.99, "image_query": "laptop"},
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
                'image_url': await get_real_image(item['image_query'], 0),
                'product_url': f"/store/bazaar/{item['id']}/",
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

import random

async def fetch_amazon_api(query: str, min_price: str, max_price: str, brand: str) -> list:
    """
    Simulates fetching products from Amazon Product Advertising API.
    For the hackathon, we generate targeted cards that link directly to Amazon.
    """
    await asyncio.sleep(0.4)
    results = []
    
    search_terms = [brand, query] if brand else [query]
    base_q = "+".join(search_terms).replace(' ', '+')
    
    # Generate a random price within the user's budget to look realistic
    min_p = float(min_price) if min_price else 50.0
    max_p = float(max_price) if max_price else min_p + 500.0
    simulated_price = round(random.uniform(min_p, min_p + (max_p - min_p) * 0.5), 2)
    
    # Construct real Amazon Search URL with price filters
    amazon_url = f"https://www.amazon.com/s?k={base_q}"
    if min_price or max_price:
        # Amazon uses cents for price filters: p_36:min-max
        min_cents = int(min_p * 100)
        max_cents = int(max_p * 100)
        amazon_url += f"&rh=p_36%3A{min_cents}-{max_cents}"
        
    title = f"{brand.title()} {query.title()} - Premium Edition" if brand else f"Top Rated {query.title()}"
    
    image_url = await get_real_image(query, 0)
    
    results.append({
        'id': f"amz_1",
        'title': title,
        'price': simulated_price,
        'currency': '$',
        'store_name': 'Amazon',
        'image_url': image_url,
        'product_url': amazon_url,
        'rating': 4.7
    })
    
    return results

async def fetch_alibaba_api(query: str, min_price: str, max_price: str, brand: str) -> list:
    """
    Simulates fetching products from Alibaba API.
    """
    await asyncio.sleep(0.6)
    results = []
    
    search_terms = [brand, query] if brand else [query]
    base_q = "+".join(search_terms).replace(' ', '+')
    
    min_p = float(min_price) if min_price else 10.0
    max_p = float(max_price) if max_price else min_p + 100.0
    # Alibaba is usually cheaper (wholesale)
    simulated_price = round(random.uniform(min_p, min_p + (max_p - min_p) * 0.3), 2)
    
    alibaba_url = f"https://www.alibaba.com/trade/search?SearchText={base_q}"
    
    title = f"Wholesale {brand.title()} {query.title()} Bulk" if brand else f"Factory Direct {query.title()}"
    
    image_url = await get_real_image(query, 1)
    
    results.append({
        'id': f"ali_1",
        'title': title,
        'price': simulated_price,
        'currency': '$',
        'store_name': 'Alibaba',
        'image_url': image_url,
        'product_url': alibaba_url,
        'rating': 4.5
    })
    
    return results

async def fetch_daraz_api(query: str, min_price: str, max_price: str, brand: str) -> list:
    """Simulates fetching products from Daraz."""
    await asyncio.sleep(0.3)
    results = []
    
    search_terms = [brand, query] if brand else [query]
    base_q = "+".join(search_terms).replace(' ', '+')
    
    min_p = float(min_price) if min_price else 20.0
    max_p = float(max_price) if max_price else min_p + 200.0
    simulated_price = round(random.uniform(min_p, min_p + (max_p - min_p) * 0.4), 2)
    
    daraz_url = f"https://www.daraz.com.bd/catalog/?q={base_q}"
    title = f"{brand.title()} {query.title()} - Daraz Mall" if brand else f"Authentic {query.title()} (Local)"
    image_url = await get_real_image(query, 2)
    
    results.append({
        'id': f"daraz_1",
        'title': title,
        'price': simulated_price,
        'currency': '$',
        'store_name': 'Daraz',
        'image_url': image_url,
        'product_url': daraz_url,
        'rating': 4.3
    })
    return results

async def fetch_ebay_api(query: str, min_price: str, max_price: str, brand: str) -> list:
    """Simulates fetching products from eBay."""
    await asyncio.sleep(0.5)
    results = []
    
    search_terms = [brand, query] if brand else [query]
    base_q = "+".join(search_terms).replace(' ', '+')
    
    min_p = float(min_price) if min_price else 15.0
    max_p = float(max_price) if max_price else min_p + 150.0
    simulated_price = round(random.uniform(min_p, min_p + (max_p - min_p) * 0.6), 2)
    
    ebay_url = f"https://www.ebay.com/sch/i.html?_nkw={base_q}"
    title = f"Pre-Owned {brand.title()} {query.title()}" if brand else f"Vintage {query.title()} - Free Shipping"
    image_url = await get_real_image(query, 3)
    
    results.append({
        'id': f"ebay_1",
        'title': title,
        'price': simulated_price,
        'currency': '$',
        'store_name': 'eBay',
        'image_url': image_url,
        'product_url': ebay_url,
        'rating': 4.1
    })
    return results

async def fetch_startech_api(query: str, min_price: str, max_price: str, brand: str) -> list:
    """REAL LIVE SCRAPER for StarTech.com.bd!"""
    results = []
    
    search_terms = [brand, query] if brand else [query]
    base_q = "+".join(search_terms).replace(' ', '+')
    url = f"https://www.startech.com.bd/product/search?search={base_q}"
    
    try:
        async with httpx.AsyncClient(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}) as client:
            response = await client.get(url, timeout=6.0, follow_redirects=True)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('div', class_='p-item', limit=5)
                
                for idx, item in enumerate(items):
                    # Title and Link
                    title_elem = item.find('h4', class_='p-item-name')
                    if not title_elem: continue
                    a_tag = title_elem.find('a')
                    title = a_tag.text.strip() if a_tag else title_elem.text.strip()
                    href = a_tag.get('href') if a_tag else url
                    
                    # Image
                    img_elem = item.find('img')
                    img_url = img_elem.get('src') if img_elem else "https://via.placeholder.com/400x300?text=No+Image"
                    
                    # Price parsing (converting BDT to USD roughly)
                    price_elem = item.find('div', class_='p-item-price')
                    price_val = 0.0
                    if price_elem:
                        price_text = price_elem.text.replace(',', '')
                        match = re.search(r'\d+', price_text)
                        if match:
                            price_val = float(match.group())
                            price_val = round(price_val / 110.0, 2) # Rough BDT to USD conversion for sorting
                    
                    results.append({
                        'id': f"st_{idx}",
                        'title': title,
                        'price': price_val,
                        'currency': '$', # Normalized
                        'store_name': 'StarTech (LIVE)',
                        'image_url': img_url,
                        'product_url': href,
                        'rating': 4.9
                    })
    except Exception as e:
        print(f"StarTech Scraper error: {e}")
        
    return results

async def search_all_stores(query: str, min_price: str = '', max_price: str = '', brand: str = '') -> list:
    # Fan-out to all stores concurrently using asyncio.gather
    # If one store fails, the others will still complete successfully thanks to try-except blocks inside each fetch
    results = await asyncio.gather(
        fetch_fakestore_api(query),
        fetch_dummyjson_api(query),
        fetch_mock_bazaar_api(query),
        fetch_bestbuy_api(query), 
        fetch_amazon_api(query, min_price, max_price, brand),
        fetch_alibaba_api(query, min_price, max_price, brand),
        fetch_daraz_api(query, min_price, max_price, brand),
        fetch_ebay_api(query, min_price, max_price, brand),
        fetch_startech_api(query, min_price, max_price, brand)
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
            if 'StarTech' not in item.get('store_name', ''):
                continue
            
        filtered_results.append(item)
    
    # Sort results by price (ascending) as a default aggregation strategy
    filtered_results.sort(key=lambda x: x['price'])
    
    return filtered_results
