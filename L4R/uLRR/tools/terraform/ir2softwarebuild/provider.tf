terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.66.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "=4.0.4"
    }

    random = {
      source  = "hashicorp/random"
      version = "3.5.1"
    }

    local = {
      source  = "hashicorp/local"
      version = "2.4.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "cs00056-we-ir2generic-rg"
    storage_account_name = "terraformstateir2st"
    container_name       = "ir2softwarebuildtfstatefile"
    key                  = "terraform.tfstate"
  }
}


provider "azurerm" {
  features {
    virtual_machine {
      delete_os_disk_on_deletion     = true
      skip_shutdown_and_force_delete = true
    }
    key_vault {
      purge_soft_delete_on_destroy    = true
      recover_soft_deleted_key_vaults = true
    }
  }

}