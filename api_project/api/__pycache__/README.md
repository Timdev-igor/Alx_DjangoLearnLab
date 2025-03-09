# Authentication & Authorization in `api_project`

This project uses **Token Authentication** to secure API endpoints. Below are the steps to register, obtain a token, and use it for authentication in API requests.

---

## 1. Register/Login a User
Before accessing the API, you need to create a user.

### Register a User
You can create a user using the Django admin panel or via the Django shell:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a username, email, and password.

---

## 2. Obtain an Authentication Token
Django REST Framework provides an endpoint to get a token for an authenticated user.

### Get a Token
Send a **POST request** to `/api-token-auth/` with your username and password:

```bash
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
     -d "username=your_username&password=your_password"
```

### Response Example
If authentication is successful, the response will contain a token:

```json
{
    "token": "your_generated_token"
}
```

---

## 3. Use the Token in API Requests
After obtaining the token, include it in the `Authorization` header of your requests.

### Example: Access Protected API Endpoint
```bash
curl -H "Authorization: Token your_generated_token" \
     http://127.0.0.1:8000/books_all/
```

If authentication is successful, you'll get a JSON response containing book data.

---

## 4. Testing with Postman
1. Open Postman and create a new request.
2. Select **Authorization → Bearer Token**.
3. Paste your token in the field.
4. Send a **GET** request to `http://127.0.0.1:8000/books_all/` to access the API.

---

## 5. Debugging Issues
- **403 Forbidden** → You might not have permission; check `permission_classes` in your views.
- **401 Unauthorized** → You didn’t provide a valid token in the request.
- **400 Bad Request** → Check if you’re sending the correct credentials.

---

## Next Steps
- Implement **user registration API** if needed (`dj-rest-auth` can help).
- Add **refresh tokens** using `djangorestframework-simplejwt`.

---

This should be enough for now! Let me know if you need more details. 🚀

