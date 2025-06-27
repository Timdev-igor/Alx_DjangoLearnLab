# readme 
created app name tenet1
register app in settings
# models&orm
making models and their relationships
migrating
executing them in shell/running a script
# admin view
create a superuser
`python manage.py createsuperuser`

register the models in admin 
the url is already regestier in project 
`urlpatterns = [ path('admin/', admin.site.urls),]`
    
run server
## model relationships
# Without optimization (Multiple queries)
books = Book.objects.all()
for book in books:
    print(book.author.name)  # Extra query per book!

# Optimized (Joins author table in one query)
books = Book.objects.select_related("author").all()
## For Many-to-Many or Reverse ForeignKey, use
books = Book.objects.prefetch_related("reviews").all()
## views and url config
register ur views in app/urls and also make sure ur app views are registad in the projects url 
`path('app_name/', include('app_name.urls')),` -relpace app_name with the actual name of ur app
in app/urls register urls like :
# httpresponse 
`urlpatterns = [path('hello/', hello_view, name='hello'),]`
# CBV
`urlpatterns = [path('hello-cbv/', HelloView.as_view(), name='hello_cbv'),]`
## Note: .as_view() is required to convert the class-based view into a callable view.

## Generic Class-Based Views 
`Generic Class-Based Views urlpatterns = [ path('books/', BookListView.as_view(), name='book_list'),]`
listview,detailview,etc
## url register views

## template and static content
impliment statics in settings
create the static directory and store the static files eg images ,css,js
forms!

## user authentication
-new user accounts creation:
     signup,login,logout,profile--1 create the views in views.py
     mostly using CBV and include reverse_lazy if necessarry
     make the templates
     define redirects in settings.py
     reverse_lazy='' //for redirects

## custo user models and auth
refer to new app===customuser / useraccount

Username (leave blank to use 'tim'): andre
Email address: timothyochiengdev@gmail.com
Password: 1234####
Password (again):
Superuser created successfully.
PS C:\django_stuff\telesto> 