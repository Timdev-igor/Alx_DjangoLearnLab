# Permissions and Groups Setup

This Django application uses custom permissions and groups to control access to specific parts of the app.

## Permissions
- `can_view`: Allows viewing of posts.
- `can_create`: Allows creating new posts.
- `can_edit`: Allows editing existing posts.
- `can_delete`: Allows deleting posts.

## Groups
- **Viewers**: Can view posts.
- **Editors**: Can view, create, and edit posts.
- **Admins**: Can perform all actions (view, create, edit, delete).

## How to Use
1. Assign users to groups in the Django admin panel.
2. Use the `@permission_required` decorator in views to enforce permissions.