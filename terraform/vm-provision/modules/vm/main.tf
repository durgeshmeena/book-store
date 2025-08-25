terraform {
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
}


# public ip
resource "azurerm_public_ip" "public_ip" {
  name                = "${var.vm_name}-pip"
  location            = var.rg_location
  resource_group_name = var.rg_name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# nic
resource "azurerm_network_interface" "nic" {
  name                = "${var.vm_name}-nic"
  location            = var.rg_location
  resource_group_name = var.rg_name

  ip_configuration {
    name                          = "tf-devops-internal"
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }
}

# NSG
resource "azurerm_network_interface_security_group_association" "nic_nsg" {
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = var.nsg_id
}

# linux vm
resource "azurerm_linux_virtual_machine" "vm" {
  name                = var.vm_name
  location            = var.rg_location
  resource_group_name = var.rg_name
  size                = var.vm_size
  admin_username      = var.admin_username
  admin_ssh_key {
    username   = var.admin_username
    public_key = azapi_resource_action.ssh_public_key_gen.output.publicKey
  }

  network_interface_ids = [
    azurerm_network_interface.nic.id,
  ]

  os_disk {
    name                = "${var.vm_name}-osdisk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  provisioner "remote-exec" {
    script = "../../scripts/vm_tools.sh"

    connection {
      type        = "ssh"
      user        = var.admin_username
      private_key = azapi_resource_action.ssh_public_key_gen.output.privateKey
      host        = azurerm_public_ip.public_ip.ip_address
    }
    
  }
}