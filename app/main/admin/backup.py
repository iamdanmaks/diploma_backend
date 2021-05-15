import base64
import gzip
import pickle

from datetime import datetime
from flask import Response
from flask import request
from flask import redirect
from flask import url_for
from flask_admin import BaseView, expose

from app.main import db
from app.main.model import User
from app.main.model import Organization
from app.main.model import Query
from app.main.model import Voice
from app.main.model import UnsignedQuery
from app.main.model import BlacklistToken


class BackupView(BaseView):
    @expose('/')
    def index(self):
        return self.render(
            'backup.html'
        )
    
    @expose('/make_backup')
    def copy(self):
        database = {
            'user': list(User.query.all()),
            'organization': list(Organization.query.all()),
            'voice': list(Voice.query.all()),
            'query': list(Query.query.all()),
            'unsigned_query': list(UnsignedQuery.query.all()),
            'blacklist_tokens': list(BlacklistToken.query.all())
        }
        data = pickle.dumps(database)
        data = gzip.compress(data)
        data = base64.b64encode(data).decode('utf-8')
        
        return Response(data,
            mimetype='plain/txt',
            headers={'Content-Disposition': f'attachment;filename=easyvoice-{datetime.now().strftime("%m/%d/%Y:%H.%M")}.backup'})
    

    @expose('/restore_backup', methods=['POST'])
    def restore(self):
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
            print(f'Clear table {table}')
        db.session.commit()
        
        backup = request.files.get('backup')
        backup = base64.b64decode(backup.read())
        backup = gzip.decompress(backup)
        backup = pickle.loads(backup)
        
        def key_predicate(key):
            return not key.startswith('_') and key != 'id'

        for k, v in backup.items():
            for inst in v:
                if k != 'query':
                    newobj = inst.__class__()
                else:
                    newobj = inst.__class__(inst.public_id, inst.text)
                d = {ke: va for ke, va in inst.__dict__.items() if key_predicate(ke)}
                newobj.__dict__.update(d)
                db.session.add(newobj)
        db.session.commit()
        
        return redirect(url_for('backup.index'))
