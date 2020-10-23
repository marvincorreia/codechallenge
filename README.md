# Code Challenge App
Django Web APP

# Sobre
Aplicação web para validação e teste de código em tempo real
utilizando websocket e subprocessos em python

# Pré requisitos

- [Git](https://git-scm.com/)
- [Python 3.7](https://www.python.org/downloads/release/python-370/)

# Instalação

### Clonando o repositório ###
Antes de configurar o ambiente virtual para o projeto, primeiro deve-se ter clonado
o repositório no github para sua máquina local e entrar na pasta raiz do projeto.

```
git clone https://github.com/marvincorreia/codechallenge.git
cd codechallenge
```

### Pipenv ###
O projeto tem como dependência principal o python 3.7
 e utiliza para esse efeito o gerenciador de dependências chamado [pipenv](https://pypi.org/project/pipenv/),
criado por Kenneth Reitz e que se tornou no recurso oficial recomendado para 
gerenciar dependências no Python.

O *pipenv* pode ser instalado através do *pip* via terminal ou bash:

```
pip install pipenv
``` 
ou 
```
sudo apt install pipenv
```

O projeto possui 2 ficheiros, [Pipfile](https://github.com/marvincorreia/codechallenge/blob/master/Pipfile) 
e [Pipfile.lock](https://github.com/marvincorreia/codechallenge/blob/master/Pipfile.lock),
onde estão documentados as dependencias do projeto.

Após ter clonado o repositório basta configurar o ambiente virtual usando o pipenv,
apartir do diretorio raiz do projeto:

**OBS:** *Apartir deste ponto os comandos devem ser executados dentro da pasta raiz do projeto **/codechallenge** *

***Criar ambiente virtual python para o projeto:***
 
```
pipenv --python 3.7
```
ou
```
pipenv --three
```

output:

```
Successfully created virtual environment!
Virtualenv location:C:\Users\Username\.virtualenvs\codechallenge-xxxxx
```

Instalar as dependencias especificadas no ficheiro Pipfile.lock para o ambiente:

```
pipenv update
```

Após o download dos packages de dependencia, o ambiente estará configurada para rodar
a aplicação web.

# Testando o servidor
Estando no diretório raiz do projeto */codechallenge* execute

```
pipenv shell
# ativar ambiente virtual
```
```
python manage.py runserver
# rodar servidor
```
Agora é só acessar atravéz do browser neste endereço [localhost](http://localhost:8000/)

