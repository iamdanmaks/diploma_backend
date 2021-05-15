import uuid
import datetime
from flask import current_app, render_template
from flask_mail import Message
from flask_babel import _
from itsdangerous import URLSafeTimedSerializer

from .token_service import encode_auth_token, decode_auth_token
from app.main import db, mail
from app.main.model.user import User
from app.main.model.organization import Organization


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            apply_reason=data['apply_reason'],
            registration_date=datetime.datetime.utcnow()
        )
        
        organization = Organization.query.filter_by(name=data['organization_name']).first()

        if not organization:
            organization = Organization(
                name=data['organization_name'],
                public_id=str(uuid.uuid4()),
                registration_date=datetime.datetime.utcnow()
            )
            organization.api_token = encode_auth_token(
                    days=365*1000, 
                    seconds=5, 
                    organization_id=organization.public_id
                )
            new_user.organization_admin = True
            db.session.add(organization)
        elif organization != True:
            return {
                'status': 'fail',
                'message': _('Organization already exists. You should be invited or change the name of organization')
            }, 401

        save_changes(new_user)

        organization.user_id.append(new_user)

        db.session.commit()

        send_email(
            'Please, confirm your email',
            render_template('activate.html', 
            confirm_url=f"http://localhost:5000/user/confirm?token={generate_confirmation_token({'email': new_user.email})}"),
            new_user.email
        )

        response_object = {
            'status': 'success',
            'message': _('Successfully registered.')
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': _('User already exists. Please Log in.'),
        }
        return response_object, 409


# ===== EMAIL FUNCTIONS =====

def send_email(subject, template, to):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_USERNAME']
    )
    mail.send(msg)


def confirm_email(token):
    try:
        data = confirm_token(token)
        email = data.get('email')
    except:
        return {
            'status': 'fail',
            'message': _('The confirmation link is invalid or has expired')
        }, 400
    if email:
        user = User.query.filter_by(email=email).first()
        user.email_confirmed = True
        db.session.commit()
        return {
            'status': 'success',
            'message': _('Email was confirmed'),
            'Authorization': encode_auth_token(days=1, seconds=5, user_id=user.public_id)
        }, 200
    else:
        return {
            'status': 'fail',
            'message': 'User not found'
        }, 404


def generate_confirmation_token(info):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(info, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        info = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return info


def get_user_by_token(token):
    return User.query.filter_by(public_id=decode_auth_token(token)[0]).first()


def invite_user(token, email):
    user = get_user_by_token(token)
    
    pub_id = str(uuid.uuid4())
    
    new_user = User(
        public_id=pub_id,
        email=email,
        username=pub_id,
        password=pub_id,
        apply_reason=f"Invited by {user.username} on {str(datetime.datetime.utcnow())}",
        registration_date=datetime.datetime.utcnow()
    )

    organization = Organization.query.filter_by(id=user.organization_id).first()
    organization.user_id.append(new_user)

    save_changes(new_user)

    send_email(
        f'You were invited to {organization.name} by {user.first_name} {user.last_name}',
        render_template('register.html', 
        # invite link should be changed after frontend
        confirm_url=f"http://localhost:5000/user/confirm?token={generate_confirmation_token({'email': new_user.email})}"),
        new_user.email
    )

    return {
        'status': 'success',
        'message': _('New user was invited')
    }, 200


# ===== PASSWORD RESET =====
def reset_link(email):
    send_email(
        f"You've tried to reset password",
        render_template('register.html', 
        # reset link should be changed after frontend
        confirm_url=f"http://localhost:5000/user/reset-password?token={generate_confirmation_token({'email': new_user.email})}"),
        email
    )

    return {
        'status': 'success',
        'message': _('New user was invited')
    }, 200


def reset_password(token, password):
    try:
        data = confirm_token(token)
        email = data.get('email')
    except:
        return {
            'status': 'fail',
            'message': _('The confirmation link is invalid or has expired')
        }, 400
    if email:
        user = User.query.filter_by(email=email).first()
        user.password = password
        db.session.commit()
        return {
            'status': 'success',
            'message': _('Password was reset')
        }, 200
    else:
        return {
            'status': 'fail',
            'message': _('User not found')
        }, 404


# ===== CRUD =====
def map_user(user):
    return {
        'public_id': user.public_id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'registration_date': str(user.registration_date),
        'organization_admin': user.organization_admin
    }


def get_a_user(token):
    user = get_user_by_token(token)
    if user:
        return {
            'public_id': user.public_id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'registration_date': str(user.registration_date),
            'organization_admin': user.organization_admin
        }, 200
    else:
        return {
            'status': 'fail',
            'message': _('User not found')
        }, 404


def edit_user(token, data):
    user = get_user_by_token(token)

    if user:
        if 'first_name' in data:
            user.first_name = data.get('first_name')
        if 'last_name' in data:
            user.last_name = data.get('last_name')
        if 'username' in data:
            if not User.query.filter_by(username=data.get('username')).first():
                user.username = data.get('username')
                user.password = data.get('password')
            else:
                return {
                    'status': 'fail',
                    'message': _('Username is already taken')
                }, 400
        if 'new_password' in data:
            if user.check_password(data.get('old_password')):
                user.password = data.get('new_password')
            else:
                return {
                    'status': 'fail',
                    'message': _('Password is wrong')
                }, 401
        
        db.session.commit()
        return {
            'status': 'success',
            'message': _('Profile was successfully edited')
        }, 200

    else:
        return {
            'status': 'fail',
            'message': _('User not found')
        }, 404


def delete_user(token):
    try:
        User.query.filter_by(public_id=decode_auth_token(token)[0]).delete()
        db.session.commit()
    except Exception as e:
        print(e)
        return {
            'status': 'fail',
            'message': _('Something went wrong')
        }, 400

    return {
        'status': 'success',
        'message': _('Profile was successfully deleted')
    }, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()
