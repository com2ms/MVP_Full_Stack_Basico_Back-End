from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, validates

from .base import Base


class Pet(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    raca = Column(String, nullable=True)
    idade = Column(Integer, nullable=True)
    peso = Column(Float, nullable=True)
    
    tutor_id = Column(Integer, ForeignKey('tutores.id', ondelete='CASCADE'), nullable=False)

    tutor = relationship("Tutor", back_populates="pets")
    medicacoes = relationship("Medicacao", back_populates="pet", cascade="all, delete-orphan")

    def __init__(self, nome, especie, tutor_id, raca=None, idade=None, peso=None):
       """
        Cria tabela de Pets.

        Argumentos:
            nome: Nome do Pet.
            especie: Espécie do animal (ex: gato, cachorro).
            tutor_id: Tutor(a) responsável pelo Pet.
            raca: Raça do Pet (opcional).
            idade: Idade do Pet em anos (opcional).
            peso: Peso do Pet em kg (opcional).
        """
       
       self.nome = nome
       self.especie = especie
       self.tutor_id = tutor_id
       self.raca = raca
       self.idade = idade
       self.peso = peso

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especie": self.especie,
            "raca": self.raca,
            "idade": self.idade,
            "peso": self.peso,
            "tutor_id": self.tutor_id,
            "nome_tutor": self.tutor.nome #if self.tutor else "Não informado"
        }
