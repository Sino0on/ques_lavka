from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from product.models import Category, Product


class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = RichTextField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f'{self.question}'

    class Meta:
        ordering = ['-created_at']


class SingletonModel(models.Model):
    """
    Модель, которая всегда имеет только один экземпляр.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Если модель уже существует, удалите ее
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Если модель еще не существует, создайте ее
        if not cls.objects.exists():
            cls.objects.create()
        return cls.objects.get()


class SiteSetting(SingletonModel):
    contacts = models.TextField(blank=True, verbose_name='Контакт')
    emails = models.TextField(blank=True, verbose_name='Почта')
    best_category1 = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='best_sitesettings_1')
    best_category2 = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='best_sitesettings_2')
    best_category3 = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='best_sitesettings_3')
    best_category4 = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='best_sitesettings_4')
    best_category5 = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='best_sitesettings_5')
    main_category1 = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='main_sitesettings_1')
    main_category2 = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='main_sitesettings_2')
    main_product1 = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='main_product_1')
    main_product2 = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='main_product_2')
    main_product3 = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='main_product_3')
    main_product4 = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='main_product_4')


class Meta:
        verbose_name = 'Настройка сайта'
        verbose_name_plural = 'Настройки сайта'

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True, null=True)
    promo_code = models.CharField(max_length=255, blank=True, null=True)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length=123, default='waiting', blank=True)

    def __str__(self):
        return f'{self.pk} - {self.user}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class FreedomPayConfig(models.Model):
    merchant_id = models.CharField(max_length=255, verbose_name="ID магазина")
    secret_key = models.CharField(max_length=255, verbose_name="Секретный ключ магазина")
    secret_key_payout = models.CharField(max_length=255, verbose_name="Секретный ключ для возврата средств")
    api_url = models.URLField(verbose_name="Api Ссылка freedompay")
    result_url = models.URLField(verbose_name="Ссылка для результата")
    success_url = models.URLField(verbose_name="Успешная ссылка")
    failure_url = models.URLField(verbose_name="Не успешная ссылка")
    testing_mode = models.BooleanField(default=False, verbose_name="Тест режим")

    class Meta:
        verbose_name = "Настройка FreedomPay"
        verbose_name_plural = "Настройки FreedomPay"

    def __str__(self):
        return self.merchant_id


# models.py
from django.db import models

class ContactRequest(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Application(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

