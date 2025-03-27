# Social Media API - Posts & Comments

## Endpoints

### Posts
- `GET /api/posts/` - List all posts (paginated)
- `POST /api/posts/` - Create a post (Auth required)
- `GET /api/posts/{id}/` - Retrieve a single post
- `PUT /api/posts/{id}/` - Update a post (Author only)
- `DELETE /api/posts/{id}/` - Delete a post (Author only)


### Comments
- `GET /api/comments/` - List all comments (paginated)
- `POST /api/comments/` - Create a comment (Auth required)
- `GET /api/comments/{id}/` - Retrieve a single comment
- `PUT /api/comments/{id}/` - Update a comment (Author only)
- `DELETE /api/comments/{id}/` - Delete a comment (Author only)

## Authentication
- Token-based authentication is required for creating posts/comments.