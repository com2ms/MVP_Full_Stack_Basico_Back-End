from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError
from typing import Optional

from model import Pet, Medicacao, Session, Tutor

# Importações dos Schemas
from schemas.tutor import AdicionarTutor, TutorDeletadoResposta, TutorIdPath, TutorResposta, ListaTutorResposta, TutorEditadoBody
from schemas.pet import AdicionarPet, PetDeletadoResposta, PetIdPath, PetResposta, PetEditadoBody, ListaPetResposta, PetListaItem
from schemas.medicacao import AdicionarMedicacao, MedicacaoDeletadaResposta, MedicacaoIdPath, MedicacaoResposta, MedicacaoEditadaBody, ListaMedicacaoResposta


info = Info(title="Controle de Medicações para Pets", version="0.0.1.1")

app = OpenAPI(__name__, info=info)
app.json.sort_keys = False 

CORS(app)

#///////////////////////////////////////////////////////////////////////
# Definição das Tags
tutor_tag = Tag(name="Tutor", description="Gerenciamento de tutores")
pet_tag = Tag(name="Pet", description="Gerenciamento de pets")
medicacao_tag = Tag(name="Medicação", description="Gerenciamento de medicações")
home_tag = Tag(name="Home", description="Redirecionamento para /openapi")

#///////////////////////////////////////////////////////////////////////
# Pasta Home - Redirecionamento para OpenApi/Swagger
@app.get('/', tags=[home_tag])
def home():
    """
    Redirecionamento para /openapi.
    """
    return redirect('/openapi')
    

# 1. OPERAÇÕES TUTOR
#///////////////////////////////////////////////////////////////////////

# 1.1. Cadastro de novo tutor

@app.post('/add_tutor', tags=[tutor_tag], responses={"201": TutorResposta})
def add_tutor(form: AdicionarTutor):
    """
    Cadastra um novo tutor.
    """
    
    session = Session()

    try:
        novo_tutor = Tutor(
            nome=form.nome,       
            cpf=form.cpf,         
            telefone=form.telefone, 
            email=form.email,     
            endereco=form.endereco 
        )

        session.add(novo_tutor)
        session.commit()

        return {
            "mensagem": "Tutor cadastrado!", 
            "tutor": novo_tutor.to_dict()
        }, 201

    except ValueError as erro_validacao:
        session.rollback()
        return {"erro": str(erro_validacao)}, 400

    except IntegrityError as erro:
        session.rollback()
        mensagem_banco = str(erro.orig).lower()
        
        if "cpf" in mensagem_banco:
            return {"erro": "Este CPF já está cadastrado na base."}, 409
        if "telefone" in mensagem_banco:
            return {"erro": "Este telefone já está cadastrado para outro tutor."}, 409
        if "email" in mensagem_banco or "ix_tutores_email_unique" in mensagem_banco:
            return {"erro": "Este e-mail já está cadastrado na base."}, 409
      
        return {"erro": "Dados duplicados enviados para a base."}, 409

    except Exception as e:
        session.rollback()
        return {"erro": f"Não foi possível salvar: {str(e)}"}, 400

    finally:
        session.close()


#  1.2. Consulta Tutor por ID

@app.get("/get_tutor/<int:id>", tags=[tutor_tag], responses={"200": TutorResposta})
def get_tutor(path: TutorIdPath):
    """
    Busca um tutor cadastrado através do seu ID.
    """
    session = Session()
    try:

        tutor = session.query(Tutor).filter(Tutor.id == path.id).first()
         
        if not tutor:
            return {"erro": "Tutor não encontrado"}, 404
            
        return {
            "mensagem": "Tutor encontrado!", 
            "tutor": tutor.to_dict()
        }, 200
        
    except Exception as e:
        return {"erro": f"Erro ao buscar tutor: {str(e)}"}, 500
        
    finally:
        session.close()


#  1.3. Consulta e lista todos os tutores

@app.get('/get_tutores', tags=[tutor_tag], responses={"200": ListaTutorResposta})
def get_tutores():
    """
    Lista todos os tutores cadastrados.
    """
    session = Session()
    try:
        tutores = session.query(Tutor).all()
        
        resultado = [t.to_dict() for t in tutores]
        
        return {"tutores": resultado}, 200
        
    except Exception as e:
        return {"erro": f"Erro ao buscar tutores: {str(e)}"}, 500
        
    finally:
        session.close()


#  1.4. Edição dados de tutor
    
@app.put('/edit_tutor/<int:id>', tags=[tutor_tag], responses={"200": TutorResposta})
def edit_tutor(path: TutorIdPath, form: TutorEditadoBody): 
    """
    Edita os dados de um tutor existente baseado no ID.
    Preencha somente os campos a serem alterados. Campos não preenchidos serão ignorados e permanecerão inalterados.
    """
    session = Session()
    
    tutor = session.query(Tutor).filter(Tutor.id == path.id).first()
    if not tutor:
        session.close()
        return {"erro": "Tutor não encontrado"}, 404
        
    dados_para_atualizar = form.model_dump(exclude_unset=True, exclude_none=True)
    
    for campo, valor in dados_para_atualizar.items():
        setattr(tutor, campo, valor)
        
    try:
        session.commit()
        return {
            "mensagem": "Dados do tutor atualizados com sucesso!", 
            "tutor": tutor.to_dict()
        }, 200
    except IntegrityError:
        session.rollback()
        return {"erro": "E-mail, CPF ou telefone já está sendo utilizado por outro tutor."}, 409
    except Exception as e:
        session.rollback()
        return {"erro": f"Erro interno: {str(e)}"}, 500
    finally:
        session.close()



#  1.5. Deleção de tutor (deleta pets em cascata).

@app.delete('/del_tutor/<int:id>', tags=[tutor_tag], responses={"200": TutorDeletadoResposta})
def del_tutor(path: TutorIdPath):
    """
    Remove um tutor e todos os seus pets cadastrados em cascata.
    """

    session = Session()
    
    try:

        tutor = session.query(Tutor).filter(Tutor.id == path.id).first()
        
        if not tutor:
            return {"erro": "Tutor não encontrado"}, 404
            
        session.delete(tutor)
        session.commit()
        
        return {"mensagem": "Tutor e pets vinculados deletados!"}, 200
        
    except Exception as e:
        session.rollback()
        return {"erro": f"Erro interno ao deletar tutor: {str(e)}"}, 500
        
    finally:
        session.close()

#///////////////////////////////////////////////////////////////////////


#  2. OPERAÇÕES PETs
#///////////////////////////////////////////////////////////////////////

# 2.1. Cadastro de novo pet vinculado a um tutor

@app.post('/add_pet', tags=[pet_tag], responses={"201": PetResposta})
def add_pet(form: AdicionarPet):
    """
    Cadastra um novo pet vinculado a um tutor.
    """
    session = Session()
    
    try:
        # Verifica se o ID do tutor é válido.
        tutor_existe = session.query(Tutor).filter(Tutor.id == form.tutor_id).first()
        if not tutor_existe:
            session.close()
            return {"erro": f"Não foi possível cadastrar. O tutor com ID {form.tutor_id} não existe."}, 404

        novo_pet = Pet(
            nome=form.nome,
            especie=form.especie,
            raca=form.raca,
            idade=form.idade,
            peso=form.peso,
            tutor_id=form.tutor_id
        )
    
        session.add(novo_pet)
        session.commit()

        return {
            "mensagem": "Pet cadastrado!", 
            "pet": novo_pet.to_dict()
        }, 201

    except ValueError as erro_validacao:
        session.rollback()
        return {"erro": str(erro_validacao)}, 400
        
    except IntegrityError:
        session.rollback()
        return {"erro": "Erro de integridade ou dados duplicados enviados para a base."}, 409
        
    except Exception as e:
        session.rollback()
        return {"erro": f"Não foi possível salvar: {str(e)}"}, 400
        
    finally:
        session.close()


#  2.2. Consulta de pets por ID

@app.get("/get_pet/<int:id>", tags=[pet_tag], responses={"200": PetResposta})
def get_pet(path: PetIdPath):
    """
    Busca e retorna os detalhes de um pet específico baseado no ID.
    """
    session = Session()

    try:

        pet = session.query(Pet).filter(Pet.id == path.id).first()

        if not pet:
            return {"erro": "Pet não encontrado"}, 404

        return {
            "mensagem": "Pet encontrado!",
            "pet": pet.to_dict()
         }, 200

    except Exception as e:
        return {"erro": f"Erro interno ao buscar pet: {str(e)}"}, 500

    finally:
        session.close()


#  2.3. Consulta e lista todos os pets

@app.get('/get_pets', tags=[pet_tag], responses={"200": ListaPetResposta})
def get_pets():
    """
    Lista todos os pets cadastrados.
    """
    session = Session()
    try:
        pets = session.query(Pet).all()
        
        resultado = [p.to_dict() for p in pets]
        
        return {"pets": resultado}, 200
        
    except Exception as e:
        return {"erro": f"Erro ao buscar pets: {str(e)}"}, 500
        
    finally:
        session.close()


#  2.4. Edição dados de pet

@app.put('/edit_pet/<int:id>', tags=[pet_tag], responses={"200": PetResposta})
def edit_pet(path: PetIdPath, form: PetEditadoBody):
    """
    Edita os dados de um pet existente baseado no ID. 
    Preencha somente os campos a serem alterados. Campos não preenchidos serão ignorados e permanecerão inalterados.
    """
    session = Session()
    
    pet = session.query(Pet).filter(Pet.id == path.id).first()
    if not pet:
        session.close()
        return {"erro": "Pet não encontrado"}, 404
        
    # Extrai apenas os campos que o usuário realmente preencheu e enviou válidos
    dados_para_atualizar = form.model_dump(exclude_unset=True, exclude_none=True)
    
     # Atualiza os atributos do pet dinamicamente
    for campo, valor in dados_para_atualizar.items():
        setattr(pet, campo, valor)
    
    try:
        session.commit()

        return {
            "mensagem": "Dados do pet atualizados com sucesso!",
            "pet": pet.to_dict()
         }, 200
         
    except ValueError as erro_validacao:
        session.rollback()
        return {"erro": str(erro_validacao)}, 400
    
    except Exception as e:
        session.rollback()
        return {"erro": f"Erro ao atualizar: {str(e)}"}, 400
        
    finally:
        session.close()


#  2.5. Deleção de pet

@app.delete('/del_pet/<int:id>', tags=[pet_tag], responses={"200": PetDeletadoResposta})
def del_pet(path: PetIdPath):
    """
    Remove um pet cadastrado baseado no ID. Medicações vinculadas a este pet também serão removidas em cascata.
    """
    session = Session()
    
    try:

        pet = session.query(Pet).filter(Pet.id == path.id).first()
        
        if not pet:
            return {"erro": "Pet não encontrado"}, 404
            
        session.delete(pet)
        session.commit()
        
        return {"mensagem": "Pet removido com sucesso!"}, 200
        
    except Exception as e:
        session.rollback()
        return {"erro": f"Erro interno ao deletar: {str(e)}"}, 500
        
    finally:
        session.close()

#///////////////////////////////////////////////////////////////////////


#  3. OPERAÇÕES MEDICAÇÕES
#///////////////////////////////////////////////////////////////////////

# 3.1. Cadastro de nova medicação vinculada a pet

@app.post('/add_medicacao', tags=[medicacao_tag], responses={"201": MedicacaoResposta})
def add_medicacao(form: AdicionarMedicacao): #  Alterado de 'body' para 'form' para alinhar com Form Data
    """
    Registra uma nova medicação vinculada a um pet.
    """
    session = Session()
    
    try:
        # 1. VERIFICAÇÃO: Checa se o pet informado realmente existe no banco
        pet_existe = session.query(Pet).filter(Pet.id == form.pet_id).first()
        if not pet_existe:
            session.close()
            return {"erro": f"Não foi possível cadastrar. O pet com ID {form.pet_id} não existe."}, 404

        nova_medicacao = Medicacao(
            nome_medicacao=form.nome_medicacao,
            dosagem=form.dosagem,
            frequencia=form.frequencia,
            data_inicio=form.data_inicio,
            data_fim=form.data_fim,        
            pet_id=form.pet_id       
        )

        session.add(nova_medicacao)
        session.commit()  

        return {
            "mensagem": "Medicação cadastrada!",
            "medicacao": nova_medicacao.to_dict()
        }, 201
        
    except ValueError as erro_validacao:
        session.rollback()
        return {"erro": str(erro_validacao)}, 400
        
    except IntegrityError:
        session.rollback()
        return {"erro": "Erro de integridade ou dados duplicados enviados para a base."}, 409
        
    except Exception as e:
        session.rollback()
        return {"erro": f"Não foi possível salvar: {str(e)}"}, 400
        
    finally:
        session.close()


#  3.2. Consulta e lista medicação por ID

@app.get("/get_medicacao/<int:id>", tags=[medicacao_tag], responses={"200": MedicacaoResposta})
def get_medicacao(path: MedicacaoIdPath):
    """
    Busca e retorna os detalhes de uma medicação específica baseado no ID.
    """
    session = Session()

    try:

        medicacao = session.query(Medicacao).filter(Medicacao.id == path.id).first()

        if not medicacao:
            return {"erro": "Medicação não encontrada"}, 404

        return {
            "mensagem": "Medicação encontrada!",
            "medicacao": medicacao.to_dict()    
        }, 200


    except Exception as e:
        return {"erro": f"Erro interno ao buscar medicação: {str(e)}"}, 500

    finally:
        session.close()

#  3.3. Consulta e lista todos medicamentos em uso

@app.get('/get_medicacoes', tags=[medicacao_tag], responses={"200": ListaMedicacaoResposta})
def get_medicacoes():
    """
    Lista todas as medicações cadastradas com os nomes dos respectivos animais
    """
    session = Session()
    try:
        medicacoes = session.query(Medicacao).all()
        
        resultado = [m.to_dict() for m in medicacoes]
        
        return {"medicacoes": resultado}, 200
    except Exception as e:
        return {"erro": f"Erro ao buscar medicações: {str(e)}"}, 500
    finally:
        session.close()


#  3.4. Edição dados de medicação

@app.put('/edit_medicacao/<int:id>', tags=[medicacao_tag], responses={"200": MedicacaoResposta})
def edit_medicacao(path: MedicacaoIdPath, form: MedicacaoEditadaBody):
    """
    Edita os dados de uma medicação existente baseado no ID. 
    Preencha somente os campos a serem alterados. Campos não preenchidos serão ignorados e permanecerão inalterados.
    """
    session = Session()
    
    try:
        
        medicacao = session.query(Medicacao).filter(Medicacao.id == path.id).first()
        if not medicacao:
            session.close()
            return {"erro": "Medicação não encontrada"}, 404

        dados_brutos = form.model_dump(exclude_unset=True)
        
        dados_para_atualizar = {}
        for campo, valor in dados_brutos.items():
            if valor is None and campo != 'data_fim':
                continue  # Ignora campos obrigatórios vazios
            dados_para_atualizar[campo] = valor

        for campo, valor in dados_para_atualizar.items():
            setattr(medicacao, campo, valor)
        
        session.commit()
        
        return {
            "mensagem": "Dados da medicação atualizados com sucesso!",
            "medicacao": medicacao.to_dict()
        }, 200

    except ValueError as erro_validacao:
        session.rollback()
        return {"erro": str(erro_validacao)}, 400

    except Exception as e:
        session.rollback()
        return {"erro": f"Não foi possível salvar: {str(e)}"}, 400
        
    finally:
        session.close()


# 3.5. Deleção de medicamentos

@app.delete('/del_medicacao/<int:id>', tags=[medicacao_tag], responses={"200": MedicacaoDeletadaResposta})
def del_medicacao(path: MedicacaoIdPath):
    """
    Remove uma medicação cadastrada baseado no ID.
    """
    session = Session()
    
    try:

        medicacao = session.query(Medicacao).filter(Medicacao.id == path.id).first()
        
        if not medicacao:
            return {"erro": "Medicação não encontrada"}, 404
            
        session.delete(medicacao)
        session.commit()
        
        return {"mensagem": "Medicação removida com sucesso!"}, 200
        
    except Exception as e:
        session.rollback()
        return {"erro": f"Erro ao remover: {str(e)}"}, 500
        
    finally:
        session.close()

#///////////////////////////////////////////////////////////////////////


# INICIALIZAÇÃO DO SERVIDOR EM MODO DEBUG
#///////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    # Adicionando o host e a porta direto no código
    app.run(host='0.0.0.0', port=5000, debug=True)
