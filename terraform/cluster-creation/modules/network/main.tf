terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

# allow 6443
resource "azurerm_network_security_rule" "kube_api" {
  name                        = "Allow-Kube-API"
  priority                    = 1004
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = 6443
  source_address_prefix      = "*"
  destination_address_prefix = "*"
  resource_group_name = var.rg_name
  network_security_group_name = var.nsg_name
}


# allow port 80
resource "azurerm_network_security_rule" "http" {
  name                        = "Allow-HTTP"
  priority                    = 1005
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = 80
  source_address_prefix      = "*"
  destination_address_prefix = "*"
  resource_group_name = var.rg_name
  network_security_group_name = var.nsg_name
}

# allow port 443
resource "azurerm_network_security_rule" "https" {
  name                        = "Allow-HTTPS"
  priority                    = 1006
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = 443
  source_address_prefix      = "*"
  destination_address_prefix = "*"
  resource_group_name = var.rg_name
  network_security_group_name = var.nsg_name
}