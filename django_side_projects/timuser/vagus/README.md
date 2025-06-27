### **User Authentication & Permissions in Django**  

#### **1️⃣ Creating Users**  
- **Using `AbstractUser` (Simple Approach)**  
  1. Create a custom model inheriting from `AbstractUser`.  
  2. Set `AUTH_USER_MODEL = 'myapp.CustomUser'` in `settings.py`.  
  3. Run `makemigrations` and `migrate`.  

- **Using `AbstractBaseUser` (Requires User Manager)**  
  1. Create a `UserManager` to handle user creation.  
  2. Define a custom user model inheriting from `AbstractBaseUser`.  
  3. Set `AUTH_USER_MODEL` in `settings.py`.  
  4. Run `makemigrations` and `migrate`.  

---

#### **2️⃣ Authentication Backend**  
- Create `authentication.py` and define email-based authentication:  
  ```python
  from django.contrib.auth.backends import BaseBackend
  from django.contrib.auth import get_user_model

  class EmailBackend(BaseBackend):
      def authenticate(self, request, email=None, password=None):
          User = get_user_model()
          try:
              user = User.objects.get(email=email)
              if user.check_password(password):
                  return user
          except User.DoesNotExist:
              return None

      def get_user(self, user_id):
          User = get_user_model()
          return User.objects.filter(pk=user_id).first()
  ```
- Add it to `AUTHENTICATION_BACKENDS` in `settings.py`:  
  ```python
  AUTHENTICATION_BACKENDS = ["myapp.authentication.EmailBackend", "django.contrib.auth.backends.ModelBackend"]
  ```

---

#### **3️⃣ Defining Views & URLs**  
- **Views (`views.py`)**:  
  ```python
  from django.shortcuts import render, redirect
  from django.contrib.auth import authenticate, login

  def login_view(request):
      if request.method == "POST":
          email = request.POST["email"]
          password = request.POST["password"]
          user = authenticate(request, email=email, password=password)
          if user:
              login(request, user)
              return redirect("home")
      return render(request, "login.html")
  ```
- **URLs (`urls.py`)**:  
  ```python
  from django.urls import path
  from myapp.views import login_view

  urlpatterns = [path("login/", login_view, name="login")]
  ```

---

#### **4️⃣ Templates & Permissions**  
- Create a **`login.html`** template with an email-password form.  
- Use Django's built-in **permissions** (`@login_required`, `@permission_required`).  

---

### **✅ Summary**  
- **Use `AbstractUser` for simple cases**, `AbstractBaseUser` for full customization.  
- **Create a custom authentication backend** for email login.  
- **Define views & templates** for user authentication.  
- **Use Django permissions** to control access.  

Let me know if you need more details! 🚀

