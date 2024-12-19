locals {
  vm_size_small = {
    type = "Standard_D4s_v3",
    disk = "99"
  }

  vm_size_medium = {
    type = "Standard_D8s_v3",
    disk = "199"
  }

  vm_size_large = {
    type = "Standard_D16s_v3",
    disk = "399"
  }

  vm_size_xxlarge = {
    type = "Standard_D48s_v3",
    disk = "1199"
  }

  image_linux         = "20_04-lts-gen2" # Maketplace Linux image
  image_linux_version = "latest"

  image_win         = "windows-software-build-image" # Custom Windows image
  image_win_version = "1.2.4"

  key_vault_user_permissions = {
    ar_terraform_builder = {
      object_id          = "50be04f3-618b-42bf-9b0e-46b5d83d03cd",
      secret_permissions = ["Backup", "Delete", "Get", "List", "Purge", "Recover", "Restore", "Set"]
    },
    janis = {
      object_id          = "8992d2a8-42b8-430b-9acd-bbe13989d30b",
      secret_permissions = ["Backup", "Delete", "Get", "List", "Purge", "Recover", "Restore", "Set"]
    },
    moritz = {
      object_id          = "f46ed0dd-3368-4900-89d9-818398c3d4f9",
      secret_permissions = ["Get", "List"]
    },
    diogo = {
      object_id          = "85a1b1ee-fc50-4be0-a360-0c78137c4753",
      secret_permissions = ["Get", "List"]
    },
    meghana = {
      object_id          = "fa3ffacc-0546-45f5-b7a0-39a5dbda3c0f",
      secret_permissions = ["Get", "List"]
    },
    sujjith = {
      object_id          = "ecbd0b9a-a822-4f30-bfbb-59d7b292e12c",
      secret_permissions = ["Get", "List"]
    },
    rui = {
      object_id          = "5d99f306-c345-4b1b-b6f4-c5259d2c6922",
      secret_permissions = ["Get", "List"]
    },
  }

  linux_vmss_ressourses = {
    "cx-lnx-l" = {
      vm_size       = local.vm_size_large.type
      vm_disk_size  = local.vm_size_large.disk
      image_name    = local.image_linux
      image_version = local.image_linux_version
    }
    "cx-lnx-m" = {
      vm_size       = local.vm_size_medium.type
      vm_disk_size  = local.vm_size_medium.disk
      image_name    = local.image_linux
      image_version = local.image_linux_version
    }
    "docu-lnx-m" = {
      vm_size       = local.vm_size_medium.type
      vm_disk_size  = local.vm_size_medium.disk
      image_name    = local.image_linux
      image_version = local.image_linux_version
    }
    "int-lnx-m" = {
      vm_size       = local.vm_size_medium.type
      vm_disk_size  = local.vm_size_medium.disk
      image_name    = local.image_linux
      image_version = local.image_linux_version
    }
    "int-lnx-xxl" = {
      vm_size       = local.vm_size_xxlarge.type
      vm_disk_size  = local.vm_size_xxlarge.disk
      image_name    = local.image_linux
      image_version = local.image_linux_version
    }
    "dev-lnx-l" = {
      vm_size       = local.vm_size_large.type
      vm_disk_size  = local.vm_size_large.disk
      image_name    = local.image_linux
      image_version = local.image_linux_version
    }
    "com-lnx-s" = {
      vm_size       = local.vm_size_small.type
      vm_disk_size  = local.vm_size_small.disk
      image_name    = local.image_linux
      image_version = local.image_linux_version
    }
  }

  win_vmss_ressourses = {
    "cx-win-l" = {
      vm_size       = local.vm_size_large.type
      vm_disk_size  = local.vm_size_large.disk
      image_name    = local.image_win
      image_version = local.image_win_version
    }
    "int-win-m" = {
      vm_size       = local.vm_size_medium.type
      vm_disk_size  = local.vm_size_medium.disk
      image_name    = local.image_win
      image_version = local.image_win_version
    }
    "dev-win-l" = {
      vm_size       = local.vm_size_large.type
      vm_disk_size  = local.vm_size_large.disk
      image_name    = local.image_win
      image_version = local.image_win_version
    }
  }

  bosch_ips_kv = [
    "209.221.240.184/32",
    "177.11.252.18/32",
    "139.15.142.49/32",
    "103.205.152.154/32",
    "194.39.218.23/32",
    "45.112.37.64/28",
    "139.15.98.128/29",
    "194.39.218.20/32",
    "209.221.240.153/32",
    "194.39.218.19/32",
    "119.40.64.9/32",
    "139.15.3.133/32",
    "119.40.69.128/30",
    "119.40.64.26/32",
    "194.39.218.13/32",
    "194.39.218.17/32",
    "103.4.125.23/32",
    "170.245.134.184/29",
    "195.11.167.73/32",
    "194.39.218.14/32",
    "45.112.38.96/28",
    "119.40.9.128/30",
    "209.221.242.192/28",
    "103.4.125.25/32",
    "194.39.218.11/32",
    "209.221.240.192/29",
    "209.221.240.196/32",
    "119.40.64.224/27",
    "103.205.152.156/32",
    "177.11.252.23/32",
    "47.88.93.169/32",
    "103.4.127.176/32",
    "103.4.125.26/32",
    "119.40.64.12/32",
    "194.39.218.12/32",
    "119.40.72.61/32",
    "208.44.45.133/32",
    "103.205.152.155/32",
    "177.11.252.56/30",
    "177.11.252.15/32",
    "194.39.218.18/32",
    "103.205.152.157/32",
    "139.15.98.0/25",
    "194.39.218.21/32",
    "209.221.240.152/32",
    "103.205.153.48/28",
    "194.39.218.22/32",
    "194.39.218.10/32",
    "202.111.0.160/28",
    "194.39.218.15/32",
    "119.40.64.15/32",
    "216.213.57.133/32",
    "103.221.241.133/32",
    "194.39.218.16/32",
    "40.74.28.0/23",
    "139.15.99.64/27"
  ]

  bosch_ips_st = [
    "209.221.240.184",
    "177.11.252.18",
    "139.15.142.49",
    "103.205.152.154",
    "194.39.218.23",
    "45.112.37.64/28",
    "139.15.98.128/29",
    "194.39.218.20",
    "209.221.240.153",
    "194.39.218.19",
    "119.40.64.9",
    "139.15.3.133",
    "119.40.69.128/30",
    "119.40.64.26",
    "194.39.218.13",
    "194.39.218.17",
    "103.4.125.23",
    "170.245.134.184/29",
    "195.11.167.73",
    "194.39.218.14",
    "45.112.38.96/28",
    "119.40.9.128/30",
    "209.221.242.192/28",
    "103.4.125.25",
    "194.39.218.11",
    "209.221.240.192/29",
    "209.221.240.196",
    "119.40.64.224/27",
    "103.205.152.156",
    "177.11.252.23",
    "47.88.93.169",
    "103.4.127.176",
    "103.4.125.26",
    "119.40.64.12",
    "194.39.218.12",
    "119.40.72.61",
    "208.44.45.133",
    "103.205.152.155",
    "177.11.252.56/30",
    "177.11.252.15",
    "194.39.218.18",
    "103.205.152.157",
    "139.15.98.0/25",
    "194.39.218.21",
    "209.221.240.152",
    "103.205.153.48/28",
    "194.39.218.22",
    "194.39.218.10",
    "202.111.0.160/28",
    "194.39.218.15",
    "119.40.64.15",
    "216.213.57.133",
    "103.221.241.133",
    "194.39.218.16",
    "139.15.99.64/27"
  ]

  bosch_ips_acr = [
    for ip in local.bosch_ips_st : {
      action   = "Allow"
      ip_range = ip
    }
  ]
}






#### IP desciption ####
# 209.221.240.184
# 177.11.252.18
# 139.15.142.49
# 103.205.152.154
# 194.39.218.23
# 45.112.37.64/28
# 139.15.98.128/29
# 194.39.218.20
# 209.221.240.153
# 194.39.218.19
# 119.40.64.9
# 139.15.3.133
# 119.40.69.128/30
# 119.40.64.26
# 194.39.218.13
# 194.39.218.17
# 103.4.125.23
# 170.245.134.184/29
# 195.11.167.73
# 194.39.218.14
# 45.112.38.96/28
# 119.40.9.128/30
# 209.221.242.192/28
# 103.4.125.25
# 194.39.218.11
# 209.221.240.192/29
# 209.221.240.196
# 119.40.64.224/27
# 103.205.152.156
# 177.11.252.23
# 47.88.93.169
# 103.4.127.176
# 103.4.125.26
# 119.40.64.12
# 194.39.218.12
# 119.40.72.61
# 208.44.45.133
# 103.205.152.155
# 177.11.252.56/30
# 177.11.252.15
# 194.39.218.18
# 103.205.152.157
# 139.15.98.0/25
# 194.39.218.21
# 209.221.240.152
# 103.205.153.48/28
# 194.39.218.22
# 194.39.218.10
# 202.111.0.160/28
# 194.39.218.15
# 119.40.64.15
# 216.213.57.133
# 103.221.241.133
# 194.39.218.16
# 40.74.28.0/23 - Azure Devops portal IP