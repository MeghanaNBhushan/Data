data "local_file" "cloudinit" {
  filename = "${path.module}/cloud-init.yaml"
}


resource "tls_private_key" "module_linux_vmss" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "azurerm_linux_virtual_machine_scale_set" "module_linux_vmss" {
  name                 = "${var.name_of_vmss}-vmss"
  resource_group_name  = var.resource_group_name
  location             = var.location
  sku                  = var.vm_size
  instances            = 0
  admin_username       = "intadmin"
  computer_name_prefix = var.name_of_vmss

  overprovision          = false
  single_placement_group = false

  custom_data = base64encode(data.local_file.cloudinit.content)

  admin_ssh_key {
    username   = "intadmin"
    public_key = tls_private_key.module_linux_vmss.public_key_openssh
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = var.image_name
    version   = var.image_version
  }

  os_disk {
    caching              = "ReadOnly"
    storage_account_type = "Standard_LRS"
    disk_size_gb         = var.vm_disk_size

    diff_disk_settings {
      option    = "Local"
      placement = "CacheDisk"
    }
  }

  network_interface {
    name    = "${var.name_of_vmss}-nic"
    primary = true

    ip_configuration {
      name      = "internal"
      primary   = true
      subnet_id = var.subnet_id
    }
  }

  lifecycle {
    ignore_changes = [
      extension,
      tags,
      automatic_instance_repair,
      automatic_os_upgrade_policy,
      instances
    ]
  }

  boot_diagnostics {
    storage_account_uri = null
  }

  tags = {
    environment = "prod"
    managedBy   = "Terraform"
  }
}

resource "azurerm_key_vault_secret" "module_linux_vmss" {
  name         = "${azurerm_linux_virtual_machine_scale_set.module_linux_vmss.name}-private-key"
  value        = tls_private_key.module_linux_vmss.private_key_pem
  key_vault_id = var.key_vault_id

}