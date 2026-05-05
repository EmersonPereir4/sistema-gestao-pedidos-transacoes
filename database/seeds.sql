--==========================================================
-- INSERÇÃO DE DADOS INICIAIS (SEEDS)
--==========================================================


--==========================================================
-- USUÁRIOS
--==========================================================
--- Usuário admin padrão
INSERT INTO usuario (login, senha, tipo)
VALUES ('admin', 'admin123', 'ADMIN');


--==========================================================
-- PRODUTOS
--==========================================================
-- TABELA PRODUTOS (TIPOS DE JOGOS)
-- Inserimos os jogos disponíveis no sistema
-- Cada registro representa um tipo de jogo com suas regras
INSERT INTO produto (
    nome, -- Nome do jogo (Único no sistema)
    descricao, -- Explicação para o usuário
    valor_unitario, -- Precço de uma aposta
    numeros_por_aposta, -- Quantidade de números a serem escolhidos
    numero_maximo -- Maior número permitido
) VALUES

--==========================================================
-- Jogo 1: QuinaMax
--==========================================================
(
    'QuinaMax',
    'Escolha 5 números de 1 a 50',
    5.00,
    5,
    50
) ON CONFLICT (nome) DO NOTHING; -- Evita duplicação caso o script seja executado mais de uma vez.

INSERT INTO pedido (id_cliente, id_usuario, valor_total, status)
VALUES (1, 1, 0, 'PENDENTE')
RETURNING id_pedido;

INSERT INTO item_pedido (id_pedido, id_produto, quantidade, valor_unitario, valor_total)
VALUES (2, 1, 1, 5.00, 5.00)
returning id_item;

INSERT INTO item_pedido (id_pedido, id_produto, quantidade, valor_unitario, valor_total)
VALUES (2, 2, 2, 10.00, 20.00)
returning id_item;


INSERT INTO aposta (id_item, numeros)
VALUES (3, '[1, 5, 10, 20, 30]');

INSERT INTO aposta (id_item, numeros)
VALUES
(4, '[1, 2, 3, 4, 5, 6]'),
(4, '[1, 2, 3, 4, 5, 6]');


UPDATE pedido
SET valor_total = 25.00
WHERE id_pedido = 2;

SELECT * FROM pedido;
SELECT * FROM item_pedido;
SELECT * FROM aposta;