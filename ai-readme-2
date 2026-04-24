Here is a concise picture of **autobuild**.

## What it is

**autobuild** is a personal **homelab automation** repo: mostly a **GNU Makefile** plus **cloud-init templates** that build **Ubuntu KVM/libvirt guests** from official **cloud images**, with optional **Ansible** registration. There is almost no application code; the “logic” lives in Make targets, `sed`, and file layout.

## How a VM is created (main flow)

1. **`distro`** — A small catalog of Ubuntu releases (e.g. `noble`, `jammy`, `resolute`). Each line is: label, version hint, image URL, filename. The Makefile picks `DISTRO` and uses `wget` to populate `/var/lib/kvmbld/sources/...`.

2. **`sources` → `base` → `image` / `rootfs`** — The downloaded qcow2 is copied into a **shared base** under `/var/lib/kvmbld/base/<distro>/`. Each VM gets its own **`rootfs.qcow2` as a qcow2 overlay** on that base (`qemu-img create ... -b ...`), so many VMs can share one backing image.

3. **Extra disks** — Optional **swap**, **data** (under `/data/virt/<shortname>/`), **db**, **dblog**, **web/docroot** qcow2s are created when the corresponding size variables are non-zero.

4. **`role` → `user-data`** — Cloud-init **`user-data`** is assembled by copying `user-data-dir/<DISTRO>/user-data.tmpl` and **splicing in role-specific fragments** at placeholder lines (`#PACKAGES`, `#BOOTCMD`, `#MOUNTS`, `#RUNCMD`, `#APT`) from:
   - `packages-dir/<DISTRO>/packages-<ROLE>`
   - `bootcmd-dir/...`, `mounts-dir/...`, `runcmd-dir/...`, `apt-dir/...`

   So **`ROLE=general`**, **`ROLE=docker`**, etc. pick different package lists and first-boot scripts per distro.

5. **`network-config`** — From `network-config/<DISTRO>/` templates, either **static** (IP from `getent hosts <shortname>` — hence the README’s **/etc/hosts** requirement) or **DHCP**.

6. **`meta-data`** — Written under the per-VM image dir: instance id, **role**, **env**, hostname, and your **`~/.ssh/id_rsa.pub`**. It also copies the generated **`user-data`** next to it for `virt-install`.

7. **`node` target** — Runs **`virt-import`** with **`virt-install`**, attaching root (+ optional disks) and passing **`--cloud-init`** paths for meta-data, user-data, and network-config. Then it **appends an Ansible inventory line** on the host, **syncs inventory** to an `ansible@ansible` server, runs **`sshreset`**, starts the VM, and creates a **`fresh`** snapshot.

Other notable targets: **`Delete`** (destroy VM, remove snapshots, undefine, clean pools/dirs, trim Ansible + sshreset), **`backup`** / **`live-backup`**, **`snapshot`**.

## Directory roles (mental model)

| Area | Role |
|------|------|
| `Makefile` | Orchestration, paths, virt-install/virsh, Ansible hooks |
| `distro` | Image URL catalog |
| `user-data-dir/`, `runcmd-dir/`, `packages-dir/`, … | Per-distro + per-role cloud-init pieces |
| `network-config/` | Netplan-style cloud-init network templates |
| `tools/Makefile` | **Separate** TLS/cert steps (`certtool`, CA/server keys) — not the VM builder |

## Root-level YAML files

`user-data.yaml`, `network-config.yaml`, and `meta-data.yaml` at the repo root look like **standalone cloud-init examples** (or leftovers). The **Makefile-driven path** builds **`network-config` and `meta-data` under `$(IMGDIR)/$(SNAME)/`**, not from those root files.

## Host assumptions (from `README.md` + Makefile)

KVM/libvirt, **`br0`**, writable **`/data`** and **`/var/lib/kvmbld`**, static IP workflow tied to **`getent hosts`**, full **libvirt** + **`virt-install`**. Defaults are tuned for a specific machine (RAM, vCPUs, `DOMAIN`, Ansible server).

---

**In one sentence:** autobuild is a **Make + cloud-init + qcow2 overlay** pipeline that downloads Ubuntu cloud images, stitches role-specific first-boot config, and **`virt-install`s** KVM guests with optional disks and **Ansible inventory** integration.
