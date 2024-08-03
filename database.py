from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///contatos.db', echo=True)

Base = declarative_base()

class Contatos(Base):
    __tablename__ = "contatos"

    id_contato = Column(Integer, primary_key=True)
    nome_contato = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    celular = Column(String(30), nullable=True)
    celular_alt = Column(String(30), nullable=True)
    tags = Column(String(30), nullable=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
