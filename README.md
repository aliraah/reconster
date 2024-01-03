# reconster

# reconster
Following script starts in the `/root/recon` directory. For each folder inside `/recon` the following tasks are repeated: 

- if a file named `wildcard`exits, the program name is set to the name of the directory
- subdomain enumeration via `subfinder` with the `wildcard` file as input
- piping subdomain into `dnsx` for DNS resolution
- saving unique results in a text file: `resolved_subdomains.txt`
- finding live subdomains via `httpx` and saving results as `live_subdomains.txt`
- further digging with `httpx` to find more details on each host (status code, page title, web server etc.) → results: `httpx.txt`
- separating live hosts based on their status code:
    - 200 OK → `200_subs.txt`
    - 403 Forbidden → `403_subs.txt`
    - 404 Not Found → `404_subs.txt`
 
```
#!/bin/bash
#recon.sh

baseDir="/root/recon"

if [[ -d "$baseDir" ]]; then
        for dir in "$baseDir"/*/; do
                if [[ -f "${dir}/wildcard" ]]; then
                        programName=$(basename "$dir")
                        echo "Recon for $programName:"
                        subfinder -dL "${dir}/wildcard" -all -silent | dnsx -silent | anew -q "${dir}/resolved_subdomains.txt"
                        httpx -l "${dir}/resolved_subdomains.txt" -silent | anew "${dir}/live_subdomains.txt"
                        echo "..."
                        httpx -l "${dir}/live_subdomains.txt" -sc -title -server -nc -silent | anew "${dir}/httpx.txt"
                        echo "Seperating hosts by status code"
                        cat "${dir}/httpx.txt" | grep '\[200\]' | cut -d ' ' -f 1 | anew "${dir}/200_subs.txt" | notify -silent -bulk -pc "${dir}/notify-config.yaml"
                        cat "${dir}/httpx.txt" | grep '\[403\]' | cut -d ' ' -f 1 | anew "${dir}/403_subs.txt"
                        cat "${dir}/httpx.txt" | grep '\[404\]' | cut -d ' ' -f 1 | anew "${dir}/404_subs.txt"

                        cat "${dir}/200_subs.txt" | fff -d 200 -S -o "${dir}/roots"

                else
                        programName=$(basename "$dir")
                        echo "No wildcard found for $programName!"
                fi
        done
else
        echo "Directory '$baseDir' does not exist."
fi
```
