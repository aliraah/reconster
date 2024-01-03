# reconster

# reconster
Following script starts in the `/root/recon` directory. For each folder inside `/recon` the following tasks are repeated: 

- if a file named `wildcard` exists, the program name is set to the name of the directory
- subdomain enumeration via `subfinder` with the `wildcard` file as input
- piping subdomain into `dnsx` for DNS resolution
- saving unique results in a text file: `resolved_subdomains.txt`
- finding live subdomains via `httpx` and saving results as `live_subdomains.txt`
- further digging with `httpx` to find more details on each host (status code, page title, web server etc.) → results: `httpx.txt`
- separating live hosts based on their status code:
    - 200 OK → `200_subs.txt`
    - 403 Forbidden → `403_subs.txt`
    - 404 Not Found → `404_subs.txt`
- reuesting the body of each live host (status 200) using @tomnomnom's `fff` and saving the respons under a `roots` folder for futher digging
- piping `httpx.txt` into `cut` & `sed` to clean the formatting, then pinging each host -> `pinged.tmp`
- using `grep`, `cut`, and `sed` to clean and filter unwanted results -> `pinged_ips.tmp`
- checking to see which IPs are behind a WAF or a CDN via `cdncheck` ->  `waf-cdn.txt`
- finally using `comm` to get rid of IPs behind a WAF/CDN, leaving us with IPs we can directly hit -> `direct_ips.txt`
 
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

                        cat "${dir}/httpx.txt" | cut -d " " -f 1 | sed 's,http://,,' | sed 's,https://,,' | xargs -I{} ping -t 2 -c 4 {} | anew "${dir}/pinged.tmp"
                        cat "${dir}/pinged.tmp" | grep PING | cut -d " " -f 3 | sed 's,(,,' | sed 's,),,' | anew "${dir}/pinged_ips.tmp"
                        cdncheck -i "${dir}/pinged_ips.tmp" -waf -cdn | anew "${dir}/waf-cdn.txt"
                        comm -23 <(sort "${dir}/pinged_ips.tmp") <(sort "${dir}/waf-cdn.txt") | anew "${dir}/direct_ips.txt"
                        rm "${dir}/*.tmp"

                else
                        programName=$(basename "$dir")
                        echo "No wildcard found for $programName!"
                fi
        done
else
        echo "Directory '$baseDir' does not exist."
fi
```

<br>
<br>
