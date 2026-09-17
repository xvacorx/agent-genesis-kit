---
name: proxmox-pve-architect
description: "Proxmox VE 8/9, ZFS mirror storage, LXC container orchestration, Netbird mesh networking, GLPI/ITAM automation, and GPU passthrough diagnostics for srv-conectica."
allowed-tools: Read, Glob, Grep, Bash
risk: unknown
source: conectica-it
---

# Proxmox VE Architect — Infrastructure, LXC, ZFS & ITAM Runbooks

> **Target Environment:** `srv-conectica` (PVE 9.x, Kernel 7.x, Intel HD 4600 + AMD Radeon RX 580).
> **Network Limits:** Only operate on host, LXCs, and authorized overlay networks (`<PROXMOX_HOST_IP>`). Physical LAN is restricted.
> **Security Law:** Never store or print credentials in plain text. Always SSH via user key `~/.ssh/id_ed25519`.

---

## 1. Quick Access & Remote Execution Protocol

### 1.1 SSH Command Execution
```bash
# Direct command on Proxmox host
ssh -i ~/.ssh/id_ed25519 root@<PROXMOX_HOST_IP> "<command>"

# Direct command inside specific LXC container (e.g., VMID 300 - GLPI)
ssh -i ~/.ssh/id_ed25519 root@<PROXMOX_HOST_IP> "pct exec <VMID> -- <command>"
```

### 1.2 Common Container Map
| VMID | Hostname | Function | Key Services |
| :--- | :--- | :--- | :--- |
| **100** | `npm` | Nginx Proxy Manager | Docker, SSL Let's Encrypt |
| **101** | `netbird` | Netbird Server & Dashboard | VPN Mesh Controller |
| **102** | `fog-pxe` | FOG PXE Server | TFTP, NFS (`/Datos/images`) |
| **103** | `gw-proxy` | Local Gateway Proxy | Squid, Forwarder |
| **200** | `teampass` | Password Vault | Apache, MySQL |
| **201** | `authentik`| SSO Identity Provider | Docker, PostgreSQL, Redis |
| **300** | `glpi` | GLPI Central & ITAM Reaper | Apache, PHP 8.x, MySQL, Cron |
| **301** | `rustdesk`| RustDesk ID & Relay | `hbbs`, `hbbr` |
| **303** | `zabbix` | Zabbix Monitoring Server | Zabbix Server, Web UI, MySQL |
| **405** | `snap-tools`| Snapotter OCR & IT-Tools | Docker, GPU Passthrough |

---

## 2. ZFS Mirror Health & Maintenance

`srv-conectica` uses two ZFS mirror pools:
- `rpool` (SSD Mirror ~444GB): OS and high-IOPS LXC root disks.
- `Datos` (HDD Mirror ~928GB): FOG images, backups, heavy ISO storage.

### 2.1 Health Check & Scrub Commands
```bash
# Check status, errors, and scrub progress
zpool status -v

# Check space and fragmentation
zpool list -o name,size,alloc,free,frag,cap,health

# Start periodic scrub (scheduled via cron)
zpool scrub rpool
zpool scrub Datos

# Check SSD Wear-out status
pveam status  # or smartctl -a /dev/sdX
```

---

## 3. LXC Lifecycle & Resource Tuning

### 3.1 Container Operations
```bash
# Status of all containers
pct list

# Start / Stop / Restart with timeout
pct start <vmid>
pct shutdown <vmid> --timeout 30
pct reboot <vmid>

# Inspect configuration (cores, memory, mount points)
pct config <vmid>
```

### 3.2 Dynamic Memory & Core Resizing
```bash
# Increase RAM to 4GB (4096MB) on the fly without reboot
pct set <vmid> -memory 4096 -swap 1024

# Adjust CPU cores
pct set <vmid> -cores 4
```

---

## 4. GLPI Central & ITAM Reaper 2.2 Runbook

### 4.1 ITAM Reaper Garbage Collector
Located at `/root/glpi_garbage_collector.sh` in container `300` (`glpi`):
* Cron Schedule: Every day at 3:00 AM.
* Features: Deduplicates PCs, Printers, and Network devices; purges deleted records.
* Manual Dry-Run / Trigger:
  ```bash
  pct exec 300 -- /root/glpi_garbage_collector.sh --dry-run
  pct exec 300 -- php /var/www/netscan/glpi_deduplicate_assets.php
  ```

### 4.2 Netscan Bot v3.2
* Scans network subnets, escapes SQL injections, auto-queries SNMP sysDescr/sysObjectID.
* Status check:
  ```bash
  pct exec 300 -- systemctl status netscan_bot.service
  ```

---

## 5. GPU Passthrough & Hardware Diagnostics

* Primary GPUs:
  - `00:02.0 VGA compatible controller: Intel Corporation Xeon E3-1200 v3/4th Gen Core Processor Integrated Graphics Controller`
  - `01:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere [Radeon RX 470/480/570/570X/580/580X/590]`
* Check GPU availability and driver bind:
  ```bash
  lspci -nnk -s 01:00.0
  ls -l /dev/dri/
  ```
* Passing GPU render node to LXC:
  - Add to `/etc/pve/lxc/<vmid>.conf`:
    ```text
    lxc.cgroup2.devices.allow: c 226:* rwm
    lxc.mount.entry: /dev/dri/renderD128 dev/dri/renderD128 none bind,optional,create=file
    ```
