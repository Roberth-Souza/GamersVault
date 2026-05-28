# Visão Geral do Projeto

O **Gamers Vault** é uma plataforma digital planejada para simplificar a  distribuição de jogos. O projeto foi concebido sob a metodologia ágil (Scrum) visando entregas incrementais de valor.

## 🎯 Objetivo
Desenvolvimento de um aplicativo (sistema de terminal em Python) focado no ecossistema de uma loja de jogos moderna.

## 👥 Público-Alvo
Gamers com faixa etária entre **16 e 35 anos**, abrangendo desde jogadores casuais até entusiastas hardcore. O sistema foi pensado para englobar os consumidores e unificar a relação entre fornecedores de jogos e a comunidade consumidora.

---

## 📋 Escopo do Projeto

Na sua essência técnica, o Gamers Vault é um **sistema CRUD (Create, Read, Update, Delete)** completo e relacional, conectado a um banco de dados MySQL. O projeto viabiliza a criação, listagem, atualização e exclusão segura de quatro grandes eixos de dados: Usuários, Fornecedores, Jogos e Pedidos.

Abaixo estão os pilares de desenvolvimento do sistema:

### Principais Funcionalidades (Core Features)

Nesta primeira versão , focamos em construir a base transacional e de segurança da plataforma:

**🔐 Segurança e Gestão de Contas**
O sistema possui diferentes níveis de acesso (Administrador e Cliente). O registro de usuários é protegido por algoritmos de criptografia de ponta (bcrypt), garantindo que as senhas nunca fiquem expostas no banco de dados.
Além disto, o sistema possui diversas validações de segurança, como sanitização rigorosa de entradas afim de evitar SQL Injection, validação de formatos de email, nome, sites e outros campos de cadastro

**💰 Carteira Virtual (Simulação de Saldo)**
Para viabilizar a experiência completa de e-commerce nesta versão, implementamos um sistema dinâmico de carteira. Ao se cadastrar, a plataforma simula um aporte inicial gerando um saldo aleatório para o cliente flexibilizar suas compras de teste no catálogo, além de prever bloqueios automáticos caso a compra exceda o valor em conta.

**🫱🏻‍🫲🏾 Gestão de Múltiplos Fornecedores e Catálogo**
O ecossistema é alimentado pelos administradores, que gerenciam as empresas publicadoras (fornecedores) e seus respectivos jogos. O cliente final consome esse catálogo através de uma interface de busca filtrável por categorias ou ordenação de preços.
O sistema também conta com medidas de segurança, não permitindo a exclusão de um fornecedor caso haja jogos ou pedidos vinculados a ele, garantindo a integridade referencial do banco de dados.

**🛒 Processamento de Pedidos e Histórico**
Um motor de checkout completo que permite ao usuário adicionar múltiplos itens na sessão (Carrinho de Compras). Ao finalizar, o sistema isola o pedido no banco de dados, "congelando" o preço unitário do jogo no momento da transação. Isso garante consistência contábil, permitindo que o administrador altere o preço do jogo no futuro sem corromper o histórico de compras antigas do cliente.

### Roadmap de Funcionalidades Futuras:
- [ ] **Integração de Jogos Físicos:** Expansão do banco de dados para controlar estoque físico e frete.
- [ ] **Módulo de Comunidade e Reviews:** Permitir que clientes analisem jogos e interajam uns com os outros.
- [ ] **Interface Gráfica (GUI Web):** Migrar a interface moderna para React ou outro framework de Front-end, acoplada a este próprio backend.

---

## 👨‍💻 Equipe e Organograma (Scrum Framework)

A equipe foi dividida usando metodologias ágeis para garantir o foco no produto:

| Papel | Nome |
| :--- | :--- |
| **Product Owner (PO)** | Roberth Souza da Silva |
| **Scrum Master** | Yan Santa Helena |
| **Desenvolvedor** | João Victor Cohen |
| **Desenvolvedor** | Arthur Rabelo |
| **Desenvolvedor** | Bernardo Scorse |
