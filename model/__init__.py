import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .pet import Pet
from .base import Base
from .medicacao import Medicacao
from .tutor import Tutor


# Define o caminho onde o banco de dados sqlite será salvo / verifica se o caminho já existe antes de criar.
db_path = "banco_dados/"
if not os.path.exists(db_path):
    os.makedirs(db_path)

db_url = 'sqlite:///banco_dados/clinica.sqlite3'
engine = create_engine(db_url, echo=False)

# Configura a fábrica de sessões para o app.py importar
Session = sessionmaker(bind=engine)

# Inicializador automático de Tabelas
Base.metadata.create_all(engine)
