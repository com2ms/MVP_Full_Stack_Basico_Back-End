import re
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship, validates

from .base import Base

class Medicacao(Base):
    __tablename__ = 'medicacoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_medicacao = Column(String, nullable=False)
    dosagem = Column(String, nullable=False)
    frequencia = Column(String, nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)
    
    # Chave estrangeira referenciando o Pet correspondente
    pet_id = Column(Integer, ForeignKey('pets.id', ondelete='CASCADE'), nullable=False)

    # Mapeamento reverso da relação
    pet = relationship("Pet", back_populates="medicacoes")

    def __init__(self, nome_medicacao, dosagem, frequencia, data_inicio, pet_id, data_fim=None):
        """
        Cria tabela de Medicacoes.

        Argumentos:
            nome_medicacao: Nome da Medicacao.
            dosagem: Dosagem da Medicacao.
            frequencia: Frequência de administração.
            data_inicio: Data de início do tratamento.
            pet_id: ID do Pet ao qual a medicacao está associada.
            data_fim: Data de término do tratamento (opcional).
        """
        self.nome_medicacao = nome_medicacao
        self.dosagem = dosagem
        self.frequencia = frequencia
        self.data_inicio = data_inicio
        self.pet_id = pet_id
        self.data_fim = data_fim

    def to_dict(self):
        # Retorna o dicionário completo com data no formato DD/MM/AAAA e o nome do pet incluído
        return {
            "id": self.id,
            "nome_medicacao": self.nome_medicacao,
            "dosagem": self.dosagem,
            "frequencia": self.frequencia,
            "data_inicio": self.data_inicio.strftime('%d/%m/%Y'),
            "data_fim": self.data_fim.strftime('%d/%m/%Y') if self.data_fim else None,
            "pet_id": self.pet_id,
            "nome_pet": self.pet.nome if self.pet else "Desconhecido"
        }

    # Ajuste para impedir que a data de término seja anterior à data de início
    @validates('data_inicio', 'data_fim')
    def validar_periodo_medicacao(self, chave, valor):
        inicio = valor if chave == 'data_inicio' else self.data_inicio
        fim = valor if chave == 'data_fim' else self.data_fim

        if inicio and fim and fim < inicio:
            raise ValueError("A data de término do tratamento não pode ser anterior à data de início.")
        return valor
