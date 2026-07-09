# Bazaarcart 🛒
### *The High-Performance, Unified E-Commerce Search Engine*

Bazaarcart is a modern, unified e-commerce search platform designed to solve the fragmentation of online shopping. By utilizing a high-performance asynchronous engine, Bazaarcart allows users to search across multiple independent marketplaces simultaneously, aggregate data in real-time, and view normalized results inside a sleek, premium interface.

---

## 🏗️ Architectural Overview

Bazaarcart is engineered for speed, resilience, and scalability. Instead of querying external marketplaces sequentially, it utilizes a parallel execution model to deliver sub-second response times.

```text
                  +-------------------------+
                  |  Premium Glassmorphic   |
                  |     Frontend (UI)       |
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  |  FastAPI / Python Web   |
                  |        Backend          |
                  +------------+------------+
                               |
                               v
               +-------------------------------+
               | Asynchronous Fan-Out Engine   |
               |     (asyncio + httpx)         |
               +---------------+---------------+
                               |
         +---------------------+---------------------+
         |                     |                     |
         v                     v                     v
+-----------------+   +-----------------+   +-----------------+
|   Live Scraper  |   |   Real APIs     |   | Smart Simulators|
|(StarTech,Rokomari)  | (FakeStore, etc)|   | (Amazon, Daraz) |
+-----------------+   +-----------------+   +-----------------+

Core Architectural Highlights
Asynchronous Fan-Out Engine: Built using Python's asyncio and httpx. The backend queries up to 7 different external APIs and scrapers concurrently, ensuring response times remain sub-second regardless of the number of integrations.

Resilient Fault-Tolerant Design: Implemented strict isolation barriers for every integration. If an external store API times out or crashes, the exception is gracefully handled, allowing the remaining stores to render flawlessly.

Dynamic Data Normalization: Features an intelligent aggregation layer that ingests highly fragmented JSON schemas and normalizes them into a unified Bazaarcart standard format:

JSON
{
  "title": "Product Name",
  "price": 0.00,
  "image": "https://...",
  "link": "https://..."
}
✨ Key Features
🕷️ Live Web Scraper (StarTech): A real-time scraping module utilizing BeautifulSoup4 that bypasses basic bot protections to extract live pricing, images, and accurate titles directly from local e-commerce sites (StarTech.com.bd).

🎮 Smart Mock Integrations: Advanced API simulators for enterprise giants (Amazon, Daraz, Alibaba, eBay) that dynamically construct valid search URLs with exact query and price-bound parameters pre-applied.

📸 Real-World Image Injection: A background secondary fetcher that maps authentic product photography from live databases (like DummyJSON) into mock listings to maintain a premium and cohesive UI.

🖥️ Internal Proxy Viewer: A native routing mechanism (/web-details/) that can silently fetch external website components and render them cleanly inside the Bazaarcart ecosystem, reducing user bounce rates.

🎛️ Global Smart Filtering: An efficient, in-memory aggregation filter allowing users to apply global constraints (Minimum Price, Maximum Price, Brand) uniformly across all connected stores.

🎨 Premium Glassmorphic UI: A state-of-the-art interface built with Vanilla CSS and modern JavaScript. It features deep dark-mode aesthetics, responsive CSS Grid layouts, interactive micro-animations, and full-card clickability.

🛠️ Tech Stack
Backend: Python 3.10+, asyncio, httpx, BeautifulSoup4, FastAPI (or your specific framework, e.g., Flask/Django)

Frontend: HTML5, Vanilla CSS3 (Glassmorphism, CSS Grid, Flexbox), Modern JavaScript (ES6+)

Data Sources: FakeStore API, DummyJSON API, StarTech (Live Scraping)

🚀 Getting Started
Prerequisites
Ensure you have Python 3.10 or higher installed on your system.

Installation
Clone the repository:

Bash
git clone [https://github.com/yourusername/bazaarcart.git](https://github.com/yourusername/bazaarcart.git)
cd bazaarcart
Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install the dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
# Update this line with your actual entry point command (e.g., uvicorn main:app --reload)
python app.py 
Open your browser and navigate to http://localhost:8000 to experience Bazaarcart.

🔮 Future Scope & Roadmap
[ ] AI-Powered Semantic Search: Implement Vector Embeddings (e.g., Pinecone + OpenAI) to understand user intent rather than relying solely on strict keyword matching.

[ ] User Accounts & Price Alerts: Allow users to create profiles, track specific items across platforms, and receive web/email notifications when a price drops.

[ ] Browser Extension: Develop a lightweight cross-browser extension that auto-checks Bazaarcart for cheaper alternatives whenever a user visits a standalone e-commerce site.

[ ] Machine Learning Price Predictor: Analyze historical price trends across crawled stores to advise users whether to "Buy Now" or "Wait" for seasonal drops.
