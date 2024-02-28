#!/bin/bash

baseDir="/root/recon"
scriptsDir="/root/recon/scripts"

if [[ -d "$baseDir" ]]; then
        for dir in "$baseDir"/*/; do
                if [[ -f "${dir}/rootdomain.txt" ]]; then
                        programName=$(basename "$dir")
                        echo "Gathering subs for $programName..."
                        subfinder -dL "${dir}/rootdomain.txt" -all -silent | anew -q "${dir}/all_subs.txt"
                        echo "Resolving found subdomains..."
                        dnsx -l "${dir}/all_subs.txt" -silent | anew -q "${dir}/resolved.txt"
                        echo "Gathering http metadata..."
                        httpx -l "${dir}/resolved.txt" -sc -title -ct -location -server -td -method -ip -cname -asn -cdn > "${dir}/metadata.txt"                      
                        echo "Separating subs by status code..."
                        # Using sed to remove the color output in metadata file so the grep doens't freak out later on
                        sed 's/\x1B\[[0-9;]*[JKmsu]//g' "${dir}/metadata.txt" > "${dir}/metadata.tmp"
                        grep '\[200\]' "${dir}/metadata.tmp" | cut -d " " -f 1 | cut -d "/" -f 3 > "${dir}/200.txt"
                        grep '\[301\]' "${dir}/metadata.tmp" | cut -d " " -f 1 | cut -d "/" -f 3 > "${dir}/301.txt"
                        grep '\[302\]' "${dir}/metadata.tmp" | cut -d " " -f 1 | cut -d "/" -f 3 > "${dir}/302.txt"
                        grep '\[401\]' "${dir}/metadata.tmp" | cut -d " " -f 1 | cut -d "/" -f 3 > "${dir}/401.txt"
                        grep '\[403\]' "${dir}/metadata.tmp" | cut -d " " -f 1 | cut -d "/" -f 3 > "${dir}/403.txt"
                        grep '\[404\]' "${dir}/metadata.tmp" | cut -d " " -f 1 | cut -d "/" -f 3 > "${dir}/404.txt"
                        grep '\[502\]' "${dir}/metadata.tmp" | cut -d " " -f 1 | cut -d "/" -f 3 > "${dir}/502.txt"
                        grep '\[503\]' "${dir}/metadata.tmp" | cut -d " " -f 1 | cut -d "/" -f 3 > "${dir}/503.txt"
                        cat "${dir}/metadata.tmp" | grep '\[200\]' | notify -bulk -pc "${dir}/provider-config.yaml"
                        echo "Inserting records into the database..."
                        programName=$(basename "$dir")
                        python3 "${scriptsDir}/insert.py" "${dir}/all_subs.txt" ${programName}
                        echo "Updating status codes..."
                        python3 "${scriptsDir}/update.py" "${dir}" ${programName}
                else
                        programName=$(basename "$dir")
                        echo "No root domains found for $programName!"
                fi
        done
else
        echo "Directory '$baseDir' does not exist."
fi