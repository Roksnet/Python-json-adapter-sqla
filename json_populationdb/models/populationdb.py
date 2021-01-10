from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    Date,
    DateTime,
    Float,
    Boolean,
    LargeBinary,
    ForeignKey,
    ForeignKeyConstraint,
    DefaultClause,
    event,
    and_,
    or_,
    MetaData,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    mapper,
    )

from .meta import Base


class Person(Base):
    "Person's data"
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)    
    givenname = Column(String(128))
    surname = Column(String(128))
    personcode = Column(String(11))
    full_address = Column(String(512))
    docno = Column(String(50))
    status = Column(String(1)) # status: E - alive, S - dead, M - something else, P - unknown
    photo = Column(LargeBinary)
    birthdate = Column(Date)
    sex = Column(String(1)) # sex: M, F
    signature = Column(LargeBinary)    
    documents = relationship('Document', backref='Person')

    @property
    def name(self):
        return '%s %s' % (self.givenname, self.surname)
   
class Document(Base):
    "Identity document of a person"
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)    
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False, index=True)
    doc_type = Column(Integer, nullable=False) # 1 - ID card, 2 - passport
    doc_no = Column(String(50), nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=False)

    @property
    def doc_type_name(self):
        if self.doc_type == 1:
            return 'ID card'
        else:
            return 'Passport'
