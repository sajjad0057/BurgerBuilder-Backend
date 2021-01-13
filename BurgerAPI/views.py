from rest_framework.viewsets import ModelViewSet
from .models import UserProfile, Order,CustomerDetail,Ingredient
from .serializers import UserProfileSerializer, OrderSerializer

# Create your views here.

class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()



class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()