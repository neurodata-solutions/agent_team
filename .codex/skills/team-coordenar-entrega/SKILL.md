---
name: team-coordenar-entrega
description: Coordene entregas da equipe quando um pedido exigir decomposição, delegação, dependências e integração de evidências.
---

# Team — coordenar entrega

## Objetivo e entradas

Transformar um pedido em tarefas delimitadas, executáveis e integráveis. Receba
o objetivo do solicitante, o repositório/ambiente, o estado conhecido, as
restrições de autoridade e o critério de aceitação.

## Procedimento e decisões

1. Leia `TEAM_CONTRACT.md`, o registro relevante e as definições dos papéis.
2. Separe resultado desejado, não-objetivos, dependências e riscos.
3. Defina cada tarefa com id, responsável, caminho, versão, escopo, critérios,
   referências e entrega esperada; reserve o checkout apenas documentalmente.
4. Delegue somente trabalho independente e autorizado. Não paralelize tarefas
   que escrevam os mesmos arquivos.
5. Acompanhe estados e evidências; investigue divergências antes de integrar.
6. Encerre quando todos os critérios tiverem prova suficiente, registrando
   limitações e próximo passo reversível.

## Limites e dependências

Não é scheduler, lock, autorização de deploy ou substituto do dono do serviço.
Não leia segredos. Use `cavecrew` apenas quando delegação comprimida for
explicitamente solicitada; use `verify-and-stop` para a prova final.

## Entrega e evidências

Entregue quadro de tarefas, dependências, conflitos, decisão e critério de
encerramento no formato do contrato. Evidencie caminhos, commits, ids reais de
delegação, comandos e resultados; classifique ausente, indisponível e falho.

## Impedimentos

Pare se faltar autoridade, checkout identificado, critério de aceitação ou
prova de uma dependência. Registre a causa concreta e a informação necessária.
