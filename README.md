## MangekyoScanner
MangekyoScanner is a robust and efficient reconnaissance tool designed for penetration testers and cybersecurity enthusiasts. Using the power of well-known tools such as Nmap and Gobuster, it automates the process of IP scanning and directory fuzzing, providing comprehensive data about a given target.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Mangekyou_Sharingan_Sasuke_%28Eternal%29.svg/1200px-Mangekyou_Sharingan_Sasuke_%28Eternal%29.svg.png" width="400" height="400">
</p>

## Disclaimer
MangekyoScanner is created for educational purposes only. Any misuse of this software will not be the responsibility of the author. Use it responsibly.

## Features

- Validates IP addresses.
- Runs `nmap` and `gobuster` for reconnaissance.
- Supports concurrent processing with Python threading.

## Installation

Before running MangekyoScanner, make sure you have Python3 and pip installed. Also, you should install `nmap` and `gobuster` on your system.

**Step 1: Clone the repository**

```bash
git clone https://github.com/yourusername/MangekyoScanner.git
```
***Step 2: Change to the cloned directory**

```bash
cd MangekyoScanner
```

# Usage

You can run the MangekyoScanner as follows:

```bash

python mangekyo_scanner.py -u 192.168.1.1 -t 200 -w /path/to/wordlist
```

**Command-line options:**

-u, --url: Target URL or IP address (required)

-t, --threads: Number of threads to use (default is 100)

-w, --wordlist: Path to the wordlist file (required)

## Example

Here's an example of how to use MangekyoScanner:

```bash

python mangekyo_scanner.py -u 192.168.1.100 -t 50 -w /path/to/wordlist
```

In the example above, the script is scanning the target at IP address 192.168.1.100, using 50 threads, and the wordlist located at /path/to/wordlist.
