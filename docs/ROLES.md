# Roles (`ROLE`)

`ROLE` picks cloud-init fragments under `packages-dir`, `bootcmd-dir`, `mounts-dir`, `runcmd-dir`, and `apt-dir` for the chosen **`DISTRO`**. If a file is missing for a distro/role pair, the `role` target fails when `sed` tries to read it.

## Role names in the tree

These role keys appear as `packages-<ROLE>` files (some only on specific distros):

| Role | Typical purpose |
|------|------------------|
| `general` | Baseline server packages; default `ROLE` |
| `ansible` | Ansible control/target tooling |
| `apache` | Apache web stack |
| `docker` | Docker CE and related packages |
| `dockldap` | Docker + LDAP-oriented setup |
| `gitlab` | GitLab dependencies |
| `gitolite` | Gitolite git hosting |
| `gitserver` | Generic git server packages |
| `gluster` | GlusterFS client/server pieces |
| `jenkins` | Jenkins CI |
| `qemu` | QEMU/KVM build helpers |
| `libvirt` | **noble / resolute**: nested virt, NFS, monitoring—KVM hypervisor guest |
| `389ds` | Directory Server (noble) |
| `plain` | Minimal variant (noble) |

Always confirm files exist for your `DISTRO`:

```bash
ls packages-dir/noble/packages-*
```

## Desktop and web UIs

`autobuild_gui.py` and `web-ui/public/index.html` expose a fixed list (no `libvirt` or `389ds` in the dropdown yet). Use the CLI for newer roles:

```bash
make -e NAME=kvm01.example.com ROLE=libvirt node
```

## Adding a role

1. Add `packages-dir/<DISTRO>/packages-<newrole>` (YAML `packages:` list).
2. Add matching `bootcmd-`, `mounts-`, `runcmd-`, and `apt-` templates where needed (copy from `general` or closest role).
3. Test with `make -e NAME=test.<domain> ROLE=<newrole> stats` then `node`.
