from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional


# ENTRADAS DE DADOS
#///////////////////////////////////////////////////////////////////////

class AdicionarTutor(BaseModel):
    """
    Schema para adição de um novo tutor no sistema.
    """

    nome: str = Field(..., min_length=1, description="Nome completo do tutor.", example="João Silva")
    cpf: str = Field(..., min_length=11, description="CPF contendo apenas (11) números.", example="12345678900")
    telefone: str = Field(..., min_length=1, description="Telefone de contato com DDD.", example="11999999999")
    email: str | None = Field(default=None, description="E-mail opcional.", example="joao.silva@email.com")
    endereco: str | None = Field(default=None, description="Endereço opcional.", example="Rua das Flores, 123")

    @field_validator('nome', 'cpf', 'telefone', 'email', 'endereco', mode='before')
    @classmethod
    def limpar_entradas_do_formulario(cls, entrada):
        if isinstance(entrada, (int, float)):
            return str(entrada)
        
        if isinstance(entrada, str):
            entrada_limpa = entrada.strip()
            if entrada_limpa == "" or entrada_limpa == "None" or entrada_limpa.lower() == "null":
                return None
                
        return entrada


class TutorIdPath(BaseModel):
    """
    Identifica o parâmetro ID que vem na URL (/get_tutor/3).
    """
    id: int = Field(..., description="ID do tutor")


class TutorEditadoBody(BaseModel):
    """
    Dados para edição de tutor.
    """
    nome: str | None = Field(default=None, description="Novo nome do tutor.", example="João Silva Alterado")
    cpf: str | None = Field(default=None, description="Novo CPF - apenas (11) números.", example="12345678900")
    telefone: str | None = Field(default=None, description="Novo telefone com DDD sem o zero.", example="11999999999")
    email: str | None = Field(default=None, description="Novo e-mail.", example="joao.novo@email.com")
    endereco: str | None = Field(default=None, description="Novo endereço.", example="Nova Rua, 456")

    @field_validator('nome', 'cpf', 'telefone', 'email', 'endereco', mode='before')
    @classmethod
    def limpar_entradas_do_formulario(cls, entrada):
        if isinstance(entrada, (int, float)):
            return str(entrada)
        
        if isinstance(entrada, str):
            entrada_limpa = entrada.strip()
            if entrada_limpa == "" or entrada_limpa == "None" or entrada_limpa.lower() == "null":
                return None
                
        return entrada

#///////////////////////////////////////////////////////////////////////

# RESPOSTAS
#///////////////////////////////////////////////////////////////////////

class TutorListaItem(BaseModel):
    """
    Estrutura exibição de dados de tutor.
    """
    id: int
    nome: str
    cpf: str = Field(..., description="CPF do tutor cadastrado.")
    telefone: str
    email: str | None = Field(default=None, description="E-mail do tutor")
    endereco: str | None = Field(default=None, description="Endereço do tutor")

    model_config = ConfigDict(from_attributes=True)  


class TutorResposta(BaseModel):
    """
    Resposta padrão para criação ou edição de um único tutor.
    """
    mensagem: str
    tutor: TutorListaItem


class ListaTutorResposta(BaseModel):
    """
    Resposta para listagem geral de tutores.
    """
    tutores: list[TutorListaItem]


class TutorDeletadoResposta(BaseModel):
    """
    Resposta para quando um tutor for deletado.
    """
    mensagem: str
    
#///////////////////////////////////////////////////////////////////////
