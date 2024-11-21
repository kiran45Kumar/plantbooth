from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from user.models import Customer
from django.views.generic import TemplateView
from vendor.models import Vendors
from products.models import Category,Subcategory
from django.core.exceptions import ObjectDoesNotExist

def vendorPage(request):
    user_id = request.session.get('user_id')
    vendor_exists = False
    message = ""
    try:
        # Check if the vendor exists
        vendorexists = Vendors.objects.get(user_id=user_id)
        vendor_exists = True
        message = "Seller Account already exists."
    except ObjectDoesNotExist:
        # Vendor does not exist, continue to show the form
        vendor_exists = False
        message = "Create Your Seller Account"

    return render(request, 'vendor/vendor.html', {
        'currentUser': request.session.get('user_name'),
        'currentUserId': user_id,
        'vendor_exists': vendor_exists,
        'message': message
    })
def createProduct(request):
    user_id = request.session['user_id']
    vendors = Vendors.objects.filter(user_id=user_id)
    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'vendor/createProduct.html', {
        'currentUser': request.session['user_name'],
        'currentUserId': request.session['user_id'],
        'vendors': vendors,
        'categories': categories
    })


class CreateVendor(APIView):
    def post(self, request):
        user_id = request.POST.get('user_id')
        vendor_name = request.POST.get('vendor_name')
        vendor_email = request.POST.get('vendor_email')
        vendor_phone = request.POST.get('vendor_phone')
        vendor_city = request.POST.get('vendor_city')
        vendor_state = request.POST.get('vendor_state')
        vendor_profile = request.FILES.get('vendor_profile')
        vendor_country = request.POST.get('vendor_country')
        vendor_rating = request.POST.get('vendor_rating')
        if  Vendors.objects.filter(vendor_email = vendor_email).exists():
            return JsonResponse({"status":"fail","message":"Email already Exists! Try with anothe one"})
        user = Customer.objects.get(user_id = user_id)
        vendor = Vendors()
        vendor.user_id = user
        vendor.vendor_name = vendor_name
        vendor.vendor_email = vendor_email
        vendor.vendor_phone = vendor_phone
        vendor.vendor_city = vendor_city
        vendor.vendor_state = vendor_state
        vendor.vendor_profile = vendor_profile
        vendor.vendor_country = vendor_country
        vendor.vendor_rating = vendor_rating 
        vendor.save()
        request.session['vendor_name'] = vendor.vendor_name
        return JsonResponse({"status":"pass"})
def vendorDashbord(request):
    vendor_cid=request.session['user_id']
    vendors = Vendors.objects.filter(user_id = vendor_cid)
    return render(request, 'vendor/vendordashboard.html',{'vendors':vendors})
def vendorData(request):
    vendor_cid=request.session['user_id']
    vendors = Vendors.objects.filter(user_id = vendor_cid)
    return render(request, 'vendor/viewvendor.html', {'vendor':vendors})
class ViewVendor(TemplateView):
    template_name = "vendor/viewvendor.html"

    def get_context_data(self, **kwargs):
        vendor_cid=self.request.session['user_id']
        context = super().get_context_data(**kwargs)
        vendordata = Vendors.objects.get(user_id =vendor_cid)
        context['vendordata'] = vendordata
        return context

class DeleteVendor(APIView):
    def post(self, request):
        id = request.POST['id']
        Vendors.objects.filter(vendor_id = id).delete()
        return JsonResponse({"status":"pass"})
class UpdateVendor(APIView):
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