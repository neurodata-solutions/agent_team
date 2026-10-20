# Plano de discos do host `srv` (Proxmox VE 7.4-3, Debian 11.6)

Data: 2026-10-20. Autor: Claude (pedido do Paolo: "temos que organizar… temos que planejar bem isso").
Status: proposta. Nada além da fase 0 foi executado.

## Inventário real (lsblk/smartctl, 20/10)

| Disco | Modelo | Tipo | Saúde | Uso hoje |
|---|---|---|---|---|
| `sdc` | Husky SSD 512 GB | SSD SATA | PASSED, 6.087 h, sem desgaste | Proxmox (`pve-root` 96 GB, swap 8 GB) + `local-lvm` (thin 348 GB) |
| `sdb` | Kingston SV300 120 GB | SSD SATA (~2013) | PASSED, 25.330 h, 14,7 TB gravados | **fora do Proxmox**: partições de um Windows antigo (NTFS) |
| `sda` | WD5000LPVX 500 GB | HDD 2,5" 5400 rpm | PASSED, 11.340 h, 0 setores realocados | `hdd-storage` (thin 442 GB): CT103, VM 101 |

- **Não há NVMe visível** para o sistema. Se existe fisicamente, não está instalado ou a BIOS não o detecta.
- **Não há nenhum backup** (`/var/lib/vz/dump` vazio; nenhum storage com `content backup` além de `local`).
- `local-lvm` estava com 362 GB alocados num pool de 348 GB (82% de uso real): se encher, CT100, CT102 e VM 101 corrompem juntos.
- CT100 (produção: Jaaz, Postiz, OpenReply, renderizador, n8n, bancos…) encheu o disco em 13/10 e 20/10.

## Princípios

0. **Desempenho (Paolo, 20/10): o HDD é lento (2,5", 5400 rpm).** Nada que serviços de produção leiam/gravem com frequência vai
   para ele: bancos, imagens Docker, filas, cache, temporários de render ficam em SSD. HDD só para frio (laboratório parado,
   arquivo de mídia antiga) e backups, de preferência gravados de madrugada.

1. Backup antes de qualquer mudança de disco, e em disco diferente do original.
2. SSD bom (Husky) para o que é quente: sistema, discos raiz dos guests, bancos, imagens Docker.
3. HDD para o que é frio e grande: saídas de mídia, laboratórios parados, backups.
4. SSD antigo (Kingston) só para dados descartáveis/reconstruíveis (scratch, cache, temporários de render).
5. Nunca mais alocar além do tamanho real de um pool thin; alerta em 85%.

## Layout alvo

| Disco | Pool/Storage | Conteúdo | Alocado |
|---|---|---|---|
| Husky 512 SSD | `pve-root` 96 GB | Proxmox, ISOs/templates (`local`) | — |
| | `local-lvm` 348 GB | CT100 rootfs 160 GB, CT102 32 GB (folga para crescer o CT100 depois) | 192 GB |
| Kingston 120 SSD | novo `ssd-scratch` (lvmthin ~110 GB) | CT100 `mp1` `/mnt/scratch`: `video_jobs`, temporários de render, cache de build | ~100 GB |
| WD 500 HDD | `hdd-storage` 442 GB | VM 101 (120 GB, laboratório parado), CT103 (20 GB), CT100 `mp0` `/mnt/hdd` 120 GB só para **arquivo frio** (mídia antiga já publicada, `/root/pessoal`, backups de deploy). Saídas em uso continuam no SSD. | 260 GB |
| | novo `hdd-backup` (dir, LV thin 150 GB, ext4) | `vzdump` de CT100/CT102/CT103 | 150 GB |

Total no HDD: 410 GB de 442 GB.

## Executado

- 20/10: VM 101 copiada para `hdd-storage` (`qm move-disk` sem `--delete`); `qm config 101` aponta para o HDD; originais em
  `local-lvm` como `unused0`/`unused1`; apagados em 20/10 com OK do Paolo (`qm disk unlink … --force`).
  `local-lvm`: 81,9% → 49,2% (185 GB livres); alocado 192 GB de 348 GB, fim do excesso de alocação.
- 20/10: backup da configuração do host em `/root/backups/host-config-20261020-090812/` (288 KB, `chmod 700`):
  `etc.tgz` (`/etc/pve` com configs dos guests, rede, fstab, apt, lvm, systemd, cron, postfix, grub, kernel) e `info/`
  (pveversion, lsblk, blkid, `sfdisk -d` dos 3 discos, `vgcfgbackup` de `pve` e `vg-hdd`, pvesm, configs `qm`/`pct`, pacotes, IPs,
  rotas, units). `SHA256SUMS` conferido. Fica no SSD (root do host) até existir `hdd-backup` na fase 1; não foi copiado para
  nenhum guest porque `/etc/pve` tem chaves e segredos.
- Husky 512 GB confirmado SATA 2,5" (SATA 3.2, 6 Gb/s, controlador Intel 8 Series/C220 AHCI); nenhum controlador NVMe no PCIe.
  NVMe futuro só com adaptador PCIe → M.2, provavelmente sem boot (vira disco de dados rápido para o CT100).

## Fases

### Fase 0: tirar o SSD da zona de risco (em andamento)
- VM 101 (EveEng, parada, sem backup) copiada para `hdd-storage` com `qm move-disk` **sem `--delete`**.
- Depois de conferir `qm config 101`, apagar os discos originais (`unusedN`) no `local-lvm` → libera ~114 GB. Precisa de OK.
- Decidir se a VM 101 ainda é necessária (se não, pode até ser removida).

### Fase 1: backups (antes de mexer em mais nada)
1. Criar LV thin `vg-hdd/backup` 150 GB, ext4, montado em `/mnt/hdd-backup` (fstab), storage `dir` `hdd-backup` `content backup`.
2. Job `vzdump` noturno (snapshot, zstd) para CT100, CT102, CT103; retenção `keep-daily=7,keep-weekly=4`.
   CT100: `--exclude-path` para `/var/lib/docker/overlay2` e `/var/lib/docker/buildkit` (imagens são reconstruíveis; volumes e bancos entram).
3. Rodar o primeiro backup manual e testar restauração de um arquivo.
4. Depois: cópia fora do host (outro equipamento ou nuvem). Backup no mesmo servidor não protege contra perda do servidor.

### Fase 2: Kingston como scratch
1. Paolo confirma que **nada no Windows antigo do `sdb` é necessário** (apagar é irreversível).
2. `wipefs`, `pvcreate`, `vgcreate vg-ssd2`, thin pool, storage `ssd-scratch` (`content rootdir,images`).

### Fase 3: CT100 com discos de dados (janela de manutenção)
1. `pct set 100 -mp0 hdd-storage:120,mp=/mnt/hdd,backup=1` e `-mp1 ssd-scratch:100,mp=/mnt/scratch,backup=0`.
   Se ficar pendente, reiniciar o CT100 na janela (2–3 min fora do ar).
2. Mover, um serviço por vez (parar → copiar → apontar volume/bind → subir → conferir):
   `opensuite_moneyprinter_outputs` (9,6 GB), `facefusion_facefusion-data` (4,7 GB), `opensuite_openshorts_output` (3 GB),
   `video_jobs` do Jaaz, `/root/pessoal` (8,4 GB), backups de `/root/deploy`.

### Fase 4: alerta
- `scratchpad/disco-alerta.sh` (timer 30 min, 85%, e-mail root + journal). Pronto para instalar.

## Decisões pendentes do Paolo
1. Existe um NVMe físico? (se sim, muda o plano: NVMe vira o disco quente e o Husky vira dados).
2. O Windows do Kingston pode ser apagado?
3. A VM 101 (EveEng) ainda é usada?
4. Horário da janela da fase 3.
5. Destino da cópia de backup fora do host.
