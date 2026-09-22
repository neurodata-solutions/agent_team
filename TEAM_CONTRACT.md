# Contrato comum de coordenação

## Escopo e autoridade

- Cada tarefa deve declarar `objetivo`, `escopo`, `fora_do_escopo` e
  `critério_de_aceitação`.
- O agente só pode executar ações autorizadas pela tarefa. Diagnóstico é
  somente leitura por padrão.
- Nunca ler, copiar ou expor valores de secrets, tokens ou credenciais.
- Host, CT, container, checkout, imagem e serviço devem ser identificados
  antes de qualquer alteração.
- Antes de iniciar, ler `STATUS.md` e as notas pertinentes em `tasks/`
  (filtrando por `projeto:` no frontmatter) para o projeto/serviço da
  tarefa. `STATUS.md` e `tasks/` são a memória oficial e compartilhável do
  time — não um
  banco interno de memória de ferramenta (claude-mem ou equivalente), que é
  local a uma única superfície, pode ficar indisponível sem aviso e não é
  lido por Codex/Antigravity. Decisão relevante sem entrada correspondente
  em `TASK_REGISTER.md` não está registrada para efeito deste contrato.
- Resultados são evidências, não autorização para a próxima ação.
- Um relato de tarefa que afirme commit, push ou implantação não é prova por
  si só: confirmar no histórico local (`git log`/`rev-parse`) e no checkout
  correto antes de repassar isso como fato consumado.

## Delegação

- O coordenador divide o trabalho em tarefas pequenas, independentes e com
  dono único.
- Cada delegação deve conter: `id`, `objetivo`, `critério_de_aceitação`,
  `projeto`, `máquina`, `caminho`, `versão/estado`, `escopo_permitido`,
  `dependências`, `skills/referências` e `entrega_esperada`.
- A lista acima contém onze campos; `skills/referências` é um campo único.
- Não executar trabalho duplicado; registrar bloqueios e divergências.
- O coordenador registra o modo operacional escolhido e uma justificativa curta;
  pode ampliá-lo diante de risco concreto autorizado pela tarefa.
- Não permitir alterações concorrentes no mesmo checkout: o coordenador deve
  reservar o checkout por tarefa e liberar a reserva no retorno.
- Subagentes só devem ser usados quando a tarefa pedir delegação ou quando o
  coordenador registrar explicitamente a necessidade. Este registro é
  documental; não é um scheduler nem mecanismo automático de execução.

### Modo operacional comprovado no Codex

Na superfície Codex avaliada, o caminho comprovado é um subagente genérico com
papel e skills fornecidos explicitamente no pedido. A seleção nativa de um
perfil TOML por nome não foi comprovada, e o carregamento automático de
`SKILL.md` também não foi comprovado. Não trate a existência de
`.codex/agents/*.toml`, `skills.config`, `AGENTS.md` ou uma declaração do
subagente como evidência de carregamento.

Para uma delegação explícita, o agente principal deve:

1. identificar objetivo, escopo, versão e critérios de aceitação;
2. fornecer ao subagente os caminhos absolutos de
   `/root/agent-team/TEAM_CONTRACT.md`, da definição em
   `/root/agent-team/agents/<papel>.md` e da skill principal em
   `/root/agent-team/.codex/skills/<skill>/SKILL.md`;
3. solicitar a leitura desses arquivos antes de executar o trabalho;
4. disponibilizar somente as referências auxiliares pertinentes;
5. registrar o identificador da execução e evidências das leituras; e
6. consolidar o resultado no formato deste contrato.

Essa associação textual orienta o agente, mas não é um controle técnico.
Limites escritos em prompts ou skills não provam sandbox, isolamento,
permissões, modelo, aprovação ou carregamento de configuração. Só declare
esses controles quando houver evento/metadado ou outra evidência operacional
da ferramenta.

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

## Uso de skills

Antes de agir, cada agente verifica se alguma skill disponível se aplica —
tanto as próprias da equipe (`.codex/skills/team-*`) quanto, na superfície
Claude, as skills globais já instaladas (pacote `superpowers`, escopo
`user`, disponível a toda sessão Claude Code deste host, incluindo
subagentes `team-*`). Skill aplicável e não invocada é falha de processo,
não escolha de estilo — mesma exigência que `using-superpowers` descreve
para o Claude, estendida a qualquer superfície com skill equivalente.

Mapeamento por papel (ver também a linha `Auxiliares` de cada
`agents/<papel>.md`):

| Papel | Skill (superfície Claude) |
|---|---|
| Debug | `systematic-debugging` |
| Desenvolvedor | `test-driven-development` |
| Code Reviewer | `requesting-code-review` / `receiving-code-review` |
| Coordenador | `writing-plans`, `brainstorming` |
| QA / Tester | `verification-before-completion` |

`superpowers` é plugin do Claude Code e não tem equivalente instalável em
Codex CLI nem Antigravity/Gemini (runtimes sem sistema de plugin
compatível) — nessas superfícies a mentalidade acima vale igualmente, mas
só através das skills próprias da equipe (`.codex/skills/team-*`).

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

Antes de um rebuild ou recreate de container, verificar `git status` no
checkout que será usado na imagem e perguntar a qualquer outra sessão
conhecida que esteja editando o mesmo checkout se há trabalho não commitado
em progresso. Um rebuild leva junto todas as mudanças não commitadas da
árvore, terminadas ou não.

Decisões compartilháveis ficam em documentos próprios com origem, data e
escopo. Não ler bancos internos de memória das ferramentas para sincronizá-las.
Permissões descritas no prompt não substituem controles efetivamente aplicados
pela ferramenta.

### Checklist de deploy de container (obrigatório) — origem: TASK-20260920-001..004

Cinco erros reais e distintos aconteceram numa única sessão (20/09) por pular
estes passos. Cada item aqui corrigiu um incidente real, não é hipotético:

1. **Checkout host vs. container pode divergir mesmo parecendo igual.**
   `/root/jaaz` (e qualquer outro projeto montado em CT) pode existir como
   cópia solta no host E dentro do CT ao mesmo tempo, sem serem a mesma
   pasta. Antes de editar, confirmar com `md5sum` dos dois lados. Depois de
   editar e antes de buildar, `pct push` + `md5sum` dos dois lados de novo.
   Builds passaram com sucesso lendo a cópia errada e sem nenhum aviso.
2. **`docker network connect` sem `--alias` derruba nomes DNS customizados.**
   Reconectar uma rede manualmente registra só o nome do container — apelidos
   como `jaaz` (usado por outros serviços via hostname curto) somem
   silenciosamente. Sempre conferir `docker inspect --format
   '{{json .NetworkSettings.Networks}}'` do container ORIGINAL (todas as
   redes E aliases) antes de recriar, e usar `--alias` em cada
   `network connect`/`docker run --network-alias`.
3. **`docker rename` não libera a porta.** Pra trocar um container preservando
   rollback, sempre `docker stop` antes de `rename`/`run` do novo — nunca só
   `rename` com o antigo ainda rodando na mesma porta.
4. **Extração de env-vars por regex: testar contagem antes de usar.** Um
   regex de prefixo mal escrito (`^(INFISICAL_|X)=` em vez de
   `^INFISICAL_.*=|X=`) capturou 2 de 7 variáveis sem erro nenhum — o
   container subiu e crashou em loop. Sempre contar quantas variáveis foram
   extraídas e abortar se o número não bater com o esperado, antes de rodar
   `docker run`.
5. **Verificar o artefato final, não só que o build passou.** `docker build`
   sem erro não prova que a mudança está no bundle/imagem — cache de layer,
   arquivo errado sincronizado, ou minificação escondendo o símbolo esperado
   podem mascarar isso. Sempre extrair o arquivo de dentro da imagem
   construída (`docker create` + `docker cp`) e grep por uma string literal
   que só existe na mudança nova (não um nome de função/variável — minificação
   renomeia identificadores locais) antes de liberar o deploy.
6. **Tarefa de fundo assíncrona sem referência guardada pode nunca rodar.**
   `asyncio.create_task(coro())` sem guardar o retorno em algo com referência
   forte (ex.: um `set()` em nível de módulo) pode ser destruída pelo garbage
   collector silenciosamente, sem exceção nem log — o loop simplesmente não
   roda, às vezes por horas, sem nenhuma evidência em log. Sintoma: uma
   automação de fundo "funcionou ontem, não funciona hoje" sem nenhum erro
   visível. Sempre guardar a referência (`task = asyncio.create_task(...)`) e
   nunca deixar um `except Exception: pass` silencioso num loop de fundo —
   pelo menos logar a exceção.
7. **`@app.on_event("startup")` não dispara se o app já tem `lifespan`
   customizado.** Em várias versões de FastAPI/Starlette, `FastAPI(lifespan=X)`
   e `@app.on_event("startup")` no mesmo app são incompatíveis — o segundo
   simplesmente não roda, sem erro nenhum. Se o app já usa `lifespan=`,
   colocar toda inicialização de tarefa de fundo dentro dele, nunca num
   `on_event` separado.
8. **Nome de container de backup precisa ser único por execução, não fixo
   por data.** Um script de redeploy que roda mais de uma vez no mesmo dia
   (comum ao iterar um fix) e usa `docker rename antigo backup-AAAAMMDD`
   colide na segunda execução — e o `stop` já rodou antes do `rename` falhar,
   deixando o site fora do ar até correção manual. Usar um sufixo com
   timestamp completo (`date +%Y%m%d%H%M%S`) ou um `docker rm` do nome de
   backup antes de reusá-lo.

## Loop de trabalho e auditoria de agentes

- Ao iniciar uma tarefa de código ou infraestrutura com mais de um passo, usar
  `dev-task-loop` durante todo o trabalho: classificar o pedido, definir o
  critério de pronto, coletar evidências primárias, agir no menor escopo e
  verificar o resultado por observação.
- Depois que qualquer agente declarar uma tarefa concluída, usar
  `agent-work-auditor` antes de aceitar o trabalho como pronto, especialmente
  antes de merge, deploy ou encerramento. O auditor deve repetir as
  verificações relevantes, confirmar identidade de versão e fazer busca de
  recorrência do mesmo defeito em telas, módulos ou fluxos relacionados.
- Ao receber log bruto de CI/CD, scanner de segurança/infraestrutura ou
  transcrição de agente sem alegação de conclusão, usar `dev-output-triage`
  para separar achados críticos de ruído e recalcular a severidade pelo
  contexto real.
- As três skills obedecem a este contrato: usam o formato obrigatório de
  entrega, os estados `concluída` / `parcial` / `bloqueada` e o vocabulário de
  validação `passou` / `falhou` / `indisponível` / `não executada`.
- Nenhuma dessas skills autoriza merge, deploy, recreate, alteração de
  produção ou próxima ação operacional. Resultado é evidência; autorização
  continua pertencendo ao responsável pelo processo.
- Nunca ler, copiar ou expor valores de secrets, tokens ou credenciais. Em
  relatórios e scans, registrar apenas local, nome e linha, nunca o conteúdo.
- Se as skills não estiverem instaladas ou disponíveis, aplicar estas regras
  manualmente e declarar essa limitação na validação.

## Ciclo de melhoria de agentes

O time usa um ciclo curto e auditável para transformar execuções reais em
melhorias verificáveis do harness dos agentes. O material operacional fica em
`improvement-loop/`.

**Obrigatório, não opcional:** toda tarefa que fechar como `bloqueada`, ou
cuja causa confirmada já apareça em outra entrada de `tasks/`
(erro recorrente), só pode ser dada por encerrada depois de virar uma
entrada permanente — checklist do domínio correspondente (seguindo o
modelo do "Checklist de deploy de container" acima) quando o domínio já
tiver um, ou um registro em `improvement-loop/` (`eval-case`/`feedback`)
quando não tiver. Registrar a causa em `TASK_REGISTER.md` sem convertê-la
em checagem reutilizável não conta como ciclo concluído — é assim que o
mesmo erro se repete em sessões futuras sem que ninguém perceba o padrão.

1. Definir o resultado esperado e as afirmações que precisam ser provadas.
2. Registrar a execução, sua identidade de versão e os artefatos produzidos,
   sem incluir secrets, tokens ou credenciais.
3. Coletar feedback humano ou automatizado, distinguindo fato observado de
   hipótese e verificando recorrência em fluxos/telas/módulos semelhantes.
4. Converter falhas ou padrões recorrentes em um caso de avaliação com
   assertions, checks, limiar e referência à execução original.
5. Propor uma alteração pequena no harness (instruções, roteamento, ferramentas
   ou requisitos de saída), executá-la e repetir a avaliação.
6. Entregar o resultado no formato deste contrato, incluindo antes/depois,
   limitações e próximo passo autorizável.

O ciclo não cria autorização para merge, deploy, alteração de produção ou
coleta automática de dados. A referência conceitual adotada é o exemplo oficial
do OpenAI Cookbook sobre Agent Improvement Loop; a implementação local é
intencionalmente sem serviço remoto, banco ou upload automático.
