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

* **URL Web do Infisical:** [Painel de Secrets Overview](https://192.168.0.200:8620/organizations/d36ac3d6-a0cd-4a15-bee6-cd91e3d679c8/projects/secret-management/e88ec536-c83a-4b68-a826-172e1e534b02/overview?environments=%5B%22dev%22%2C%22staging%22%2C%22prod%22%5D)
* **Projeto:** `opensuite` (`e88ec536-c83a-4b68-a826-172e1e534b02`)
* **Ambientes Sincronizados:** `dev`, `staging` e `prod`
* **Backend Interno:** `http://infisical-backend:8080` (Docker) / `http://127.0.0.1:18080` (CT100)

### Chaves Registradas:
- **No Root (`/`):**
  - `gitvideo`: GitHub Personal Access Token (`github_pat_...`) da conta `neurodata-solutions`.
  - `GITVIDEO_REPO_URL`: `https://github.com/neurodata-solutions/estudio-visual.git`
  - `GITVIDEO_BRANCH`: `jaaz`
- **Na Pasta `/jaaz`:**
  - `GITVIDEO_PAT`: PAT para clones/pushes via HTTPS.
  - `GITVIDEO_REPO_URL`: `https://github.com/neurodata-solutions/estudio-visual.git`
  - `GITVIDEO_SSH_URL`: `git@github.com:neurodata-solutions/estudio-visual.git`
  - `GITVIDEO_BRANCH`: `jaaz`
  - `GITVIDEO_UPSTREAM_URL`: `https://github.com/11cafe/jaaz.git`
  - `GITVIDEO_SSH_KEY`: Chave privada OpenSSH (`id_ed25519`) para deploy automatizado.

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
