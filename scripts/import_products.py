import requests
from django.utils.dateparse import parse_datetime
from decouple import config
from product.models import Product, Category  # замени yourapp на имя твоего Django приложения

def import_products_from_api(photo=None):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/product'
    headers = {"Authorization": f"Bearer {config('MS_TOKEN')}"}
    for i in ['0', '999', '1900']:
        response = requests.get(url+f"?offset={i}", headers=headers)

        if response.status_code != 200:
            print(f"Ошибка при получении данных: {response.status_code}")
            return

        products = response.json()['rows']
        print(len(products))
        for product_data in products:
            category = Category.objects.filter(name=product_data.get("pathName")).first()
            print(category)
            print(product_data.get("pathName"))

            if product_data.get("barcodes") != None:
                barcodes = product_data.get("barcodes")[0].get('ean13')
            else:
                barcodes = None
            product, created = Product.objects.update_or_create(
                old_id=product_data.get("id"),
                defaults={
                    "updated": parse_datetime(product_data.get("updated")),
                    "name": product_data.get("name"),
                    "code": product_data.get("code"),
                    "external_code": product_data.get("externalCode"),
                    "archived": product_data.get("archived"),
                    "path_name": product_data.get("pathName"),
                    "sale_price": product_data.get("salePrices")[0].get('value'),
                    "buy_price": product_data.get("buyPrice").get('value'),
                    "barcodes": barcodes,
                    "payment_item_type": product_data.get("paymentItemType"),
                    "discount_prohibited": product_data.get("discountProhibited"),
                    "weight": product_data.get("weight"),
                    "volume": product_data.get("volume"),
                    "variants_count": product_data.get("variantsCount"),
                    "is_serial_trackable": product_data.get("isSerialTrackable"),
                    "category": category,
                }
            )
            print(f"{'Создан' if created else 'Обновлён'} продукт: {product.name}")
    return True