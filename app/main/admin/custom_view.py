from flask_admin.contrib.sqla import ModelView


class CustomModelView(ModelView):
    can_edit = True
    can_delete = True
    page_size = 50
    create_modal = True
    edit_modal = True


class UserView(CustomModelView):
    column_exclude_list = ['password_hash', ]
    column_searchable_list = ['first_name', 'last_name', 'email', 'apply_reason', 'public_id']
    column_filters = [
        'email', 
        'admin', 
        'organization_id', 
        'registration_date', 
        'email_confirmed', 
        'organization_confirmed'
    ]


class OrganizationView(CustomModelView):
    column_searchable_list = ['name', 'description', 'public_id']
    column_filters = [
        'is_demo',
        'registration_date'
    ]


class VoiceView(CustomModelView):
    column_searchable_list = ['name', 'description', 'public_id']
    column_filters = [
        'is_general'
    ]


class QueryView(CustomModelView):
    column_searchable_list = ['public_id', 'text']
    column_filters = [
        'date',
        'lang'
    ]


class UnsignedQueryView(CustomModelView):
    column_searchable_list = ['ip_address']
    column_filters = [
        'last_query'
    ]
