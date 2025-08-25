variable "rg_name" {}
variable "rg_location" {}
variable "rg_id" {}
variable "subnet_id" {}
variable "nsg_id" {}
variable "vm_name" {}
variable "vm_size" {
  default = "Standard_DC2s_v3"
}
variable "admin_username" {}