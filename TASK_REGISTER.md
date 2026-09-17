# Registro documental de tarefas

Modelo de coordenação e histórico manual. Não executa, agenda, bloqueia ou
sincroniza agentes automaticamente.

## Entrada

```yaml
id: TASK-YYYYMMDD-###
objetivo: ""
responsavel: ""
projeto: ""
maquina: ""
caminho: ""
versao_estado: ""
escopo_permitido: ""
dependencias: []
skills_referencias: []
criterios_aceitacao: []
entrega_esperada: ""
checkout_reservado: ""
estado: planejada
```

## Retorno

```yaml
estado: concluida # ou parcial, bloqueada
resultado: ""
evidencias: []
arquivos_alterados: []
verificacoes: []
limitacoes: []
proximo_passo: ""
integrador: "coordenador"
```

---

## Integração dos adaptadores nativos Codex (2026-09-17)

```yaml
id: TASK-20260917-CODEX-001
objetivo: "Adaptar os nove papéis compartilhados ao formato de agentes personalizados do Codex e validar delegação real de Reviewer e Tester"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "codex-cli 0.154.0; branch master; commit-base f114d48357f7316ce2b234568b658b6f1057a026"
escopo_permitido: "somente .codex/agents/*.toml e este registro; sem alterações globais, Claude, Antigravity, piloto, serviços ou permissões"
dependencias: ["TASK-20260916-001", "TASK-20260916-002"]
skills_referencias: ["OpenAI Docs: Codex Subagents", "agents/*.md", "TEAM_CONTRACT.md", "investigate-first", "surgical-patch", "safe-refactor", "lean-build"]
criterios_aceitacao:
  - "nove adaptadores TOML com name, description e developer_instructions"
  - "referências compartilhadas e skills pertinentes resolvem"
  - "delegação nativa real de code-reviewer e tester, somente leitura"
  - "30 testes existentes executados sem instalação e sem repetir avaliação de 200 mil amostras"
entrega_esperada: "adaptadores, prova de reconhecimento/delegação, resultados e limitações"
checkout_reservado: "liberado após commit local"
estado: concluida
resultado: "Criados nove adaptadores em .codex/agents/. A sessão nova 01a0ae92-c2be-7760-a438-961e206a418b carregou o projeto sem erro; a CLI não oferece listagem de definições. Reconhecimento nativo comprovado por delegação real para code-reviewer e tester nesta sessão: /root/code_reviewer_codex e /root/tester_codex. Os outros sete arquivos estão válidos e referenciados, mas não foram declarados reconhecidos sem uma execução nativa correspondente."
evidencias:
  - "documentação oficial: https://developers.openai.com/codex/subagents (TOML em .codex/agents; campos obrigatórios; resolução por name)"
  - "codex --version -> codex-cli 0.154.0"
  - "tomli validou os nove TOMLs; TEAM_CONTRACT.md, nove agents/*.md e skills pertinentes existem"
  - "execução nativa code-reviewer: /root/code_reviewer_codex; revisão estática sem alterações, zero defeitos"
  - "execução nativa tester: /root/tester_codex; python3 -m unittest test_hhmmss.py -v -> 30/30 OK, exit 0"
arquivos_alterados:
  - ".codex/agents/ambiente-linux-devops.toml"
  - ".codex/agents/code-reviewer.toml"
  - ".codex/agents/coordenador.toml"
  - ".codex/agents/debug.toml"
  - ".codex/agents/desenvolvedor.toml"
  - ".codex/agents/engenheiro-mcp.toml"
  - ".codex/agents/gestor-mcp.toml"
  - ".codex/agents/qa.toml"
  - ".codex/agents/tester.toml"
  - "TASK_REGISTER.md"
verificacoes:
  - "piloto permaneceu sem alterações"
  - "não houve instalação, execução da avaliação de 200 mil amostras, push, deploy ou mudança global"
limitacoes:
  - "Codex CLI 0.154.0 não expõe comando de listagem de agentes personalizados; reconhecimento dos sete papéis não foi inferido de AGENTS.md nem declarado antecipadamente"
  - "revisão não executou testes por escopo; resultado histórico 30/30 foi confirmado separadamente pelo Tester"
proximo_passo: "abrir uma nova sessão em /root/agent-team e pedir explicitamente Spawn coordenador para uma tarefa; a sessão deve carregar .codex/agents/ antes de qualquer reconhecimento"
integrador: "coordenador"
```

Uma reserva de checkout é convenção documental para evitar concorrência; não é
um lock automático.

---

## Piloto HH:MM:SS (2026-09-15) — coordenação

Contexto comum a TASK-20260915-001..004:
projeto: pilot-hhmmss (temporário, isolado, sem dependências externas)
maquina: host srv (Debian, Python 3.9.2, pytest 8.4.2)
caminho: /tmp/claude-0/-root/7027eeff-bb9d-4bd5-b80b-055587a6d248/scratchpad/pilot-hhmmss/
contrato_interface: arquivo `hhmmss.py` na raiz; `def seconds_to_hhmmss(seconds) -> str`
fora_do_escopo: qualquer path fora do diretório do piloto; aplicações, containers,
  infraestrutura, segredos, rede, serviços; instalar pacotes; git commit/push.
criterios_aceitacao_confirmados (2026-09-16, retomada da execução):
  - "Entrada: inteiro não negativo de segundos."
  - "0 -> \"00:00:00\""
  - "61 -> \"00:01:01\""
  - "3661 -> \"01:01:01\""
  - "86400 -> \"24:00:00\""
  - "Horas podem ultrapassar 23 e ultrapassar dois dígitos (sem módulo 24)."
  - "Valores negativos (int) geram ValueError."
  - "str, float, bool e None geram TypeError (bool é subclasse de int em Python — checagem explícita)."

```yaml
id: TASK-20260915-001
objetivo: "Implementar seconds_to_hhmmss em hhmmss.py"
responsavel: "desenvolvedor"
checkout_reservado: "liberado (hhmmss.py entregue)"
dependencias: []
estado: concluida
resultado: "hhmmss.py criado com checagem explícita de bool antes de int, tipo antes de valor, sem módulo 24 nas horas"
evidencias: ["ls -la pilot-hhmmss/", "cat hhmmss.py (verificado pelo coordenador)"]
arquivos_alterados: ["pilot-hhmmss/hhmmss.py"]
verificacoes: ["smoke check do próprio desenvolvedor: passou (informativo, não formal)"]
limitacoes: []
proximo_passo: "revisão (TASK-003) e QA (TASK-004)"
integrador: "coordenador"
```

```yaml
id: TASK-20260915-002
objetivo: "Escrever test_hhmmss.py a partir apenas dos critérios de aceitação (unittest, stdlib)"
responsavel: "tester"
checkout_reservado: "liberado (test_hhmmss.py entregue)"
dependencias: []
estado: concluida
resultado: "29 testes unittest cobrindo aceitação, limites de hora sem módulo 24, negativos->ValueError, tipos inválidos (str/float/bool/None)->TypeError"
evidencias: ["comando: python3 -m unittest test_hhmmss.py -v (cwd=pilot-hhmmss/)", "saída: Ran 29 tests in 0.001s / OK", "exit code: 0", "reexecutado de forma independente pelo coordenador: mesmo resultado (29/29, exit 0)"]
arquivos_alterados: ["pilot-hhmmss/test_hhmmss.py"]
verificacoes: ["passou"]
limitacoes: ["não cobre Decimal/Fraction/complex/numpy.int64", "não cobre subclasses de int além de bool", "maior valor exercitado: 3.600.000s (1000h)", "mensagens de exceção não são asseridas, só o tipo"]
proximo_passo: "revisão (TASK-003) e QA (TASK-004)"
integrador: "coordenador"
```

```yaml
id: TASK-20260915-003
objetivo: "Revisar implementação e testes (somente leitura)"
responsavel: "code-reviewer"
checkout_reservado: "nenhum (leitura)"
dependencias: [TASK-20260915-001, TASK-20260915-002]
estado: concluida
resultado: "Nenhum defeito de correção. hhmmss.py sha256 357b12f5... test_hhmmss.py sha256 b8972e99... Cobertura de linha/ramo 100% por inspeção (não medida com coverage.py)."
evidencias: ["leitura integral hhmmss.py:1-37 e test_hhmmss.py:1-148", "code-review-graph indisponível para diretório fora de repositório (erro esperado, registrado)"]
arquivos_alterados: []
verificacoes: ["não executada (fora de escopo do revisor)"]
limitacoes: ["achado #1 (baixa severidade, opcional): suíte não testa precedência TypeError-antes-de-ValueError para não-int negativos (ex.: -1.0); implementação já está correta (verificado por inspeção), é lacuna de cobertura, não defeito", "achados #2-#5: informativos, sem ação recomendada"]
proximo_passo: "QA (TASK-004); achado #1 fica registrado como melhoria opcional, não bloqueante"
integrador: "coordenador"
```

```yaml
id: TASK-20260915-004
objetivo: "Executar testes e validar critério de aceitação"
responsavel: "qa"
checkout_reservado: "nenhum (execução read-only sobre os arquivos)"
dependencias: [TASK-20260915-001, TASK-20260915-002]
estado: concluida
resultado: "Parecer QA: passou. 8/8 critérios de aceitação verificados com evidência própria (reexecução da suíte + checagens manuais pontuais + oráculo diferencial em 200.009 amostras, 0 divergências)."
evidencias: ["python3 -m unittest test_hhmmss.py -v -> 29/29 OK, exit 0 (reexecutado 2x)", "checagens manuais: 0,61,3661,86400,86399,90000,359999,360000,360123,3600000,10**18", "oráculo diferencial (script próprio fora do piloto): 200009 amostras, 0 divergências", "hashes sha256 de hhmmss.py e test_hhmmss.py inalterados antes/depois"]
arquivos_alterados: []
verificacoes: ["passou"]
limitacoes: ["suíte não trava precedência tipo-antes-de-valor para não-int negativos (ex.: -1.0); comportamento hoje correto (verificado manualmente), lacuna é só de cobertura", "subclasses de int não-bool (IntEnum etc.) são aceitas silenciosamente, sem teste; não viola nenhum critério declarado", "sem prova por VCS de que nada fora do piloto mudou (/root não é repo git nesta sandbox); apoio em hashes/mtimes e no escopo somente-leitura das ações"]
proximo_passo: "encerrar piloto como bem-sucedido; follow-up opcional não bloqueante: 2-3 testes extras de precedência de exceção e subclasses de int"
integrador: "coordenador"
```

## Encerramento do piloto original (2026-09-16)

Critério de encerramento atingido: TASK-001..004 concluídas, 8/8 critérios de
aceitação verificados por dois métodos independentes (suíte do Tester +
reexecução/oráculo do QA), 0 defeitos de produto, 1 lacuna de cobertura de
baixa severidade registrada como não bloqueante (achado #1 do reviewer).
Diretório do piloto permanece intocado fora dos dois arquivos entregues.
Nenhuma alteração em aplicações, containers, infraestrutura, segredos,
permissões ou configurações de auto-mode. Nenhum deploy, push ou instalação.

---

## Preservação e Adaptação Gemini/Antigravity (2026-09-16)

```yaml
id: TASK-20260916-001
objetivo: "Preservar piloto em /root/agent-team/pilots/hhmmss, adicionar teste de -1.0 e adaptar equipe para Gemini/Antigravity"
responsavel: "coordenador"
checkout_reservado: "liberado (/root/agent-team/)"
dependencias: [TASK-20260915-001, TASK-20260915-002, TASK-20260915-003, TASK-20260915-004]
estado: concluida
resultado: "Piloto copiado de /tmp/claude-0/... para /root/agent-team/pilots/hhmmss/. Adicionado teste test_float_negativo em test_hhmmss.py. Executada suíte completa (30/30 testes OK). Criado resumo EVIDENCIAS.md. Adaptador Antigravity estruturado em /root/agent-team/adapters/antigravity/ com 9 subagentes definidos nativamente via define_subagent."
evidencias: ["python3 -m unittest test_hhmmss.py -v -> 30/30 OK em 0.003s", "arquivos em /root/agent-team/pilots/hhmmss/ verificados", "adaptador criado em /root/agent-team/adapters/antigravity/"]
arquivos_alterados: ["pilots/hhmmss/hhmmss.py", "pilots/hhmmss/test_hhmmss.py", "pilots/hhmmss/EVIDENCIAS.md", "adapters/antigravity/subagents.json", "adapters/antigravity/README.md"]
verificacoes: ["passou"]
limitacoes: ["registro dinâmico de subagentes no Antigravity depende de chamada define_subagent por sessão"]
proximo_passo: "acionar subagente team-code-reviewer para validação independente (TASK-20260916-002)"
integrador: "coordenador"
```

```yaml
id: TASK-20260916-002
objetivo: "Revisar piloto persistido através de subagente independente no Antigravity"
responsavel: "code-reviewer (subagente team-code-reviewer)"
checkout_reservado: "nenhum (leitura)"
dependencias: [TASK-20260916-001]
estado: concluida
resultado: "Subagente nativo team-code-reviewer (id 976b22a8-1802-4de1-bebe-bf06a6507d4e) executou a revisão de /root/agent-team/pilots/hhmmss/. Confirmou 0 defeitos, conformidade total com os 8 critérios e validação da resolução do teste -1.0."
evidencias: ["transcript: file:///root/.gemini/antigravity-cli/brain/976b22a8-1802-4de1-bebe-bf06a6507d4e/.system_generated/logs/transcript.jsonl", "relatório entregue via mensagem inter-agente de alta prioridade"]
arquivos_alterados: []
verificacoes: ["passou"]
limitacoes: ["somente leitura estática, sem execução dinâmica de comandos pelo subagente de revisão (conforme restrição de papéis)"]
proximo_passo: "versionar artefatos no repositório dedicado /root/agent-team"
integrador: "coordenador"
```
