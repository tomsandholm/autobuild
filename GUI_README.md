# Autobuild Manager GUI

Standalone **PyQt5** desktop app (`autobuild_gui.py`) that runs `make node` and `make Delete` from the project root.

## Features

- **Authentication**: login gate before operations.
- **Node creation**: FQDN + role → `make node NAME=… ROLE=…`.
- **Node deletion**: confirmation before `make Delete`.
- **Console**: live stdout/stderr from Make.
- **Logging**: timestamped files under `logs/` (`autobuild_YYYYMMDD_HHMMSS.log`).

## Prerequisites

- Python 3
- PyQt5: `pip install PyQt5`
- Same host prerequisites as [README.md](README.md) (libvirt, Makefile paths, `pubkeys/keys`, etc.)

## Usage

```bash
make gui
# or
./autobuild_gui.py
```

### Authentication

On first run, creates `.auth.json` in the repo root (git-ignored) with defaults:

- **Username**: `admin`
- **Password**: `password`

Edit `.auth.json` to change credentials.

### Roles in the dropdown

`general`, `ansible`, `apache`, `docker`, `dockldap`, `gitlab`, `gitolite`, `gitserver`, `gluster`, `jenkins`, `qemu`

Roles such as **`libvirt`** and **`389ds`** are CLI-only unless added to `autobuild_gui.py`. See [docs/ROLES.md](docs/ROLES.md).

### Create / delete

1. Enter FQDN (e.g. `webserver.tsand.org`).
2. Choose role (or use CLI for others).
3. **Create Node** or **Delete Node** (confirm delete).

RAM, disk sizes, and `DISTRO` use Makefile defaults; override from the shell if needed:

```bash
make -e NAME=webserver.tsand.org ROLE=apache RAM=4096 node
```
