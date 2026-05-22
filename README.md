# Autobuild

`autobuild` is a Makefile-driven toolkit designed to automate the creation and deployment of Ubuntu KVM virtual machines on a libvirt host. It streamlines the process of downloading cloud images, configuring disks, assembling cloud-init metadata, and provisioning VMs with specific roles. NOTICE that you must switch to branch 'wsl' from main if you are installing under wsl2.

## Features

- **Secured Accounts**: new group created to match FQDN and user-accounts must be member to ssh in.[^1]
- **Automated Provisioning**: Uses `virt-install` and `cloud-init` for "boot-and-go" VM creation.
- **Role-Based Configuration**: Tailors VMs (packages, boot commands, mounts, etc.) based on a defined `ROLE` (e.g., `docker`, `jenkins`, `gluster`).
- **Disk Management**: Automatically creates and attaches root, swap, data, database, and web document root disks.
- **Network Flexibility**: Supports both static and DHCP network configurations via templates.
- **Ansible Integration**: Automatically registers new nodes in an Ansible inventory and triggers SSH key resets.
- **Snapshots**: Automatically creates a "fresh" snapshot after the initial installation.
- **Proxy Support**: Optional proxy configuration for APT and cloud-init.

[^1]: I did this as AD user accounts offers unrestricted host login, this is a way to corral the users on a machine.

## Prerequisites

- **Host OS**: Ubuntu/Kubuntu (tested on 24.04).
- **KVM/Libvirt**: Must be installed, configured, and enabled.
- **Network Bridge**: A host bridge named `br0` is required.
- **Permissions**: Full write access to:
  - `/data` (or configured `DATADIR`)
  - `/var/lib/kvmbld` (or configured `VARDIR`)
- **DNS/Hosts**: For static IP setups, the FQDN must be resolvable (e.g., in `/etc/hosts`) so the Makefile can determine the IP address.

## Directory Structure

| Directory | Description |
| :--- | :--- |
| `user-data-dir/` | Base `cloud-config` templates per distribution. |
| `packages-dir/` | Lists of packages to install, organized by distribution and role. |
| `bootcmd-dir/` | Role-specific boot command fragments. |
| `mounts-dir/` | Role-specific mount configurations. |
| `runcmd-dir/` | Role-specific run command fragments. |
| `apt-dir/` | Role-specific APT configuration fragments. |
| `network-config/` | Templates for static and DHCP network configurations. |
| `tools/` | Supplemental scripts and tools. |

## Key Makefile Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `NAME` | (Required) | The FQDN of the VM. |
| `DISTRO` | `noble` | The Ubuntu distribution (e.g., `focal`, `jammy`, `noble`). |
| `ROLE` | `general` | The role of the VM (determines configuration fragments). |
| `ENV` | `dev` | The environment tag (e.g., `dev`, `prod`). |
| `RAM` | `4096` | RAM in MB. |
| `VCPUS` | `4` | Number of virtual CPUs. |
| `ROOTSIZE` | `32` | Root disk size in GB. |
| `SWAPSIZE` | `8` | Swap disk size in GB. |
| `DATASIZE` | `16` | Data disk size in GB. |
| `NET` | `static` | Network type (`static` or `dhcp`). |
| `PROXY` | `true` | Enable/disable proxy templates. |
| `ANSIBLE` | `true` | Enable/disable Ansible registration. |

## Usage

### GUI Interface (Recommended)

For a user-friendly experience, you can use the standalone Qt GUI. It supports authentication, real-time command output, and automatic logging.

```bash
make gui
```

See [GUI_README.md](GUI_README.md) for more details.

### Creating a Node

To create a new VM, provide the FQDN and optionally the role:

```bash
make -e NAME=node01.tsand.org ROLE=docker node
```

### Deleting a Node

This will destroy the VM, remove its storage, and clean up Ansible entries:

```bash
make -e NAME=node01.tsand.org Delete
```

### Listing Images

```bash
make list
```

### Creating a Snapshot

```bash
make -e NAME=node01.tsand.org snapshot
```

### Backup

```bash
make -e NAME=node01.tsand.org backup
```

## How it Works

1. **Sources**: Downloads the official Ubuntu cloud image if not present.
2. **Base**: Prepares a base qcow2 image from the source.
3. **Image**: Creates a node-specific root disk using the base image as a backing file and resizes it.
4. **Role**: Assembles a `user-data` file by inlining fragments from various directories based on the `ROLE` and `DISTRO`.
5. **Disks**: Creates additional disks (swap, data, etc.) as configured.
6. **Network**: Generates `network-config` and `meta-data` files.
7. **Node**: Runs `virt-install` with all prepared disks and cloud-init configurations.
8. **Finalize**: Registers the node with Ansible and starts the VM.
