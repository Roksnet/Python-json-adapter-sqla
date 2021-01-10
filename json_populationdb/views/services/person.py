from datetime import datetime
import base64
from pyramid.view import view_config
from pyramid.response import Response
from ...models import Person
import sqlalchemy
import json
import logging
log = logging.getLogger(__name__)

MAX_ITEMS = 20

@view_config(route_name='persons', renderer='json', request_method='GET')
def list_persons(request):
    "Service for searching persons"
    # input: search criteria (givenname, surname, code)
    # output: list of persons matching search criteria
    errstatus = 400 # bad request
    error = None
    try:
        params = request.params
        givenname = params.get('givenname')
        surname = params.get('surname')    
        personcode = params.get('personcode')
        try:
            max_results = params.get('max_results') or MAX_ITEMS
        except:
            error = 'Invalid max_results'

        if not error:
            errstatus = 500 # internal server error
            
            # Option 1: query using SQLAlchemy object relational mapping (ORM)
            #error, items = _query_persons_orm(request, givenname, surname, personcode, max_results)

            # Option 2: query using SQLAlchemy plain SQL
            error, items = _query_persons_sql(request, givenname, surname, personcode, max_results)

            if not error:
                res = {'items': items}
                return res
            
    except Exception as ex:
        log.error(ex)
        error = 'error occurred'
        
    res = {'error': error}
    return Response(json.dumps(res), status=errstatus)

def _query_persons_orm(request, givenname, surname, personcode, max_results):
    "Persons query using SQLAlchemy ORM"
    error = None
    persons = []
    q = request.dbsession.query(Person)
    if givenname:
        q = q.filter(Person.givenname.ilike(givenname))
    if surname:
        q = q.filter(Person.surname.ilike(surname))
    if personcode:
        q = q.filter(Person.personcode==personcode)

    if not personcode and not surname:
        error = 'Parameters are missing or invalid.'
    else:
        q = q.limit(max_results)
        for p in q.all():
            item = {'personcode': p.personcode,
                    'givenname': p.givenname,
                    'surname': p.surname,
                    }
            persons.append(item)
    return error, persons

def _query_persons_sql(request, givenname, surname, personcode, max_results):
    "Persons query using plain SQL"
    error = None
    persons = []
    params = {}
    sql = 'SELECT personcode, givenname, surname FROM person'
    if givenname:
        sql += ' WHERE givenname LIKE :givenname'
        params['givenname'] = givenname
    if surname:
        sql += ' WHERE surname LIKE :surname'
        params['surname'] = surname
    if personcode:
        sql += ' WHERE personcode=:personcode'
        params['personcode'] = personcode
    if max_results:
        sql += ' LIMIT %d' % max_results
    if not personcode and not surname:
        error = 'Parameters are missing or invalid.'
    else:
        data = request.dbsession.execute(sqlalchemy.text(sql), params)
        for r in data:
            item = {'personcode': r[0],
                    'givenname': r[1],
                    'surname': r[2],
                    }
            persons.append(item)
    return error, persons

@view_config(route_name='person', renderer='json', request_method='GET')
def get_person(request):
    "Service for detail data about a person"

    error = None
    errstatus = 400
    try:
        personcode = request.matchdict.get('code')
        if not personcode:
            error = 'Code is missing'
        else:
            errstatus = 500
            q = request.dbsession.query(Person)
            q = q.filter(Person.personcode==personcode)
            p = q.first()
            if p:
                item = {'personcode': p.personcode,
                        'givenname': p.givenname,
                        'surname': p.surname,
                        'full_address': p.full_address,
                        'docno': p.docno,
                        'status': p.status,
                        }
                if p.photo:
                    data = base64.b64encode(p.photo).decode('ascii')
                    item['photo'] = data
                return item
            else:
                error = 'Person not found'
                errstatus = 404
    except Exception as ex:
        log.error(ex)
        error = 'error occurred'
    res = {'error': error}
    return Response(json.dumps(res), status=errstatus)

