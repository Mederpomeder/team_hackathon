from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Order, Product
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

