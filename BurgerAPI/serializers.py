from rest_framework.serializers import ModelSerializer
from .models import UserProfile, Order, CustomerDetail, Ingredient



# Customized User Model Serializer :


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id","email","password"]
        
        extra_kwargs = {
            "password": {
                "write_only" : True,
                "style" : {"input_type" : "password"},
            }
        }
    
    
    def create(self,validated_data):
        user = UserProfile.objects.create_user(
            email = validated_data["email"],
            password=validated_data["password"]
        )
        return user
    
    
# Ingredient Serializer

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        exclude = ["id"]
        
        
# CustomerDetail Serializer :

class CustomerDetailSerializer(ModelSerializer):
    class Meta:
        model = CustomerDetail
        fields = "__all__"
    
    
        
        
# Oder serializer :

class OrderSerializer(ModelSerializer):
    ingredients = IngredientSerializer()  # Nesting IngredientSerializer
    customer = CustomerDetailSerializer() # Nesting CustomerDetailSerializer
    class Meta:
        model = Order
        fields = "__all__"
        
    def create(self,validated_data):
        print("validated_data ------>",validated_data)
        ingredient_data = validated_data.pop("ingredients")
        customer_data = validated_data.pop("customer")
        ingredients = IngredientSerializer.create(
            IngredientSerializer(),validated_data=ingredient_data,
            )
        customer = CustomerDetailSerializer.create(
            CustomerDetailSerializer(),validated_data=customer_data
            )
        '''
        update_or_create() querySet accoreding to documentaion:
        -------------------------------------------------------------------
        Returns a tuple of (object, created), where object is the 
        created or updated object and created is a boolean specifying 
        whether a new object was created
        '''
        order,created= Order.objects.update_or_create(
            ingredients = ingredients,
            customer = customer,
            price = validated_data.pop("price"),
            orderTime = validated_data.pop("orderTime"),
            user = validated_data.pop("user"),
        )
        return order
