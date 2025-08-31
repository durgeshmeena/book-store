
output "kubeconfig" {
  value     = module.vm.kubeconfig
  sensitive = true
}
