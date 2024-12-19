################################################################################
# Data Sources - Referral existing, unmanaged resources
################################################################################

data "azurerm_client_config" "current" {
}

data "azurerm_resource_group" "ir2softwarebuild" {
  name = "cs00056-we-ir2softwarebuild-rg"
}

data "azurerm_resource_group" "bdc_location" {
  name = "cs00056-we-rg"
}

data "azurerm_resource_group" "ir2generic" {
  name = "cs00056-we-ir2generic-rg"
}

data "azurerm_virtual_network" "bdc_location" {
  name                = "cs00056-we-vnet"
  resource_group_name = data.azurerm_resource_group.bdc_location.name
}

data "azurerm_subnet" "default" {
  name                 = "DefaultSubnet"
  virtual_network_name = data.azurerm_virtual_network.bdc_location.name
  resource_group_name  = data.azurerm_resource_group.bdc_location.name
}

data "azurerm_private_dns_zone" "bdc_location" {
  name                = "cs.boschdevcloud.com"
  resource_group_name = data.azurerm_resource_group.bdc_location.name
}

data "azurerm_key_vault" "generic" {
  name                = "ir2-secrets-kv"
  resource_group_name = data.azurerm_resource_group.ir2generic.name
}


################################################################################
# Key Vault 
################################################################################

resource "azurerm_key_vault" "vmss_secrets" {
  name                = "vmss-secrets-kv"
  resource_group_name = data.azurerm_resource_group.ir2softwarebuild.name
  location            = data.azurerm_resource_group.ir2softwarebuild.location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "premium"

  network_acls {
    bypass                     = "None"
    default_action             = "Deny"
    virtual_network_subnet_ids = [data.azurerm_subnet.default.id]
    ip_rules                   = local.bosch_ips_kv
  }

  tags = {
    environment = "prod"
    managedBy   = "Terraform"
  }
}

resource "azurerm_key_vault_access_policy" "vmss_secrets" {
  for_each = local.key_vault_user_permissions

  key_vault_id       = azurerm_key_vault.vmss_secrets.id
  tenant_id          = data.azurerm_client_config.current.tenant_id
  object_id          = each.value.object_id
  secret_permissions = each.value.secret_permissions
}



################################################################################
# Storage Accounts
################################################################################

resource "azurerm_storage_account" "software_build" {
  name                     = "swbuildir2st"
  resource_group_name      = data.azurerm_resource_group.ir2softwarebuild.name
  location                 = data.azurerm_resource_group.ir2softwarebuild.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  network_rules {
    default_action             = "Deny"
    virtual_network_subnet_ids = [data.azurerm_subnet.default.id]
    ip_rules                   = local.bosch_ips_st
  }

  tags = {
    environment = "prod"
    managedBy   = "Terraform"
  }
}

resource "azurerm_storage_account" "software_build_high_secure" {
  name                     = "swbuildir2highsecurest"
  resource_group_name      = data.azurerm_resource_group.ir2softwarebuild.name
  location                 = data.azurerm_resource_group.ir2softwarebuild.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  enable_https_traffic_only       = true
  public_network_access_enabled   = false
  allow_nested_items_to_be_public = false

  network_rules {
    default_action = "Deny"
  }

  tags = {
    environment = "prod"
    managedBy   = "Terraform"
  }
}

resource "azurerm_private_endpoint" "software_build_high_secure_blob" {
  name                          = "${azurerm_storage_account.software_build_high_secure.name}-blob-pep"
  custom_network_interface_name = "${azurerm_storage_account.software_build_high_secure.name}-blob-nic"
  resource_group_name           = data.azurerm_resource_group.ir2softwarebuild.name
  location                      = data.azurerm_resource_group.ir2softwarebuild.location
  subnet_id                     = data.azurerm_subnet.default.id

  private_service_connection {
    name                           = "${azurerm_storage_account.software_build_high_secure.name}-blob-psc"
    private_connection_resource_id = azurerm_storage_account.software_build_high_secure.id
    is_manual_connection           = false
    subresource_names              = ["blob"]
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [data.azurerm_private_dns_zone.bdc_location.id]
  }

  tags = {
    environment = "prod"
    managedBy   = "Terraform"
  }
}

resource "azurerm_private_endpoint" "software_build_high_secure_file" {
  name                          = "${azurerm_storage_account.software_build_high_secure.name}-file-pep"
  custom_network_interface_name = "${azurerm_storage_account.software_build_high_secure.name}-file-nic"
  resource_group_name           = data.azurerm_resource_group.ir2softwarebuild.name
  location                      = data.azurerm_resource_group.ir2softwarebuild.location
  subnet_id                     = data.azurerm_subnet.default.id

  private_service_connection {
    name                           = "${azurerm_storage_account.software_build_high_secure.name}-file-psc"
    private_connection_resource_id = azurerm_storage_account.software_build_high_secure.id
    is_manual_connection           = false
    subresource_names              = ["file"]
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [data.azurerm_private_dns_zone.bdc_location.id]
  }

  tags = {
    environment = "prod"
    managedBy   = "Terraform"
  }
}

resource "azurerm_private_dns_a_record" "software_build_high_secure_blob" {
  name                = azurerm_private_endpoint.software_build_high_secure_blob.name
  zone_name           = data.azurerm_private_dns_zone.bdc_location.name
  resource_group_name = data.azurerm_resource_group.bdc_location.name
  ttl                 = 3600
  records             = [azurerm_private_endpoint.software_build_high_secure_blob.private_service_connection.0.private_ip_address]

}

resource "azurerm_private_dns_a_record" "software_build_high_secure_file" {
  name                = azurerm_private_endpoint.software_build_high_secure_file.name
  zone_name           = data.azurerm_private_dns_zone.bdc_location.name
  resource_group_name = data.azurerm_resource_group.bdc_location.name
  ttl                 = 3600
  records             = [azurerm_private_endpoint.software_build_high_secure_file.private_service_connection.0.private_ip_address]

}



################################################################################
# Virtual Machine Scale Sets
################################################################################

module "linux_vmss" {
  for_each = local.linux_vmss_ressourses

  source              = "./modules/linux_vmss"
  name_of_vmss        = each.key
  resource_group_name = data.azurerm_resource_group.ir2softwarebuild.name
  location            = data.azurerm_resource_group.ir2softwarebuild.location
  vm_size             = each.value.vm_size
  vm_disk_size        = each.value.vm_disk_size
  image_name          = each.value.image_name
  image_version       = each.value.image_version
  subnet_id           = data.azurerm_subnet.default.id
  key_vault_id        = azurerm_key_vault.vmss_secrets.id

  depends_on = [
    azurerm_key_vault_access_policy.vmss_secrets
  ]
}

module "win_vmss" {
  for_each = local.win_vmss_ressourses

  source              = "./modules/win_vmss"
  name_of_vmss        = each.key
  resource_group_name = data.azurerm_resource_group.ir2softwarebuild.name
  location            = data.azurerm_resource_group.ir2softwarebuild.location
  vm_size             = each.value.vm_size
  vm_disk_size        = each.value.vm_disk_size
  image_name          = each.value.image_name
  image_version       = each.value.image_version
  subnet_id           = data.azurerm_subnet.default.id
  key_vault_id        = azurerm_key_vault.vmss_secrets.id

  depends_on = [
    azurerm_key_vault_access_policy.vmss_secrets
  ]
}



################################################################################
# Shared Image
################################################################################

resource "azurerm_shared_image_gallery" "sig" {
  name                = "ir2cg"
  resource_group_name = data.azurerm_resource_group.ir2softwarebuild.name
  location            = data.azurerm_resource_group.ir2softwarebuild.location
  description         = "IR2 poject images"
}

resource "azurerm_shared_image" "windows_software_build" {
  name                = "windows-software-build-image"
  gallery_name        = azurerm_shared_image_gallery.sig.name
  resource_group_name = data.azurerm_resource_group.ir2softwarebuild.name
  location            = data.azurerm_resource_group.ir2softwarebuild.location
  os_type             = "Windows"
  hyper_v_generation  = "V2"

  identifier {
    publisher = "bosch"
    offer     = "software-build"
    sku       = "ir2-windows-10"
  }
}



################################################################################
# Azure Container Registry
################################################################################

resource "azurerm_container_registry" "acr" {
  name                   = "ir2acr"
  resource_group_name    = data.azurerm_resource_group.ir2softwarebuild.name
  location               = data.azurerm_resource_group.ir2softwarebuild.location
  sku                    = "Premium"
  admin_enabled          = false
  anonymous_pull_enabled = false

  network_rule_set {
    default_action = "Deny"

    virtual_network {
      action    = "Allow"
      subnet_id = data.azurerm_subnet.default.id
    }

    ip_rule = local.bosch_ips_acr
  }
}

# Pull user
data "azurerm_container_registry_scope_map" "pull" {
  name                    = "_repositories_pull"
  resource_group_name     = data.azurerm_resource_group.ir2softwarebuild.name
  container_registry_name = azurerm_container_registry.acr.name
}

resource "azurerm_container_registry_token" "common-pull" {
  name                    = "c3acrpll"
  container_registry_name = azurerm_container_registry.acr.name
  resource_group_name     = data.azurerm_resource_group.ir2softwarebuild.name
  scope_map_id            = data.azurerm_container_registry_scope_map.pull.id
}

resource "azurerm_container_registry_token_password" "common-pull" {
  container_registry_token_id = azurerm_container_registry_token.common-pull.id

  password1 {
    expiry = "2025-11-28T17:57:36+08:00"
  }
}

resource "azurerm_key_vault_secret" "common-pull-user" {
  name         = "${azurerm_container_registry.acr.name}-pull-user"
  value        = azurerm_container_registry_token.common-pull.name
  key_vault_id = data.azurerm_key_vault.generic.id
  content_type = "username"

  tags = {
    created_by = "terraform"
    purpose    = "to access azure container registry"
  }
}

resource "azurerm_key_vault_secret" "common-pull-password" {
  name            = "${azurerm_container_registry.acr.name}-pull-password"
  value           = azurerm_container_registry_token_password.common-pull.password1[0].value
  key_vault_id    = data.azurerm_key_vault.generic.id
  content_type    = "password"
  expiration_date = azurerm_container_registry_token_password.common-pull.password1[0].expiry

  tags = {
    created_by = "terraform"
    purpose    = "to access azure container registry"
  }

}


# Push user
data "azurerm_container_registry_scope_map" "push" {
  name                    = "_repositories_push"
  resource_group_name     = data.azurerm_resource_group.ir2softwarebuild.name
  container_registry_name = azurerm_container_registry.acr.name
}

resource "azurerm_container_registry_token" "common-push" {
  name                    = "c3acrpsh"
  container_registry_name = azurerm_container_registry.acr.name
  resource_group_name     = data.azurerm_resource_group.ir2softwarebuild.name
  scope_map_id            = data.azurerm_container_registry_scope_map.push.id
}

resource "azurerm_container_registry_token_password" "common-push" {
  container_registry_token_id = azurerm_container_registry_token.common-push.id

  password1 {
    expiry = "2025-11-28T17:57:36+08:00"
  }
}

resource "azurerm_key_vault_secret" "common-push-user" {
  name         = "${azurerm_container_registry.acr.name}-push-user"
  value        = azurerm_container_registry_token.common-push.name
  key_vault_id = data.azurerm_key_vault.generic.id
  content_type = "username"

  tags = {
    created_by = "terraform"
    purpose    = "to access azure container registry"
  }
}

resource "azurerm_key_vault_secret" "common-push-password" {
  name            = "${azurerm_container_registry.acr.name}-push-password"
  value           = azurerm_container_registry_token_password.common-push.password1[0].value
  key_vault_id    = data.azurerm_key_vault.generic.id
  content_type    = "password"
  expiration_date = azurerm_container_registry_token_password.common-push.password1[0].expiry

  tags = {
    created_by = "terraform"
    purpose    = "to access azure container registry"
  }
}