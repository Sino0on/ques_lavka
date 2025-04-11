import requests
import time
from io import BytesIO
from django.core.files.base import ContentFile
from decouple import config
from product.models import Product, ImageProduct  # не забудь заменить на своё приложение


def import_product_images():
    base_url = 'https://api.moysklad.ru/api/remap/1.2/entity/product'
    headers = {"Authorization": f"Bearer {config('MS_TOKEN')}"}

    products = Product.objects.all()

    for product in products:
        if product.images.exists():
            print(f"⏭ Пропущен: у продукта {product.old_id} уже есть изображения.")
            continue
        time.sleep(0.3)  # 🔒 не банят за частые запросы
        print(product.id)
        response = requests.get(f"{base_url}/{product.old_id}/images", headers=headers)
        if response.status_code != 200:
            print(f"Ошибка получения изображений для продукта {product.old_id}")
            continue
        if response.json()['rows'] == []:
            continue

        image_data = response.json()['rows'][0]

        miniature = image_data.get("miniature")
        if not miniature:
            print(f"Нет miniature для продукта {product.old_id}")
            continue

        image_url = miniature.get("href")
        if not image_url:
            continue

        # Убираем "?miniature=true"
        image_url = image_url.split('?')[0]

        # Скачиваем изображение
        try:
            img_response = requests.get(image_url, stream=True, headers=headers)
            if img_response.status_code == 200:
                file_name = image_url.split("/")[-1]

                image_file = ContentFile(img_response.content)
                image_instance = ImageProduct(product=product)
                image_instance.image.save(file_name+'.jpg', image_file, save=True)

                print(f"✅ Изображение сохранено для продукта {product.old_id}")
            else:
                print(f"⚠️ Не удалось скачать изображение по ссылке: {image_url}")
        except Exception as e:
            print(f"Ошибка при скачивании изображения: {e}")
    return True