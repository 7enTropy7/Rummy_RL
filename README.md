# Rummy_RL

A Proximal Policy Optimization(PPO) based agent that learns to play rummy by playing against itself.

![ezgif com-gif-maker](https://user-images.githubusercontent.com/36446402/136848216-c9977dcc-d3c5-48ec-bbd0-71c8ff124b1e.gif)


## Directory Structure
```bash
.
├── Federated\ Rummy
│   ├── Client_A
│   │   ├── __pycache__
│   │   │   ├── ftp_client.cpython-38.pyc
│   │   │   ├── grandma.cpython-38.pyc
│   │   │   └── model.cpython-38.pyc
│   │   ├── client.py
│   │   ├── ftp_client.py
│   │   ├── grandma.py
│   │   ├── local_ckpts
│   │   ├── model.py
│   │   └── reset.py
│   ├── Client_B
│   │   ├── __pycache__
│   │   │   ├── ftp_client.cpython-38.pyc
│   │   │   ├── grandma.cpython-38.pyc
│   │   │   └── model.cpython-38.pyc
│   │   ├── client.py
│   │   ├── ftp_client.py
│   │   ├── grandma.py
│   │   ├── local_ckpts
│   │   ├── model.py
│   │   └── reset.py
│   ├── Client_C
│   │   ├── __pycache__
│   │   │   ├── ftp_client.cpython-38.pyc
│   │   │   ├── grandma.cpython-38.pyc
│   │   │   └── model.cpython-38.pyc
│   │   ├── client.py
│   │   ├── ftp_client.py
│   │   ├── grandma.py
│   │   ├── local_ckpts
│   │   ├── model.py
│   │   └── reset.py
│   └── Server
│       ├── __pycache__
│       │   ├── model.cpython-38.pyc
│       │   ├── socketio_server.cpython-38.pyc
│       │   └── utils.cpython-38.pyc
│       ├── config.json
│       ├── ftp_server.py
│       ├── global_ckpt
│       │   ├── actor_G
│       │   └── critic_G
│       ├── incoming_ckpts
│       │   ├── actors
│       │   └── critics
│       ├── model.py
│       ├── reset.py
│       ├── run_socketio.py
│       ├── socketio_server.py
│       └── utils.py
├── README.md
├── Rummy\ PPO
│   ├── __pycache__
│   │   ├── grandma.cpython-38.pyc
│   │   ├── model.cpython-38.pyc
│   │   ├── model.cpython-39.pyc
│   │   └── test.cpython-39.pyc
│   ├── ckpt
│   │   ├── actor_torch_ppo
│   │   └── critic_torch_ppo
│   ├── grandma.py
│   ├── main.py
│   └── model.py
├── Single\ player
│   ├── main.py
│   ├── model.py
│   └── test.py
└── requirements.txt
```