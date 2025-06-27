import requests

# Step 1: Get a token
url = 'http://127.0.0.1:8000/api-token-auth/'
data = {'username': 'admin', 'password': 'adminpassword'}  # Use your superuser credentials
response = requests.post(url, data=data)
token = response.json().get('token')
print("Token:", token)

# Step 2: Use the token to access the API
headers = {'Authorization': f'Token {token}'}

# Create a post
data = {'title': 'My First Post', 'content': 'This is a test post.'}
response = requests.post('http://127.0.0.1:8000/api/posts/', headers=headers, json=data)
print("Create Post Response:", response.json())

# List posts
response = requests.get('http://127.0.0.1:8000/api/posts/', headers=headers)
print("List Posts Response:", response.json())

# Update a post (replace `1` with the ID of the post you want to update)
post_id = response.json()[0]['id']
data = {'title': 'Updated Post', 'content': 'This post has been updated.'}
response = requests.put(f'http://127.0.0.1:8000/api/posts/{post_id}/', headers=headers, json=data)
print("Update Post Response:", response.json())

# Delete a post (replace `1` with the ID of the post you want to delete)
response = requests.delete(f'http://127.0.0.1:8000/api/posts/{post_id}/', headers=headers)
print("Delete Post Response:", response.status_code)