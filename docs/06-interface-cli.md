# Interface de Linha de Comando (CLI) e UX

Embora o **Gamers Vault** opere exclusivamente no terminal (CLI), a Experiência do Usuário (UX) foi desenhada para ser tolerante a falhas, fluida e amigável. Evitamos as frustrações comuns de sistemas de console que obrigam o usuário a reiniciar o programa por causa de um pequeno erro de digitação.

A interface gráfica de texto é orquestrada separadamente da lógica de banco de dados, dividida principalmente nos arquivos `main.py` (menu de entrada e autenticação), `menu_admin.py` (painel gerencial) e `menu_cliente.py` (loja e carrinho).

---

## 🔄 1. Loops Isolados de Validação (Retenção de Estado)

O principal desafio em formulários CLI (como o cadastro de Fornecedores ou Jogos) é a perda de progresso. Se o administrador preencher o Nome e o Preço corretamente, mas errar a formatação da Data ou do CNPJ, o sistema não deve derrubar toda a operação e fazê-lo começar do zero.

**Nossa Abordagem:**
Desenvolvemos um sistema de mini-loops (`while True`) independentes para cada campo (Input). O sistema "prende" a navegação apenas no campo que falhou a validação. 

Exemplo estrutural utilizado durante o fluxo de registro de um Jogo:

```python
    # O progresso anterior (Nome, Preço, etc) já está salvo na memória local da função.

    while True:
        data_lancamento = input("\nDigite a data de lançamento (YYYY-MM-DD) ou '0' para cancelar: ")
        
        if data_lancamento == '0':
            return # Cancela graciosamente toda a operação
            
        try:
            validar_data(data_lancamento)
            break # Input correto! Quebra esse mini-loop e vai para a próxima pergunta
            
        except ValueError as err:
            # Captura a falha na camada de serviço e exibe sem derrubar a aplicação
            print(f"Erro na data de lançamento: {err}")
            # O laço se repete, pedindo a data novamente.

    # O sistema segue para a próxima etapa (Tamanho do jogo)...
```

Com essa estrutura, aplicamos o conceito de *"Fail-Safe"*. O terminal vira um guia passo-a-passo e interativo, orientando a digitação até o escopo estar 100% perfeito para o envio ao MySQL.

---

## 🛑 2. A Regra do "0"

Para que o usuário não se sinta preso em um beco sem saída caso inicie um cadastro sem querer ou não saiba qual dado inserir, definimos o número `0` como uma "Tecla de Escape Global".

Quase todo campo interativo do sistema escuta se o usuário digitou apenas `"0"`.
- **Nos Formulários e Inputs:** Aciona um `continue` ou `return` na camada visual, descartando as variáveis temporárias e devolvendo o usuário ao menu anterior. Tudo silenciosamente, sem transações pendentes.
- **Nos Menus:** Funciona como o botão de Logout ou Voltar convencional.

Essa uniformidade (saber que o `0` sempre te tira da tela atual e te leva para trás) traz muita segurança para quem opera a aplicação.

---

## 🔀 3. Roteamento de Visualização por Perfil

Em vez de poluir um painel único com dezenas de opções onde metade retornaria "Acesso Negado", a modularização separou drasticamente a apresentação baseada na autenticação.

Após a checagem com o `bcrypt` em `main.py`, a aplicação identifica a flag `"tipo"` do banco:
- Se for **Cliente:** É despejado no `menu_cliente.py`, focando apenas no consumo (Catálogo, Carrinho In-Memory e Histórico de Compras).
- Se for **Admin:** O sistema é flexível. Antes de carregar, ele pergunta se o administrador deseja ir para o Painel Gerencial em si (estoque, fornecedores, controle de pedidos) ou se deseja simular a visão de Cliente para efetuar compras com a própria conta.

Esse é o segredo de separação de responsabilidades (View x Controller) aplicado diretamente e de forma limpa em Python nativo.
