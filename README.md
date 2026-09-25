# MVP Desenvolvimento Full Stack Básico
# Desenvolvimento de ferramenta para Controle de Medicações para Pets - Back-End


## Sobre o Projeto

O objetivo é desenvolver uma ferramenta para uso em clínicas veterinárias ou em ambiente doméstico que permita o cadastro de Tutores(as), seus Pets Vinculados e as Medicações que esse Pet faz uso. A idéia nasceu da rotina diária de cuidar de uma cadelinha chamada Pimenta que em 2026 completou 12 anos de vida e que ao longo desses anos foi acumulando uma lista razoável de prescrições médicas.

O presente projeto visa atender os requisitos de entrega para o MVP do Sprint **Desenvolvimento Full Stack Básico**, mas especificamente da parte de **Back-End**.

A parte de **Front-End** está salva em repositório próprio **([Front-End](https://github.com/com2ms/MVP_Full_Stack_Basico_Front-End.git))**.


## Como executar o Projeto:

Antes de começar, você vai precisar ter instalado em sua máquina o [Python 3.x](https://python.org) (Recomendado versão 3.10 ou superior) e o [Git](https://git-scm.com) (opcional, para clonar o repositório).

Clone o repositório ou faça o download do mesmo. Extraia os arquivos do arquivo compactado. A pasta resultante deve apresentar a estrutura que segue:

```text
/MVP_Full_Stack...Back-End.../
                       │
                       ├── README.md           # Documentação do projeto
                       ├── app.py              # Servidor Flask
                       ├── requirements.txt    # Lista de dependências e bibliotecas
                       ├── model/              # Modelos do banco de dados
                       └── schemas/            # Schemas Pydantic
```

Assim como no exemplo em Aula, este projeto foi desenvolvido com o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html). Recomenda-se que se faça o mesmo.

Abra o terminal e vá até a raiz do Projeto ('../MVP_Full_Stack...Back-End.../'). Execute os comandos abaixo de acordo com seu Sistema Operacional para criar o ambiente virtual:

* **No Windows (PowerShell):**
  ```bash
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **No Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

Com o ambiente virtual rodando ('venv' ativada), instale todos os pacotes necessários rodando no Terminal:

```bash
pip install -r requirements.txt
```

Após o término da instalação das bibliotecas, execute o comando abaixo para executar a API:

```bash
flask run --host 0.0.0.0 --port 5000
```

Abra o navegador e acesse [http://localhost:5000](http://localhost:5000) para testar as rotas da API.

As rotas CRUD integradas ao sistema são:

* `POST /add_tutor` | `POST /add_pet` | `POST /add_medicacao`
* `GET /get_tutor/<id>` | `GET /get_pet/<id>` | `GET /get_medicacao/<id>`
* `GET /get_tutores` | `GET /get_pets` | `GET /get_medicacoes`
* `PUT /edit_tutor/<id>` | `PUT /edit_pet/<id>` | `PUT /edit_medicacao/<id>`
* `DELETE /del_tutor/<id>` | `DELETE /del_pet/<id>` | `DELETE /del_medicacao/<id>`
