from src.parser import ProductParser
from src.database import DatabaseRepository


def main():
    parser = ProductParser()
    repo = DatabaseRepository('products.db')
    url = "https://opt-opt-opt.ru/"
    print(f"Парсинг: {url}")

    try:
        products = parser.parse_page(url)
        print(f"Найдено товаров: {len(products)}")

        for product in products[:10]:
            print(f"[{product['id']}] {product['name']}")
            print(f"   {product['message']}")
            print()

        parser.save_to_db(products, repo)
        print(f"Сохранено в products.db")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        repo.close()


if __name__ == "__main__":
    main()