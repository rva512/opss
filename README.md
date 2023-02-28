keylogger

There is a client(victim) and server(attacker) script.

Once victim is infected with keylogger and running in the background, it will open a reverse shell to the running script at attacker machine.

The client script accepts commands over the reverse shell.

commands:

hook - starts keylogging and saves data in a temprary folder.
unhook - stops keylogging
exfil - sends keylog data to server and deletes temporary folder used to store data.
