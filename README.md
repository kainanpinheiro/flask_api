<h1 align="center">API Estoque/Vendas de livros</h1>

### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
[Git](https://git-scm.com), [Python](https://www.python.org/), [Docker](https://www.docker.com/).
Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/)

### 🎲 Rodando o Back End (servidor)

```bash
# Clone este repositório
$ git clone <https://github.com/kainanpinheiro/flask_api>

# Acesse a pasta do projeto no terminal/cmd
$ cd flask_api

# Criando uma imagem do Postgres com o docker
$ docker run --name database -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
# Crie um arquivo .env copiando o conteúdo do .env.example e adicione as configurações do seu banco de dados :)

# Crie uma virtualenv
$ virtualenv venv

# Instale as dependências
$ pip install -r requirements.txt

# Rode as migrations
$ python models.py db upgrade

# Execute a aplicação em modo de desenvolvimento
$ python run.py

# O servidor inciará na porta:5000 - acesse <http://localhost:5000>
```
