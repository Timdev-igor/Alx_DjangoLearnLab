
"""
In this example, the MyModelListCreateAPIView inherits from the ListCreateAPIView 
class provided by DRF. The queryset attribute is set to MyModel.objects.all(),
 which fetches all instances of the MyModel model.
The get_queryset() method is overridden to add a dynamic filter based on the name query parameter.

from rest_framework import generics
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

    def get_queryset(self):
        queryset = self.queryset
        name_filter = self.request.query_params.get('name', None)
        if name_filter is not None:
            queryset = queryset.filter(name__icontains=name_filter)
        return queryset
    """
from rest_framework import serializers
from .models import Book
from datetime import datetime

#serializer.py for ur model 
class BookSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()# custom field
    class Meta:
        model = Book
        fields = '__all__'

    #VALIDATION./In this example, 
    # the validate method checks if the name field in the incoming data is at least 5 characters long.
    #  If the validation fails,
    # a ValidationError is raised, which will be returned to the client in the response.
    
    def validate(self, data):
        if len(data['title']) < 5:
            raise serializers.ValidationError("Name must be at least 5 characters long.")
        return data
    #ADDING CUSTOM FIELD In this example,
    #  the days_since_created field is a custom field 
    # that calculates the number of days since the model instance was created.
    def get_days_since_created(self, obj):
      return (datetime.now().date() - obj.published_date).days  # ✅ Convert to date
    
