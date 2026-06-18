# HealthOn

Sistema web desenvolvido em Django para gerenciamento de prescrições médicas digitais.

##SEGUIR A SEÇÃO DE COMO EXECUTAR O PROJETO

## Funcionalidades Implementadas

### Médico

* Login com seleção de perfil
* Dashboard médico
* Cadastro de pacientes
* Edição de pacientes
* Exclusão de pacientes
* Listagem de pacientes
* Cadastro de prescrições
* Edição de prescrições
* Exclusão de prescrições
* Listagem de prescrições

### Paciente

* Login com seleção de perfil
* Visualização das próprias prescrições
* Consulta de medicamento, dosagem, validade e status da receita

### Farmácia

* Perfil disponível na tela de login para representar a proposta completa do sistema.
* O fluxo farmacêutico de validação de prescrições e registro de dispensação está previsto para versões futuras.

---

## Tecnologias Utilizadas

* Python 3
* Django
* SQLite
* Bootstrap 5
* HTML5
* CSS3

---

## Usuários de Teste

### Médico

**Documento:** `22222222222`
**Senha:** `123`

### Paciente - Maria Silva

**Documento:** `11111111111`
**Senha:** `123`

### Paciente - João Souza

**Documento:** `44444444444`
**Senha:** `123`

### Farmácia

**Documento:** `33333333333`
**Senha:** `123`

---

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DO_PROJETO
```

### 2. Criar um ambiente virtual

```bash
python -m venv venv
```

### 3. Ativar o ambiente virtual

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Executar as migrações

```bash
python manage.py migrate
```

### 6. Carregar os dados iniciais

```bash
python manage.py loaddata dados_iniciais.json
```

### 7. Iniciar o servidor

```bash
python manage.py runserver
```

### 8. Acessar o sistema

Abra o navegador e acesse:

```txt
http://127.0.0.1:8000/
```

---

## Estrutura dos Dados Iniciais

O projeto utiliza o arquivo:

```txt
dados_iniciais.json
```

Este arquivo contém:

* Usuários de demonstração
* Pacientes cadastrados
* Prescrições cadastradas

O banco de dados **não é enviado para o GitHub**. Após executar as migrações, os dados são carregados utilizando o comando:

```bash
python manage.py loaddata dados_iniciais.json
```

---

## Fluxo de Teste Recomendado

### Teste do Médico

1. Entrar com o perfil Médico.
2. Acessar a dashboard médica.
3. Consultar os pacientes cadastrados.
4. Consultar as prescrições cadastradas.
5. Criar uma nova prescrição.
6. Editar uma prescrição existente.
7. Excluir uma prescrição.

### Teste do Paciente

1. Sair da conta do médico.
2. Entrar com um dos pacientes de teste.
3. Visualizar as prescrições vinculadas ao seu CPF.
4. Consultar validade, medicamento, dosagem e status da receita.

---

## Desenvolvedores

* Caio Monteiro Rangel
* Cauã Gilberto Paiva Lainha
* João Victor Nascimento Ribeiro
* João Victor Santos Araújo

Projeto desenvolvido para a disciplina de Desenvolvimento Web.
