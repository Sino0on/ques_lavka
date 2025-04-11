import requests
from django.utils.dateparse import parse_datetime
from decouple import config
from product.models import Category  # замени yourapp на имя твоего Django приложения


def import_categories_from_api():
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/productfolder'
    headers = {"Authorization": f"Bearer {config('MS_TOKEN')}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка при получении данных: {response.json()}")
        return

    categories = response.json()['rows']

    for category_data in categories:
        category, created = Category.objects.update_or_create(
            old_id=category_data.get("id"),
            defaults={
                "updated": parse_datetime(category_data.get("updated")),
                "name": category_data.get("name"),
                "external_code": category_data.get("externalCode"),
                "archived": category_data.get("archived"),
                "path_name": category_data.get("pathName"),
                # "image": можно будет загрузить отдельно, если в API есть ссылка на изображение
            }
        )
        print(f"{'Создана' if created else 'Обновлена'} категория: {category.name}")
    return True