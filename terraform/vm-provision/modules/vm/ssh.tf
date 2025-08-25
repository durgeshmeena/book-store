resource "random_pet" "ssh_key_name" {
  prefix    = "ssh"
  separator = ""
}

resource "azapi_resource_action" "ssh_public_key_gen" {
  type        = "Microsoft.Compute/sshPublicKeys@2022-11-01"
  resource_id = azapi_resource.ssh_public_key.id
  action      = "generateKeyPair"
  method      = "POST"

  response_export_values = ["publicKey", "privateKey"]
}

resource "azapi_resource" "ssh_public_key" {
  type      = "Microsoft.Compute/sshPublicKeys@2022-11-01"
  name      = "${var.vm_name}-ssh-key"
  location  = var.rg_location
  parent_id = var.rg_id
}

output "ssh_private_key" {
  value     = azapi_resource_action.ssh_public_key_gen.output.privateKey
  sensitive = true
}

output "ssh_public_key" {
  value = azapi_resource_action.ssh_public_key_gen.output.publicKey
}
