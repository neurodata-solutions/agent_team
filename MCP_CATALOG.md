# Catálogo inicial de MCPs

Data da verificação: 2026-09-17  
Projeto: `/root/agent-team`  
Modo da tarefa: **Padrão** — levantamento delimitado com conferência técnica
independente.

Este catálogo é documental. Não habilita servidores, concede acesso, inicia
processos, conecta clientes ou altera configurações.

## Estados e evidência

- **Configurado**: há uma declaração na configuração do cliente.
- **Execução anteriormente comprovada**: existe evidência histórica de uma
  chamada ou execução, sem afirmar funcionamento atual.
- **Funcionamento não verificado**: não houve handshake, chamada ou teste nesta
  tarefa.

Versões ausentes permanecem `não disponíveis`; nomes de servidores não são
usados para inferir ferramentas.

## Catálogo

| Identificador | Finalidade e origem | Configuração, execução e transporte | Classe | Ferramentas clientes configuradas | Projeto/dados e efeitos conhecidos | Autenticação | Estado, evidência e responsável |
|---|---|---|---|---|---|---|---|
| `codex.code-review-graph` | Grafo local de análise de código; origem `/root/.local/bin/code-review-graph`; versão não declarada | `/root/.codex/config.toml:29-37`; comando local `serve --repo /root/jaaz`, `cwd=/root/jaaz`; transporte não declarado explicitamente (processo local, stdio apenas inferido) | interno | `semantic_search_nodes_tool`, `query_graph_tool`, `list_repos_tool`, `get_architecture_overview_tool`, `get_minimal_context_tool`, `get_review_context_tool` (`config.toml:39-55`) | Projeto `/root/jaaz`; consultas de nós, arquitetura, contexto e impacto conforme nomes configurados; nenhuma ferramenta de escrita declarada | `CRG_SERIAL_PARSE=1`; mecanismo de autenticação não declarado; nenhum segredo lido | **Configurado** e **execução anteriormente comprovada** por chamadas registradas de `get_review_context` no `TASK_REGISTER.md`; funcionamento atual não verificado; responsável não identificado |
| `codex.postman` | MCP remoto Postman; origem `https://mcp.postman.com/mcp`; versão não declarada | `/root/.codex/config.toml:22-27`; HTTPS remoto; transporte remoto HTTPS | externo | Somente `createCollectionRequest` aparece configurado, com aprovação `approve` | Coleções/requisições Postman; a operação configurada pode criar uma requisição, mas não foi executada | Bearer via variável `POSTMAN_API_KEY`; valor não lido | **Configurado**; nenhuma execução comprovada; funcionamento não verificado; responsável não identificado |
| `claude.code-review-graph` | Mesma origem local do grafo; versão não declarada | `/root/.mcp.json:2-15`, habilitado em `/root/.claude/settings.local.json:29-31`; comando local com `type=stdio`, `cwd=/root/jaaz` | interno | Não enumeradas na configuração Claude; não inferir o conjunto do Codex | Projeto `/root/jaaz`; capacidades não confirmadas para este cliente | `CRG_SERIAL_PARSE=1`; autenticação não declarada | **Configurado**; há registro histórico de `get_review_context`, mas o cliente não é distinguido; funcionamento atual não verificado; responsável não identificado |
| `claude.caveman` | MCP Caveman executado localmente; origem `/root/.caveman/bin/caveman-mcp`; versão/propriedade não declaradas | `/root/.claude.json:1297-1303`; comando local stdio, `args=[]` | externo (classificação provisória; origem/propriedade externa não comprovada) | Nenhuma ferramenta listada; não inferir capacidades | Projeto/dados não declarados; efeitos não verificáveis | Ambiente declarado vazio; autenticação não declarada | **Configurado**; sem execução comprovada; funcionamento não verificado; responsável não identificado |
| `gemini.code-review-graph` | Grafo local de análise de código; origem `/root/.local/bin/code-review-graph`; versão não declarada | `/root/.gemini/antigravity/mcp_config.json:2-14` e `/root/.gemini/settings.json:2-14`; comando local, `cwd=/root/jaaz`; transporte não rotulado explicitamente nesses JSONs | interno | Não enumeradas; não inferir ferramentas do nome | Projeto `/root/jaaz`; capacidades não confirmadas para Gemini/Antigravity | `CRG_SERIAL_PARSE=1`; autenticação não declarada | **Configurado**; nenhuma execução específica comprovada; funcionamento não verificado; responsável não identificado |

`/root/.gemini/config/mcp_config.json` foi encontrado vazio/inválido como JSON,
sem servidores catalogáveis. Ele é uma lacuna de origem de configuração, não um
MCP ativo.

## Matriz de acesso proposta

As operações abaixo são propostas documentais. Não representam permissões,
configuração efetiva ou controle técnico aplicado.

| Papel | MCP | Projeto/ambiente | Operações propostas | Limites | Controle necessário |
|---|---|---|---|---|---|
| `gestor-mcp` | `code-review-graph` por cliente | `/root/jaaz`, clientes locais | Ler catálogo, origem, estado e evidência; consultar contexto somente se a ferramenta estiver disponível e isso for autorizado | Sem iniciar servidor, alterar configuração ou conceder acesso | Autorização explícita da tarefa e registro de cliente/revisão |
| `gestor-mcp` | `codex.postman` | Postman remoto | Somente catalogar configuração e operação declarada | Não criar coleções/requisições nem testar conexão | Aprovação específica, credencial já autorizada e confirmação do owner |
| `engenheiro-mcp` | `code-review-graph` | `/root/jaaz` | Consultas de arquitetura, dependências e contexto somente se essas ferramentas forem expostas ao cliente e o diagnóstico for autorizado | Sem escrita no grafo, atualização ou mudança de processo | Escopo de repositório/versão identificado; ferramenta de consulta disponível |
| `code-reviewer` | `code-review-graph` | Projeto/revisão identificados | Consultar impacto e contexto, confirmando na fonte | Somente leitura e sem extrapolar a referência | Commit/diff explícito e evidência de cliente ativo |
| `coordenador` | Qualquer MCP | Projeto da tarefa | Nenhuma operação automática; delegar somente conforme modo e risco | Não habilitar servidores nem inferir capacidades | Contrato, autorização e registro de execução |

## Lacunas

- Não há prova de handshake ou funcionamento atual para nenhum servidor nesta
  tarefa.
- O cliente que produziu o registro histórico de `get_review_context` não foi
  identificado de forma independente.
- O cache `/root/.claude/mcp-needs-auth-cache.json` não forneceu estado de
  autenticação utilizável para o catálogo.
- Versões dos servidores locais e do MCP Postman não estão declaradas.
- Claude e Gemini/Antigravity não enumeram ferramentas nos arquivos examinados.
- Não há MCP configurado para pesquisa web nesta equipe; o Postman atende
  coleções/requisições, não pesquisa geral.
- Não há consulta autorizada a serviços internos nesta etapa.
- Responsáveis formais não foram identificados nas configurações.
- Nenhum MCP configurado foi classificado como `administrativo`; a linha de
  governança do coordenador na matriz não é uma classificação de servidor.

## Duplicação observável

`code-review-graph` aparece configurado para Codex, Claude e Gemini/Antigravity
com a mesma origem `/root/.local/bin/code-review-graph` e o mesmo projeto
`/root/jaaz`. Isso pode gerar divergência de versão, ambiente ou ferramentas
expostas entre clientes; nenhuma sincronização ou equivalência foi presumida.

## Fontes examinadas

- `/root/.codex/config.toml`
- `/root/.mcp.json`
- `/root/.claude/settings.local.json`, `/root/.claude/settings.json`,
  `/root/.claude/mcp-needs-auth-cache.json` e
  `/root/.claude.json` (somente estruturas MCP pertinentes)
- `/root/.gemini/antigravity/mcp_config.json`
- `/root/.gemini/settings.json`
- `/root/.gemini/config/mcp_config.json`
- `TEAM_CONTRACT.md`, `agents/gestor-mcp.md`,
  `.codex/skills/team-gerenciar-mcp/SKILL.md` e referências históricas em
  `TASK_REGISTER.md`

Nenhum valor de credencial foi lido ou incluído. Nenhum comando de inicialização
foi executado.
