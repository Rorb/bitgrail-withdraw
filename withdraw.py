'''
    Hey guys, sorry the formatting sucks. I threw it together over a month ago for personal use, not public.
    
	Basic explanation:
		1. Download python (python2 to be exact) from the internet.
		2. Run the following terminal command (without quotes): "pip install requests"
		3. Save this script as a file on your computer named, for example, "withdraw.py"
		4. Open it up in notepad (or some other text editor)
		5. Ctrl-F for "EDIT_HERE" and edit the four variables below you need to change (your API key, your API secret key, how much you want to withdraw, and the wallet you want to withdraw to). Lines ~70-75.
    6. Run it using your Python executable (eg, double click it or run it through your terminal window by doing 'python <filename>')

	If you're confused about your 'API Key' part (step 5): you make an API key within your BitGrail account after you log in. Steps below:
		1. Log into your BitGrail account (2FA included)
		2. Press the 'Account' drop-down (top right corner)
		3. Select 'API KEYS' from the drop-down
		4. Press 'GENERATE NEW API PAIR' (top right corner)
		5. Toggle 'Allow Withdraw' on.
		6. Enter your password & 2FA
		7. The two items it gives you ('API key' & 'API secret') are used in step #5 above.

	REMEMBER: You can skip all code and just CTRL-F for the text "EDIT_HERE" to change the parts you need to change.

    Hope this lets you withdraw. Tips appreciated: xrb_3hihrui4s1q79qk88pwzx95eghfyxd1s1ir5uck6bbr1jrp8fsfo5theu9mc
'''

import requests
import hashlib, hmac
import time


## Supporting functions
def sign(data, secret):
    signature = hmac.new(secret, data, digestmod=hashlib.sha512).hexdigest()

    return signature

## Generic API Call
def callAPI(key, secret, api, payload=dict()):
    bitgrailURL = 'https://api.bitgrail.com/v1/%s'
    url = bitgrailURL % api

    payload['nonce'] = int(time.time() * 1000)
    
    kvFormat = '{}={}'
    payload = '&'.join([kvFormat.format(element, str(payload[element])) for element in payload.keys()])

    headers = {
        'KEY': key,
        'SIGNATURE': sign(payload, secret),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # verify=False for burp
    req = requests.post(url, payload, verify=False, headers=headers)
    try:
        return req.json()['response']
    except:
        return req.text

# Withdraw a currency to a wallet
def withdraw(key, secret, currency, amount, wallet):
    payload = {
        'coin': currency,
        'amount': amount,
        'address': wallet
    }
    return callAPI(key, secret, 'withdraw', payload)

# EDIT_HERE: The variables below (4 in total)
def main():
    key = ''                    # EDIT_HERE: Put your API key
    secret = ''                 # EDIT_HERE: Put your API secret key
    coin = 'XRB'
    amount = ''                 # EDIT_HERE: Put the amount you wish you withdraw, as a string in quotes
    wallet = 'xrb_xxx'          # EDIT_HERE: Put your wallet
    withdraw(key, secret, coin, amount, wallet)


main()


