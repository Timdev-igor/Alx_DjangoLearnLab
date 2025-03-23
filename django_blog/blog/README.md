## authentication
Register: ` http://127.0.0.1:8000/blog/register/`
- User fills out the registration form.
Login: `http://127.0.0.1:8000/blog/login/`
- User enters username and password.If valid, user is logged in and redirected to the profile page.
Logout:` http://127.0.0.1:8000/blog/logout/`
Profile:`http://127.0.0.1:8000/blog/profile/`
Only logged-in users can access this page (@login_required decorator is used)