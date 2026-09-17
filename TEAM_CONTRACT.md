# Contrato comum de coordenação

## Escopo e autoridade

- Cada tarefa deve declarar `objetivo`, `escopo`, `fora_do_escopo` e
  `critério_de_aceitação`.
- O agente só pode executar ações autorizadas pela tarefa. Diagnóstico é
  somente leitura por padrão.
- Nunca ler, copiar ou expor valores de secrets, tokens ou credenciais.
- Host, CT, container, checkout, imagem e serviço devem ser identificados
  antes de qualquer alteração.
- Resultados são evidências, não autorização para a próxima ação.

## Delegação

- O coordenador divide o trabalho em tarefas pequenas, independentes e com
  dono único.
- Cada delegação deve conter: `id`, `objetivo`, `critério_de_aceitação`,
  `projeto`, `máquina`, `caminho`, `versão/estado`, `escopo_permitido`,
  `dependências`, `skills/referências` e `entrega_esperada`.
- Não executar trabalho duplicado; registrar bloqueios e divergências.
- Não permitir alterações concorrentes no mesmo checkout: o coordenador deve
  reservar o checkout por tarefa e liberar a reserva no retorno.
- Subagentes só devem ser usados quando a tarefa pedir delegação ou quando o
  coordenador registrar explicitamente a necessidade. Este registro é
  documental; não é um scheduler nem mecanismo automático de execução.

## Entrega obrigatória

Cada agente responde com:

```text
Tarefa: <id>
Estado: concluída | parcial | bloqueada
Escopo verificado: <paths/serviços/versão>
Evidências: <comandos, arquivos, linhas ou observações seguras>
Achados: <fatos; separar hipótese de causa confirmada>
Alterações: nenhuma | <arquivos alterados e motivo>
Validação: passou | falhou | indisponível | não executada
Riscos/bloqueios: <itens>
Próximo passo sugerido: <ação reversível e autorizável>
```

`Arquivos alterados` deve ser `nenhuma` em diagnóstico/revisão. `Verificações`
devem distinguir executada, passou, falhou, indisponível e não executada.

## Identidade de versões

Sempre registrar, quando aplicável: repositório, remote, branch, commit,
imagem/tag, container/CT e caminho montado. Não assumir que `/root` no host e
`/root` no CT100 são a mesma árvore.

## Estados

`planejada` → `em execução` → `concluída`, `parcial` ou `bloqueada`.

`concluída` exige o critério de aceitação; `parcial` indica trabalho útil sem
prova completa; `bloqueada` exige a causa do bloqueio e a informação/autoridade
necessária.

## Ações operacionais

Antes de uma ação operacional, confirmar máquina, serviço e efeito esperado.
Editar código não equivale a implantar. Grafos devem corresponder ao projeto e
à versão; informações relevantes devem ser confirmadas na fonte.

Decisões compartilháveis ficam em documentos próprios com origem, data e
escopo. Não ler bancos internos de memória das ferramentas para sincronizá-las.
Permissões descritas no prompt não substituem controles efetivamente aplicados
pela ferramenta.
