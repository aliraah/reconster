#!/bin/bash

baseDir="/root/recon"

if [[ -d "$baseDir" ]]; then
	for dir in "$baseDir"/*/; do
		if [[ -f "${dir}/wildcard" ]]; then
			programName=$(basename "$dir")
			echo "Fetching subdomains for $programName..."
			# Can integrate additional tools here like sublist3r, findomain, assetfinder etc.
			subfinder -dL "${dir}/wildcard" -all -silent | dnsx -silent | anew -q "${dir}/resolved_subdomains.txt"

			echo "Digging further for resolved subdomains..."
			cat "${dir}/resolved_subdomains.txt" | xargs -I{} dig CNAME {} | anew cnames.txt
			# Can be later checked for potenial subdomain takeovers + alert 

			echo "Fetching live hosts..."
			httpx -l "${dir}/resolved_subdomains.txt" -silent | anew "${dir}/live_subdomains.txt" 

			echo "Fetching server data..."
			httpx -l "${dir}/live_subdomains.txt" -sc -title -server -nc -silent | anew "${dir}/httpx.txt"

			echo "Seperating hosts by status code..."
			cat "${dir}/httpx.txt" | grep '\[200\]' | cut -d ' ' -f 1 | anew "${dir}/200_subs.txt" | notify -silent -bulk -pc "${dir}/notify-config.yaml"
			# Might add some fuzzing integration for 4xx hosts later
			cat "${dir}/httpx.txt" | grep '\[403\]' | cut -d ' ' -f 1 | anew "${dir}/403_subs.txt"
			cat "${dir}/httpx.txt" | grep '\[404\]' | cut -d ' ' -f 1 | anew "${dir}/404_subs.txt"

			echo "Saving live hosts bodies in the roots directory ..."
			# 200 ms delay (= max 5 requests/sec) not to trigger WAF
			cat "${dir}/200_subs.txt" | fff -d 200 -S -o "${dir}/roots"
			# Here we can use `gf` to look for interesting patters


		else
			programName=$(basename "$dir")
			echo "No wildcard found for $programName!"
		fi
	done
else
	echo "Directory '$baseDir' does not exist."
fi
