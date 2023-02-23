# python-port-forward
Simple Python Port Forwarding Script written in Python 3.

Slight modification of: https://gist.github.com/WangYihang/e7d36b744557e4673d2157499f6c6b5e to accomodate config file.

```
 +-----------------------------+         +---------------------------------------------+         +--------------------------------+
 |     My Laptop (Alice)       |         |            Intermediary Server (Bob)        |         |    Internal Server (Carol)     |
 +-----------------------------+         +----------------------+----------------------+         +--------------------------------+
 | $ ssh -p 1022 carol@1.2.3.4 |<------->|    IF 1: 1.2.3.4     |  IF 2: 192.168.1.1   |<------->|       IF 1: 192.168.1.2        |
 | carol@1.2.3.4's password:   |         +----------------------+----------------------+         +--------------------------------+
 | carol@hostname:~$ whoami    |         | $ python pf.py --listen-host 1.2.3.4 \      |         | 192.168.1.2:22(OpenSSH Server) |
 | carol                       |         |                --listen-port 1022 \         |         +--------------------------------+
 +-----------------------------+         |                --connect-host 192.168.1.2 \ |
                                         |                --connect-port 22            |
                                         +---------------------------------------------+
```

## Config File Format
`<localhost> <localport> <remotehost> <remoteport>`
```
127.0.0.1 2000 192.168.0.1 2001
127.0.0.1 2002 192.168.0.1 2003
127.0.0.1 2004 192.168.0.1 2005
...
```

## How to Run
`python port-forward.py`