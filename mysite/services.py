import requests
import xml.etree.ElementTree as ET

from hashlib import md5
from datetime import datetime

from .models import FreedomPayConfig


class FreedomPayService:
    @staticmethod
    def make_flat_params_array(arr_params, parent_name=''):
        flat_params = {}
        for i, (key, val) in enumerate(arr_params.items(), start=1):
            name = f"{parent_name}{key}{i:03d}"
            if isinstance(val, dict):
                flat_params.update(FreedomPayService.make_flat_params_array(val, name))
            else:
                flat_params[name] = str(val)
        return flat_params

    @staticmethod
    def generate_signature(request, script_name, secret_key):
        flat_request = FreedomPayService.make_flat_params_array(request)
        ksorted_request = dict(sorted(flat_request.items()))
        values_list = [script_name] + list(ksorted_request.values()) + [secret_key]
        concat_string = ';'.join(values_list)
        return md5(concat_string.encode()).hexdigest()

    @staticmethod
    def get_freedompay_config():
        config = FreedomPayConfig.objects.first()
        if not config:
            raise ValueError("FreedomPay configuration not found.")
        return config

    @staticmethod
    def create_payment(order, user_email, user_phone):
        try:
            config = FreedomPayService.get_freedompay_config()

            url = f"{config.api_url}/init_payment.php"
            params = {
                'pg_merchant_id': config.merchant_id,
                'pg_order_id': order.id,
                'pg_amount': float(order.total),
                'pg_currency': 'KGS',
                'pg_description': f"Оплата заказа #{order.id}",
                'pg_user_phone': user_phone,
                'pg_user_contact_email': user_email,
                'pg_result_url': config.result_url,
                'pg_success_url': config.success_url,
                'pg_failure_url': config.failure_url,
                'pg_testing_mode': int(config.testing_mode),
                'pg_salt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }

            # Генерация подписи
            params['pg_sig'] = FreedomPayService.generate_signature(params, 'init_payment.php', config.secret_key)

            response = requests.post(url, data=params)
            response.raise_for_status()

            print(f"FreedomPay Response: {response.text}")

            root = ET.fromstring(response.text)
            payment_url = root.find('pg_redirect_url')

            if payment_url is None or not payment_url.text:
                raise ValueError("Payment URL is missing in the response.")

            return payment_url.text

        except requests.RequestException as e:
            raise RuntimeError(f"Failed to connect to FreedomPay: {str(e)}")

        except ET.ParseError:
            raise ValueError("Failed to parse FreedomPay response.")

        except ValueError as e:
            raise RuntimeError(str(e))

    @staticmethod
    def verify_signature(params, script_name):
        config = FreedomPayService.get_freedompay_config()

        # Извлекаем подпись из параметров и удаляем её
        signature = params.get('pg_sig')
        if not signature:
            return False

        params = {key: value for key, value in params.items() if key != 'pg_sig'}

        # Генерируем подпись
        generated_signature = FreedomPayService.generate_signature(params, script_name, config.secret_key)

        # Сравниваем подписи
        return signature == generated_signature
