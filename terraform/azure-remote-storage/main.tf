

terraform {
  required_version = ">=1.3.0"

  required_providers {

    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }

  }

}


provider "azurerm" {
  features {}
}

# resource group needs to be created first if this is the first tf provisioning
# skipping this since resource group is created in vm-provision
resource "azurerm_storage_account" "tfstate" {
  name                            = var.storage_account_name
  resource_group_name             = var.rg_name
  location                        = var.rg_location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  allow_nested_items_to_be_public = false

}

resource "azurerm_storage_container" "tfstate" {
  name                  = var.container_name
  storage_account_name  = azurerm_storage_account.tfstate.name
  container_access_type = "private"
}
