from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView,DetailView,ListView,View,CreateView
from .models import Category,Brand,Product,CartItem,Order,Cart
from .forms import OrderForm,UserCreateForm
from django.http import HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from context_processors.processors import cart_view
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'
    products = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'products': self.products[3:],
            'carousel_products': self.products[:3],
        }
        return context


class Register(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("shop:home")
    template_name = "register.html"
    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('acc_active_email.html', {
            'user': new_user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
            'token':account_activation_token.make_token(new_user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class CategoryDetailView(DetailView):
    model = Category
    # context ketword for category's products is "products", due to the
    # "related_name" parameter in Product model

class ProductDetailView(DetailView):
    model = Product


class CartView(TemplateView):
    template_name = 'cart.html'


class CheckOutView(CreateView):
    template_name = 'check_out.html'
    form_class = OrderForm
    model = Order

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        cart = cart_view(self.request)['cart']
        self.object.cost = cart.total_amount()
        self.object.items.add(cart)
        self.object.status = 'processing'
        self.object.save()
        del self.request.session['total']
        del self.request.session['cart_id']
        return super().form_valid(form)


class SearchListView(ListView):
    model = Product
    template_name = "search_results.html"

    def get_queryset(self):
        # Fetch the queryset from the parent get_queryset
        queryset = super().get_queryset()
        # Get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            # Return a filtered queryset
            return queryset.filter(title__icontains=q)
        # Return the base queryset
        return queryset


class ThankYouView(TemplateView):
    template_name = 'thank_you.html'


class YourPlaceView(ListView):
    context_object_name = 'orders'
    template_name = 'yourplace.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-id')


def add_to_cart_view(request):  # ,slug):
    slug = request.GET.get('slug')
    product = Product.objects.get(slug=slug)
    cart = cart_view(request)['cart']
    cart.add_to_cart(product)
    return JsonResponse({'cart_total': cart.items.count()})

def remove_from_cart_view(request):  # ,slug):
    slug = request.GET.get('slug')
    product = Product.objects.get(slug=slug)
    cart = cart_view(request)['cart']
    cart.remove_from_cart(product)
    return JsonResponse({'cart_total': cart.items.count(),'total_amount': cart.total_amount()})

def change_item_quantity(request):
    cart = cart_view(request)['cart']
    quantity = request.GET.get('quantity')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id=int(item_id))
    cart_item.change_item_quantity(quantity)
    return JsonResponse({'cart_total':cart.items.count(), 'item_price':cart_item.item_price, 'total_amount':cart.total_amount()})
