from typing import Any
from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from user.models import Customer
from products.models import DeliveryLocation, Product, Cart, Orders

# Create your views here.
def userdashboard(request):
    customer_id = request.session['user_id']
    customer = Customer.objects.filter(user_id = customer_id)
    user_id = request.session['user_id']
    cart_items = Cart.objects.filter(cid = user_id)
    cartcount = Cart.objects.filter(cid = user_id).count()
    addresses = Orders.objects.filter(cid=user_id).values(
        'first_name', 'last_name', 'user_address', 'user_landmark', 
        'user_city', 'user_state', 'user_country', 'user_postal_code'
    ).distinct()
    return render(request, 'user/dashboard.html',{'customers':customer,'currentUser':request.session['user_name'],'currentUserId':request.session['user_id'],'count':cartcount,"addresses":addresses})
def index(request):
    user_id = request.session['user_id']
    # delivery = DeliveryLocation.objects.filter(user_id=user_id)
    products = Product.objects.all()
    cartcount = Cart.objects.filter(cid = user_id).count()
    cart_items = Cart.objects.filter(cid = user_id).order_by('-created_at')[0:2]
    context = {
        'currentUser': request.session.get('user_name', '') , # safely get user_name
        'count':cartcount,
        'cart_items':cart_items
    }
    return render(request, 'user/index.html', context)
def login(request):
    return render(request, 'user/login.html')
def signup(request):
    return render(request, 'user/signup.html')
def BasePost(request):
    return render(request,'user/base.html',{'currentUser':request.session['user_name']})
class CreateUser(APIView):
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        if Customer.objects.filter(user_email = email).exists():
            return JsonResponse({"status":"fail","message":"Email Already Exists"})
        customer = Customer()
        customer.user_name = username
        customer.user_email = email
        customer.user_password = password
        customer.user_phone = mobile
        customer.save()
        return JsonResponse({"status":"pass"})
class LoginCheck(APIView):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.objects.get(user_email=email)
        try:
            if Customer.objects.filter(user_email = email, user_password = password).exists():
                request.session['user_name'] = customer.user_name
                request.session['user_id'] = customer.user_id
                return JsonResponse({"status": "pass","role":customer.role})
            else:
                return JsonResponse({"status": "false",'message':"Invalid Credentials"})  # Wrong password
        except Customer.DoesNotExist:
            return JsonResponse({"status": "fail", "message":"Your email doesn't exist."})
from django.views.generic.base import TemplateView
class ViewUser(TemplateView):
    template_name = 'view.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        userdata = Customer.objects.all()
        context['userdata'] = userdata
        return context
class DeleteUser(APIView):
    def post(self, request):
        id = request.POST['id']
        Customer.objects.filter(user_id = id).delete()
        return JsonResponse({"status":"pass"})
class UpdateUser(APIView):
    def post(self, request):
        user_id = request.data.get('id')
        username = request.data.get('customername')
        email = request.data.get('customeremail')
        mobile = request.data.get('customerphone')
        password = request.data.get('customerpassword')
        Customer.objects.filter(user_id = user_id).update(user_name = username, user_email = email, user_password = password, user_phone = mobile)
        return JsonResponse({"status":"pass"})
def logout(request):
    request.session.pop('user_id',None)
    request.session.pop('user_name',None)
    return redirect('login')