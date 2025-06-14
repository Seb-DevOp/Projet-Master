terraform {
  backend "gcs" {
    bucket = "bucket_projet_master_dev"
    prefix = "vm/projet"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Réseau VPC personnalisé
resource "google_compute_network" "vpc_network" {
  name                    = "vpc-ci-cd-projet-master-dev"
  auto_create_subnetworks = false
}

# Sous-réseau
resource "google_compute_subnetwork" "subnet" {
  name          = "subnet-ci-cd-projet-master-dev"
  region        = var.region
  network       = google_compute_network.vpc_network.id
  ip_cidr_range = "10.0.0.0/24"
}

# Adresse IP publique
resource "google_compute_address" "public_ip" {
  name   = "ci-cd-ip-projet-master-dev"
  region = var.region
}

# Règle de firewall : SSH, HTTP, HTTPS
resource "google_compute_firewall" "default" {
  name    = "allow-ssh-http-projet-master-dev"
  network = google_compute_network.vpc_network.id

  allow {
    protocol = "tcp"
    ports    = ["22", "443", "8080"]
  }

  source_ranges = ["87.89.182.243/32", "79.174.192.82/32", "0.0.0.0/0"]
}

# Disque de données séparé
resource "google_compute_disk" "data_disk" {
  name  = "ci-cd-data-disk-dev"
  type  = "pd-standard"
  zone  = var.zone
  size  = 15 # Disque DATA de 15GB
}

# Machine virtuelle avec script de démarrage
resource "google_compute_instance" "vm" {
  name         = "ci-cd-vm-projet-master-dev"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      size  = 10 # Disque OS de 10GB
    }
  }

  attached_disk {
    source      = google_compute_disk.data_disk.id
    device_name = "data-disk"
  }

  network_interface {
    network    = google_compute_network.vpc_network.id
    subnetwork = google_compute_subnetwork.subnet.id

    access_config {
      nat_ip = google_compute_address.public_ip.address
    }
  }

  # Ajout de la clé SSH dans les métadonnées
  metadata = {
    ssh-keys = "${var.admin_username}:${var.public_ssh_key}"
  }

metadata_startup_script = <<EOT
#!/bin/bash

# Mise à jour fstab
cat <<EOF > /etc/fstab
LABEL=cloudimg-rootfs   /        ext4   defaults        0 1
LABEL=UEFI      /boot/efi       vfat    umask=0077      0 1
/dev/lab_vg/lv_opt  /opt  ext4  defaults  0 0
/dev/lab_vg/lv_var  /var  ext4  defaults  0 0
EOF

mount -a

echo "==== Début du startup-script ====" >> /var/log/startup-script.log

# Installation des paquets nécessaires
apt-get update >> /var/log/startup-script.log 2>&1
apt-get install -y docker.io docker-compose git >> /var/log/startup-script.log 2>&1

# Ajout de l'utilisateur ubuntu au groupe docker
usermod -aG docker ubuntu

# Activation et démarrage du service docker
systemctl enable docker
systemctl start docker

# Création du dossier monitoring et docker-compose.yml pour Jenkins
mkdir -p /home/ubuntu/monitoring
cd /home/ubuntu/monitoring

cat <<EOF > docker-compose.yml
version: '3'
services:
  jenkins:
    build: .
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home

volumes:
  jenkins_home:
EOF

# Lancement de Jenkins via docker-compose
docker-compose up -d >> /var/log/startup-script.log 2>&1

echo "==== Fin du startup-script ====" >> /var/log/startup-script.log

EOT


  tags = ["http-server", "https-server"]
}

# Affichage de l'adresse IP publique
output "vm_ip" {
  value = google_compute_address.public_ip.address
}
