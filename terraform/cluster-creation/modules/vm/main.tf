
# execute bash script
resource "null_resource" "setup_kind_cluster" {

  triggers = {
    always_run = timestamp()
  }

  provisioner "file" {
    source      = "../../scripts/cluster_setup.sh"
    destination = "/tmp/cluster_setup.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/cluster_setup.sh",
      "bash /tmp/cluster_setup.sh ${var.vm_ip}"
    ] 
  }

  connection {
    type        = "ssh"
    host       = var.vm_ip
    user       = var.admin_username
    private_key = var.ssh_private_key
  }
}

# store ssh private key
resource "local_file" "ssh_private_key" {

  content  = var.ssh_private_key
  filename = "${path.module}/id_rsa"
  file_permission = "0600"
}

# fetch kubeconfig
resource "null_resource" "fetch_kubeconfig" {
  depends_on = [ null_resource.setup_kind_cluster ]

  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "scp -O -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -i ${local_file.ssh_private_key.filename} ${var.admin_username}@${var.vm_ip}:/home/${var.admin_username}/.kube/azure-public-kubeconfig ${path.module}/../../azure-kubeconfig && rm ${path.module}/id_rsa"
  }

}

# save kubeconfig to terraform output
output "kubeconfig" {
  value     = file("${path.module}/../../azure-kubeconfig")
  sensitive = true
}