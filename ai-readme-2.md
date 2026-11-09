# AI / assistant orientation

**Canonical docs** (kept in sync with the tree):

- [README.md](README.md) — setup, variables, usage
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — Make pipeline, paths, UIs
- [docs/ROLES.md](docs/ROLES.md) — `ROLE` names and distro coverage

## Quick facts

- **Primary artifact**: root `Makefile` + `distro` + `*-dir/` template trees.
- **Storage defaults**: `VARDIR=/var/lib/libvirt`, `DATADIR=/var/lib/libvirt/data` (not `/var/lib/kvmbld`).
- **Provision**: `make -e NAME=fqdn ROLE=… node` on the libvirt host.
- **WSL**: use branch `wsl` for WSL-side work; build VMs on the KVM host (`main` on hypervisor).
- **Sensitive**: `pubkeys/keys`, proxy/password templates, GUI `.auth.json`.
- **`setup` file**: not an installer—captured bulk output.

When editing behavior, read the matching `packages-*`, `bootcmd-*`, and `runcmd-*` files for the `DISTRO`/`ROLE` pair before changing the Makefile.
