# Acessos e permissões: o que passa, o que é bloqueado e o caminho certo

**Leitura obrigatória** para qualquer agente (Claude, Codex, Antigravity) antes de planejar ações em
infraestrutura, containers, segredos ou serviços do host `srv` (Proxmox 7.4).

Regra de manutenção: quando uma ação for bloqueada pela primeira vez, ou passar pela primeira vez, **atualize este arquivo na mesma sessão**, com data e evidência.

Mapa levantado em 2026-10-08 (sessão Flow Studio, Claude Opus 5.5).

## Como a permissão funciona no Claude Code deste host

1. **Regras allow:** ficam em `/root/.claude/settings.local.json`. O que casa com uma delas roda sem pergunta. O que não casa vai para o **classificador do modo automático**, que pode negar.
2. **A regra só casa com comando simples.** Uma linha com `&&`, `;`, `|`, `cd …`, `sh -c '…'` ou várias linhas **não** casa com `Bash(pct exec *)`, mesmo começando com `pct exec`, e cai no classificador.
   → Para usar uma regra existente, rode o comando **sozinho, numa chamada só**.
3. **Uma negação vale para o resultado, não só para o comando.** Não tente o mesmo objetivo por outra ferramenta, outra sintaxe ou outro agente.
4. **O `!` do usuário não passa pelo classificador.** O que o usuário roda com `! comando` executa direto.
5. **O classificador é instável às vezes.** Já negou leitura simples (ver tabela) e já respondeu "no verdict". Uma negação estranha não autoriza contornar: registre aqui e use o caminho do usuário.

Regras allow existentes (08/10): `Read(//etc/**)`, `Read(//proc/**)`, `pveversion`, `lscpu`, `ip -br addr`, `qm list *`, `qm status *`, `pct list *`, `pct exec *`, `pct push *`, `pct pull *`, `pct resize *`, `systemctl is-active *`, `dmesg`, `who`, `shutdown *`, `rtk grep *` e dois `curl` para 192.168.0.200.

## Mapa verificado

### Passou

| Ação | Exemplo | Data |
|---|---|---|
| Ler arquivos de projeto em `/root` (repos, relatórios, sessões do Codex em `~/.codex/sessions`) | `Read`, `grep` | 08/10 |
| Criar, editar e fazer commit **local** em repos próprios (sem push) | `/root/flow-studio-api`, `/root/agent-team` | 08/10 |
| Criar venv do projeto com uv e instalar pacotes nele | `uv venv --python 3.12 .venv` | 08/10 |
| Rodar servidor de teste em 127.0.0.1 numa porta livre | `uvicorn … --port 8791` | 08/10 |
| Delegar revisão ao Codex somente leitura, em segundo plano | `codex exec -s read-only -C <dir> -o <arq>` | 08/10 |
| Consultar o Proxmox (leitura) | `pct list`, `pct config 102`, `pvesm status`, `pveversion`, `ping` | 08/10 |
| Ler o estado de containers do CT100 sem valores secretos | `pct exec 100 -- docker ps`, `docker inspect … --format '{{label}}'`, ler README/compose com valores mascarados | 08/10 |
| Ler o banco do Postiz (só `select`) | `pct exec 100 -- docker exec postiz-postgres psql -U postiz-user -d postiz-db-local -c "select …"` | 09/10 |
| Alterar produção **com OK explícito do usuário**, backup antes e comando simples | `update "Post" set "deletedAt"…` por IDs; `POST /api/video/autonomy/config` via `docker exec opensuite-jaaz python3 -c …` | 09/10 |
| Ler arquivo de config (sem segredos) dentro do container de produção | `docker exec opensuite-jaaz python3 -c "json.load(open('…/autonomy_state.json'))"` | 09/10 |
| Rodar a suíte do Jaaz em container descartável no host | `docker run --rm -v <worktree>:/src:ro python:3.12-slim …` | 09/10 |
| Buscar documentação externa | `curl https://ai.google.dev/…md.txt`, Firecrawl | 08/10 |

### Bloqueado, e o caminho certo

| Ação | Motivo dado | Caminho certo |
|---|---|---|
| Ler variáveis de ambiente de container de produção (até só os nomes), ex.: `docker exec opensuite-jaaz … /proc/*/environ`. Em 19/10 também bloqueou carregar o ambiente do app num teste do N1 | Production Reads / Credential Exploration | Pedir ao usuário só o **nome** da variável ou da pasta do Infisical. Nunca o valor. |
| Procurar tokens e chaves em arquivos, logs ou configs (`grep CLOUDFLARE_API_TOKEN …`, config do Codex) | Credential Exploration | O segredo é usado via `infisical run --env=… --path=… -- <script>`, executado pelo usuário com `!`. O agente nunca vê o valor. |
| Criar container (`pct create`) | Modify Shared Resources | Script versionado em `deploy/`, testado com `bash -n`, entregue como **um** comando `!` completo. |
| Reiniciar serviço de produção (OmniRoute CT102, set/2026) | bloqueado no auto mode | Script no scratchpad e o usuário roda com `!` |
| Usar o token de uma integração da Postiz (tabela `Integration`) na Graph API da Meta | Não bloqueia, mas **vazou** em 19/10: a mensagem de erro da Meta ("Malformed access token …") repete o token. | O token é composto `user___page`: usar a parte certa. Nunca imprimir o JSON de erro cru; passar sempre por `re.sub(r'EAA\w+','[token]', …)`. Se vazar, pedir ao usuário para reconectar a conta na Postiz. |
| Mover arquivo de segredo e reiniciar serviço no CT103 numa linha só (`pct exec 103 -- sh -c 'mv … && systemctl restart flow-studio-api'`) | Remote Shell Writes (13/10) | Script no scratchpad e o usuário roda com `!`. Validar a chave antes, só com chamadas que não custam (listar modelos). |
| Ler `package.json`, `git diff` e `src/platform.ts` em `/root/flow-mcp-source` (pasta onde o Codex está trabalhando) | Modify Shared Resources (falso positivo) | Não insistir. Escrever código que não dependa desse detalhe, ou pedir ao usuário. |

## Pegadinhas do ambiente (não são permissão, mas causam erro)

| Situação | O que acontece | Faça assim |
|---|---|---|
| Porta **8787** | É do gateway Caveman. O flow-mcp usa 8787 por padrão e não sobe a API dele. | `FLOW_MCP_PORT=8792`. Antes de escolher porta, `ss -ltn \| grep :PORTA`. |
| `curl` local | Passa por um proxy do ambiente e devolve `cave_route_not_found`. | `curl --noproxy '*' …` |
| Python do host | 3.9, sem `venv`/`ensurepip`. | `uv venv --python 3.12` (não instalar `python3-venv` no host). |
| `ffprobe` | Não instalado. | `ffmpeg -hide_banner -i arquivo` e ler `Duration:`/`Audio:` no stderr. |
| Template de CT | O PVE 7.4 recusa `debian-12-standard_12.12` ("unsupported debian version"). | Usar `debian-11-standard_11.7-1`. |
| Debian 11 em CT novo | O bullseye saiu dos espelhos normais, então o primeiro `apt-get update` falha e o provisionamento com `set -e` para logo no início (CT 103, 08/10). | Repositórios em `archive.debian.org` (`debian`, `debian-security`). Conferir com `pct exec <id> -- timeout 60 apt-get update` antes de provisionar. |
| `pct exec <id> -- <comando>` sozinho | Passa pela regra `Bash(pct exec *)` (verificado em 08/10 no CT 103: `systemctl is-active`, `dpkg -s`, `apt-get update`, rodar o script de provisionamento). | Um comando por chamada, sem `&&`, `\|` ou `sh -c`. |
| Tela | O host não tem `DISPLAY`: nada que precise de navegador com tela (login Google, Flow) roda nele. | CT 103 com Xvfb e noVNC (`/root/flow-studio-api/deploy/`). |
| pytest do Jaaz | Um módulo do app fecha o `stdout` durante a importação: o pytest perde a saída ("I/O operation on closed file") e alguns módulos exigem `POSTIZ_API_KEY`/`POSTGRES_PASSWORD` só para importar. | `POSTIZ_API_KEY=test-only POSTGRES_PASSWORD=test-only pytest -s --continue-on-collection-errors --junitxml=…` e ler o XML. |
| YouTube | `yt-dlp` é bloqueado ("Sign in to confirm you're not a bot"). | Firecrawl para descrição e capítulos, ou legenda já baixada (`/tmp/flow-video/`). |
| Infisical CLI no host | Não está logado. O servidor é self-hosted em `192.168.0.200:8620` com certificado autoassinado. | O usuário roda `! infisical login` e informa projeto e pasta. |

## Regras de conduta

1. **Consultar este mapa antes** de planejar qualquer ação em infra, container, rede, segredo ou serviço.
2. **Ação bloqueada:**
   - não tentar outro caminho para o mesmo resultado;
   - preparar um script versionado e já testado (`bash -n`, modo simulação);
   - entregar **um único comando `!` completo**.
3. **Nunca entregar comando com marcador** (`<pasta>`, `<id>`). No bash, `<` vira redirecionamento e o comando quebra (aconteceu em 08/10). Se falta um valor, **perguntar antes** e só depois entregar o comando final.
4. **Ordem das etapas:** dizer explicitamente o que precisa rodar antes ("primeiro crie o CT, depois o túnel") e conferir o estado (`pct status 103`) antes de pedir o próximo passo.
5. **Liberar permanentemente** algo recorrente:
   - propor uma regra allow **específica** (ex.: `Bash(bash /root/flow-studio-api/deploy/create_ct103.sh)`), nunca genérica;
   - aplicar só com OK explícito do usuário;
   - registrar a regra aqui.
6. **Segredo nunca passa pelo agente**, nem com permissão: só `infisical run` ou injeção no serviço.
