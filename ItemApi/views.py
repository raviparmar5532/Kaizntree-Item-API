from .models import Item, Tag
from .serializers import ItemSerializer
from datetime import datetime
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner

class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    #Enabling custom filters
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(user = user)

        #from to created_on date filter
        from_created_on_parameter = self.request.query_params.get('from_created_on', datetime.min)
        to_created_on_parameter = self.request.query_params.get('to_created_on', datetime.now())
        queryset = queryset.filter(created_on__range = (from_created_on_parameter, to_created_on_parameter))

        #filter by stock available (available_stock > 0)
        stock_available_parameter = self.request.query_params.get('stock_available', None)
        if stock_available_parameter:
            queryset = queryset.filter(available_stock__gt=0)


        return queryset
