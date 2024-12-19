variable "name_of_vmss" {
  description = "Name of the VMSS. Must be unique."
  type        = string
}

variable "resource_group_name" {
  description = "Name of the RG where the VMSS should be"
  type        = string
}

variable "location" {
  description = "Loctaion of the VMSS"
  type        = string
}

variable "vm_size" {
  description = "Size the VM should have"
  type        = string
}

variable "vm_disk_size" {
  description = "Size the VM disk should have"
  type        = string
}

variable "subnet_id" {
  description = "Subnet id of the relaled VNet"
  type        = string
}

variable "key_vault_id" {
  description = "Key vault id where the private key should be stored"
  type        = string
}

variable "image_name" {
  description = "Name of the image that should be assigned"
  type        = string
}

variable "image_version" {
  description = "Version of the image that should be assigned"
  type        = string
}