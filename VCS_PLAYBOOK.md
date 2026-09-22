# Playbook de Versionamento e Git (VCS Playbook)

> **Regra de Ouro da Equipe:** Comitar e dar push deve ser um processo rápido, fácil e à prova de falhas. Nenhum agente ou operador deve perder tempo adivinhando chaves, URLs ou repositórios remotos.

---

## 1. Video Studio (Jaaz / Estúdio Visual)

| Propriedade | Valor |
| :--- | :--- |
| **Repositório GitHub** | `git@github.com:neurodata-solutions/estudio-visual.git` (HTTPS: `https://github.com/neurodata-solutions/estudio-visual.git`) |
| **Conta / Organização** | `neurodata-solutions` |
| **Branch Oficial de Trabalho** | `jaaz` (rastreia `origin/jaaz`) |
| **Diretório no Host (Proxmox)** | `/root/jaaz` |
| **Diretório no LXC CT100 (Docker)** | `/root/jaaz` |
| **Container de Execução** | `opensuite-jaaz` no CT100 (Porta Web: `57988`) |
| **Upstream de Referência** | `https://github.com/11cafe/jaaz.git` |

---

## 2. Segredos e Credenciais no Infisical

**Movido para fora deste repositório em 2026-09-22** — este arquivo faz
parte do vault Obsidian sincronizado (repo `agent-team` tem remote git e é
clonado em múltiplos dispositivos). URLs internas, inventário de onde
ficam PAT/chave SSH e outros detalhes de infraestrutura de segredos nunca
devem entrar em git, mesmo em repositório privado.

Conteúdo completo agora fica em `/root/.secrets-notes/vcs-playbook-infisical.md`
(local a este host, fora de qualquer repositório git).

---

## 3. Como Comitar e Enviar (Rápido e Fácil)

### Opção A (Recomendada - 1 comando):
Tanto no Host Proxmox quanto no CT100, execute:
```bash
gitvideo-push "sua mensagem descritiva de commit"
```
Ou dentro de `/root/jaaz`:
```bash
./push.sh "sua mensagem descritiva de commit"
```
*O utilitário faz `git add`, `git commit`, `git pull --rebase` e `git push` automaticamente em menos de 5 segundos.*

### Opção B (Git Padrão):
O ambiente já está configurado com chaves SSH e upstream padrão. Você pode simplesmente rodar:
```bash
cd /root/jaaz
git add <arquivos>
git commit -m "feat(video-studio): descrição"
git push
```
*(Não precisa passar remote nem branch, pois `push.default current` e `push.autoSetupRemote` já estão ativos).*

---

## 4. Cuidados Essenciais (.gitignore e Mídias)
- **NUNCA comite arquivos de mídia gerados:** O diretório `server/data/` (vídeos, temporários, renders) contém quase 1GB de dados e está no `.gitignore`.
- Se criar novos diretórios de cache ou renderização, garanta que estejam no `.gitignore` antes de fazer `git add`.
