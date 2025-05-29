variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "europe-west1-b"
}

variable "admin_username" {
  description = "Username for SSH access"
  type        = string
}

variable "public_ssh_key" {
  description = "SSH public key string"
  type        = string
}