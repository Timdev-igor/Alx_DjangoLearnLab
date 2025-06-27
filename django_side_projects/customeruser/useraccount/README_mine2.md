## custom user  and authentication
`this will cover creating custom user models`
## 1
define the user model
register authentication in settings
## 2
  We'll create a custom authentication backend that allows users to log in using their email.
    creating an authentication file
    update settings.py to have
                     """
                      AUTHENTICATION_BACKENDS = [
                    'your_app.auth_backends.EmailBackend',  # Custom email login backend
                    'django.contrib.auth.backends.ModelBackend',  # Default Django backend (keep this)
                       ]

                       """
## 3 
create forms.py  to handle user registration and login.//
   Inside useraccount/forms.py, create a registration and login form:
## 4 
create views for Registration and Login
define the logic to handle user authentication.
# 5
define urls
make the template views
run the project //

## permission and authorization
Add rest_framework.authtoken to INSTALLED_APPS in settings.py:
add auth acces in settings 
add endpoint for users to get authenticated//urls
make views with permissions for authenticated users only



## APIs
add rest framework into installed apps
define ur model
create a serializer for ur model(serializer.py)
define a view for the model
define url and run (http://127.0.0.1:8000/user/books/)
**adding extra fields
## serializers  and query sets
validation
making nested serializers == when retrieving a Book, it includes its Author and Reviews.
