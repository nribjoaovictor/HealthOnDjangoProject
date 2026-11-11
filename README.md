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

# Parte Vercel - Executar a partir daqui
-----

**Projeto desenvolvido para a disciplina de Projeto de Sistemas — IFES Campus Serra.**
## Demonstração somente leitura na Vercel

A branch `deploy-vercel-readonly` prepara uma demonstração pública com **SQLite**,
sem PostgreSQL. Nenhum push, merge ou deploy é executado automaticamente por estes
scripts. O banco local `db.sqlite3` e o fixture legado `dados_iniciais.json` não são
usados no build de produção nem devem ser enviados à Vercel.

### Desenvolvimento local

Use Python **3.12**, instale `requirements.txt` e execute `python manage.py migrate`
antes de iniciar o servidor. A nova migração adiciona `Paciente.cadastrado_por`,
sem remover registros. Os pacientes antigos continuam acessíveis aos médicos que
já emitiram suas receitas; pacientes sem receitas e sem médico responsável devem
ser vinculados pelo administrador local. Novos cadastros recebem esse vínculo
automaticamente. As gravações e o visual local continuam disponíveis, respeitando
as permissões abaixo. As sessões usam cookies assinados também localmente.

Não defina `VERCEL=1` ou `HEALTHON_READ_ONLY=1` para o desenvolvimento normal.
O arquivo `.env` não é carregado automaticamente; exporte as variáveis no shell.

### Permissões

- Médico: dashboard com contagens próprias; pacientes cadastrados por ele ou com
  prescrições emitidas por ele; somente suas prescrições e respectivos itens.
  Pode consultar e gerenciar o catálogo de medicamentos no ambiente local.
- Paciente: somente dashboard, listagem e detalhes das próprias prescrições.
- Farmácia: consulta das prescrições para validação e dispensação, conforme o fluxo
  acadêmico original; somente seus próprios dados e farmacêuticos. Não acessa o
  cadastro geral de pacientes nem edita receitas. A consulta global de receitas
  é uma permissão explícita desse perfil neste sistema de demonstração.
- Criação de contas de médicos/farmácias: administração Django local (`/admin/`),
  não pelos perfis clínicos. O perfil farmacêutico não tem dashboard/login próprio.
- Na demonstração, todas as operações de escrita e os formulários de alteração
  são bloqueados inclusive por URL, qualquer que seja o perfil. `/admin/` fica
  indisponível. Apenas views de consulta explicitamente autorizadas e login/logout
  são executados. Os controles de alteração ficam ocultos na interface.

### Banco fictício e verificação local

```bash
python scripts/build_demo.py
python manage.py test
python scripts/check_demo.py
```

O primeiro comando cria um banco **novo**, executa as migrações nele e insere dados
fictícios definidos no próprio script. Não abre/copia o banco local nem lê o fixture
legado. Cada build substitui `demo/demo.sqlite3`; o artefato é ignorado pelo Git.
O script de verificação abre esse arquivo com `mode=ro&immutable=1`, testa login,
logout, dashboards, CSRF, HTTPS, cookies e o bloqueio de todas as rotas de escrita,
e verifica que o conteúdo do arquivo permaneceu igual. Uma tentativa de escrita
pelo ORM também precisa falhar com erro de banco somente leitura.

Contas públicas **exclusivamente fictícias**, senha `demo123`:

| Perfil | Documento | Conta adicional para testar isolamento |
| --- | --- | --- |
| Médico | `22222222222` | `55555555555` |
| Paciente | `11111111111` | `44444444444` |
| Farmácia | `33333333333` | `66666666666` |

As credenciais `123` descritas anteriormente pertencem somente ao fixture legado
local; esse fixture não é usado na demonstração publicada.

Para simular produção em outro terminal, após gerar o banco:

```bash
export HEALTHON_READ_ONLY=1
export SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
python manage.py check --deploy
python manage.py collectstatic --noinput
```

O modo de produção exige HTTPS e cookies seguros; `runserver` HTTP puro não é um
ambiente de teste de login de produção. `scripts/check_demo.py` usa requisições
HTTPS simuladas com o cliente Django. Para voltar ao modo local, remova as variáveis
com `unset HEALTHON_READ_ONLY SECRET_KEY`.

### Publicação, somente após autorização

1. Revise os arquivos e autorize separadamente commit/push e publicação. Conectar
   um repositório à Vercel pode disparar deploy automaticamente; faça isso apenas
   após autorizar a publicação.
2. Importe a raiz do projeto na Vercel com o preset Django. Pela CLI, utilize
   Vercel CLI **50.38.0 ou superior**. O projeto usa a detecção nativa de `manage.py`
   e `healthon.wsgi.application`, sem builders legados ou rewrites globais.
3. Configure as variáveis em **Production e Preview**:

   | Variável | Valor |
   | --- | --- |
   | `SECRET_KEY` | Chave aleatória exclusiva, pelo menos 50 caracteres; gere com `get_random_secret_key()` e armazene somente na Vercel |
   | `ALLOWED_HOSTS` | Hosts exatos separados por vírgula, ex.: `healthon-exemplo.vercel.app,saude.exemplo.com` |
   | `CSRF_TRUSTED_ORIGINS` | Origens HTTPS exatas, ex.: `https://healthon-exemplo.vercel.app,https://saude.exemplo.com` |

   A Vercel fornece `VERCEL=1`, que força modo somente leitura, `DEBUG=False`, HTTPS,
   HSTS e cookies seguros. `VERCEL_URL` e `VERCEL_PROJECT_PRODUCTION_URL` acrescentam
   os hosts exatos gerados pela plataforma. Requisições de mesma origem passam na
   validação CSRF; inclua origens adicionais somente quando forem necessárias.
   Não use curingas nem coloque a chave em arquivos versionados.
4. Mantenha o build definido por `[tool.vercel.scripts]` em `pyproject.toml`:
   `python scripts/build_demo.py`. Remova eventuais overrides antigos no painel.
   A Vercel instala as dependências e executa `collectstatic` automaticamente a
   partir de `STATIC_ROOT`; os estáticos são servidos pelo CDN em `/static/`.
5. `.vercelignore` exclui bancos preexistentes, ambientes virtuais e diretórios
   locais, inclusive `.aws`, `.codex`, `.agents` e `.vscode`. `vercel.json` inclui
   explicitamente apenas o SQLite de demonstração gerado e reforça exclusões no
   bundle da função. Antes da primeira publicação, inspecione o bundle do build:
   ele deve conter `demo/demo.sqlite3` e nunca `db.sqlite3`, `dados_iniciais.json`,
   `.env*` ou diretórios de credenciais. Não faça upload manual do banco original.
6. Após autorização, publique pela interface ou CLI e confirme no endereço HTTPS:
   login dos três perfis, consultas, logout, CSS e respostas 403 para alterações.
   A integração real com o ambiente Vercel só pode ser validada após esse passo.

Referência utilizada: [documentação oficial de Django na Vercel](https://vercel.com/docs/frameworks/full-stack/django).
A versão de Python está fixada em `.python-version`; mantenha as dependências de
`pyproject.toml` e `requirements.txt` sincronizadas ao atualizá-las.

### Limitações

- Demonstração estática: cada atualização de dados exige novo build; não há
  persistência de cadastros, dispensações, auditoria ou recuperação de senha.
- `UsuarioFake` mantém a autenticação acadêmica com senhas em texto simples. O
  artefato contém somente senhas públicas fictícias. Este preparo não transforma
  o sistema em uma aplicação clínica para dados reais.
- Cookies assinados protegem a integridade, mas não criptografam o conteúdo. Não
  coloque dados sensíveis na sessão. Logout apaga o cookie do navegador; uma cópia
  previamente roubada continua utilizável até expirar (uma hora). Não há revogação
  centralizada sem armazenamento de sessões.
- `immutable=1` exige que o banco não seja alterado durante a execução da função;
  o build gera o arquivo completo e o runtime apenas o lê.
- Bootstrap e Bootstrap Icons continuam usando o CDN externo já existente.

## Popular os perfis existentes com dados acadêmicos

No ambiente local, com as migrações já aplicadas e o modo somente leitura desativado:

```bash
venv/bin/python manage.py seed_demo
```

Se o ambiente virtual estiver ativado, use `python manage.py seed_demo`. O comando
exige pelo menos um médico, paciente e farmácia já cadastrados; não cria pessoas,
usuários ou perfis e não modifica senhas. Toda a operação ocorre em uma transação.

O seed disponibiliza um catálogo de 10 medicamentos, com apresentações e
concentrações ilustrativas, reaproveitando medicamentos equivalentes já existentes.
Adiciona 12 prescrições com códigos `HO-DEMO-V1-001` a `HO-DEMO-V1-012`, 18 itens,
os quatro status suportados e, com os dois pacientes do exemplo, 3 dispensações
(`Venda`) com 5 itens (`ItemVenda`). As receitas são distribuídas entre os pacientes
existentes; quando há médico responsável cadastrado, o vínculo é respeitado.
As datas usam a data local do primeiro seed; receitas vencidas têm validade passada.
Reexecuções preservam as datas e os dados existentes e não duplicam os exemplos.
Uma colisão de código com registro que não pertence ao seed cancela a transação.

Além disso, receitas anteriores sem medicamentos recebem um item ilustrativo;
nenhum campo original da receita é sobrescrito. Medicamentos reaproveitados também
não são alterados. Os totais criados são exibidos ao término do comando. Edições
posteriores dos exemplos não são sobrescritas nas reexecuções.

O model `Venda` relaciona farmácia, paciente, prescrição e itens, mas não possui
campo de farmacêutico. O seed utiliza as farmácias existentes e preserva os
farmacêuticos; não exige/cria funcionários. Não há página própria de vendas no
sistema: a dispensação aparece como status da receita no dashboard e nas consultas;
os detalhes financeiros ficam registrados em `Venda`/`ItemVenda`.

Na Vercel, `scripts/build_demo.py` continua criando um banco independente, com as
mesmas seis contas públicas e senha `demo123`, e agora chama a mesma função de seed.
O resultado do build tem 11 medicamentos, 14 prescrições (as duas originais mais
12 novas), 20 itens de prescrição, 3 vendas e 5 itens de venda. O runtime continua
somente leitura e o comando `seed_demo` recusa execução nesse modo. Para atualizar
a versão publicada será necessário um novo deploy, após autorização.

Os medicamentos usam nomes/apresentações realistas; fabricantes, vínculos,
receitas, preços e instruções são fictícios e não têm finalidade clínica.

Validação:

```bash
venv/bin/python manage.py test
venv/bin/python scripts/build_demo.py
venv/bin/python scripts/check_demo.py
```

Os testes cobrem reexecução, preservação de identidades, reaproveitamento de
medicamentos, rollback de colisões, relações de dispensação, datas/status, listagens,
detalhes, acesso por perfil e funcionamento do banco demonstrativo somente leitura.
