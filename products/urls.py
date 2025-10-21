from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .servises.flash_sale import FlashSaleListCreateView, check_flash_sale
from .views import ProductViewSet, ReviewViewSet, CategoryViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sale/', FlashSaleListCreateView.as_view(), name='sale'),
    path('check-sale/<int:product_id>/', check_flash_sale, name='product-view-history-create'),
]