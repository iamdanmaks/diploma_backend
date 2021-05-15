import requests
import time
import uuid
from datetime import datetime

from flask import current_app

from app.main import db, client
from app.main.model.query import Query
from app.main.model.unsigned_query import UnsignedQuery
from app.main.model.voice import Voice
from app.main.model.organization import Organization

from flask_babel import _


def signed_voicing_query(data):
    new_query = Query(
        public_id=str(uuid.uuid4()),
        text=data.get('text')
    )

    voice = Voice.query.filter_by(public_id=data.get('voice')).first()

    start = time.time()
    
    resp = requests.post(
        current_app.config['TACOTRON_MICROSERVICE_URL'] + '/voice/',
        json={
            'voice_id': voice.public_id,
            'query_id': new_query.public_id,
            'text': data.get('text')
        }
    )
    
    new_query.time_processed = time.time() - start

    db.session.add(new_query)

    organization = Organization.query.filter_by(public_id=data.get('organization')).first()

    organization.query_id.append(new_query)
    voice.query_id.append(new_query)

    db.session.commit()

    return {
        'status': 'success',
        'message': _('Query was processed'),
        'result': client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': current_app.config['BUCKET_NAME'],
                'Key': new_query.public_id + '.wav'
            },
            ExpiresIn=3600
        )
    }, 200


def unsigned_voicing_query(ip_address, data):
    caller = UnsignedQuery.query.filter_by(ip_address=ip_address).first()
    token_num = len(data.get('text'))
    
    if caller:
        if caller.last_query < datetime.utcnow():
            caller.tokens_left = 1000 - token_num
            caller.last_query = datetime.utcnow()
        else:
            if caller.tokens_left >= token_num:
                caller.tokens_left -= token_num
                caller.last_query = datetime.utcnow()
            else:
                return {
                    'status': 'fail',
                    'message': _('Not enough free tokens')
                }, 400
    else:
        new_caller = UnsignedQuery(
            ip_address=ip_address,
            tokens_left=1000-token_num,
            last_query=datetime.utcnow()
        )

        db.session.add(new_caller)
        db.session.commit()

    qid = ip_address

    resp = requests.post(
        current_app.config['TACOTRON_MICROSERVICE_URL'] + '/voice/',
        json={
            'voice_id': data.get('public_id'),
            'query_id': qid,
            'text': data.get('text')
        }
    )

    return {
        'status': 'success',
        'message': _('Query was processed'),
        'result': client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': current_app.config['BUCKET_NAME'],
                'Key': qid + '.wav'
            },
            ExpiresIn=3600
        )
    }


def map_query(query):
    voice = Voice.query.filter_by(id=query.voice_id).first()

    if voice:
        voice_name = voice.name
    else:
        voice_name = None

    return {
        'text': query.text,
        'date': str(query.date),
        'language': query.lang,
        'time_processed': query.time_processed,
        'voice': voice_name,
        'url': client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': current_app.config['BUCKET_NAME'],
                'Key': query.public_id + '.wav'
            },
            ExpiresIn=3600
        )
    }


def get_queries(organization_id):
    organization = Organization.query.filter_by(public_id=organization_id).first()

    queries = Query.query.filter_by(organization_id=organization.id)

    mapped = []
    for q in queries:
        mapped.append(map_query(q))

    return mapped, 200
