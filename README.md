# Autobuild

Makefile-driven automation for **Ubuntu KVM/libvirt** guests: download official cloud images, build **qcow2** disks (shared backing store + per-VM overlays), assemble **cloud-init** from role-specific fragments, and provision with **`virt-install --import`**. Optional **Ansible** inventory registration and post-install snapshots.

Presentation: [autobuild-presentation-1.pdf](presentation/autobuild-presentation-1.pdf)

Deeper technical notes: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) · Role matrix: [docs/ROLES.md](docs/ROLES.md)

## Features

- **Secured SSH access**: cloud-init creates a group derived from the VM FQDN; only listed user accounts in that group can log in.[^1]
- **Role-based first boot**: `ROLE` selects package lists and `bootcmd` / `mounts` / `runcmd` / `apt` fragments per distro (e.g. `docker`, `jenkins`, `libvirt`).
- **Disk layout**: root (overlay on a shared base image), optional swap, data, DB, dblog, and web docroot disks.
- **Networking**: static (IP from `getent hosts <shortname>`) or DHCP templates under `network-config/`.
- **Ansible**: appends the host under `[virt]` in `/etc/ansible/hosts`, syncs to `ansible@ansible`, runs `sshreset` (disable with `ANSIBLE=false`).
- **Snapshots**: `fresh` snapshot after `make node`; additional snapshots via `make snapshot`.
- **Proxy**: `PROXY=true` (default) uses proxy-specific apt/user-data templates; set `PROXY=none` to disable.
- **UIs**: PyQt5 desktop GUI (`make gui`) and Node/Express web UI (`make web-ui-server`).

[^1]: Corrals users compared to unrestricted AD-backed host login.

## WSL2 vs libvirt host

Provisioning requires **KVM, libvirt, and `virt-install` on the hypervisor**, not inside WSL alone. For WSL-oriented workflow and paths, use the **`wsl` branch** when working from WSL2:

```bash
git checkout wsl   # when developing or syncing from WSL; use main on the libvirt host
```

Day-to-day builds and `make node` should run on the **Ubuntu/Kubuntu libvirt host** (bridge `br0`, `qemu:///system`).

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| Host OS | Ubuntu/Kubuntu (tested with **noble** / 24.04+) |
| KVM / libvirt | Installed, user in `libvirt` group; `virsh` / `virt-install` on `PATH` |
| Bridge | **`br0`** attached to guest networking |
| Storage | Writable **`VARDIR`** and **`DATADIR`** (see below) |
| DNS / hosts | For **`NET=static`**, short hostname must resolve (`getent hosts <shortname>`) |
| Ansible (optional) | Local `/etc/ansible/hosts`, SSH to `ansible@ansible` |
| SSH key | `~/.ssh/id_rsa.pub` injected into meta-data |
| `pubkeys/keys` | Referenced when assembling `user-data` (not in git; create locally) |

### Default storage paths (Makefile)

| Variable | Default | Purpose |
|----------|---------|---------|
| `VARDIR` | `/var/lib/libvirt` | sources, base images, per-VM disks under `images/` |
| `DATADIR` | `/var/lib/libvirt/data` | optional `/data`-style data disks |
| `ETCDIR` | `/etc/kvmbld` | host-side metadata (if used) |

Older docs referred to `/var/lib/kvmbld` and `/data/virt`; overrides are supported via `make -e VARDIR=... DATADIR=...`.

## Repository layout

| Path | Purpose |
|------|---------|
| `Makefile` | Targets, defaults, virt-install, Ansible hooks |
| `distro` | Distro name → cloud image URL and filename |
| `user-data-dir/` | Base cloud-config templates per release |
| `packages-dir/`, `bootcmd-dir/`, `mounts-dir/`, `runcmd-dir/`, `apt-dir/` | Per-distro, per-`ROLE` fragments |
| `network-config/` | Static and DHCP network templates |
| `bin/`, `tools/` | Backup helpers, TLS tooling (`tools/Makefile`) |
| `autobuild_gui.py`, `gui.py` | Qt management GUIs |
| `web-ui/` | Browser UI (Express + static frontend) |
| `update-ansible` | Insert FQDN into `[virt]` inventory |
| Root `gluster-*`, `ha-*`, `clear-cluster` | Gluster / HA helper scripts (manual ops) |

Root-level `user-data.yaml`, `network-config.yaml`, and `meta-data.yaml` are **examples**; the Makefile writes authoritative files under `$(IMGDIR)/$(SNAME)/`.

## Key variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NAME` | *(required)* | VM FQDN (short name = libvirt domain) |
| `DISTRO` | `noble` | Key from `distro` (`jammy`, `resolute`, `noblearm`, …) |
| `ROLE` | `general` | Configuration profile; see [docs/ROLES.md](docs/ROLES.md) |
| `ENV` | `dev` | Stored in meta-data as `aenv` |
| `RAM` | `8192` | MiB |
| `VCPUS` | `4` | vCPU count |
| `ROOTSIZE` | `16` | Root disk GiB (0 = no resize) |
| `SWAPSIZE` | `8` | Swap GiB (0 = no swap disk) |
| `DATASIZE` | `16` | Data disk GiB (0 = skip) |
| `DBSIZE`, `DBLOGSIZE`, `WEBSIZE` | `0` | Optional extra disks |
| `NET` | `static` | `static` or `dhcp` |
| `PROXY` | `true` | `true` or `none` |
| `ANSIBLE` | `true` | `true` or `false` |
| `OS-VARIANT` | `ubuntu25.04` | Passed to `virt-install` |

Run `make stats NAME=host.example.com` to print resolved URLs, IP, and paths.

## Usage

### Command line

```bash
# Overview
make help

# Create a node (NAME required)
make -e NAME=node01.tsand.org ROLE=docker node

# Destroy VM, storage, pools, Ansible line, image dir
make -e NAME=node01.tsand.org Delete

# List image directories
make list

# Snapshot (Makefile target)
make -e NAME=node01.tsand.org snapshot

# Offline backup (shutdown, tar qcow2 + XML)
make -e NAME=node01.tsand.org backup
make -e NAME=node01.tsand.org restore

# Live disk backup via libvirt
make -e NAME=node01.tsand.org live-backup

# LibreBooking playbooks on host (Ansible limit = FQDN)
make -e NAME=node01.tsand.org librebooking
```

### Desktop GUI

```bash
make gui
```

See [GUI_README.md](GUI_README.md).

### Web UI

```bash
make web-ui-server   # npm install if needed; starts via pm2 on port 3000
```

See [web-ui/README.md](web-ui/README.md). Run on the **same host** as libvirt/Makefile.

## Build pipeline (summary)

1. **sources** — `wget` cloud image into `$(SRCDIR)/$(DISTRO)/`.
2. **base** — copy to shared `$(BASEDIR)/$(DISTRO)/rootfs.qcow2`.
3. **image** — per-VM root qcow2 overlay + optional `qemu-img resize`.
4. **role** — splice fragments into `user-data` (`#PACKAGES`, `#BOOTCMD`, `#MOUNTS`, `#RUNCMD`, `#APT`, `#SSHKEYS`).
5. **disks** — optional swap, data, db, dblog, docroot images.
6. **network-config** / **meta-data** — cloud-init networking and instance metadata.
7. **node** — `virt-install`, Ansible registration, `virsh start`, `fresh` snapshot.

Full detail: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Distros (`distro` file)

| Name | Ubuntu | Notes |
|------|--------|--------|
| `noble`, `noblemin`, `noblearm` | 24.04 | Default build: `noble` amd64 |
| `jammy`, `jammymin` | 22.04 | |
| `focal`, `focalmin` | 20.04 | |
| `bionic`, `bionicmin` | 18.04 | |
| `resolute` | 26.04 | Pre-release cloud image |
| `xenial`, `cosmic` | Legacy | |

The `noblemin` row in `distro` omits the fourth `;filename` field; use the explicit filename from the URL if you rely on that row.

## Security

Templates and generated `user-data` may contain **password hashes, proxy URLs, and SSH keys**. Treat the repo and build host as sensitive. `.auth.json` (GUI) and `pubkeys/` are local-only artifacts.
