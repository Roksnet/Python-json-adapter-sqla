import argparse
import sys
import os
from datetime import date

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """
    #model = models.mymodel.MyModel(name='one', value=1)
    #dbsession.add(model)

    # ADD SOME EXAMPLE DATA IF DATABASE IS EMPTY

    path = os.path.dirname(os.path.realpath(__file__))
    photo = open(os.path.join(path, 'init_photo.jpg'), 'rb').read()
    signature = open(os.path.join(path, 'init_signature.jpg'), 'rb').read()
    
    item = models.Person(givenname='EDMUND',
                         surname='HACTENUS',
                         personcode='37001196628',
                         full_address='JÄRVA MAAKOND, PAIDE LINN, KESKÖÖ TN 25A',
                         docno='29342429',
                         status='E',
                         birthdate=date(1970,1,19),
                         photo=photo,
                         signature=signature,
                         documents=[models.Document(doc_type=1,
                                                    doc_no='100200',
                                                    valid_from=date(2011,12,14),
                                                    valid_until=date(2015,12,14)),
                                    models.Document(doc_type=1,
                                                    doc_no='200300',
                                                    valid_from=date(2015,12,10),
                                                    valid_until=date(2029,12,10)),
                                    ],
                         )
    dbsession.add(item)
    item = models.Person(givenname='PILLE',
                         surname='HUQUAESTUM',
                         personcode='45803029574',
                         birthdate=date(1958,3,2),
                         full_address='TARTU MAAKOND, TARTU LINN, MESIJUTU TN 14',
                         docno='31002000',
                         status='E',
                         photo=photo,
                         signature=signature,
                         documents=[models.Document(doc_type=1,
                                                    doc_no='100100',
                                                    valid_from=date(2012,2,4),
                                                    valid_until=date(2025,2,4)),
                                    models.Document(doc_type=2,
                                                    doc_no='300100',
                                                    valid_from=date(2012,2,5),
                                                    valid_until=date(2025,2,5)),
                                    ],
                         )
    dbsession.add(item)    

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
