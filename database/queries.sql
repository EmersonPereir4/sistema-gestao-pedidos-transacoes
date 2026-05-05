-- ===========================================================================
-- CONSULTAS ÚTEIS DO SISTEMA
-- Descrição: Queries para análise e relatórios
-- ===========================================================================

-- Total faturado
SELECT SUM(valor_total)
FROM pedido
WHERE status = 'PAGO';

-- Pedidos por cliente
SELECT c.nome, COUNT (p.id_pedido) AS total_pedidos
FROM pedido p
JOIN cliente c ON p.id_cliente = c.id_cliente
GROUP BY c.nome
ORDER BY total_pedidos DESC;

-- Quantidade por forma de pagamento
SELECT forma_pagamento, COUNT(*) AS total
FROM pagamento
GROUP BY forma_pagamento
ORDER BY total DESC;

-- Total faturado por forma de pagamento
SELECT forma_pagamento, SUM(valor_pago) AS total
FROM pagamento
GROUP BY forma_pagamento
ORDER BY total DESC;

-- Faturamento dos últimos 15 dias
SELECT SUM(valor_pago)
FROM pagamento
WHERE data_pagamento >= CURRENT_DATE - INTERVAL '15 days';

-- Forma de pagamento mais utilizada
SELECT forma_pagamento, COUNT(*) AS total
FROM pagamento
GROUP BY forma_pagamento
ORDER BY total DESC
LIMIT 1;