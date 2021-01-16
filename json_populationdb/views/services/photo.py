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
    status_code = 400
    try:
        personcode = request.matchdict.get('code')
        body = request.json_body
        if not personcode:
            error = 'Person code missing'
        else:
            q = request.dbsession.query(Person)
            q = q.filter(Person.personcode==personcode)
            p = q.first()
            if not p:
                error = 'Person not found'
                status_code = 404
            else:
                imgdata = body.get('photo')
                if not imgdata:
                    error = 'Photo missing'
                else:
                    img = base64.b64decode(imgdata)
                    p.photo = img
                    request.tm.commit()
                    request.tm.begin()
                    res = {'message': 'Photo updated successfully'}
                    return res
    except Exception as ex:
        request.tm.abort()
        request.tm.begin()
        error = 'error occurred'
    request.response.status_code = status_code
    res = {'error': error}
    return res

