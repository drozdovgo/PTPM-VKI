import requests
from bs4 import BeautifulSoup
from .database import DatabaseRepository


class ProductParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept-Language': 'ru-RU,ru;q=0.9'
        }

    def parse_page(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return self._extract_products(response.text)

    def parse_html(self, html_content):
        return self._extract_products(html_content)

    def _extract_products(self, html):
        soup = BeautifulSoup(html, 'lxml')
        products = []
        product_blocks = soup.find_all('div', class_='bx_catalog_item')

        for idx, block in enumerate(product_blocks, start=1):
            image_link = block.find('a', class_='bx_catalog_item_images')
            title = image_link.get('title', '') if image_link else ""
            articul_block = block.find('div', class_='bx_catalog_item_articul')
            if not articul_block or not title:
                continue

            articul_text = articul_block.get_text(strip=True)
            brand = "Неизвестный бренд"
            if "Торговая марка" in articul_text:
                parts = articul_text.split("Торговая марка")
                if len(parts) > 1:
                    brand_part = parts[1].split("Размеры:")[0].strip()
                    brand = brand_part if brand_part else "Неизвестный бренд"

            price_tag = block.find('div', class_='bx_price')
            price = price_tag.get_text(strip=True) if price_tag else "Цена не указана"
            message = f"Товар: {title}. Цена: {price}"

            products.append({
                'id': idx,
                'name': brand,
                'message': message
            })

        return products

    def save_to_db(self, parsed_data, repository):
        for item in parsed_data:
            try:
                repository.add(
                    comment_id=item['id'],
                    username=item['name'],
                    message=item['message']
                )
            except ValueError as e:
                print(f"Пропущено: {e}")