from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import date, datetime


# ENTRADAS DE DADOS
#///////////////////////////////////////////////////////////////////////

class AdicionarMedicacao(BaseModel):
    """
    Schema para adição de uma nova medicação no sistema.
    """
    pet_id: int = Field(..., description="ID do pet cadastrado no banco.")
    nome_medicacao: str = Field(..., min_length=1, description="Nome da medicação.", example="Amoxicilina")
    dosagem: str = Field(..., min_length=1, description="Dosagem da medicação.", example="500mg")
    frequencia: str = Field(..., min_length=1, description="Frequência de uso da medicação.", example="2x ao dia")
    data_inicio: str | date = Field(..., description="Data de início do tratamento em formato DD/MM/AAAA.", example="15/03/2026")
    data_fim: str | date | None = Field(default=None, description="Data de término do tratamento em formato DD/MM/AAAA. Campo opcional.", example="15/03/2027")
    

    @field_validator('nome_medicacao', 'dosagem', 'frequencia', 'data_inicio', 'data_fim', mode='before')
    @classmethod
    def limpar_e_converter_formulario(cls, entrada, info):
        # Limpa textos vazios ou "null" 
        if isinstance(entrada, str):
            entrada_limpa = entrada.strip()
            if entrada_limpa == "" or entrada_limpa == "None" or entrada_limpa.lower() == "null":
                return None
        
        # Ajuste formato data DD/MM/AAAA
        if info.field_name in ('data_inicio', 'data_fim') and isinstance(entrada, str):
            try:
                return datetime.strptime(entrada.strip(), "%d/%m/%Y").date()
            except ValueError:
                raise ValueError(f"A {info.field_name} deve estar no formato válido DD/MM/AAAA (ex: 15/03/2026).")
                
        return entrada


class MedicacaoIdPath(BaseModel):
    """
    Identifica o parâmetro ID que vem na URL (/edit_medicacao/3).
    """
    id: int = Field(..., description="ID da medicação que será editada")


class MedicacaoEditadaBody(BaseModel):
    """
    Schema para edição de medicação existente.
    """
    nome_medicacao: str | None = Field(default=None, description="Novo nome da medicação.")
    dosagem: str | None = Field(default=None, description="Nova dosagem.")
    frequencia: str | None = Field(default=None, description="Nova frequência.")
    data_inicio: str | date | None = Field(default=None, description="Nova data de início no formato DD/MM/AAAA.")  
    data_fim: str | date | None = Field(default=None, description="Nova data de fim no formato DD/MM/AAAA.")
    pet_id: int | None = Field(default=None, description="ID do pet caso mude de animal.")

    @field_validator('nome_medicacao', 'dosagem', 'frequencia', 'data_inicio', 'data_fim', 'pet_id', mode='before')
    @classmethod
    def limpar_e_converter_formulario(cls, entrada, info):
        # Limpa textos vazios ou "null"
        if isinstance(entrada, str):
            entrada_limpa = entrada.strip()
            if entrada_limpa == "" or entrada_limpa == "None" or entrada_limpa.lower() == "null":
                return None

        # Ajuste formato data DD/MM/AAAA
        if info.field_name in ('data_inicio', 'data_fim') and isinstance(entrada, str):
            try:
                return datetime.strptime(entrada.strip(), "%d/%m/%Y").date()
            except ValueError:
                raise ValueError(f"A {info.field_name} deve estar no formato válido DD/MM/AAAA.")
                
        return entrada


#///////////////////////////////////////////////////////////////////////

# RESPOSTAS 
#///////////////////////////////////////////////////////////////////////

class MedicacaoListaItem(BaseModel):
    """
    Estrutura de exibição de uma única medicação.
    """
    id: int
    nome_medicacao: str
    dosagem: str
    frequencia: str
    data_inicio: str
    data_fim: str | None = Field(default=None, description="Data de fim caso exista")
    pet_id: int
    nome_pet: str 

    model_config = ConfigDict(from_attributes=True)


class MedicacaoResposta(BaseModel):
    """
    Resposta padrão para criação ou edição de uma única medicação.
    """
    mensagem: str
    medicacao: MedicacaoListaItem


class ListaMedicacaoResposta(BaseModel):
    """
    Resposta para listagem geral de todas as medicações.
    """
    medicacoes: list[MedicacaoListaItem]


class MedicacaoDeletadaResposta(BaseModel):
    """
    Resposta para quando uma medicação for deletada.
    """
    mensagem: str
    
#///////////////////////////////////////////////////////////////////////
