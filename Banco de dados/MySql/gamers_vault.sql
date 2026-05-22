/*-- 1. Cria o banco de dados do gamer vault e entra nele
CREATE DATABASE gamers_vault;
USE gamers_vault;

-- 2. Tabela Fornecedores
CREATE TABLE fornecedores (
    id_fornecedor INT AUTO_INCREMENT PRIMARY KEY,
    nome_fornecedor VARCHAR(100) NOT NULL,
    cnpj_fornecedor VARCHAR(18) UNIQUE NOT NULL,
    email_fornecedor VARCHAR(100) UNIQUE NOT NULL,
    site_fornecedor VARCHAR(150)
);

-- 3. Tabela Usuários
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(100) NOT NULL,
    email_usuario VARCHAR(100) UNIQUE NOT NULL,
    senha_usuario CHAR(60) NOT NULL,
    data_cadastro_usuario DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_usuario ENUM('cliente', 'admin') NOT NULL DEFAULT 'cliente',
    saldo DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

-- 4. Tabela Jogos
CREATE TABLE jogos (
    id_jogo INT AUTO_INCREMENT PRIMARY KEY,
    id_fornecedor_fk INT NOT NULL,
    nome_jogo VARCHAR(150) NOT NULL,
    categoria_jogo VARCHAR(50) NOT NULL,
    data_lancamento_jogo DATE,
    descricao_jogo TEXT,
    preco_base_jogo DECIMAL(10,2) NOT NULL,
    tamanho_download_jogo VARCHAR(50), 
    url_download_jogo VARCHAR(255),
    CONSTRAINT fk_jogo_fornecedor
        FOREIGN KEY (id_fornecedor_fk) REFERENCES fornecedores(id_fornecedor)
        ON DELETE RESTRICT ON UPDATE CASCADE
  );

-- 5 Tabela dos pedidos

CREATE TABLE pedidos (
    id_pedido              INT           AUTO_INCREMENT PRIMARY KEY,
    id_usuario_pedido_fk   INT           NOT NULL,
    status_pedido          ENUM('pendente','pago','cancelado') NOT NULL DEFAULT 'pago',
    valor_pedido           DECIMAL(10,2) NOT NULL,
    forma_pagamento_pedido ENUM('pix','cartao_credito','cartao_debito','boleto') NOT NULL,
    data_pedido            DATETIME      DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pedido_usuario
        FOREIGN KEY (id_usuario_pedido_fk) REFERENCES usuarios(id_usuario)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 6 Tabela que armazena os jogos no pedido

CREATE TABLE item_pedido (
    id_item_pedido        INT            AUTO_INCREMENT PRIMARY KEY,
    id_pedido_fk          INT            NOT NULL,
    id_jogo_pedido_fk     INT            NOT NULL,
    quantidade_item       INT            NOT NULL DEFAULT 1,
    preco_unitario        DECIMAL(10,2)  NOT NULL,    -- preço no momento da compra
    CONSTRAINT fk_itempedido_pedido
        FOREIGN KEY (id_pedido_fk) REFERENCES pedidos(id_pedido)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_itempedido_jogo
        FOREIGN KEY (id_jogo_pedido_fk) REFERENCES jogos(id_jogo)
        ON DELETE RESTRICT ON UPDATE CASCADE
);*/
