--=========================================================
-- SISTEMA DE GESTÃO DE PEDIDOS E TRANSAÇÕES
--=========================================================

--=========================================================

-- TABELA USUARIO
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL, -- ADMIN / FUNCIONARIO / CLIENTE
    ativo BOOLEAN DEFAULT TRUE
)

--=========================================================
--=========================================================

-- TABELA CLIENTE
-- Armazena dados dos clientes.
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY, -- Identificador do cliente.
    id_usuario INTEGER UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL CHECK (length(nome) >= 3), -- Campo não pode ser VAZIO, obrigatório no mínimo 3 caracteres.
    telefone VARCHAR(20) CHECK (telefone IS NOT NULL OR telefone ~ '^[0-9]{10,11}$'), -- Apenas números (DDD + número), entre 10 e 11 dígitos.
    cpf VARCHAR(11) UNIQUE NOT NULL CHECK (cpf ~'^[0-9]{11}$'), -- CPF com exatamente 11 dígitos numéricos e único.
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data automática de cadastro.
    ativo BOOLEAN DEFAULT TRUE, -- Controle de ativação do cliente (não deletar registros).

    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);

--=========================================================
--=========================================================

-- TABELA PEDIDOS
create table pedido (
    id_pedido SERIAL PRIMARY KEY, -- Identificador do pedido.

    id_cliente INTEGER NOT NULL, -- Dono do pedido
    id_usuario INTEGER NOT NULL, -- Quem criou o pedido
    
    valor_total DECIMAL(10, 2) NOT NULL CHECK (valor_total >= 0), -- Valor total do pedido (não pode ser negativo).
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDENTE', 'PAGO', 'CANCELADO')),

    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data e hora do pedido.
    
    CONSTRAINT fk_pedido_cliente
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),

    CONSTRAINT fk_pedido_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

--=========================================================
--=========================================================

-- TABELA PRODUTO
-- Define os tipos de jogos disponíveis.
CREATE TABLE produto (
    id_produto SERIAL PRIMARY KEY, -- Identificador do jogo.
    nome VARCHAR(50) NOT NULL UNIQUE, -- Nome do jogo (não pode repetir).
    descricao TEXT, -- Explicação do jogo (ex: "Escolha 5 números de 1 a 50").
    valor_unitario DECIMAL(10, 2) NOT NULL CHECK (valor_unitario > 0), -- Preço do jogo, não pode ser 0 e nem negativo.
    numeros_por_aposta INT NOT NULL CHECK (numeros_por_aposta > 0), -- Quantidade de números que o jogador deve escolher.
    numero_maximo INT NOT NULL CHECK (numero_maximo > 1),
    prazo_validade_dias INT NOT NULL DEFAULT 7 CHECK (prazo_validade_dias > 0),
    ativo BOOLEAN DEFAULT TRUE, -- Permite ativar/desativar o jogo sem excluir
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



--=========================================================
--=========================================================

-- TABELA ITEM_PEDIDO
CREATE TABLE item_pedido (
    id_item SERIAL PRIMARY KEY, -- Identificador do item.
    id_pedido INTEGER NOT NULL, -- Pedido ao qual o item pertence.
    id_produto INTEGER NOT NULL, -- Produto (jogo) escolhido.
    quantidade INTEGER NOT NULL CHECK (quantidade > 0), -- Quantidade comprada (mínimo 1).
    valor_unitario DECIMAL(10, 2) NOT NULL CHECK (valor_unitario >0), -- Valor no momento da compra (independente do produto).
    valor_total DECIMAL(10, 2) NOT NULL CHECK (valor_total >= 0),

    CONSTRAINT fk_item_pedido_pedido
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),

    CONSTRAINT fk_item_pedido_produto
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);

--=========================================================
--=========================================================

-- TABELA APOSTA
CREATE TABLE aposta (
    id_aposta SERIAL PRIMARY KEY,
    id_item INT NOT NULL, -- Relaciona com o item do pedido.
    numeros JSONB NOT NULL CHECK (jsonb_array_length(numeros) > 0), -- Números escolhidos (formato JSON).
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data de criação da aposta.
    data_validade TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP + INTERVAL '7 days', -- Data limite da validade
    status VARCHAR(20) NOT NULL DEFAULT 'ATIVO'  CHECK (status IN ('ATIVO', 'EXPIRADO', 'CONFERIDO')), -- Estado da aposta.

    CONSTRAINT fk_aposta_item
    FOREIGN KEY (id_item) REFERENCES item_pedido(id_item)
);

--=========================================================
--=========================================================

-- TABELA PAGAMENTO
CREATE TABLE pagamento (
    id_pagamento SERIAL PRIMARY KEY,

    id_pedido INT NOT NULL, -- Pedido ao qual o pagamento pertece.
    id_usuario INTEGER NOT NULL,

    forma_pagamento VARCHAR(20) NOT NULL CHECK (forma_pagamento IN ('PIX', 'DEBITO', 'CREDITO', 'DINHEIRO')), -- Forma de pagamento permitida.

    data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data e hora do pagamento.

    valor_pago DECIMAL(10, 2) NOT NULL CHECK (valor_pago >= 0), -- Valor pago (não pode ser negativo),
    troco DECIMAL(10, 2) DEFAULT 0 CHECK (troco >= 0), -- Troco (somente quando for em dinheiro)

    CONSTRAINT fk_pagamento_pedido
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),

    CONSTRAINT fk_pagamento_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

--=========================================================
--=========================================================

-- Índice criado para melhorar preformance em consultas que filtram ou relacionam pagamentos com pedidos.
-- Evita varredura completa da tabela (full scan) em operações frequente de busca do sistema.
CREATE INDEX idx_pagamento_pedido ON pagamento(id_pedido);
