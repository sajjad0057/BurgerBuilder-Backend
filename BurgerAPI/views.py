from rest_framework.viewsets import ModelViewSet
from .models import UserProfile, Order,CustomerDetail,Ingredient
from .serializers import UserProfileSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()



class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    
    permission_classes = [
        #IsAuthenticated,
    ]
    
    
    # according To filtering Documentation in DRF :
    def get_queryset(self):
        queryset = Order.objects.all()
        id = self.request.query_params.get("id",None)
        if id is not None :
            queryset = queryset.filter(user__id=id)
            
        return queryset
    
'''
# By this query_set http://example.com/api/order?id=2  means thats link show just order id 2
if we don't pass ?id=2 end of this url,when show all orders

'''
    