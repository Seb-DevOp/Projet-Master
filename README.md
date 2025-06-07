# Projet-Master
# 🚀 Déploiement via GitHub + GCP

Ce projet a pour but de déployer une infrastructure ou un service en utilisant **Google Cloud Platform (GCP)** avec une configuration automatisée via **GitHub Actions**.

---

## 🧾 Prérequis

- Un compte **GitHub**
- Un compte **Google Cloud Platform** (GCP)
- Accès à une **machine Linux ou WSL**
- Un éditeur de code (VS Code recommandé)

---

## ☁️ Étape 1 — Créer un compte GCP

1. Aller sur [https://cloud.google.com/](https://cloud.google.com/)
2. Créer un compte GCP ou se connecter avec Google.
3. Profiter du **crédit gratuit de 300$** offert pour les nouveaux utilisateurs.

---

## 🔑 Étape 2 — Créer un compte de service GCP

1. Accéder à la console GCP : [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Aller dans **IAM & Admin > Comptes de service**
3. Créer un **nouveau compte de service**
   - Rôle : `Owner` ou un rôle personnalisé suffisant
4. Une fois le compte créé :
   - Cliquer sur "Clés" → "Ajouter une clé" → **Format JSON**
   - Télécharger et conserver ce fichier JSON **précieusement**

---

## 🔐 Étape 3 — Injecter la clé JSON dans GitHub

1. Aller dans le dépôt GitHub → **Settings** > **Secrets and variables** > **Actions**
2. Cliquer sur `New repository secret`
3. Ajouter un secret :
   - **Name** : `GCP_CREDENTIALS`
   - **Value** : Contenu **complet** du fichier JSON (copier/coller)

---

## 🗝️ Étape 4 — Générer une clé SSH

Sur ton terminal Linux ou WSL :

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
Clé privée : ~/.ssh/id_rsa
Clé publique : ~/.ssh/id_rsa.pub

---

## 🔐 Étape 5 — Ajouter la clé publique dans GitHub
Ouvre le fichier ~/.ssh/id_rsa.pub dans un éditeur de texte.

Va dans ton dépôt GitHub → Settings → Secrets and variables → Actions

Clique sur "New repository secret"

Ajoute un secret :

Name : SSH_PUBLIC_KEY

Value : colle le contenu de id_rsa.pub

## 🔐 Étape 6 — Connexion SSH (facultatif)
Une fois que ton infrastructure est déployée (via GCP, Terraform, ou autre), tu pourras te connecter au serveur distant avec :

ssh -i ~/.ssh/id_rsa utilisateur@adresse_ip_du_serveur

# Fonctionnement des push

La prod ce deplois à chaque push sur le main
La Non prod ce deplois à chaque push sur le Develop