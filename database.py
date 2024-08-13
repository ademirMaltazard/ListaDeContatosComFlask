from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///contatos.db', echo=True, connect_args={'check_same_thread': False})

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    senha = Column(String(50), nullable=False)

    contatos = relationship("Contatos", back_populates="users")


class Contatos(Base):
    __tablename__ = "contatos"

    id_contato = Column(Integer, primary_key=True)
    nome_contato = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    celular = Column(String(30), nullable=True)
    celular_alt = Column(String(30), nullable=True)
    tags = Column(String(30), nullable=True)

    id_user = Column(Integer, ForeignKey('users.id_user'))
    users = relationship('Users', back_populates='contatos')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
