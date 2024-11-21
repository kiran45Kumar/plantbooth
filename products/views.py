from django.shortcuts import render,redirect,get_object_or_404
# Create your views here.
from django.http import JsonResponse
from rest_framework.views import APIView
from user.models import Customer
from django.views.generic import TemplateView
from vendor.models import Vendors
from .models import Product, Category, Subcategory, DeliveryLocation,Cart, Orders
from django.http import HttpResponse
from django.views import View
import requests
from datetime import timezone
from .models import Category, Subcategory, AnotherSubcategory
from .utils import extract_key_points
class add_to(APIView):
    def post(self,request):
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        customer_id = request.POST.get("customer_id")
        try:
            product = Product.objects.get(product_id = product_id)
            customer = Customer.objects.get(user_id = customer_id)
            cart = Cart()
            cart.cid = customer
            cart.product = product
            cart.quantity = quantity
            cart.save()
            return JsonResponse({"status":"success"})
        except Product.DoesNotExist:
            return JsonResponse({"status":"fail","message":"product not found"})
        except Customer.DoesNotExist:
            return JsonResponse({"status":"fail","message":"Customer not found"})
        return JsonResponse({"status":"success"})

def category(request):
    return render(request, 'products/categories.html')

def category_list(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'vendor/createProduct.html', {'categories': categories})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def get_another_subcategories(request):
    subcategory_id = request.GET.get('subcategory_id')
    another_subcategories = AnotherSubcategory.objects.filter(subcategory_id=subcategory_id).values('id', 'name')
    return JsonResponse(list(another_subcategories), safe=False)

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        subcategory_name = request.POST.get('subcategory_name')
        another_subcategory_name = request.POST.get('another_subcategory_name')

        # Create category if it doesn't exist
        category, created = Category.objects.get_or_create(name=category_name)

        # Create subcategory
        subcategory, createdat = Subcategory.objects.get_or_create(name=subcategory_name, category=category)

        # Create another subcategory under the subcategory
        AnotherSubcategory.objects.create(name=another_subcategory_name, subcategory=subcategory)

        return redirect('add_category')  # Redirect to a success page or category list

    return render(request, 'products/categories.html')

class GetRegion(View):
    def post(self, request):
        pincode = request.POST.get('pincode')
        customer_id = request.POST.get('customer_id')
        
        # API call to get the region from the pincode
        response = requests.get(f'https://api.postalpincode.in/pincode/{pincode}')
        data = response.json()

        if data[0]['Status'] == "Success":
            region = data[0]['PostOffice'][0]['District']
            
            # Save to database (optional)
            user = Customer.objects.get(user_id = customer_id)
            DeliveryLocation.objects.update_or_create(user_id = user,pincode=pincode, defaults={'region': region})

            return JsonResponse({'status': 'success', 'region': region})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid Pincode'})
class CreateProduct(APIView):
    def post(self, request):
        user_id = request.POST.get('user_id')
        vendor_id = request.POST.get('vendor_id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        barcode = request.POST.get('barcode')
        benefits = request.POST.get('benefit')
        care_tips = request.POST.get('caretips')
        product_img = request.FILES.get('product_img')
        category_id = request.POST.get('product_category')
        sub_category_id = request.POST.get('product_subcategory')
        subsub_category_id = request.POST.get('product_ano_subcategory')
        category = Category.objects.get(id = category_id)
        sub_category = Subcategory.objects.get(id = sub_category_id)
        subsub_category = AnotherSubcategory.objects.get(id = subsub_category_id)
        user = Customer.objects.get(user_id = user_id)
        vendor = Vendors.objects.get(vendor_id = vendor_id)
        product = Product()
        product.user_id = user
        product.vendor_id = vendor
        product.product_name = name
        product.product_desc = desc
        product.product_price = price
        product.product_quantity = quantity
        product.product_barcode = barcode
        product.product_benefits = benefits
        product.care_tips = care_tips
        product.product_image = product_img
        product.category = category
        product.sub_category = sub_category
        product.subsub_category = subsub_category
        product.save()
        return JsonResponse({"status":"pass"})
class ViewProduct(TemplateView):
    template_name = "products/product.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user_id = self.request.session['user_id']
        vendors = Vendors.objects.filter(user_id = user_id)
        products = Product.objects.filter(user_id = user_id)
        context = {'products': products,'vendors':vendors}
        return context
class DeleteProduct(APIView):
    def post(self, request):
        id = request.POST['id']
        Product.objects.filter(product_id = id).delete()
        return JsonResponse({"status":"pass"})
class UpdateProduct(APIView):
    def post(self, request):
        vendor_id = request.POST.get('id')
        vendor_name = request.POST.get('vendor_name')
        vendor_email = request.POST.get('vendor_email')
        vendor_phone = request.POST.get('vendor_phone')
        vendor_city = request.POST.get('vendor_city')
        vendor_state = request.POST.get('vendor_state')
        vendor_profile = request.POST.get('vendor_profile')
        vendor_country = request.POST.get('vendor_country')
        vendor_rating = request.POST.get('vendor_rating')
        vendor = Vendors.objects.filter(vendor_id = vendor_id).update( 
            vendor_name = vendor_name,
            vendor_email = vendor_email,
            vendor_phone = vendor_phone,
            vendor_city = vendor_city,
            vendor_state = vendor_state,
            vendor_country = vendor_country)
        return JsonResponse({"status":"pass"})
def productView(request,id):
    user_id = request.session['user_id']
    product = Product.objects.get(product_id = id)
    return render(request, 'products/productview.html',{'product':product})
class DeleteCart(APIView):
    def post(self, request):
        id = request.POST['id']
        Cart.objects.filter(id = id).delete()
        return JsonResponse({"status":"pass"})
def display(request,cid,product_id):
    allmed = Product.objects.get(product_id = product_id)
    allcustomers = Customer.objects.all()
    allsuppliers = Vendors.objects.all()
    return render(request, 'products/display.html',{'allmed':allmed, 'allcustomer':allcustomers,'allsupplier':allsuppliers,'currentUserId':request.session['customer_id'],'currentUser':request.session['user_name'],'count':request.session['count'],'currentUserEmail':request.session['customer_email']})
def shop(request):
    user_id = request.session['user_id']
    cartcount = Cart.objects.filter(cid = user_id).count()
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/shop.html',{'currentUser':request.session['user_name'],'products':products,'currentUserId':request.session['user_id'],'count':cartcount})
def about(request):
    user_id = request.session['user_id']
    cartcount = Cart.objects.filter(cid = user_id).count()
    return render(request, 'products/about.html',{'currentUser':request.session['user_name'],'count':cartcount})
def contact(request):
    user_id = request.session['user_id']
    cartcount = Cart.objects.filter(cid = user_id).count()
    return render(request, 'products/contact.html',{'currentUser':request.session['user_name'],'count':cartcount})
def faq(request):
    user_id = request.session['user_id']
    cartcount = Cart.objects.filter(cid = user_id).count()
    return render(request, 'products/faq.html',{'currentUser':request.session['user_name'],'count':cartcount})
def soon(request):
    user_id = request.session['user_id']
    cartcount = Cart.objects.filter(cid = user_id).count()
    return render(request, 'products/coming-soon.html',{'currentUser':request.session['user_name'],'count':cartcount})
def blog(request):
    user_id = request.session['user_id']
    cartcount = Cart.objects.filter(cid = user_id).count()
    return render(request, 'products/blog.html',{'currentUser':request.session['user_name'],'count':cartcount})
def product(request,id):
    user_id = request.session['user_id']
    cartcount = Cart.objects.filter(cid = user_id).count()
    product = Product.objects.get(product_id = id)
    key_points = extract_key_points(product.product_benefits)
    caretips = extract_key_points(product.care_tips)
    return render(request, 'products/mainproduct.html',{'currentUser':request.session['user_name'],'count':cartcount,'product':product,'key_points': key_points,"caretips":caretips,"currentUserId":request.session['user_id']})
def category(request):
    user_id = request.session['user_id']
    cartcount = Cart.objects.filter(cid = user_id).count()
    return render(request, 'products/category.html',{'currentUser':request.session['user_name'],'count':cartcount})
def cart_page(request):
    user_id = request.session['user_id']
    cart_items = Cart.objects.filter(cid = user_id).order_by('-created_at')
    cartcount = Cart.objects.filter(cid = user_id).count()
    return render(request, 'products/cart_page.html', {'cart_items':cart_items,"count":cartcount,'currentUser':request.session['user_name']})
def checkout(request):
    user_id = request.session['user_id']
    cart_items = Cart.objects.filter(cid = user_id).order_by('-created_at')
    cartcount = Cart.objects.filter(cid = user_id).count()
    products = Product.objects.filter(user_id = user_id)
    users = Customer.objects.filter(user_id = user_id)
    return render(request, 'products/checkout.html', {'cart_items':cart_items,"count":cartcount,'currentUser':request.session['user_name'],'currentUserId':request.session['user_id'],"products":products,'users':users})

class order_cart(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        user_phone = request.data.get('user_phone')
        user_email = request.data.get('user_email')
        user_address = request.data.get('user_address')
        user_alternate_phone = request.data.get('user_alternate_phone')
        user_landmark = request.data.get('user_landmark')
        user_city = request.data.get('user_city')
        user_state = request.data.get('user_state')
        user_postal_code = request.data.get('user_postal_code')
        country_name = request.data.get('country_name')
        order_notes = request.data.get('order_notes')
        cashondelivery = request.data.get('cashondelivery')

        customer = Customer.objects.get(user_id=user_id)
        product = Product.objects.get(product_id=product_id)
        
        order = Orders.objects.create(
            cid=customer,
            product=product,
            first_name = first_name,
            last_name=last_name,
            user_phone=user_phone,
            user_email=user_email,
            user_address=user_address,
            user_alternate_phone=user_alternate_phone,
            user_landmark=user_landmark,
            user_city=user_city,
            user_state=user_state,
            user_postal_code=user_postal_code,
            user_country = country_name,
            order_notes = order_notes,
            payment_method = cashondelivery
        )
        order.save()
        
        request.session['order_id'] = order.order_id
        
        return JsonResponse({'status': "pass", 'currentUserId': request.session['user_id']})