---
name: team-implementar-tarefa
description: Implemente uma mudança delimitada quando checkout, contrato, arquivos responsáveis e autorização estiverem definidos.
---

# Team — implementar tarefa

## Objetivo e entradas

Entregar a menor alteração coerente que satisfaça o critério. Receba tarefa,
checkout, commit/branch, contrato, arquivos/símbolos responsáveis, restrições,
dependências e prova esperada.

## Procedimento e decisões

1. Confirme repositório, branch, commit e alterações alheias; nunca sobrescreva
   trabalho não relacionado.
2. Leia implementação e testes relevantes e trace o fluxo que possui o
   comportamento. Escolha a camada responsável.
3. Para correção estreita use `surgical-patch`; para estrutura use
   `safe-refactor`; para fatia nova use `lean-build`.
4. Implemente somente o escopo autorizado, preservando interfaces, erros e
   compatibilidade não mencionados como mudança.
5. Rode verificações focadas e registre o diff, riscos e o que não foi testado.

## Limites e dependências

Não faça deploy, migração, instalação ou limpeza incidental. Não altere
segredos/configuração global. Dependências novas exigem justificativa e
autorização própria.

## Entrega e evidências

Entregue arquivos/linhas e motivo, critérios atendidos, comandos/resultados,
commit e riscos no formato do contrato. Diferencie validação executada de
prova apenas por inspeção.

## Impedimentos

Pare se checkout, contrato, autoridade ou causa responsável não estiverem
claros; reporte a menor pergunta que desbloqueia a implementação.
