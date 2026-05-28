# Camada de Serviços e Regras de Negócio

No projeto **Gamers Vault**, o arquivo `backend.py` centraliza toda a lógica pesada da aplicação. Ele atua como o "cérebro" que protege o Banco de Dados de inputs nocivos e orquestra a criptografia e o processamento de transações.

Evitamos intencionalmente mesclar o SQL nos menus interativos. Esta seção detalha os mecanismos empregados na camada de serviço.

---

## 🛡️ 1. Sanitização e Validação Preventiva (Fail-Fast)

Para garantir a higienização dos dados antes de chegarem ao banco (reduzindo tráfego desnecessário e prevenindo SQL Injection), o script possui bloco de validadores imutáveis.

### Práticas Aplicadas:
- **Tratamento de Expressões Regulares (Regex):** 
  Usado extensamente em funções como `validar_preco()` (para garantir que seja apenas número ou formato decimal `.99`) e no `validar_cnpj()` (exigindo o formato estrito `XX.XXX.XXX/XXXX-XX`).
- **Strip & Type Checking:**
  Garante que campos de `id` (`validar_id`) sejam nativamente `.isdigit()` positivos e sem espaços colaterais (`.strip()`), bloqueando injeção e travando o CRUD num ciclo inquebrável, preservando o terminal no `try/catch`.
- **Lógica de Tempo:** 
  O método `validar_data()` possui "Easter-eggs" técnicos, impedindo o cadastro de jogos lançados no futuro ou antes de 1972 (data do primeiro jogo eletrônico comercial).

---

## 🔑 2. Criptografia e Autenticação Dinâmica

As senhas dos usuários nunca trafegam nuamente no escopo da aplicação, usando a biblioteca de indústria `bcrypt`.

### Como o Login e Cadastro foram manipulados:
Ao invocar `cadastrar_usuario()`:
1. O Python gera um *Salt* randômico associado restritamente àquele usuário via `bcrypt.gensalt()`.
2. A senha passa pelo processo de hashing e é gravada no MariaDB em um campo tipificado como `CHAR(60)`.
3. No momento do acesso (`login_usuario`), não recuperamos a senha legível do banco; apenas comparamos o hash digitado de entrada com o hash em base via `bcrypt.checkpw()`.

> [!NOTE]
> É aqui na camada de serviço que abstraímos a *Simulação de Carteira Virtual*. Como o MVP não inclui gateways de pagamento reais como Stripe ou MercadoPago, a função de cadastro aciona a lib estática `random` para jogar um saldo flutuante atrativo na conta do novo cliente (0 a R$2000,00).

---

## 🛒 3. Dicionários de Memória x Conexão SQL

Uma das transações que mais exigem poder de processamento em e-commerces é o "Carrinho de Compras". Adicionar ou remover um item do carrinho reflete imediatamente em escritas/leituras de disco se manipuladas através de SQL direto.

**Nossa Abordagem (Sessões In-Memory):**
O *Carrinho do Cliente* no Gamers Vault é instanciado pura e unicamente como uma Collection Dictionary `{}` no Python, enquanto o menu estiver aberto.

O banco só escuta o carrinho de fato na hora do Checkout, acionando o método `registrar_pedido_com_itens()`.

### Transações e Estorno (Rollback) Dinâmico
A inserção de um pedido é múltipla: desconta dinheiro, grava pedido e grava sub-itens.
Se o sistema perder conexão de internet durante essa etapa contínua, os dados podem corromper (ex: cliente perde o dinheiro, mas não recebe o item). Para obviar isso:
```python
    except Exception as err:
        conexao.rollback()
        raise Exception(f"Erro ao registrar pedido: {err}")
    finally:
        if cursor:
            cursor.close()
```

**O Processo ACF:**
Garantimos a Atomicidade das operações chamando um conexao.rollback() nos blocos except. Só chamamos commit() se todas as frentes executarem assertivamente

E em todos os métodos, sem exceções, aplicamos o fechamento do cursor nas linhas do finally, anulando vazamentos de memória (Memory Leaks) nas conexões com o MySQL.