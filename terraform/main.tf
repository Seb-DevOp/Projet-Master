terraform {
  backend "gcs" {
    bucket  = "terraform-state-iotweather"
    prefix  = "vm/iotweather"
  }
}
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_compute_network" "vpc_network" {
  name = "vpc-ci-cd-projet-master"  # change le nom
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "subnet-ci-cd-projet-master" # <- nom différent
  region        = var.region
  network       = google_compute_network.vpc_network.id
  ip_cidr_range = "10.0.0.0/24"
}

resource "google_compute_address" "public_ip" {
  name   = "ci-cd-ip-projet-master"  # change le nom
  region = var.region
}

resource "google_compute_firewall" "default" {
  name    = "allow-ssh-http-projet-master" # <- nom différent
  network = google_compute_network.vpc_network.id

  allow {
    protocol = "tcp"
    ports    = ["22", "80"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_instance" "vm" {
  name         = "ci-cd-vm-projet-master"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network.id
    subnetwork = google_compute_subnetwork.subnet.id

    access_config {
      nat_ip = google_compute_address.public_ip.address
    }
  }

metadata = {
  ssh-keys = "${var.admin_username}:${var.public_ssh_key}"
}

  tags = ["http-server", "https-server"]

  
}

output "public_ip" {
  value = google_compute_address.public_ip.address
}
