
resource "tls_private_key" "module_win_vmss" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "random_password" "module_win_vmss" {
  length      = 20
  min_lower   = 1
  min_upper   = 1
  min_numeric = 1
  min_special = 1
  special     = true
}

resource "azurerm_windows_virtual_machine_scale_set" "module_win_vmss" {
  name                 = "${var.name_of_vmss}-vmss"
  resource_group_name  = var.resource_group_name
  location             = var.location
  sku                  = var.vm_size
  instances            = 0
  admin_username       = "intadmin"
  admin_password       = random_password.module_win_vmss.result
  computer_name_prefix = var.name_of_vmss

  overprovision          = false
  single_placement_group = false


  source_image_id = "/subscriptions/8d4b9996-bcab-47fc-ab9d-e88c4e461700/resourceGroups/cs00056-we-ir2softwarebuild-rg/providers/Microsoft.Compute/galleries/ir2cg/images/${var.image_name}/versions/${var.image_version}"


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

resource "azurerm_virtual_machine_scale_set_extension" "module_win_vmss" {
  name                         = "custom-script"
  virtual_machine_scale_set_id = azurerm_windows_virtual_machine_scale_set.module_win_vmss.id
  publisher                    = "Microsoft.Compute"
  type                         = "CustomScriptExtension"
  type_handler_version         = "1.9"
  auto_upgrade_minor_version   = true
  settings = jsonencode({
    "commandToExecute" = "powershell.exe -ExecutionPolicy Unrestricted -Command \"Resize-Partition -DriveLetter 'C' -Size (Get-PartitionSupportedSize -DriveLetter 'C').SizeMax\""
  })
}

resource "azurerm_key_vault_secret" "module_win_vmss" {
  name         = "${azurerm_windows_virtual_machine_scale_set.module_win_vmss.name}-password"
  value        = random_password.module_win_vmss.result
  key_vault_id = var.key_vault_id

}