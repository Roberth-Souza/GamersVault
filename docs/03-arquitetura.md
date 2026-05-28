# Arquitetura e Engenharia do Sistema

Esta seção mapeia como o código fonte, os fluxos de interface e o banco de dados do **Gamers Vault** se comunicam para manter a estabilidade do produto em funcionamento.

---

## 🏗️ Padrão de Arquitetura (Modularização)

O projeto rejeitou a ideia do "Arquivo Único" (`God Object`) desde as sprints iniciais. Adotamos um formato rudimentar de **Separação de Responsabilidades (Separation of Concerns)** inspirado no MVC. Isso tornou a base de código previsível e fácil de dar manutenção:

1. **Camada de Entrypoint (`main.py`):** O roteador inicial. Recebe o usuário recém-chegado e age apenas como Porteiro (Cadastro ou Login). Passando do porteiro, ele transfere a autoridade da tela para um dos Menus.
2. **Camadas de Apresentação (View):** `menu_cliente.py` e `menu_admin.py` não possuem conexões diretas em SQL com o Banco. O trabalho desses arquivos é exclusivamente **Dialogar** com o usuário (inputs e prints formatados) e enviar os comandos validados para as funções corretas processarem o trabalho pesado.
3. **Camada de Core/Serviço (`backend.py`):** O cérebro do E-commerce. O único arquivo com acesso à biblioteca de criptografia (`bcrypt`) e à execução de `cursors` no Banco MySQL. Aqui ficam as amarrações lógicas (Validações de email e senha, inserções SQL e proteções de constraints).
4. **Camada Isolada de Persistência (`conexao.py`):** Um construtor desacoplado do `mysql.connector`. Apenas conecta e devolve o túnel aberto, caso um dia o driver seja mudado, só alteramos um único arquivo.

---