--=========================================================

-- TRIGGER 1 : Limitar a 2 pagamentos
-- Uma função que será executada antes do INSERT
CREATE OR REPLACE FUNCTION limitar_pagamentos()
RETURNS TRIGGER AS $$ BEGIN -- Conta quantos pagamentos já existem para o pedido.
    IF (
        SELECT COUNT(*) FROM pagamento
        WHERE id_pedido = NEW.id_pedido
    ) >= 2 THEN -- Se já tiver 2 ou mais, bloqueia a operação.
    RAISE EXCEPTION 'Máximo de 2 pagamentos por pedido';
    END IF;
    -- Se estiver tudo ok, permite inserir o novo registro.
    RETURN NEW;
END;

$$ LANGUAGE plpgsql;

-- Agora ligamos essa função a tabela pagamento

CREATE TRIGGER triger_limitar_pagamentos
BEFORE INSERT ON pagamento -- Executa antes de inserir
FOR EACH ROW -- Executa para cada linha inserida
EXECUTE FUNCTION limitar_pagamentos();

--=========================================================
--=========================================================

-- TRIGGER 2: Validar troco somente para dinheiro
CREATE OR REPLACE FUNCTION validar_troco()
RETURNS TRIGGER AS $$ BEGIN -- Se a forma de pagamento NÃO for dinheiro e mesmo assim tiver troco preenchido.
    IF NEW.forma_pagamento != 'DINHEIRO' AND NEW.troco IS NOT NULL THEN -- Bloqueia a operação.
        RAISE EXCEPTION 'Troco só permitido para pagamento em dinheiro';
    END IF;
    -- Se tiver correto, permite continuar.
    RETURN NEW;
END;

$$ LANGUAGE plpgsql;

-- Associa a função a tabela pagamento

CREATE TRIGGER trigger_validar_troco
BEFORE INSERT OR UPDATE ON pagamento -- Executa antes de inserir ou atualizar
FOR EACH ROW
EXECUTE FUNCTION validar_troco();

--=========================================================
-- OBSERVAÇÃO IMPORTANTE
--=========================================================

-- NEW representa o novo registro que está sendo inserido ou atualizado
-- OLD representaria o registro antigo (em UPDATE/DELETE)

-- Essa triggers garantem:
-- Máximo de 2 pagamentos po pedido.
-- Troco só quando o pagamento dor dinheiro.