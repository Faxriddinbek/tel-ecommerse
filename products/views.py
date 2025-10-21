from django.db import models
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Product, Review, Category
from products.serializers import ProductSerializer, ReviewSerializer, CategorySerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all() #queryset(qaysi ma'lumotlar bilan ishlash kerakligini ko'rsatadi)
    serializer_class = ProductSerializer #serializer_class (shumodelni JSON formatka o'tkazishligini ifodalaydi)

    def list(self, request, *args, **kwargs): #list(metod)=> bu maxsulotlarni ko'rish uchun
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category) #agar catigory bo'lsa productlarni faqat shu kategoriyaga oidligini tekshiradi
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):# retrieve(bu faqat id orqali bitta productni oladi)
        instance = self.get_object()# id ga tegishli productnio oladi
        serializer = self.get_serializer(instance) # instance ni jsonga o'tkazadi
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5] #related_products shu katigoriyadagi productlarni 5 tasini oladi
        related_serializer = ProductSerializer(related_products, many=True) #ularni ham jsonga o'tkazadi
        return Response({
            'product': serializer.data,
            'related_products': related_serializer.data
        })
    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating = models.Avg('reviews__rating')).order_by('-avg_rating')[:2] # annotate yordamida har bir maxsulotga o'rtacha baxo qo'shadi
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data) # buesa jsonga o'tkasib beradi

    @action(detail=False, methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count()==0:
            return Response({'average_rating': 'No reviews yet!'})

        avg_rating = sum([review.rating for review in reviews]) / reviews.count()

        return Response({"average_rating": avg_rating})