---
name: team-operar-ambiente
description: Opere ou diagnostique ambientes Linux quando host, VM, CT, container, volumes, redes ou serviços precisarem ser identificados.
---

# Team — operar ambiente

## Objetivo e entradas

Estabelecer topologia e estado operacional antes de qualquer mudança. Receba
alvo, máquina, serviço, caminho montado, versão/imagem, efeito esperado e
autoridade explícita.

## Procedimento e decisões

1. Identifique host, VM/CT, container, checkout, imagem/tag, volumes, rede e
   processo/serviço; não misture árvores com o mesmo caminho nominal.
2. Faça diagnóstico somente leitura e registre origem→implantação, estado e
   sinais de saúde.
3. Separe sintoma, causa provável, dependências e impacto; escolha a menor
   mudança reversível apenas se autorizada.
4. Antes de operar, defina pré-condição, janela, rollback e verificação pós-
   mudança. Não reinicie produção por padrão.
5. Verifique o estado observado após a ação e preserve logs sem segredos.

## Limites e dependências

Não invente comandos de um provedor nem transforme um ambiente atual em regra
universal. CTs, containers e hosts são escopos distintos. Não leia credenciais,
altere permissões, rede ou serviços sem autorização.

## Entrega e evidências

Entregue topologia, comandos seguros, estado antes/depois, impacto, rollback e
limitações no formato do contrato. Evidências devem incluir máquina, serviço,
versão e caminho exatos.

## Impedimentos

Bloqueie se o alvo, origem da imagem, montagem, serviço ou autoridade estiverem
ambíguos; registre o que precisa ser confirmado.
