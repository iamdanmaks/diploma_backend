import requests
import uuid

from flask import current_app
from flask_babel import _

from app.main import db, client
from app.main.model.organization import Organization
from app.main.model.voice import Voice


def add_voice(data, file):
    new_voice = Voice(
        public_id=str(uuid.uuid4()),
        name=data.get('name'),
        description=data.get('description'),
    )
    
    # call the voice microservice
    resp = requests.post(
        current_app.config['VOICE_MICROSERVICE_URL'] + '/voice/',
        json={
            "public_id": new_voice.public_id,
            "file": file
        }
    )

    db.session.add(new_voice)
    
    organization = Organization.query.filter_by(public_id=data.get('organization')).first()
    organization.voice_id.append(new_voice)
    
    db.session.commit()
    return {
        'status': 'success',
        'message': _('Voice was saved')
    }, 201


def edit_voice(public_id, data):
    voice = Voice.query.filter_by(public_id=public_id).first()
    if voice:
        if data.get('name'):
            voice.name = data.get('name')
        if data.get('description'):
            voice.description = data.get('description')
        db.session.commit()

        return {
            'status': 'success',
            'message': _('Voice data was edited')
        }, 200
    else:
        return {
            'status': 'fail',
            'message': _('Voice not found')
        }, 404


def remove_voice(public_id):
    try:
        # delete the file from cloud storage
        voice = Voice.query.filter_by(public_id=public_id).first()
        organization = Organization.query.filter_by(id=voice.organization_id).first()
        organization.voice_id.remove(voice)

        for q in voice.query_id:
            q.voice_id = None

        Voice.query.filter_by(public_id=public_id).delete()
        db.session.commit()

        return {
            'status': 'success',
            'message': _('Voice was removed')
        }, 200
    except Exception as e:
        print(e)
        return {
            'status': 'fail',
            'message': _('Voice not found')
        }, 404


def map_voice(voice):
    return {
        'public_id': voice.public_id,
        'name': voice.name,
        'description': voice.description,
        'url': client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': current_app.config['BUCKET_NAME'],
                'Key': voice.public_id + '.wav'
            },
            ExpiresIn=3600
        )
    }


def get_voice(public_id):
    voice = Voice.query.filter_by(public_id=public_id).first()
    if voice:
        return map_voice(voice), 200
    else:
        return {
            'status': 'fail',
            'message': _('Voice not found')
        }, 404


def get_general_voice_list():
    general_voices = Voice.query.filter_by(is_general=True)
    mapped = []
    for v in general_voices:
        mapped.append(map_voice(v))
    
    return mapped, 200


def get_voices_list(organization_id):
    organization = Organization.query.filter_by(public_id=organization_id).first()
    general_voices = Voice.query.filter_by(is_general=True)

    if organization:
        voices = list(organization.voice_id) + list(general_voices)
    else:
        voices = general_voices

    mapped = []
    for v in voices:
        mapped.append(map_voice(v))
    
    return mapped, 200
