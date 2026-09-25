import re

from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship, validates

from .base import Base


class Tutor(Base):
    __tablename__ = 'tutores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)   
    telefone = Column(String, unique=True, nullable=False) 
    email = Column(String, nullable=True)
    endereco = Column(String, nullable=True)

    # Índice para ignorar quando o email for NULL sem dar conflito
    __table_args__ = (
        Index(
            'ix_tutores_email_unique', 
            'email', 
            unique=True, 
            sqlite_where=Column('email').is_not(None)      
        ),
    )

    # Relacionamento 1 para N com Pets (Cascade ativo para deleção automática)
    pets = relationship("Pet", back_populates="tutor", cascade="all, delete-orphan")

    def __init__(self, nome, cpf, telefone, email=None, endereco=None):
        """
        Cria tabela de Tutores.

        Argumentos:
            nome: Nome do Tutor.
            cpf: CPF do Tutor. Digitar somente os 11 números, sem pontos e traços.
            telefone: Telefone do Tutor, com DDD sem o zero.
            e-mail: E-mail do Tutor (opcional).
            endereco: Endereço do Tutor (opcional).
        """
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone 
        self.email = email
        self.endereco = endereco

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "email": self.email,
            "endereco": self.endereco
        }

    # Remove pontos, hífens e tudo que não for número, garantindo que restem exatamente 11 números
    @validates('cpf')
    def processar_e_limpar_cpf(self, _, cpf_recebido):
        cpf_limpo = re.sub(r'\D', '', str(cpf_recebido))
        
        if len(cpf_limpo) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
            
        return cpf_limpo
