# Gamers Vault 🎮

Um sistema completo de loja de jogos digitais desenvolvido em Python com integração a um banco de dados MySQL. Este projeto simula uma plataforma robusta de distribuição virtual, contando com controle de acesso, criptografia de senhas, validações de dados e gerenciamento financeiro completo para clientes e administradores. 🚀

---
## 📖 Documentação Completa

Para um entendimento profundo da arquitetura, validações (Fail-fast/Regex), regras de estorno e diagramas de banco de dados, organizamos toda a engenharia de software em um diretório à parte.

👉 **Para explorar os detalhes técnicos, leia a documentação completa aqui: [Acessar Índice de Documentação](docs/00-index.md)**

---

## 🚀 Funcionalidades

O sistema conta com dois painéis distintos, adaptando a experiência para diferentes perfis de usuários.

### 🎲 Sistema de Saldo Dinâmico
Ao realizar o cadastro, cada novo cliente recebe um **saldo inicial aleatório entre R$ 0,00 e R$ 2.000,00**, gerado automaticamente através da biblioteca padrão `random`. *(Dica : cadastre-se com o email `roberth@email.com` para acionar um Easter Egg de saldo infinito na conta! )*

### 👨‍💻 Painel do Administrador (Admin)
- **Gestão de Usuários:** Listar, buscar, promover (para admin) ou deletar contas.
- **Gestão de Fornecedores:** Cadastrar, consultar, editar dados e remover empresas desenvolvedoras de jogos.
- **Gestão de Jogos:** Adicionar novos títulos ao catálogo vinculados aos seus fornecedores, editar preços, categorias e deletar produtos.
- **Gestão de Pedidos:** Acompanhar histórico geral de vendas e alterar os status dos pedidos no sistema.

### 🕹️ Painel do Cliente
- **Catálogo Interativo:** Visualizar e explorar jogos, aplicando filtros por categorias, buscar por fornecedores específicos ou ordenar pelo preço.
- **Carrinho de Compras:** Sistema completo de sessão no qual o usuário adiciona os jogos de interesse e visualiza o subtotal.
- **Checkout Seguro:** Validação de saldo no momento do pagamento e escolha da forma de pagamento ideal (Pix, Cartão de Crédito, Débito ou Boleto).
- **Extrato e Histórico:** Visualização da carteira e recibos detalhados de compras passadas.

---

## 🛠️ Tecnologias & Ferramentas

- **Linguagem:** Python 3 🐍
- **Banco de Dados:** MySQL 🐬
- **Bibliotecas Externas:** 
  - `mysql-connector-python` (Conexão e queries ao banco)
  - `bcrypt` (Hashing seguro e validação de senhas)
- **Built-in Python:** `random`, `re`, `datetime`

---

## 📂 Estrutura de Arquivos

Uma arquitetura separada e modularizada, pensada para manter o código testável e limpo:

- `main.py`: Ponto de entrada da aplicação. Orquestra o menu inicial e fluxos de identificação (cadastro e login).
- `backend.py`: Core do negócio. Aqui residem todas as consultas e inserções em SQL, bem como regras rígidas de negócio e sanitização de dados.
- `menu_admin.py`: Lógica de interface de terminal voltada para as permissões do administrador.
- `menu_cliente.py`: Lógica de interface para o fluxo de busca, escolha e checkout do usuário padrão.
- `conexao.py`: Script isolado responsável pelo _handshake_ (conexão) ao SGBD MySQL.
- `gamers_vault.sql`: Script DDL. Responsável pela prototipação do banco conceitual, criação de tabelas, constrições, _foreign keys_ e enumeradores.
- `requirements.txt`: Acervo contendo as versões exata das sub-dependências do ambiente.

---

## 🗄️ Banco de Dados

O banco central relacional se chama `gamers_vault` e é moldado da seguinte forma:
- **`fornecedores`**: Armazena as parceiras dev/publisher.
- **`usuarios`**: Registra todos perfis ativos em plataforma, separando em níveis de hierarquia.
- **`jogos`**: Tabela principal constando os ativos de venda e metadados lúdicos associados.
- **`pedidos` & `item_pedido`**: Associação complexa **(1-N / N-M)**, protegendo o status temporal da compra (como preço pago no passado), interligado em restrição e gatilho de cascata.

---

## 🌐 Protótipo Web (UI/UX)

Além do núcleo em Python/CLI do sistema, projetamos um **protótipo em html** demonstrativo em formato Web para ilustrar como seria a experiência final do nosso cliente. 

O protótipo é construído com a tela do smartphone em mente. O objetivo é permitir simular as transições, os menus de configurações, o painel de perfil e a jornada completa de e-commerce!

Você pode testar e navegar pelo resultado desse protótipo renderizado em tempo real pelo GitHub Pages:
👉 **[Acessar e Testar Protótipo Web - Gamers Vault](https://roberth-souza.github.io/GamersVault/)**

👉 **Para mais informações detalhadas sobre as escolhas de design, fluxos e wireframes, leia a [documentação do protótipo aqui](docs/02.5-prototipo.md).**

---

## ⚙️ Como Instalar e Rodar

**1. Clone/Baixe este projeto.**

**2. Prepare o Banco de Dados:**
- Pelo seu terminal, ou ferramenta visual (como DBeaver / Workbench), execute o script `gamers_vault.sql` em seu servidor MariaDB ou MySQL.

**3. Configure suas Credenciais:**
- Acesse o arquivo `conexao.py` em seu VS Code.
- Altere os campos (como `user` e `password`) para os dados correspondentes à sua máquina.

**4. Configurando o Ambiente Python (Virtual Environment)**
Recomendamos o uso de ambientes virtuais para não sujar o seu sistema. Abra o terminal na raiz do Gamers Vault:

Crie o ambiente virtual:
```bash
python3 -m venv .venv
```

Ative o ambiente virtual:
* **Linux/Mac/CachyOS:**
  ```bash
  source .venv/bin/activate
  ```
* **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\activate
  ```
No terminal, certifique-se de estar na pasta do projeto e rode:
```bash
pip install -r requirements.txt
```

**5. Start na Aplicação:**
Ainda com terminal ativo no diretório da pasta `EXPOTECH`, inicialize via:
```bash
python main.py
```

---

## 👥 Desenvolvido por

Grupo 128 — Projeto acadêmico para EXPOTECH 2026, 1º período de Ciência da Computação.

---

## ⚠️ Aviso Legal (Disclaimer)

A **Gamers Vault** não é uma loja real. Trata-se exclusivamente de um projeto acadêmico e uma simulação de e-commerce criado para fins educacionais. O sistema não aceita métodos de pagamento de verdade, não coleta dados financeiros reais e não comercializa nenhum tipo de produto verdadeiro.