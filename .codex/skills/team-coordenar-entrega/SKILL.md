---
name: team-coordenar-entrega
description: Coordene entregas da equipe quando um pedido exigir decomposição, delegação, dependências e integração de evidências.
---

# Team — coordenar entrega

## Objetivo e entradas

Transformar um pedido em tarefas delimitadas, executáveis e integráveis. Receba
o objetivo do solicitante, o repositório/ambiente, o estado conhecido, as
restrições de autoridade e o critério de aceitação.

## Modos operacionais

Escolha um modo e registre uma justificativa curta antes de delegar:

- **Econômico**: padrão para tarefas pequenas, delimitadas e reversíveis;
  use um executor e as verificações pertinentes. Não crie subagentes apenas
  para representar papéis.
- **Padrão**: para complexidade moderada; use executor e verificação
  independente escolhida pelo risco, evitando repetir a mesma análise.
- **Ampliado**: para tarefas complexas ou de impacto relevante; acione os
  especialistas necessários e paralelize apenas tarefas independentes.

Amplie o modo quando surgir risco concreto coberto pela autorização existente;
não peça confirmação para uma escolha já autorizada.

## Procedimento e decisões

1. Leia `TEAM_CONTRACT.md`, o registro relevante e as definições dos papéis.
2. Separe resultado desejado, não-objetivos, dependências e riscos; escolha o
   modo proporcional e registre a justificativa.
3. Defina cada tarefa com id, responsável, caminho, versão, escopo, critérios,
   referências e entrega esperada; reserve o checkout apenas documentalmente.
4. Delegue somente trabalho independente e autorizado. Não paralelize tarefas
   que escrevam os mesmos arquivos.
5. Acompanhe estados e evidências; investigue divergências antes de integrar.
6. Forneça resumo suficiente e referências pertinentes; evite copiar histórico
   completo, faça buscas direcionadas antes de leituras extensas e carregue
   auxiliares somente quando agregarem valor.
7. Mantenha no resumo critérios, restrições e evidências. Deixe logs extensos
   em arquivos e retorne somente trechos relevantes; reutilize resultados
   anteriores apenas quando projeto, versão e condições forem aplicáveis.
8. Encerre quando os critérios estiverem suficientemente verificados. Não
   repita testes ou revisões sem mudança relevante ou dúvida concreta; limite
   tentativas e registre impedimento quando houver repetição sem progresso.

## Limites e dependências

Não é scheduler, lock, autorização de deploy ou substituto do dono do serviço.
Não leia segredos. Use `cavecrew` apenas quando delegação comprimida for
explicitamente solicitada; use `verify-and-stop` para a prova final.
Não reduza testes necessários, remova validações ou omita falhas para economizar.
Não altere modelos, provedores, planos ou roteamento. O custo por tarefa aceita
é a métrica principal; não presuma economia financeira por paralelismo ou
rapidez.

## Entrega e evidências

Entregue quadro de tarefas, dependências, conflitos, decisão e critério de
encerramento no formato do contrato. Evidencie caminhos, commits, ids reais de
delegação, comandos e resultados; classifique ausente, indisponível e falho.
Quando disponíveis, registre modo, ferramenta, modelo, provedor, número de
agentes/tentativas, tokens de entrada/saída/cache, custo e fonte/data do preço,
resultado e retrabalho. Dados ausentes são `não disponíveis`, nunca zero; não
converta caracteres em tokens.

## Impedimentos

Pare se faltar autoridade, checkout identificado, critério de aceitação ou
prova de uma dependência. Registre a causa concreta e a informação necessária.
