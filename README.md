# HealthOn

Sistema web desenvolvido em Django para gerenciamento de prescrições médicas digitais, pacientes, medicamentos, farmácias e validação de receitas.

---

# Sobre o Projeto

O **HealthOn** é uma aplicação web utilizada na disciplina de **Gerência de Projetos de Software**, do Instituto Federal do Espírito Santo (IFES) — Campus Serra.

O sistema tem como objetivo informatizar o processo de emissão, gerenciamento e validação de prescrições médicas digitais, facilitando o acesso e o controle das receitas por médicos, pacientes e farmácias. A aplicação permite o cadastro de pacientes, a emissão e consulta de prescrições e o registro da dispensação de medicamentos.

O projeto utiliza o framework **Django**, banco de dados **SQLite** e interface desenvolvida com **Bootstrap**. O gerenciamento das atividades é realizado por meio das metodologias **Scrum e Kanban**, com organização das funcionalidades em um Product Backlog, planejamento de Sprints e acompanhamento das tarefas pelo Trello.

---

# Funcionalidades Implementadas

## Médico

- Login com seleção de perfil
- Dashboard médico
- Cadastro de pacientes
- Edição de pacientes
- Exclusão de pacientes
- Listagem de pacientes
- Cadastro de prescrições médicas
- Edição de prescrições
- Exclusão de prescrições
- Listagem de prescrições
- Visualização dos detalhes da prescrição
- Adição de medicamentos à prescrição
- Cadastro de medicamentos
- Edição de medicamentos
- Exclusão de medicamentos
- Listagem de medicamentos

---

## Paciente

- Login com seleção de perfil
- Visualização das próprias prescrições
- Consulta do status da prescrição
- Consulta da validade da receita

---

## Farmácia

- Login com seleção de perfil
- Dashboard da farmácia
- Consulta das prescrições emitidas
- Registro de dispensação de prescrições
- Cadastro de farmacêuticos
- Edição de farmacêuticos
- Exclusão de farmacêuticos
- Listagem de farmacêuticos

---

# Principais Classes Implementadas

O sistema foi modelado utilizando as seguintes classes de domínio:

- Pessoa
- Paciente
- Médico
- Farmacêutico
- Farmácia
- Medicamento
- Prescrição Médica
- Item da Prescrição
- Venda
- Item da Venda
- Estado
- Cidade
- Bairro
- Endereço
- UsuarioFake (utilizado para autenticação simplificada)

---

# Tecnologias Utilizadas

- Python 3
- Django
- SQLite
- Bootstrap 5
- HTML5
- CSS3

---

# Usuários de Teste

## Médico

Documento:

```
22222222222
```

Senha:

```
123
```

---

## Paciente

Documento:

```
11111111111
```

Senha:

```
123
```

---

## Farmácia

Documento:

```
33333333333
```

Senha:

```
123
```

---

# Como Executar o Projeto

## 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DO_PROJETO
```

---

## 2. Criar ambiente virtual

```bash
python -m venv venv
```

---

## 3. Ativar ambiente virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## 5. Executar as migrações

```bash
python manage.py migrate
```

---

## 6. Carregar os dados iniciais

```bash
python manage.py loaddata dados_iniciais.json
```

---

## 7. Iniciar o servidor

```bash
python manage.py runserver
```

---

## 8. Acessar o sistema

```
http://127.0.0.1:8000/
```

---

# Estrutura dos Dados Iniciais

O projeto utiliza o arquivo:

```
dados_iniciais.json
```

Esse arquivo contém os registros necessários para utilização do sistema logo após a instalação, incluindo:

- Médico de demonstração
- Paciente(s)
- Farmácia
- Medicamentos
- Prescrições médicas
- Usuários de autenticação

O banco de dados (`db.sqlite3`) **não é enviado ao repositório**.

Após executar as migrações, basta carregar os dados utilizando:

```bash
python manage.py loaddata dados_iniciais.json
```

---

# Fluxo de Teste Recomendado

## Perfil Médico

1. Entrar utilizando o perfil Médico.
2. Acessar o Dashboard.
3. Consultar pacientes cadastrados.
4. Cadastrar um novo paciente.
5. Consultar medicamentos.
6. Cadastrar um novo medicamento.
7. Emitir uma nova prescrição.
8. Visualizar os detalhes da prescrição.
9. Adicionar medicamentos à prescrição.
10. Consultar a listagem de prescrições.

---

## Perfil Paciente

1. Sair da conta do médico.
2. Entrar utilizando um paciente.
3. Visualizar as prescrições vinculadas ao seu CPF.
4. Consultar validade e situação da receita.

---

## Perfil Farmácia

1. Entrar utilizando o perfil Farmácia.
2. Acessar a dashboard.
3. Consultar prescrições emitidas.
4. Registrar a dispensação de prescrições.
5. Consultar farmacêuticos cadastrados.

---

# Estrutura do Projeto

```
HealthOn/
│
├── login/
├── usuarios/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── static/
├── dados_iniciais.json
├── requirements.txt
├── manage.py
└── README.md
```

---

# Observações

- O sistema utiliza autenticação simplificada através da classe `UsuarioFake`.
- O projeto foi desenvolvido com fins acadêmicos.
- O banco de dados utilizado durante o desenvolvimento foi o SQLite.
- Para reinstalar completamente o sistema basta executar as migrações e carregar o arquivo `dados_iniciais.json`.

---

# Desenvolvedores

- Caio Monteiro Rangel
- João Victor Nascimento Ribeiro
- João Victor Santos Araújo
---

**Projeto desenvolvido para a disciplina de Projeto de Sistemas — IFES Campus Serra.**