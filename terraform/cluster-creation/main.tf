# Terraform providers config

terraform {
  required_version = ">=1.3.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }

  backend "azurerm" {
    resource_group_name = "tf-backend-rg"
    storage_account_name = "tfdevopsstorage"
    container_name = "tfstate"
    key = "cluster-creation.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "terraform_remote_state" "infra" {
  backend = "azurerm"

  config = {
    resource_group_name = "tf-backend-rg"
    storage_account_name = "tfdevopsstorage"
    container_name = "tfstate"
    key = "vm-provision.terraform.tfstate"
  }
  
}

# network module
module "network" {
  source      = "./modules/network"
  rg_name = data.terraform_remote_state.infra.outputs.rg_name
  nsg_name = data.terraform_remote_state.infra.outputs.nsg_name

}

# vm module
module "vm" {
  source               = "./modules/vm"
  vm_ip                = data.terraform_remote_state.infra.outputs.vm_public_ip
  ssh_private_key      = data.terraform_remote_state.infra.outputs.ssh_private_key
}
