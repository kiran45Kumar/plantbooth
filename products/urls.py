from django.urls import path
from .views import CreateProduct,ViewProduct,DeleteProduct,add_category,category,category_list,get_subcategories,get_another_subcategories,GetRegion,add_to,productView, cart_page,DeleteCart,shop
from . import views
urlpatterns = [
    path('create_product/',CreateProduct.as_view(),name='create_product'),
    path('view_product/',ViewProduct.as_view(),name='create_product'),
    path('delete_product/',DeleteProduct.as_view(),name='delete_product'),
    path('add_category/',add_category,name='add_category'),
    path('category/',category,name='category'),
    path('category_list',category_list,name="category_list"),
    path('get_subcategories/', get_subcategories, name='get_subcategories'),
    path('get_another_subcategories/', get_another_subcategories, name='get_another_subcategories'),
    path('get-region/', GetRegion.as_view(), name='get-region'),
    path('add_to/',add_to.as_view(), name='add_to'),
    path("product_view/<int:id>",productView,name='product_view'),
    path("cart_page/",cart_page,name='cart_page'),
    path('delete_cart/',DeleteCart.as_view(), name="delete_cart"),
    path('shop/',views.shop, name="shop"),
    path('about/',views.about, name="about"),
    path('contact/',views.contact, name='contact'),
    path('soon/',views.soon, name='soon'),
    path('faq/',views.faq, name='faq'),
    path('blog/',views.blog, name='blog'),
    path('product/<int:id>',views.product, name="product"),
    path('checkout/',views.checkout, name="checkout"),
    path('order_cart/',views.order_cart.as_view(), name='order_cart'),


]