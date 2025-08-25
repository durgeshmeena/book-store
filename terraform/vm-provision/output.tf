output "vm_public_ip" {
  value = module.vm.public_ip
}

output "ssh_private_key" {
  value     = module.vm.ssh_private_key
  sensitive = true
}

output "ssh_public_key" {
  value = module.vm.ssh_public_key
}

# output for other project
output "rg_name" {
  value = azurerm_resource_group.rg.name 
}

output "nsg_name" {
  value = module.network.nsg_name
}
