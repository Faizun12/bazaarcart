document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const header = document.getElementById('main-header');
    const resultsArea = document.getElementById('results-area');
    const productsGrid = document.getElementById('products-grid');
    const loadingIndicator = document.getElementById('loading-indicator');
    const resultsTitle = document.getElementById('results-title');
    const resultsMeta = document.getElementById('results-meta');

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const query = searchInput.value.trim();
        if (!query) return;

        const minPrice = document.getElementById('min-price').value;
        const maxPrice = document.getElementById('max-price').value;
        const brand = document.getElementById('brand').value.trim();

        // UI State Updates
        header.classList.add('searched');
        resultsArea.classList.remove('hidden');
        productsGrid.innerHTML = '';
        resultsTitle.textContent = `Results for "${query}"`;
        resultsMeta.textContent = '';
        
        // Show loading
        loadingIndicator.classList.remove('hidden');

        try {
            // Build query params
            const params = new URLSearchParams({ q: query });
            if (minPrice) params.append('min_price', minPrice);
            if (maxPrice) params.append('max_price', maxPrice);
            if (brand) params.append('brand', brand);

            // Fetch from our Django backend fan-out endpoint
            const response = await fetch(`/api/search/?${params.toString()}`);
            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();
            
            // Hide loading
            loadingIndicator.classList.add('hidden');
            
            if (data.count === 0) {
                resultsMeta.textContent = '0 items found.';
                productsGrid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; color: var(--text-secondary); padding: 3rem;">
                        <h3>No products found.</h3>
                        <p>Try adjusting your search terms.</p>
                    </div>
                `;
                return;
            }

            resultsMeta.textContent = `${data.count} items found across multiple stores.`;
            
            // Render Products
            data.results.forEach((product, index) => {
                const card = createProductCard(product);
                // Staggered animation delay
                card.style.animationDelay = `${index * 0.05}s`;
                productsGrid.appendChild(card);
            });

        } catch (error) {
            console.error("Search failed:", error);
            loadingIndicator.classList.add('hidden');
            resultsMeta.textContent = 'Error occurred.';
            productsGrid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; color: var(--accent-secondary); padding: 3rem;">
                    <h3>Oops! Something went wrong.</h3>
                    <p>Our search engines encountered a hiccup. Please try again.</p>
                </div>
            `;
        }
    });

    function createProductCard(product) {
        const div = document.createElement('div');
        div.className = 'product-card animate-card';
        
        // Safe defaults
        const imgUrl = product.image_url || 'https://via.placeholder.com/400x300?text=No+Image';
        const price = parseFloat(product.price).toFixed(2);
        
        div.innerHTML = `
            <div class="store-badge">${product.store_name}</div>
            <div class="product-image-container">
                <img src="${imgUrl}" alt="${product.title}" class="product-image" loading="lazy" onerror="this.src='https://via.placeholder.com/400x300?text=No+Image'">
            </div>
            <div class="product-info">
                <h3 class="product-title" title="${product.title}">${product.title}</h3>
                <div class="product-price-row">
                    <div class="product-price">
                        <span>${product.currency}</span>${price}
                    </div>
                    <a href="${product.product_url}" class="buy-btn" target="_blank" aria-label="View Product">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </a>
                </div>
            </div>
        `;
        
        return div;
    }
});
