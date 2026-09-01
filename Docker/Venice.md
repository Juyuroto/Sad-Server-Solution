# "Venice": Am I in a container?

**Date** : 19/06/2026
**Difficulté** : moyen

## Description

Essayez de déterminer si vous vous trouvez à l'intérieur d'un conteneur (comme un conteneur Docker par exemple) ou à l'intérieur d'une machine virtuelle (comme dans les autres scénarios).

---

## Test

```bash
hostnamectl
```

## Resultat

```bash
Static hostname: i-05b00e75c86f226f1
      Icon name: computer-vm
        Chassis: vm
     Machine ID: 859afa6d08904d52bcd3f5cfdeac5cce
        Boot ID: b7c234046c4b436c9a3ba4961cf4c4c1
 Virtualization: kvm
Operating System: Debian GNU/Linux 11 (bullseye)
         Kernel: Linux 5.10.0-14-cloud-amd64
   Architecture: x86-64
```

## Test

```bash
systemd-detect-virt
```

## Resultat

```bash
kvm
```

## Test

```bash
sudo fdisk -l
```

## Resultat

```bash
Disk /dev/nvme0n1: 8 GiB, 8589934592 bytes, 16777216 sectors
Disk model: Amazon Elastic Block Store              
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disklabel type: gpt
Disk identifier: E4AE2E10-9890-014B-8230-EFEDCE732D4C

Device           Start      End  Sectors  Size Type
/dev/nvme0n1p1  262144 16777182 16515039  7.9G Linux filesystem
/dev/nvme0n1p14   2048     8191     6144    3M BIOS boot
/dev/nvme0n1p15   8192   262143   253952  124M EFI System

Partition table entries are not in disk order.
```

## Explanation

>Nous sommes sur une VM Linux (Debian 11) hébergée sur Amazon AWS. On a un système d'exploitation complet avec son propre noyau (5.10.0-14-cloud-amd64), ce qui est impossible dans un conteneur (qui partage le noyau de l'hôte).