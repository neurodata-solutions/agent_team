---
name: team-testar-software
description: Desenhe e execute testes autorizados de software, classificando regressões entre produto, teste e ambiente.
---

# Team — testar software

## Objetivo e entradas

Produzir prova reproduzível do comportamento solicitado. Receba contrato,
critérios, versão, comando existente, dados/fixtures e limites de alteração.

## Procedimento e decisões

1. Converta critérios em matriz cenário→resultado, priorizando caminhos de
   risco e regressão.
2. Reuse fixtures e comandos existentes; crie dados isolados somente quando
   autorizado e necessário.
3. Confirme ambiente/dependências sem instalar nada salvo autorização.
4. Execute testes focados, capture saída e exit code, e amplie somente se o
   critério exigir. Não trate processo “running” como prova funcional.
5. Classifique cada falha como produto, teste ou ambiente e preserve reprodução.

## Limites e dependências

Não edite produção, não esconda falhas e não repita campanhas fora do escopo.
Use `verify-and-stop` para encerrar com a menor prova suficiente.

## Entrega e evidências

Entregue matriz, comandos, versões, logs seguros, regressões, cobertura e
limitações no formato do contrato. Informe arquivos alterados; em leitura
somente deve ser `nenhuma`.

## Impedimentos

Marque indisponível quando dependência, ambiente ou fixture impedir execução;
não classifique um erro ambiental como defeito do produto sem prova.
