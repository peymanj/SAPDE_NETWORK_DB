model_access_dict = {
    'user': {
        'read': 'Read',
        'create': 'Create',
        'update': 'Update',
        'delete': 'Delete',
        'search': {'name': 'Search', 'relation': 'read'},
        'related_read': {'name': 'Related read', 'relation': 'read'},
        'get_defaults': {'name': 'Get defaults', 'relation': 'read'},
    },
    'access': {
        'read': 'Read',
        'create': 'Create',
        'update': 'Update',
        'delete': 'Delete',
        'search': {'name': 'Search', 'relation': 'read'},
        'related_read': {'name': 'Related read', 'relation': 'read'},
        'get_defaults': {'name': 'Get defaults', 'relation': 'read'},
    },
    'user_access_relation': {
        'read': 'Read',
        'create': 'Create',
        'update': 'Update',
        'delete': 'Delete',
        'search': {'name': 'Search', 'relation': 'read'},
        'related_read': {'name': 'Related read', 'relation': 'read'},
        'get_defaults': {'name': 'Get defaults', 'relation': 'read'},
    },
    'database_management': {
        'read': 'Backup and Restore',
        'backup': {'name': 'Backup Database', 'relation': 'read'},
        'restore': {'name': 'Restore Database', 'relation': 'read'},
        'get_active_db_name': {'name': 'Read Active DB Name', 'relation': 'read'},
    },
    'translation': {
        'read': 'Read',
        'create': 'Create',
        'update': 'Update',
        'delete': 'Delete',
        'search': {'name': 'Search', 'relation': 'read'},
        'related_read': {'name': 'Related read', 'relation': 'read'},
        'get_defaults': {'name': 'Get defaults', 'relation': 'read'},
    },
}

view_access_dict = {
    'UiUserForm': {
        'list': 'List view',
        'form': 'Detail view',
        'create': 'Create',
        'update': 'Update',
        'delete': 'Delete',
    },
    'UiAccessForm': {
        'list': 'List view',
        'form': 'Detail view',
        'create': 'Create',
        'update': 'Update',
        'delete': 'Delete',
    },
    'UiUserAccessForm': {
        'list': 'List view',
        'form': 'Detail view',
        'create': 'Create',
        'update': 'Update',
        'delete': 'Delete',
    },
    'UiDatabaseManagementForm': {
        'list': 'Database Management',
    },
    'UiTranslationForm': {
        'list': 'List view',
        'form': 'Detail view',
        'create': 'Create',
        'update': 'Update',
        'delete': 'Delete',
    },
}