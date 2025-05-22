from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, Category, Favorite, CartItem, Cart
from django.contrib.auth.decorators import login_required
from .models import *
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from django.db import transaction
from decouple import config
from rest_framework.response import Response

from .services import FreedomPayService


@csrf_exempt
def payment_callback_view(request):
    order_id = request.GET.get('order_id')
    payment_status = request.GET.get('status')  # зависит от того, что вернёт FreedomPay
    print(payment_status)
    print(order_id)
    order = Order.objects.filter(id=order_id).first()

    if order:
        if payment_status == 'success':
            order.status = 'paid'  # если есть статус
            order.save()
        else:
            order.status = 'failed'
            order.save()

    return redirect('/')  # или показать страницу оплаты


class ProductListView(generic.ListView):
    template_name = 'catalog_new.html'
    queryset = Product.objects.all()
    model = Product
    paginate_by = 8
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        for i, j in enumerate(context['products']):
            context[f'product{i+1}'] = j
        context['favorites'] = [i.product.id for i in self.request.user.favorites.all()]
        # print(context['favorites'])
        return context


class ProductDetailView(generic.DetailView):
    template_name = 'detail.html'
    queryset = Product.objects.all()
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rec_products'] = Product.objects.all().order_by('?')[:3]
        return context


class HomePageView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_products'] = Product.objects.all()[:4]
        context['categories'] = Category.objects.all()[:5]
        for i, j in enumerate(context['categories']):
            context[f'category{i+1}'] = j
        context['site'] = SiteSetting.objects.all().first()
        context['products1'] = context['site'].main_category1.products.all()
        context['products2'] = context['site'].main_category2.products.all()
        if self.request.user.is_authenticated:
            context['favorites'] = [i.product.id for i in self.request.user.favorites.all()]
        context['favorites'] = []
        return context


class CategoriesListView(generic.ListView):
    template_name = 'categories.html'
    queryset = Category.objects.all()
    model = Category
    paginate_by = 5
    context_object_name = "categories"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        for i, j in enumerate(context['categories']):
            context[f'category{i+1}'] = j
        print(context['category1'])
        return context


class AboutView(generic.TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq'] = Faq.objects.all()
        return context



class AddressView(generic.TemplateView):
    template_name = 'addres.html'


class BasketView(generic.TemplateView):
    template_name = 'basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.request.user.cart.items.all()
        context['summa'] = sum((i.product.sale_price * i.quantity) for i in context['products'])
        return context


@login_required
def update_user_address_view(request):
    user = request.user

    if request.method == 'POST':
        form = UserAddressForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # или куда хочешь
        else:
            print(form.errors)
    else:
        form = UserAddressForm(instance=user)
    return render(request, 'addres.html', {'form': form})



class ContactsView(generic.TemplateView):
    template_name = 'contacts.html'


class FavoritesView(generic.TemplateView):
    template_name = 'favorites.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('/login/')



class LoginView(generic.TemplateView):
    template_name = 'login.html'


def loginview(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('/profile/')
    return redirect('/profile/')


def logoutview(request):
    logout(request)
    return redirect('/login/')


class RegisterView(generic.TemplateView):
    template_name = 'register.html'


class OfferView(generic.TemplateView):
    template_name = 'offer.html'


class OrdersView(generic.TemplateView):
    template_name = 'orders.html'


class ProfileView(generic.TemplateView):
    template_name = 'profile.html'


def delete_or_add_favorite(request, pk):
    product = get_object_or_404(Product, id=pk)
    fav, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product,
    )
    if not created:
        fav.delete()
    return redirect('/favorites/')




from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm  # Импортируем стандартную форму для примера
from authentication.forms import RegistrationForm, UserAddressForm  # Импортируем нашу кастомную форму

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически логиним пользователя после регистрации
            Cart.objects.create(user=user)
            return redirect('/profile/')  # Перенаправляем на страницу успеха
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


from django.views.decorators.http import require_POST



def add_basket(request, pk):
    product = get_object_or_404(Product, id=pk)
    cart = request.user.cart

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/basket/')  # Перенаправь пользователя на страницу просмотра корзины


def remove_basket(request, pk):
    product = get_object_or_404(Product, id=pk)
    cart = request.user.cart

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # Если товара нет в корзине, ничего не делаем

    return redirect('/basket/')  # Перенаправь пользователя на страницу просмотра корзины

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Order  # если есть модель заказа

@login_required(login_url='/login/')
def create_order_view(request):
    user = request.user

    if request.method == 'POST':
        # Обновляем профиль
        user.first_name = request.POST.get('first_name')
        user.phone = request.POST.get('phone')
        user.email = request.POST.get('email')
        user.country = request.POST.get('country')
        user.city = request.POST.get('city')
        user.address = request.POST.get('address')
        user.save()

        # Сохраняем заказ
        comment = request.POST.get('comment')
        promo_code = request.POST.get('promo_code')

        products = [item.product for item in request.user.cart.items.all()]
        amount = sum([p.sale_price for p in products])
        print(amount)
        amount = int(str(int(amount))[:-2])


        order = Order.objects.create(
            user=user,
            comment=comment,
            promo_code=promo_code,
            total=amount
        )


        # Добавляем в заказ
        order.products.set(products)
        request.user.cart.items.all().delete()

        payment_url = FreedomPayService.create_payment(order, request.user.email, request.user.phone)
        return redirect(payment_url)

    return render(request, 'offer.html', {
        'user': user
    })

def fail_freedom_pay(request):
    order_id = request.GET.get('pg_order_id')
    if not order_id:
        return redirect('/')

    order = get_object_or_404(Order, id=order_id)

    # Устанавливаем статус заказа как отменённый
    order.payment_status = 'failed'
    order.save()

    return redirect('/')

def success_freedom_pay(request):
    # Получаем параметры из строки запроса
    pg_order_id = request.GET.get('pg_order_id')
    pg_payment_id = request.GET.get('pg_payment_id')
    pg_salt = request.GET.get('pg_salt')
    pg_sig = request.GET.get('pg_sig')

    # Проверяем, что обязательные параметры переданы
    if not all([pg_order_id, pg_payment_id, pg_salt, pg_sig]):
        return redirect('/')

    # Проверяем подпись
    if not FreedomPayService.verify_signature(request.GET, 'payment/success/'):
        return redirect('/')

    # Находим заказ
    order = get_object_or_404(Order, id=pg_order_id)

    # Проверяем статус оплаты
    if order.payment_status == 'completed':
        return redirect('/')

    # Уменьшаем количество на складе и обновляем заказ
    with transaction.atomic():

        # Обновляем статус заказа
        order.payment_status = 'completed'
        order.save()

    return redirect('/')