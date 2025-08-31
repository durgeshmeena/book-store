# Terraform providers config

terraform {
  required_version = ">=1.3.0"
  required_providers {
    azapi = {
      source  = "azure/azapi"
      version = "~>1.5"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3.0"
    }
  }

  backend "azurerm" {
    resource_group_name = "tf-devops-rg"
    storage_account_name = "tfdevopsstorage"
    container_name = "tfstate"
    key = "vm-provision.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

provider "azapi" {
}

# azure resource group
resource "azurerm_resource_group" "rg" {
  name     = var.rg_name
  location = var.rg_location
}

# network module
module "network" {
  source      = "./modules/network"
  rg_name     = azurerm_resource_group.rg.name
  rg_location = azurerm_resource_group.rg.location
  vnet_name   = var.vnet_name
  subnet_name = var.subnet_name
  nsg_name    = var.nsg_name

}

# vm module
module "vm" {
  source               = "./modules/vm"
  rg_name              = azurerm_resource_group.rg.name
  rg_location          = azurerm_resource_group.rg.location
  rg_id                = azurerm_resource_group.rg.id
  subnet_id            = module.network.subnet_id
  nsg_id               = module.network.nsg_id
  vm_name              = var.vm_name
  admin_username       = var.admin_username
}
