from pydantic import BaseModel, Field, ConfigDict, field_validator, BaseModel
from typing import List, Optional


# ENTRADAS DE DADOS
#///////////////////////////////////////////////////////////////////////

class AdicionarPet(BaseModel):
    """
    Schema para adição de um novo Pet no sistema.
    """
    tutor_id: int = Field(..., description="ID do tutor cadastrado no banco")
    nome: str = Field(..., min_length=1, description="Nome do pet.", example="Rex")
    especie: str = Field(..., min_length=1, description="Espécie (Cachorro, Gato, etc).", example="Cachorro")
    raca: str | None = Field(default=None, description="Raça do pet opcional.", example="Vira-lata")
    idade: int | None = Field(default=None, description="Idade em anos opcional.", example=3)
    peso: float | None = Field(default=None, description="Peso em kg opcional.", example=12.5)
    
    @field_validator('raca', 'idade', 'peso', mode='before')
    @classmethod
    def limpar_entradas_do_formulario(cls, entrada):
        if isinstance(entrada, str):
            entrada_limpa = entrada.strip()
            if entrada_limpa == "" or entrada_limpa == "None" or entrada_limpa.lower() == "null":
                return None
        return entrada
    

class PetIdPath(BaseModel):
    """
    Identifica o parâmetro ID que vem na URL (/edit_pet/3).
    """
    id: int = Field(..., description="ID do Pet que será editado")


class PetEditadoBody(BaseModel):
    """
    Schema para edição de pet existente.
    """
    nome: str | None = Field(default=None, min_length=1, description="Nome do Pet")
    especie: str | None = Field(default=None, min_length=1, description="Espécie do Pet")
    raca: str | None = Field(default=None, min_length=1, description="Raça do Pet")
    idade: int | None = Field(default=None, ge=0, description="Idade do Pet em anos")
    peso: float | None = Field(default=None, ge=0, description="Peso do Pet em kg")

    @field_validator('nome', 'especie', 'raca', 'idade', 'peso', mode='before')
    @classmethod
    def limpar_entradas_do_formulario(cls, entrada):
        if isinstance(entrada, str):
            entrada_limpa = entrada.strip()
            if entrada_limpa == "" or entrada_limpa == "None" or entrada_limpa.lower() == "null":
                return None
        return entrada

#///////////////////////////////////////////////////////////////////////

# RESPOSTAS 
#///////////////////////////////////////////////////////////////////////

class PetListaItem(BaseModel):
    """
    Estrutura de exibição de um único Pet.
    """
    id: int
    nome: str
    especie: str
    raca: str | None = Field(default=None, description="Raça do Pet")
    idade: int | None = Field(default=None, description="Idade em anos")
    peso: float | None = Field(default=None, description="Peso em kg")
    tutor_id: int
    nome_tutor: str 

    model_config = ConfigDict(from_attributes=True)

class PetResposta(BaseModel):
    """
    Resposta padrão para criação ou edição de um único Pet.
    """
    mensagem: str
    pet: PetListaItem


class ListaPetResposta(BaseModel):
    """
    Resposta para listagem geral de todos os Pets.
    """
    pets: list[PetListaItem]

class PetDeletadoResposta(BaseModel):
    """
    Resposta para quando um Pet for deletado.
    """
    mensagem: str
    
#///////////////////////////////////////////////////////////////////////
