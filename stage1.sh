#!/bin/bash

baseDir="/root/recon"
# Pompt user for domain input
read -p "Enter root domain: " root_domain

read -p "Enter organization name: " org_name

if [ ! -d "${baseDir}/${org_name}" ]; then
        mkdir ${baseDir}/${org_name}
        echo "Created directory: '$org_name'"
        echo ${root_domain} > "${baseDir}/${org_name}/rootdomain.txt"
else
        echo "'$org_name' already exists."
        echo "Finding subdomains..."
fi
./stage2.sh "${baseDir}/${org_name}" $org_nam