#!/bin/bash

set -e  # Exit on any error

echo "=== Step 1: Setup Deployment Directory ==="
cd deployment || { echo "Deployment directory not found!"; exit 1; }

echo "=== Step 2: Update GCP Project ID in docker-shell.sh ==="
GCP_PROJECT="<YOUR_GCP_PROJECT>" # Replace with your GCP project ID
sed -i "s/^GCP_PROJECT=.*/GCP_PROJECT=$GCP_PROJECT/" docker-shell.sh

echo "=== Step 3: Run Deployment Container ==="
sh docker-shell.sh

echo "=== Step 4: Check Tool Versions ==="
echo "Docker container is set up. Verifying tools..."
gcloud --version
ansible --version
kubectl version --client

echo "=== Step 5: Authenticate with GCP ==="
gcloud auth list

echo "=== Step 6: Configure OS Login for Service Account ==="
gcloud compute project-info add-metadata --project "$GCP_PROJECT" --metadata enable-oslogin=TRUE

echo "=== Step 7: Create SSH Key for Deployment ==="
cd /secrets || { echo "Secrets directory not found!"; exit 1; }
ssh-keygen -f ssh-key-deployment -N ""

echo "=== Step 8: Add SSH Key to GCP OS Login ==="
gcloud compute os-login ssh-keys add --key-file=/secrets/ssh-key-deployment.pub

echo "=== Step 9: Capture Username from GCP OS Login Output ==="
USERNAME=$(gcloud compute os-login ssh-keys add --key-file=/secrets/ssh-key-deployment.pub | grep "username:" | awk '{print $2}')
echo "OS Login username: $USERNAME"

echo "=== Step 10: Update Inventory Configuration ==="
cd /app || { echo "App directory not found!"; exit 1; }
sed -i "s/<YOUR_GCP_PROJECT>/$GCP_PROJECT/" inventory.yml
sed -i "s/<USERNAME>/$USERNAME/" inventory.yml

echo "=== Step 11: Build and Push Docker Containers ==="
ansible-playbook deploy-docker-images.yml -i inventory.yml

echo "=== Step 12: Create Compute Instance in GCP ==="
ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=present

echo "=== Step 13: Update Compute Instance Details in Inventory ==="
# Manual step to get the External IP of the instance from GCP Console
echo "Get the external IP address of the compute instance from GCP Console and update the appserver>hosts in inventory.yml."

read -p "Press Enter once you have updated the IP address in inventory.yml..."

echo "=== Step 14: Provision Compute Instance ==="
ansible-playbook deploy-provision-instance.yml -i inventory.yml

echo "=== Step 15: Setup Docker Containers in the Compute Instance ==="
ansible-playbook deploy-setup-containers.yml -i inventory.yml

echo "=== Step 16: Verify Docker Containers on the Instance ==="
ssh "$USERNAME"@<External-IP> << EOF
    sudo docker container ls
    sudo docker container logs api-service -f
    sudo docker container logs frontend -f
    sudo docker container logs nginx -f
EOF

echo "=== Step 17: Setup Webserver on Compute Instance ==="
ansible-playbook deploy-setup-webserver.yml -i inventory.yml

echo "=== Deployment Complete! ==="
echo "Access the web application at http://<Your IP Address>/"
