from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Category(models.Model):
    old_id = models.CharField(max_length=255, blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    external_code = models.CharField(max_length=255, blank=True, null=True)
    archived = models.BooleanField(default=False, blank=True, null=True)
    path_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/category/')

    def __str__(self):
        return self.name


class Product(models.Model):
    old_id = models.CharField(max_length=255)
    updated = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    external_code = models.CharField(max_length=255, blank=True, null=True)
    archived = models.BooleanField(default=False)
    path_name = models.CharField(max_length=255, blank=True, null=True)

    sale_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    buy_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    barcodes = models.CharField(max_length=255, blank=True, null=True)

    payment_item_type = models.CharField(max_length=50, blank=True, null=True)
    discount_prohibited = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    volume = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    variants_count = models.IntegerField(blank=True, null=True)
    is_serial_trackable = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')


    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def get_main_image(self):
        main_image = self.images.all().first()
        if main_image:
            return main_image.image.url

        return None


class ImageProduct(models.Model):
    image = models.ImageField(upload_to='images/product/%Y/%m', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return str(self.product)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # class Meta:
        # unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} ❤️ {self.product.name}"


