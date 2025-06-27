Steps to Create Permissions
1. Define Permissions in Your Model

In your models.py, add a Meta class inside your model and define the permissions attribute. For example:
python
Copy

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        permissions = [
            ("can_view", "Can view post"),
            ("can_create", "Can create post"),
            ("can_edit", "Can edit post"),
            ("can_delete", "Can delete post"),
        ]

This creates four permissions:

    can_view: Allows users to view posts.

    can_create: Allows users to create posts.

    can_edit: Allows users to edit posts.

    can_delete: Allows users to delete posts.

2. Run Migrations

After defining permissions, run the following commands to apply the changes to your database:
bash
Copy

python manage.py makemigrations
python manage.py migrate

This will create the permissions in the database.
3. Assign Permissions to Groups or Users

You can assign permissions to groups or individual users via the Django admin panel or programmatically.
Using Django Admin:

    Go to the Django admin panel (/admin/).

    Navigate to Groups or Users.

    Select a group or user and assign the permissions.

Programmatically:
python
Copy

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

# Get the permission
content_type = ContentType.objects.get_for_model(Post)
permission = Permission.objects.get(codename='can_view', content_type=content_type)

# Assign to a user
user = User.objects.get(username='testuser')
user.user_permissions.add(permission)

# Assign to a group
group = Group.objects.get(name='Viewers')
group.permissions.add(permission)

4. Enforce Permissions in Views

Use the @permission_required decorator in your views to restrict access based on permissions. For example:
python
Copy

from django.contrib.auth.decorators import permission_required

@permission_required('app_name.can_view', raise_exception=True)
def view_post(request, post_id):
    # Your view logic here
    pass

5. Test Permissions

    Create test users and assign them permissions.

    Log in as each user and verify that they can only perform actions allowed by their permissions.

Summary

    Define permissions in the Meta class of your model.

    Run migrations to apply changes.

    Assign permissions to groups or users.

    Enforce permissions in views using @permission_required.

    Test your setup to ensure permissions work as expected.

That's it! You've successfully created and managed permissions in Django. 