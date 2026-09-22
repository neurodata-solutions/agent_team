# Agent Improvement Loop

Ciclo local para melhorar agentes a partir de execuções reais, feedback e
avaliações reproduzíveis. Ele complementa o `TEAM_CONTRACT.md`; não substitui
aprovação, revisão humana ou autorização operacional.

## Fluxo

1. Defina o que significa pronto e quais afirmações precisam de evidência.
2. Registre a execução em uma cópia de `templates/trace.template.json`.
3. Registre feedback em uma cópia de `templates/feedback.template.json`.
4. Transforme um defeito ou padrão recorrente em `templates/eval-case.template.json`.
5. Proponha uma mudança pequena no harness e registre o handoff em uma cópia
   de `templates/handoff.template.md`.
6. Rode novamente os checks, compare o resultado e atualize o caso de avaliação.

O registro deve conter referências seguras a arquivos, comandos e artefatos,
mas nunca valores de secrets, tokens, cookies, chaves ou credenciais.

## Estrutura recomendada

```text
improvement-loop/
  templates/       # modelos versionados
  traces/          # execuções reais, se o projeto optar por versioná-las
  feedback/        # feedback e achados normalizados
  evals/           # casos e resultados de avaliação
  handoffs/        # propostas de mudança no harness
  scripts/         # validação local sem dependências
```

As pastas de dados podem permanecer fora do Git quando contiverem material
sensível. O caminho e o commit de origem ainda devem ser registrados.

## Validação

```bash
python3 scripts/validate_record.py trace templates/trace.template.json
python3 scripts/validate_record.py feedback templates/feedback.template.json
python3 scripts/validate_record.py eval templates/eval-case.template.json
```

O validador confere formato e campos mínimos; não prova que a execução, o
commit, o artefato ou a conclusão são verdadeiros. Essa prova exige observar a
fonte primária e seguir o contrato da equipe.

## Entrega

Use o formato obrigatório do contrato: `Tarefa`, `Estado`, `Escopo verificado`,
`Evidências`, `Achados`, `Alterações`, `Validação`, `Riscos/bloqueios` e
`Próximo passo sugerido`.
