# Authentication System - Django Blog

## Features
- User Registration
- User Login & Logout
- Profile Management (Edit Username, Email, Bio, Profile Picture)
- CSRF Security
- Password Encryption

## How to Test
1. Run the server:
   ```bash
   python manage.py runserver
# Django Blog - Post Management

## Features
- List all posts
- View individual posts
- Create new posts (Authenticated users)
- Edit and delete posts (Only post authors)

## URLs
- `/posts/` → View all posts
- `/posts/new/` → Create a post
- `/posts/<id>/` → View a post
- `/posts/<id>/edit/` → Edit a post (Only author)
- `/posts/<id>/delete/` → Delete a post (Only author)
# Blog Post Management Features

This project includes CRUD (Create, Read, Update, Delete) functionality for blog posts.


## Permissions

- Only authenticated users can create posts.
- Only the author of a post can edit or delete it.
- All users can view posts.
# Comment Functionality

This feature allows users to leave comments on blog posts. Authenticated users can also edit or delete their comments.

## Features

1. **Add a Comment**: Authenticated users can add comments to posts.
2. **Edit a Comment**: Comment authors can edit their comments.
3. **Delete a Comment**: Comment authors can delete their comments.

## URLs

- Add a Comment: `/post/<int:post_id>/comment/new/`
- Edit a Comment: `/comment/<int:pk>/edit/`
- Delete a Comment: `/comment/<int:pk>/delete/`

## Installation
1. Clone the repo: `git clone https://github.com/yourusername/Alx_DjangoLearnLab.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Start the server: `python manage.py runserver`
# Tagging and Search Functionality

## Tagging
- Add tags to posts during creation or editing.
- Click on a tag to view all posts with that tag.

## Search
- Use the search bar to find posts by title, content, or tags.

## URLs
- Search: `/search/?q=<query>`
- Posts by Tag: `/tags/<tag_name>/`