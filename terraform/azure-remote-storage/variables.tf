variable "rg_name" {
  default = "tf-backend-rg"
}

variable "rg_location" {
  default = "centralindia"
}

variable "storage_account_name" {
  default     = "tfdevopsstorage"
  description = "Storage account name"
}

variable "container_name" {
  default     = "tfstate"
  description = "Storage container name"

}