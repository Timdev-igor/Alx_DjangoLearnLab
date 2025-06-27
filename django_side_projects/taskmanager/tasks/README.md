## covering apis

## *** Getting started ##
-add rest_framework in INSTALLEDAPPS
-define ur model
-serialize ur model with all or specific fields
-define a  API view for ur model
-defin url and run

# Serializers and QuerySets in DRF
-validation `DRF serializers include built-in validation mechanisms to ensure data integrity. `
-Customizing Serializers==Adding custom fields `days since created instance`
                          Performing validation`name be > 5 len `
                          Handling complex data structureS
                          Overriding default behavior

-QuerySets and Filtering 

class MyModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

    def get_queryset(self):
        queryset = self.queryset
        name_filter = self.request.query_params.get('name', None)
        if name_filter is not None:
            queryset = queryset.filter(name__icontains=name_filter)
        return queryset

## Optimizing QuerySets for Performance
-  Select Related and Prefetch Related: Optimize database queries by pre-fetching related data to avoid unnecessary database hits.
- Using Values and Values List: Retrieve only specific fields instead of the entire model instance to reduce data transfer.
- Caching: Cache frequently accessed queryset results to improve response times.

## ViewSets and Routers in DRF
- viewset automaticaly provide 
    list: Retrieve a list of model instances.
    create: Create a new model instance.
    retrieve: Retrieve a single model instance.
    update: Update a model instance.
    partial_update: Update a model instance with a partial set of fields.
    destroy: Delete a model instance.
- You can further customize the ViewSet by overriding or adding new methods to handle specific business logic.

## Types of ViewSets

  DRF provides several types of ViewSets, each offering different levels of functionality:

    ModelViewSet: Provides a complete set of CRUD operations for a model, including list, retrieve, create, update, and delete actions.
    ReadOnlyModelViewSet: Offers read-only operations, such as list and retrieve, suitable for exposing data without allowing modifications.
    ViewSet: A base class that allows you to define custom actions and implement specific API behavior.

## Automatic URL Routing
Routers in DRF are used to automatically generate URL patterns for your API endpoints based on the ViewSets you’ve defined
## Combining ViewSets and Routers
   router = DefaultRouter()
router.register(r'my-models', MyModelViewSet)
router.register(r'another-models', AnotherModelViewSet)

## Authentication and Permissions in DRF
