import requests
import colorama
import time
import os

colorama.init(autoreset=True)

if not os.path.exists('tokens.txt') or not os.path.exists('channel_ids.txt'):
    print(f'{colorama.Fore.RED}Error: tokens.txt or channel_ids.txt file is missing!')
    exit()

def read_tokens():
    with open('tokens.txt', 'r') as f:
        return f.read().splitlines()
    
def read_channel_ids():
    with open('channel_ids.txt', 'r') as f:
        return f.read().splitlines()
    
def get_first_16_chars(token):
    return token[:16]

tokens = read_tokens()
channel_ids = read_channel_ids()

message = input('Enter the message you want to send: ')
while True:
    try:
        delay = int(input('Enter the delay between messages (in seconds): '))
        break
    except ValueError:
        print(f'{colorama.Fore.RED}Please enter a valid number!')

successful_requests = 0
failed_requests = 0

for token in tokens:
    for channel_id in channel_ids:
        headers = {
            'Authorization': token,
        }
        payload = {
            'content': message
        }
        response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            successful_requests += 1
            print(f'{colorama.Fore.GREEN}[+] Successfully sent message to channel {channel_id}. ({get_first_16_chars(token)}...)')
        else:
            failed_requests += 1
            print(f'{colorama.Fore.RED}[-] Failed to send message to channel {channel_id}. ({get_first_16_chars(token)}...)', response.json())
        
        time.sleep(delay)

print()
print(f'{colorama.Fore.YELLOW}Finished sending messages.')
print(f'{colorama.Fore.GREEN}Successful requests: {successful_requests}')
print(f'{colorama.Fore.RED}Failed requests: {failed_requests}')