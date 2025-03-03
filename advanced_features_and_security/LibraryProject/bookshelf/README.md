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


# Security Measures

This Django application implements the following security measures:
- Secure settings (e.g., `DEBUG = False`, `CSRF_COOKIE_SECURE = True`).
- Role-based and permission-based access control.
- CSRF protection for all forms.
- Content Security Policy (CSP) to reduce XSS risks.
- Secure data handling using Django’s ORM and forms.