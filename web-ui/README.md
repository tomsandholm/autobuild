# Autobuild Web UI

Browser front end for **`make node`** and **`make Delete`**. The Express server runs from `web-ui/` but executes Make in the **parent directory** (repo root).

## Features

- Create/delete VMs by FQDN and role
- Optional RAM override (see caveat below)
- JSON API + static SPA under `public/`

## Structure

```text
web-ui/
├── server.js       # Express API
├── package.json
└── public/
    ├── index.html
    ├── script.js
    └── style.css
```

## Prerequisites

- **Node.js** and npm
- **Make**, **libvirt**, and full autobuild host setup ([README.md](../README.md))
- **`make web-ui-server`** additionally expects **pm2** globally (`npm install -g pm2`)

## Quick start

From the **autobuild repo root**:

```bash
make web-ui-server
```

This installs `node_modules` if missing and runs `pm2 start npm --name "autobuild" -- start` in `web-ui/`.

Manual run (no pm2):

```bash
cd web-ui
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000).

## API

| Method | Path | Body | Make equivalent |
|--------|------|------|-----------------|
| `POST` | `/api/node` | `{ "fqdn", "role", "ram?", "ncpu?" }` | `make node NAME=… ROLE=…` (+ optional `RAM=`) |
| `POST` | `/api/delete` | `{ "fqdn" }` | `make Delete NAME=…` |

### RAM and vCPUs

- **`ram`** in the JSON body is passed through as `RAM=…` and works.
- The UI field **NCPU** is sent as `NCPU=…`, but the Makefile variable is **`VCPUS`**, so vCPU overrides from the web UI are **ignored** until `server.js` maps `ncpu` → `VCPUS`.

### Roles

The HTML `<select>` matches the Qt GUI list. Additional roles (e.g. **`libvirt`**) work via CLI or API with a custom `role` value if fragments exist for your `DISTRO`. See [docs/ROLES.md](../docs/ROLES.md).

## Security

The server runs **`make`** with user-supplied FQDN/role and is intended for **trusted local admin use** on the hypervisor, not public exposure without authentication and hardening.
