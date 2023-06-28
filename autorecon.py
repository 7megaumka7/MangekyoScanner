import argparse
import os
import re
import subprocess
import threading
import logging
from typing import Optional
from termcolor import colored


ascii_art= '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⣿⣿⡿⠃⠘⢿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀
⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀
⠀⣸⣿⡉⠀⡀⠈⠉⠉⢙⡟⠲⠤⣄⣠⠤⠖⢻⡋⠉⠉⠁⠀⠀⠉⣿⣧⠀
⢰⣿⣿⣷⡀⠈⢻⣷⣶⣼⣤⣔⠊⠁⠈⠑⣢⣤⣧⣶⣾⡿⠁⢀⣾⣿⣿⡆
⣼⣿⣿⣿⣿⣄⠀⢉⡿⣿⣿⣿⡿⠖⠲⢿⣿⣿⣿⠿⡋⠀⣠⣾⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⡷⣏⠀⡏⠻⢿⡁⠀⠀⢈⡿⠟⢹⠀⣨⢾⣿⣿⣿⣿⣿⣿
⢻⣿⣿⣿⡿⠋⠀⠈⠳⣧⡀⠀⣷⣦⣴⣾⠀⢀⣸⠞⠁⠀⠙⢿⣿⣿⣿⡿
⠸⣿⣿⡿⠁⠀⠀⠀⠀⢸⠉⠲⢼⣿⣿⡯⠖⠋⡇⠀⠀⠀⠀⠈⢿⣿⣿⠇
⠀⠹⣿⣀⣀⣀⣀⣀⣀⣨⣧⠔⠚⣿⣿⠗⠢⢼⣅⣀⣀⣀⣀⣀⣀⣿⡏⠀
⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⢻⡿⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀
⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣷⡀⠈⠃⢀⣾⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣷⣄⢠⣾⣿⣿⣿⡿⠿⠋⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠛⠛⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
'''

print(colored(ascii_art, "red"))

logging.basicConfig(filename="mangekyo_scanner.log", 
                    level=logging.INFO, 
                    format='%(asctime)s %(message)s')

def is_valid_ip(ip: str) -> bool:
    pattern = re.compile(
        r'^'
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
        r'$'
    )
    return bool(pattern.match(ip))

def run_command(command: str) -> Optional[str]:
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        result.check_returncode()
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Command {command} failed with error: {e}")
        return None

def recon(ip: str, threads: int, wordlist: str) -> None:
    if not is_valid_ip(ip):
        raise ValueError("Invalid IP address")
    if not os.path.isfile(wordlist):
        raise ValueError("Wordlist file does not exist")
    if not isinstance(threads, int) or threads <= 0:
        raise ValueError("Number of threads should be a positive integer")

    command1 = f"nmap -sV -sC -T4 -p- --min-rate 5000 {ip}"
    command2 = f"gobuster dir -w {wordlist} -u http://{ip}/FUZZ -t {threads}"
    command3 = f"gobuster fuzz -w {wordlist} -u http://FUZZ.{ip} -t {threads}"

    thread1 = threading.Thread(target=run_command, args=(command1,))
    thread2 = threading.Thread(target=run_command, args=(command2,))
    thread3 = threading.Thread(target=run_command, args=(command3,))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A reconnaissance tool for IP addresses.")
    parser.add_argument('-u', '--url', type=str, required=True, help='Target URL or IP address')
    parser.add_argument('-t', '--threads', type=int, default=100, help='Number of threads to use')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='Path to the wordlist file')
    args = parser.parse_args()

    try:
        recon(args.url, args.threads, args.wordlist)
    except Exception as e:
        logging.error(f"Error: {e}")





