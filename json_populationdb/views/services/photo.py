from datetime import datetime
import base64
from pyramid.view import view_config
from pyramid.response import Response
from ...models import Person

import logging
log = logging.getLogger(__name__)

@view_config(route_name='photo', renderer='json', request_method='PUT')
def put_photo(request):
    error = None
    personcode = request.matchdict.get('code')
    body = request.json_body
    if not body:    
        error = 'Body is missing or not JSON'
    elif not personcode:
        error = 'Person code missing'
    else:
        q = request.dbsession.query(Person)
        q = q.filter(Person.personcode==personcode)

        if q.count() == 0:
            error = 'Person not found.'
        else:
            imgdata = body.get('photo')
            if not imgdata:
                error = 'Photo missing'
            else:
                img = base64.b64decode(imgdata)
                p = q.first()
                p.photo = img

    if error:
        message = error
        rc = 0
    else:
        rc = 1
        message = 'File saved successfully'

    return {'rc': rc,
            'message': message
            }
