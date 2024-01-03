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
- reuesting the body of each live host (status 200) using @tomnomnom's `fff` and saving the respons under a `roots` folder for futher digging
 
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

<br>
<br>
#################TO-BE-INTEGRATED-LATER################ <br>
<br>

piping `httpx.txt` into `cut` & `sed` to clean the formatting, then pinging each host and saving the result as `pinged.txt`

using `grep`, `cut`, and `sed` to clean and filter the results we want, saving as `pinged_ips.txt`

use `cdncheck` to check which of these IPs are behind a CDN or WAF 

finally using `comm` to sort and compare the 2 text files (one with all the IPs and one with IPs behind CDN or WF) ,extracting those from the list of all IPs, and we are left with IPs we can directly hit

```
cat httpx.txt | cut -d " " -f 1 | sed 's,http://,,' | sed 's,https://,,' | xargs -I{} ping -t 2 -c 4 {} | anew pinged.txt

cat pinged.txt | grep PING | cut -d " " -f 3 | sed 's,(,,' | sed 's,),,' | anew pinged_ips.txt

cdncheck -i pinged_ips.txt -waf -cdn -o cdncheck-waf-cdn

comm -23 <(sort pinged_ips.txt) <(sort cdncheck-waf-cdn) | grep -P '\d+\.\d+\.\d+\.\d+'
```
