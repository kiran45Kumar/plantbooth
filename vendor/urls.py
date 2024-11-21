from django.urls import path
from .views import vendorPage,CreateVendor,ViewVendor,DeleteVendor,UpdateVendor,vendorDashbord,createProduct
urlpatterns = [
    path("vendor/",vendorPage, name='vendor'),
    path("create_vendor/",CreateVendor.as_view(), name='create_vendor'),
    path("view_vendor/",ViewVendor.as_view(), name='view_vendor'),
    path("delete_vendor/",DeleteVendor.as_view(), name='delete_vendor'),
    path("update_vendor/",UpdateVendor.as_view(), name='update_vendor'),
    path('vendor_dashboard/',vendorDashbord, name="vendor_dashboard"),
    path('create_product_page/',createProduct,name='create_product')
]