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

## Verificação de pesquisa web na sessão Codex (2026-09-17)

```yaml
id: TASK-20260917-WEB-CAPABILITY-001
objetivo: "Comprovar pesquisa e leitura de documentação oficial Python sem instalar componentes"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "branch master; base 6a3643d; sessão Codex atual"
escopo_permitido: "MCP_CATALOG.md, TASK_REGISTER.md e uso da ferramenta web nativa desta sessão"
fora_do_escopo: "instalação de MCP, teste de outros clientes, envio de arquivos/segredos, execução de código remoto e inventário geral"
dependencias: ["MCP_CATALOG.md", "web__run"]
skills_referencias: ["verify-and-stop"]
criterios_aceitacao:
  - "pesquisa web oficial executada"
  - "página pública efetivamente aberta"
  - "resposta curta com explicação e link direto"
  - "recurso nativo diferenciado de MCP e shell HTTP"
entrega_esperada: "registro de capacidade, evidência da consulta, resposta fundamentada e commit local"
checkout_reservado: "liberado após commit"
modo_escolhido: "econômico"
justificativa_modo: "Uma ferramenta nativa, uma busca e uma abertura de página; sem delegação ou inventário adicional."
estado: concluida
resultado: "web__run pesquisou e abriu com sucesso a documentação oficial Python sobre bool/int."
evidencias:
  - "Ferramenta: web__run; versão, modelo, provedor e consumo não disponíveis."
  - "Mecanismo: search_query -> resultado oficial docs.python.org -> open da página."
  - "Consulta: site:docs.python.org bool subclass of int validation arguments."
  - "Página aberta: https://docs.python.org/3/library/stdtypes.html#boolean-type-bool"
  - "Nenhum MCP web foi identificado; exec_command não foi usado para HTTP."
  - "Nenhum código remoto foi executado e nenhum segredo foi enviado."
ferramenta: "web__run"
modelo: "não disponível"
provedor: "não disponível"
agentes: 0
tentativas: 1
tokens_entrada: "não disponíveis"
tokens_saida: "não disponíveis"
tokens_cache: "não disponíveis"
custo: "não disponível; nenhum preço consultado"
resultado_retrabalho: "sem retrabalho"
arquivos_alterados:
  - "MCP_CATALOG.md"
  - "TASK_REGISTER.md"
verificacoes:
  - "pesquisa: passou"
  - "leitura da página: passou"
  - "git diff --check: passou"
limitacoes:
  - "resultado vale somente para web__run na sessão avaliada"
  - "não comprova pesquisa web em Claude, Codex de outra sessão ou Antigravity"
  - "não comprova conectividade HTTP por terminal nem existência de MCP web"
proximo_passo: "Usar web__run quando uma tarefa autorizada exigir pesquisa com fontes; não instalar MCP web por esta evidência."
integrador: "coordenador"
```

---

## Preparação do índice code-review-graph para a equipe (2026-09-17)

```yaml
id: TASK-20260917-MCP-CODEX-GRAPH-PREP-001
objetivo: "Registrar e indexar /root/agent-team sem substituir o projeto Jaaz"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "servidor 2.3.8; registro anterior df80ebc; índice preparado em df80ebc743a783c270c70f43f097ba2ddd60e5ce"
escopo_permitido: "registro do repositório e índice local de /root/agent-team; MCP_CATALOG.md e TASK_REGISTER.md"
fora_do_escopo: "substituir Jaaz, alterar configuração compartilhada, instalar dependências, editar banco/cache, testar outros MCPs, aplicações, rede, credenciais e permissões"
dependencias: ["MCP_CATALOG.md", "/root/.codex/config.toml", "code-review-graph 2.3.8"]
skills_referencias: ["team-gerenciar-mcp", "verify-and-stop"]
criterios_aceitacao:
  - "mecanismo suportado de registro usado"
  - "índice de /root/agent-team criado/atualizado sem substituir /root/jaaz"
  - "uma consulta de leitura pós-indexação confirma projeto e revisão"
  - "limitações de Markdown/TOML e revisão indexada separada da documentação"
entrega_esperada: "catálogo, registro da indexação, consulta confirmatória e commit local"
checkout_reservado: "liberado após commit"
modo_escolhido: "econômico"
justificativa_modo: "Um executor, um registro, uma indexação e uma consulta de leitura; sem revisão adicional."
estado: concluida
resultado: "Registro CLI de /root/agent-team concluído. Build completo pelo MCP em df80ebc: 2 arquivos, 39 nós, 193 arestas, 1 comunidade, sem erros. Consulta pós-indexação retornou status ok, 39 nós/192 arestas e head_matches_build=true. Jaaz permaneceu registrado e não substituído."
evidencias:
  - "Descrições/parametrização de build_or_update_graph, list_repos e get_minimal_context examinadas."
  - "code-review-graph register /root/agent-team -> Registered: /root/agent-team."
  - "list_repos confirmou /root/jaaz e /root/agent-team."
  - "build_or_update_graph_tool(repo_root=/root/agent-team, full_rebuild=true, postprocess=full) -> status ok."
  - "get_minimal_context_tool pós-indexação -> status ok, revisão df80ebc, head_matches_build=true."
  - "Não foram executados instalação, download, dependências, escrita do grafo por comando manual, outros MCPs ou reindexação posterior."
ferramenta: "MCP do Codex + CLI code-review-graph"
modelo: "não disponível"
provedor: "não disponível"
agentes: 0
tentativas: 1
tokens_entrada: "não disponíveis"
tokens_saida: "não disponíveis"
tokens_cache: "não disponíveis"
custo: "não disponível; nenhum preço consultado"
resultado_retrabalho: "sem retrabalho; uma indexação e uma consulta"
arquivos_alterados:
  - "MCP_CATALOG.md"
  - "TASK_REGISTER.md"
verificacoes:
  - "git diff --check passou"
  - "índice e registro de Jaaz preservados"
  - "11 skills e 9 adaptadores preservados"
limitacoes:
  - "o índice parseou 2 arquivos; Markdown/TOML não foram representados semanticamente pelo resultado"
  - "o índice corresponde a df80ebc; o commit documental posterior não foi reindexado por decisão explícita"
  - "não há prova de análise semântica dos 29 Markdown e 9 TOML"
proximo_passo: "Usar consultas sobre /root/agent-team enquanto a revisão indexada permanecer válida; reindexar somente após mudança de código relevante e autorização."
integrador: "coordenador"
```

---

## Verificação operacional do MCP Codex code-review-graph (2026-09-17)

```yaml
id: TASK-20260917-MCP-CODEX-GRAPH-VERIFY-001
objetivo: "Verificar conexão e uma consulta de leitura do codex.code-review-graph sem atualizar o grafo"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "branch master; catálogo ef7179f; HEAD ef7179fd6a6f28e13fbfb9e669a875e7a648b370"
escopo_permitido: "MCP_CATALOG.md, TASK_REGISTER.md, configuração Codex pertinente e uma consulta de leitura sobre /root/agent-team"
fora_do_escopo: "Postman, Caveman, outros clientes, build/update/indexação, escrita, conexão remota, instalação, rede, credenciais e permissões"
dependencias: ["MCP_CATALOG.md", "/root/.codex/config.toml", "code-review-graph 2.3.8"]
skills_referencias: ["team-gerenciar-mcp", "verify-and-stop"]
criterios_aceitacao:
  - "servidor, cliente, versão e ferramentas enumerados sem segredos"
  - "uma consulta de leitura executada sobre /root/agent-team"
  - "projeto/versão indexada e desatualização diferenciados"
  - "nenhuma atualização ou escrita acionada"
entrega_esperada: "catálogo e registro atualizados com resultado operacional e limitações"
checkout_reservado: "liberado após commit"
modo_escolhido: "econômico"
justificativa_modo: "Um MCP, uma enumeração e uma consulta de leitura; sem revisão documental adicional."
estado: concluida
resultado: "Conexão do code-review-graph funcionou. list_repos_tool retornou somente /root/jaaz. A consulta get_minimal_context_tool para /root/agent-team foi aceita, mas retornou stale_graph porque o grafo era de f114d48 e o HEAD era ef7179f; build/update não executado."
evidencias:
  - "Comando configurado examinado: /root/.local/bin/code-review-graph serve --repo /root/jaaz, cwd /root/jaaz; nenhum segredo exposto."
  - "Versão local: code-review-graph 2.3.8."
  - "Superfície MCP enumerou 30 ferramentas."
  - "list_repos_tool: status ok, 1 repositório (/root/jaaz)."
  - "get_minimal_context_tool: status not_ready, reason stale_graph; sugestão build_or_update_graph não executada."
  - "Nenhum servidor foi iniciado manualmente, instalado, atualizado, indexado ou escrito."
ferramenta: "MCP do Codex (identificador de cliente não exposto além da superfície MCP)"
modelo: "não disponível"
provedor: "não disponível"
agentes: 0
tentativas: 1
tokens_entrada: "não disponíveis"
tokens_saida: "não disponíveis"
tokens_cache: "não disponíveis"
custo: "não disponível; nenhum preço consultado"
resultado_retrabalho: "sem retrabalho; nenhuma revisão adicional delegada"
arquivos_alterados:
  - "MCP_CATALOG.md"
  - "TASK_REGISTER.md"
verificacoes:
  - "conexão e enumeração passaram"
  - "consulta executada e classificada como dados inadequados para o HEAD atual"
  - "git diff --check passou"
limitacoes:
  - "servidor registrado para /root/jaaz, não para /root/agent-team"
  - "não há versão/estado do grafo de /root/agent-team porque ele não está registrado"
  - "não há prova de funcionamento atual além da resposta do servidor às duas chamadas"
proximo_passo: "Autorizar separadamente registro/build do grafo de /root/agent-team, se houver necessidade concreta; não executar por este catálogo."
integrador: "coordenador"
```

---

## Política de execução econômica (2026-09-17)

```yaml
id: TASK-20260917-EXECUTION-POLICY-001
objetivo: "Reduzir trabalho redundante e contexto desnecessário sem reduzir critérios ou verificações pertinentes"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "branch master; base 9da0e2f; integração Ponytail preservada"
escopo_permitido: "agents/coordenador.md, .codex/skills/team-coordenar-entrega/SKILL.md, TEAM_CONTRACT.md e este registro"
fora_do_escopo: "aplicações, serviços, MCPs, telemetria, modelos, provedores, planos, roteamento, pilotos, benchmarks e demais papéis"
dependencias: ["TEAM_CONTRACT.md", "team-coordenar-entrega", "lean-build"]
skills_referencias: ["lean-build", "verify-and-stop"]
criterios_aceitacao:
  - "três modos operacionais com seleção e justificativa curta"
  - "política de contexto, encerramento, tentativas e custos documentada"
  - "modelos/provedores/roteamento e telemetria não alterados"
  - "revisão independente curta e validação das referências"
entrega_esperada: "política documental, evidências, revisão e commit local"
checkout_reservado: "liberado após commit"
modo_escolhido: "padrão"
justificativa_modo: "Mudança documental moderada em quatro arquivos, com uma revisão independente; não exige especialistas paralelos."
estado: concluida
resultado: "Modos econômico, padrão e ampliado documentados; resumo de contexto, encerramento e observabilidade de custos adicionados sem metas artificiais. A revisão independente encontrou a ausência de fora_do_escopo e skills_referencias no registro, corrigida antes do commit."
evidencias:
  - "Leitura de TEAM_CONTRACT.md, agents/coordenador.md e .codex/skills/team-coordenar-entrega/SKILL.md."
  - "Revisão independente curta pelo subagente /root/execution_policy_reviewer."
  - "Achado médio da revisão: campos obrigatórios ausentes no registro; corrigido com fora_do_escopo e skills_referencias."
  - "git diff --check passou."
  - "Nenhum piloto, benchmark, telemetria ou configuração de modelo executado/alterado."
ferramenta: "não disponível"
modelo: "não disponível"
provedor: "não disponível"
agentes: 1
tentativas: 1
tokens_entrada: "não disponíveis"
tokens_saida: "não disponíveis"
tokens_cache: "não disponíveis"
custo: "não disponível; nenhum preço consultado"
resultado_retrabalho: "uma revisão independente; sem retrabalho após a revisão"
arquivos_alterados:
  - "agents/coordenador.md"
  - ".codex/skills/team-coordenar-entrega/SKILL.md"
  - "TEAM_CONTRACT.md"
  - "TASK_REGISTER.md"
verificacoes:
  - "referências e estrutura revisadas"
  - "git diff --check passou"
  - "Ponytail, onze skills e demais adaptadores preservados"
limitacoes:
  - "não há medição comparável de custo por tarefa aceita nesta etapa"
  - "tokens, cache, preço e provedor não foram expostos pela superfície usada"
proximo_passo: "Aplicar o modo proporcional em tarefas futuras e coletar custos somente quando a ferramenta os disponibilizar."
integrador: "coordenador"
```

---

## Catálogo inicial de MCPs (2026-09-17)

```yaml
id: TASK-20260917-MCP-CATALOG-001
objetivo: "Catalogar MCPs configurados para Codex, Claude e Gemini/Antigravity e propor acessos sem habilitar servidores"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "branch master; base 248b3d6; modo padrão"
escopo_permitido: "MCP_CATALOG.md, TASK_REGISTER.md e leituras direcionadas das configurações MCP pertinentes"
fora_do_escopo: "inventário geral de infraestrutura, conexões, handshakes, inicialização, instalação, testes remotos, mudanças em configurações, credenciais, rede, serviços ou permissões"
dependencias: ["TEAM_CONTRACT.md", "team-gerenciar-mcp", "team-construir-mcp"]
skills_referencias: ["team-gerenciar-mcp", "team-construir-mcp", "verify-and-stop"]
criterios_aceitacao:
  - "catálogo com estados, evidências, origem, transporte, capacidades e autenticação sem segredos"
  - "matriz de acesso separando propostas de controles verificados"
  - "levantamento e conferência por papéis nativos explicitamente delegados"
  - "nenhuma configuração externa alterada ou servidor conectado"
entrega_esperada: "MCP_CATALOG.md, conferência independente, lacunas e commit local"
checkout_reservado: "liberado após commit"
modo_escolhido: "padrão"
justificativa_modo: "Levantamento delimitado com conferência técnica independente; não requer paralelismo adicional."
estado: concluida
resultado: "Catálogo criado. Gestor /root/gestor_mcp_catalog levantou cinco configurações MCP catalogáveis e uma fonte Gemini vazia. Engenheiro /root/engenheiro_mcp_conferer conferiu transporte, classificação, capacidades, segredos e separação proposta/estado; cinco ajustes documentais foram aplicados."
evidencias:
  - "Leituras explícitas do contrato, papéis e skills pelos dois subagentes."
  - "Configurações examinadas: Codex config.toml, .mcp.json/Claude, .claude.json e Gemini/Antigravity mcp_config/settings."
  - "Nenhum servidor, comando de inicialização, conexão, teste remoto, instalador ou hook executado."
  - "Valores secretos não foram lidos; somente o nome POSTMAN_API_KEY foi registrado."
  - "git diff --check passou."
ferramenta: "não disponível"
modelo: "não disponível"
provedor: "não disponível"
agentes: 2
tentativas: 2
tokens_entrada: "não disponíveis"
tokens_saida: "não disponíveis"
tokens_cache: "não disponíveis"
custo: "não disponível; nenhum preço consultado"
resultado_retrabalho: "uma conferência independente; cinco correções documentais concretas; sem repetição de inventário"
arquivos_alterados:
  - "MCP_CATALOG.md"
  - "TASK_REGISTER.md"
verificacoes:
  - "referências e estrutura do catálogo revisadas"
  - "conferência independente concluída"
  - "integração Ponytail, onze skills e nove adaptadores preservados"
limitacoes:
  - "nenhum handshake ou funcionamento atual verificado"
  - "cliente da execução histórica de get_review_context não identificado"
  - "versões, owners e ferramentas Claude/Gemini não enumeradas permanecem não disponíveis"
  - "não há MCP configurado para pesquisa geral na internet ou consulta autorizada a serviços internos"
proximo_passo: "Se houver necessidade concreta, autorizar uma verificação pontual de conexão de um cliente específico; não habilitar ou instalar MCP por este catálogo."
integrador: "coordenador"
```

---

## Triagem dos achados da revisão Antigravity (2026-09-17)

```yaml
id: TASK-20260917-ANTIGRAVITY-TRIAGE
objetivo: "Classificar sete achados reportados e aplicar somente correções documentais sustentadas"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "branch master; base a450b8f; sem alteração de adaptadores TOML"
escopo_permitido: "TEAM_CONTRACT.md, agents/code-reviewer.md, .codex/skills/team-revisar-alteracao/SKILL.md e este registro"
estado: concluida
fonte_dos_achados: "Os sete temas foram delimitados pelo pedido; não há relatório Antigravity versionado no checkout. A classificação não inventa evidência ausente."
achados:
  - id: AG-01
    tema: "escopo da revisão"
    classificacao: "melhoria de clareza ou portabilidade"
    severidade: "baixa"
    justificativa: "As instruções já exigiam versão identificada, mas não enumeravam commit, diff, arquivos ou versão como formas equivalentes."
    correcao: "Skill e papel agora exigem escopo identificável e inspeção direta quando o grafo não corresponder."
  - id: AG-02
    tema: "skills auxiliares e indisponibilidade"
    classificacao: "melhoria de clareza ou portabilidade"
    severidade: "baixa"
    justificativa: "As referências caveman-review e verify-and-stop estavam nomeadas, sem procedimento explícito de resolução por arquivo ou fallback."
    correcao: "Resolução prévia por SKILL.md e registro do impedimento foram acrescentados."
  - id: AG-03
    tema: "formato de retorno"
    classificacao: "não sustentado pelas evidências"
    severidade: "informativa"
    justificativa: "A skill referencia o formato do contrato; não há duplicação do esquema que justifique defeito."
    correcao: "Nenhuma; a referência ao contrato foi preservada."
  - id: AG-04
    tema: "grafo e alternativa por inspeção direta"
    classificacao: "melhoria de clareza ou portabilidade"
    severidade: "média"
    justificativa: "A regra usava o grafo quando disponível, mas não explicitava mesma referência, desatualização ou fallback."
    correcao: "Uso condicionado ao mesmo repositório/referência, com fallback direto e limitação registrada."
  - id: AG-05
    tema: "menção a AGENTS.md"
    classificacao: "não sustentado pelas evidências"
    severidade: "informativa"
    justificativa: "O texto apenas impede tratá-lo como prova de registro; não exige esse caminho para executar a revisão."
    correcao: "Esclarecido como contexto conceitual quando aplicável, não como caminho exigido."
  - id: AG-06
    tema: "afirmação de somente leitura"
    classificacao: "melhoria de clareza ou portabilidade"
    severidade: "média"
    justificativa: "Somente leitura é limite documental da tarefa; não prova isolamento integral de shell ou MCP."
    correcao: "Papel e skill agora separam limite escrito de controles técnicos observados."
  - id: AG-07
    tema: "contagem dos campos do contrato"
    classificacao: "melhoria de clareza ou portabilidade"
    severidade: "baixa"
    justificativa: "A alegação de oito ou nove não é sustentada: a lista real contém onze campos, com skills/referências como um campo."
    correcao: "Contrato agora declara explicitamente a contagem de onze."
evidencias:
  - "Leitura de TEAM_CONTRACT.md, agents/code-reviewer.md e .codex/skills/team-revisar-alteracao/SKILL.md."
  - "code-review-graph get_review_context: risco baixo, 3 arquivos, 0 impactos modelados; grafo construído em f114d48 e head a450b8f, portanto não corresponde exatamente ao head."
  - "Fonte direta prevaleceu sobre o grafo; nenhuma execução de piloto ou eval foi feita."
arquivos_alterados:
  - "TEAM_CONTRACT.md"
  - "agents/code-reviewer.md"
  - ".codex/skills/team-revisar-alteracao/SKILL.md"
  - "TASK_REGISTER.md"
verificacoes:
  - "referências de skills e caminhos revisados"
  - "git diff --check passou"
  - "não foram alterados adaptadores TOML, aplicações, serviços, permissões ou infraestrutura"
limitacoes:
  - "Não há relatório Antigravity versionado para validar formulações além dos sete temas explicitados no pedido."
  - "O grafo está defasado em relação ao head; a revisão documental foi confirmada por inspeção direta."
  - "Não foi comprovado isolamento técnico integral de shell/MCP nesta tarefa."
proximo_passo: "Usar o escopo e o fallback documentados em futuras revisões; não declarar carregamento nativo de skills sem evento observável."
integrador: "coordenador"
```

---

## Integração local do Ponytail (2026-09-17)

```yaml
id: TASK-20260917-PONYTAIL-001
objetivo: "Incorporar duas skills do Ponytail e associá-las somente ao Desenvolvedor e ao Code Reviewer"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "branch master; origem fixada em e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156"
escopo_permitido: "third_party/ponytail, definições e skills do Desenvolvedor/Reviewer, dois adaptadores Codex e este registro"
dependencias: ["TEAM_CONTRACT.md", "team-implementar-tarefa", "team-revisar-alteracao"]
skills_referencias: ["skill-installer (orientação de aquisição; instalação global não usada)", "Ponytail skills no commit fixado"]
criterios_aceitacao:
  - "duas SKILL.md preservadas byte a byte com origem e licença"
  - "Ponytail ativo somente como auxiliar de desenvolvedor e code-reviewer"
  - "limites de simplificação documentados sem alterar o contrato"
  - "referências resolvem e revisão explícita do diff é registrada"
entrega_esperada: "cópia versionada, associações, evidência de revisão e limitações"
estado: concluida
resultado: "Skills incorporadas e associações atualizadas. O subagente Reviewer /root/ponytail_review_final revisou o diff somente por leitura; encontrou e corrigiu uma ambiguidade documental no escopo permitido, sem defeitos funcionais."
evidencias:
  - "clone somente leitura em /tmp/ponytail-src.6Y0Zrb"
  - "HEAD da origem: e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156"
  - "hashes locais das duas skills e LICENSE coincidem com git show da origem"
  - "TOML de desenvolvedor e code-reviewer parseado com tomli"
  - "Revisão explícita /root/ponytail_review_final: leituras observáveis, comparação byte a byte e git diff --check aprovado"
arquivos_alterados:
  - "third_party/ponytail/skills/ponytail/SKILL.md"
  - "third_party/ponytail/skills/ponytail-review/SKILL.md"
  - "third_party/ponytail/LICENSE"
  - "third_party/ponytail/README.md"
  - "agents/desenvolvedor.md"
  - "agents/code-reviewer.md"
  - ".codex/skills/team-implementar-tarefa/SKILL.md"
  - ".codex/skills/team-revisar-alteracao/SKILL.md"
  - ".codex/agents/desenvolvedor.toml"
  - ".codex/agents/code-reviewer.toml"
  - "TASK_REGISTER.md"
verificacoes:
  - "git diff --check passou"
  - "correção posterior de `terceiros/ponytail` para `third_party/ponytail`"
  - "não executados instaladores, hooks, scripts Ponytail, piloto HH:MM:SS ou benchmarks"
  - "demais sete papéis, onze skills próprias e adaptadores não foram alterados"
limitacoes:
  - "carregamento automático e seleção TOML não são presumidos; a próxima revisão usará caminhos explícitos"
  - "não há evidência de ganho de produtividade nesta integração"
proximo_passo: "usar as associações somente nos dois papéis; carregamento automático continua não comprovado"
integrador: "coordenador"
```

---

## Verificação de carregamento efetivo de skill (2026-09-17)

```yaml
id: TASK-20260917-SKILLS-LOAD-001
objetivo: "Verificar carregamento nativo de team-revisar-alteracao durante revisão do commit 5f3e687"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "codex-cli 0.154.0; commit 5f3e687ff4c461528d22372ca3011295fe29961d"
escopo_permitido: "revisão somente leitura do commit; registro; sem piloto, evals, instalação, edição de skills ou configuração global"
dependencias: ["TASK-20260917-SKILLS-001"]
skills_referencias: ["team-revisar-alteracao", "caveman-review", "verify-and-stop"]
criterios_aceitacao:
  - "delegação nativa code-reviewer executada ou bloqueio comprovado"
  - "adaptador, conteúdo e mecanismo de acesso distinguidos por evidência"
  - "uma única nova tentativa após falha inicial, sem declarar carregamento não observado"
entrega_esperada: "id real, parecer, eventos/metadados de carregamento, ajustes e limitações"
checkout_reservado: "nenhum (somente leitura)"
estado: parcial
resultado: "A revisão estática foi executada por /root/code_reviewer_skill_load, mas não houve prova de que o adaptador Codex tenha sido resolvido nem de carregamento nativo da skill. O conteúdo apareceu após leitura explícita do SKILL.md. A única tentativa posterior em sessão fresca 01a0aea1-30e2-7700-87cd-ece424704ec0 também não criou um subagente: não houve evento SubAgentActivity, agent_role/adaptador resolvido ou metadado de skills."
evidencias:
  - "execução real inicial: /root/code_reviewer_skill_load; revisão do commit 5f3e687 sem alterações, nenhum defeito confirmado"
  - "metadado da sessão inicial: agent_role=null e ausência de lista/evento de skills carregadas"
  - "team-revisar-alteracao só foi acessada por leitura explícita de /root/agent-team/.codex/skills/team-revisar-alteracao/SKILL.md"
  - "auxiliares realmente necessários/acessíveis: /root/.agents/skills/caveman-review/SKILL.md e /root/.agents/skills/verify-and-stop/SKILL.md"
  - "tentativa única: sessão fresca 01a0aea1-30e2-7700-87cd-ece424704ec0; o pai leu team-coordenar-entrega, mas não emitiu SubAgentActivity para code-reviewer"
  - "não foram executados piloto, evals ou instalação"
arquivos_alterados: ["TASK_REGISTER.md"]
verificacoes:
  - "revisão estática: passou"
  - "carregamento nativo automático: não comprovado"
  - "tentativa única de recuperação: falhou sem criar subagente"
  - "configuração pertinente alterada: nenhuma; causa é a superfície de delegação sem seleção de agente TOML"
limitacoes:
  - "spawn_agent desta sessão não expõe escolha de agente TOML; seu evento registrou agent_role nulo"
  - "codex exec não ofereceu uma evidência de subagente personalizado na tentativa única"
  - "o parecer comprova somente a revisão com leitura explícita, não todas as onze skills nem descoberta automática"
proximo_passo: "usar uma superfície Codex que exponha seleção nativa de custom agent antes de repetir esta verificação"
integrador: "coordenador"
```

---

## Documentação do modo operacional Codex (2026-09-17)

```yaml
id: TASK-20260917-SKILLS-LOAD-DOCS
objetivo: "Documentar o caminho explícito comprovado e preservar o estado parcial do carregamento nativo"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "codex-cli 0.154.0; base 7d688fa"
escopo_permitido: "somente TEAM_CONTRACT.md, README.md e TASK_REGISTER.md"
dependencias: ["TASK-20260917-SKILLS-LOAD-001"]
skills_referencias: ["TEAM_CONTRACT.md", "README.md"]
criterios_aceitacao:
  - "distinguir subagente genérico explícito, perfil TOML e carregamento automático"
  - "documentar procedimento de delegação com caminhos absolutos"
  - "distinguir limites escritos de controles técnicos"
  - "preservar estado parcial sem novas tentativas"
entrega_esperada: "documentação operacional e exemplo code-reviewer"
checkout_reservado: "liberado após commit local"
estado: concluida
resultado: "Documentado o modo explícito comprovado; seleção nativa TOML e carregamento automático permanecem não comprovados. Nenhuma nova delegação foi executada."
evidencias:
  - "alterados somente TEAM_CONTRACT.md, README.md e TASK_REGISTER.md"
  - "exemplo usa apenas task_name, fork_turns e message, argumentos suportados por collaboration.spawn_agent"
  - "não foram alterados adaptadores TOML, skills, aplicações ou serviços"
verificacoes: ["diff documental revisado", "git diff --check: passou", "piloto/evals: não executados"]
arquivos_alterados: ["TEAM_CONTRACT.md", "README.md", "TASK_REGISTER.md"]
limitacoes: ["documentação alternativa não comprova carregamento nativo; a tarefa SKILLS-LOAD-001 permanece parcial"]
proximo_passo: "usar uma superfície Codex com seleção nativa observável antes de reavaliar o carregamento"
integrador: "coordenador"
```

---

## Skills específicas da equipe (2026-09-17)

```yaml
id: TASK-20260917-SKILLS-001
objetivo: "Implementar skills operacionais e de eval para os nove papéis e associá-las aos agentes"
responsavel: "coordenador"
projeto: "agent-team"
maquina: "host /root"
caminho: "/root/agent-team"
versao_estado: "codex-cli 0.154.0; base dd33ea2"
escopo_permitido: "skills em .codex/skills, definições centrais, adaptadores Codex e registro; sem aplicações, MCPs, serviços, credenciais ou permissões"
dependencias: ["TASK-20260917-CODEX-001"]
skills_referencias: ["skill-creator", "investigate-first", "surgical-patch", "safe-refactor", "lean-build", "caveman-review", "verify-and-stop"]
criterios_aceitacao:
  - "nove skills principais e duas skills de eval com SKILL.md completo"
  - "associação central e [[skills.config]] dos adaptadores Codex"
  - "estrutura, sintaxe e referências validadas"
  - "revisão independente sem eval comportamental"
entrega_esperada: "skills, mapeamento, validação, revisão e limitações de carregamento"
checkout_reservado: "liberado após commit local"
estado: concluida
resultado: "Implementação concluída e revisão independente aprovada."
evidencias:
  - "quick_validate.py passou para os 11 diretórios"
  - "tomli validou os 9 adaptadores e 30 referências de skills acessíveis"
  - "definições centrais apontam skill principal e auxiliares"
  - "não foram executados evals nem o piloto Python"
  - "revisor independente /root/skills_review_codex: 11 skills, 9 TOMLs e 30 referências acessíveis; nenhum defeito funcional"
arquivos_alterados: [".codex/skills/**", "agents/*.md", ".codex/agents/*.toml", "README.md", "TASK_REGISTER.md"]
verificacoes: ["quick_validate: passou", "TOML/referências: passou", "revisão independente: passou", "carregamento em sessão nova: não executado"]
limitacoes: ["Codex 0.154.0 não fornece prova local de carregamento de skills sem iniciar uma delegação; associação textual e arquivo acessível foram distinguidos de carregamento comprovado", "Claude/Antigravity continuam dependendo de suas sessões de descoberta/registro; nenhum arquivo global foi alterado"]
proximo_passo: "fazer commit somente dos arquivos desta tarefa"
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
