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
        fields = ["id","salad","cheese","meat"]
    
        
        
# CustomerDetail Serializer :

class CustomerDetailSerializer(ModelSerializer):
    class Meta:
        model = CustomerDetail
        fields = ["id","deliveryAddress","phone","paymentType"]
    
    
        
        
# Oder serializer :

class OrderSerializer(ModelSerializer):
    ingredients = IngredientSerializer()  # Nesting IngredientSerializer
    customer = CustomerDetailSerializer() # Nesting CustomerDetailSerializer
    class Meta:
        model = Order
        fields = "__all__"
        
    def create(self,validated_data):
        #print("validated_data ------>",validated_data)
        ingredient_data = validated_data.pop("ingredients")
        customer_data = validated_data.pop("customer")
        ingredient_record = IngredientSerializer.create(
            IngredientSerializer(),validated_data=ingredient_data,
            )
        customer_record = CustomerDetailSerializer.create(
            CustomerDetailSerializer(),validated_data=customer_data
            )
        order= Order.objects.create(
            ingredients = ingredient_record,
            customer = customer_record,
            price = validated_data.pop("price"),
            orderTime = validated_data.pop("orderTime"),
            user = validated_data.pop("user"),
        )
        return order
    
    def update(self,instance,validated_data):
        # according to documentation update nested serializer :
        
        #print("validated_data ------>",validated_data)
        instance.price = validated_data.get("price",instance.price)
        instance.orderTime = validated_data.get("orderTime",instance.orderTime)
        
        
        # for IngredientSerializer
        
        instance_ingredients = instance.ingredients
        ingredient_data = validated_data.pop("ingredients")
        
        instance_ingredients.salad = ingredient_data.get('salad',instance_ingredients.salad)
        instance_ingredients.cheese = ingredient_data.get('cheese',instance_ingredients.cheese)
        instance_ingredients.meat = ingredient_data.get('meat',instance_ingredients.meat)
        instance_ingredients.save()
        
        # for CustomerDetailSerializer
        instance_customer = instance.customer
        customer_data = validated_data.pop("customer")
        
        instance_customer.deliveryAddress = customer_data.get('deliveryAddress',instance_customer.deliveryAddress)
        instance_customer.phone = customer_data.get('phone',instance_customer.phone)
        instance_customer.paymentType = customer_data.get('paymentType',instance_customer.paymentType) 
        instance_customer.save()           

        
        return instance