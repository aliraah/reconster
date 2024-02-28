# Reconster
Reconster automates several steps of reconnaissance, including subdomain discovery, DNS resolution, HTTP metadata gathering, status code analysis, notification, and database updates.


## Install
```
sudo git clone https://github.com/aliraah/reconster.git && cd reconster && chmod +x *.sh
```

## Usage
1. Create a `recon` directory under `/root` 
2. Copy the scripts into `/root/recon/scripts`
3. Run `stage1.sh` and give it a target and wait for it to finish
4. Add `$PATH` and `stage3.sh` to crontab
```
echo $PATH | crontab -
```
```
echo "0 */6 * * * /root/recon/scripts/stage3.sh >> /root/recon/scripts/logfile.log 2>&1" | crontab -
```

## TODO
- Add your MongoDB connection string, collection name and timezne to `insert.py` and `update.py`
- Create a discord server with separate text channel's for each target under your recon directory
- Create a `provider-config.yaml` containing your discords web hook inside each targets folder
```
$ cat provider-config.yaml

discord:
  - id: "crawl"
    discord_channel: "hackerone"
    discord_username: "Reconster-Bot"
    discord_format: "{{data}}"
    discord_webhook_url: "WEBHOOK-HERE"
```
- Check out my medium article series on this tool:<br>
<a href="https://medium.com/@aliraah/how-do-i-automate-my-recon-part-one-fd17dc8717c8">How do I automate my recon — Part One </a><br>
<a href="https://medium.com/@aliraah/how-do-i-automate-my-recon-part-two-b39a66b4c23d">How do I automate my recon — Part Two </a>
