# tigerSH
Simple remote shell written in python

You will need proper crypto library for importing fernet.

```
pip install cryptography
```

Debug mode is on by default, meaning key received from server in exchange will be saved to a log file.
If you don't want it, turn it off by setting **debug_mode** to **False**.

```
# Line 6 in client.py
debug_mode = False
```
