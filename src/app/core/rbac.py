from app.core.settings import settings

PERMISSION_DESCRIPTIONS: dict[str, str] = {
    'users:list': 'List users',
    'users:read': 'Read user',
    'users:create': 'Create user',
    'users:update': 'Update user',
    'users:delete': 'Delete user',
    'groups:list': 'List groups',
    'groups:read': 'Read group',
    'groups:create': 'Create group',
    'groups:update': 'Update group',
    'groups:delete': 'Delete group',
    'courses:list': 'List courses',
    'courses:read': 'Read course',
    'courses:create': 'Create course',
    'courses:update': 'Update course',
    'courses:delete': 'Delete course',
    'grades:list': 'List grades',
    'analytics:read': 'Read analytics',
    'auth:me': 'Read current user',
    'roles:update': 'Update user roles',
}


INITIAL_ROLE_SCOPES: dict[str, list[str]] = {
    settings.rbac.public_role: [
        'auth:me',
        'courses:list',
        'courses:read',
        'groups:read',
        'grades:list',
        'analytics:read',
    ],
    settings.rbac.student_role: [
        'auth:me',
        'courses:list',
        'courses:read',
        'groups:read',
        'grades:list',
        'analytics:read',
    ],
    settings.rbac.curator_role: [
        'auth:me',
        'users:list',
        'users:read',
        'groups:list',
        'groups:read',
        'courses:list',
        'courses:read',
        'grades:list',
        'analytics:read',
    ],
    settings.rbac.admin_role: ['*'],
}
