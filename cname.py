import requests, os, sys, random
'''
This is just a simple url shortener that creates a DNS CNAME record using your cloudflare domain
to the site that you send it. URL will pe passed to you and should be preceeded with a 5 digit
interger. 
'''
from routes import redirect_to
#Vars file includes API Tokens
if os.path.exists("cloudflare_vars.py"):
    pass
else:
    zone_id =input("Enter CloudFlare Zone ID: ")
    auth_bearer = input("Enter your  Authorization Bearer Token: ") 
    f = open("cloudflare_vars.py", "w+")
    f.write(f'''zone_id = "{zone_id}"\nauth_bearer = "Bearer {auth_bearer}"
    '''
    )
    f.close()
#Since i wanted this repo to be public im importing tokens
import cloudflare_vars
#check to see if site was passed as an argument, if not have the user input
if len(sys.argv) == 1:
    redir_site = input("Enter the site you would like to CNAME: ")
else:
    redir_site = sys.argv[1]

#Cloudflare DNS api GW
url = f"https://api.cloudflare.com/client/v4/zones/{cloudflare_vars.zone_id}/dns_records"
headers = {
    "Authorization":f"Bearer {cloudflare_vars.auth_bearer}",
    "Content-Type":"application/json"
}
#cname is a 5 digit pseudorandom number
cname_prefix = str(random.randint(1,99999)).zfill(5)
data = {
    "type":"CNAME",
    "name":f"{cname_prefix}",
    "content":str(redir_site),
    "ttl":"3600",
    "proxied":False,
}
response = requests.post(url, headers=headers, json=data)
resj = response.json()
#print("Status Code", response.status_code)
#print("JSON Response ", resj)
#print User their link
print(f'https://{cname_prefix}.{resj["result"]["zone_name"]}')
