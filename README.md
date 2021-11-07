# Rummy_RL

A Proximal Policy Optimization(PPO) based agent that learns to play rummy by playing against itself.

## Federated Learning

### Cloning
```bash
$ git clone https://github.com/7enTropy7/Rummy_RL.git
```
### Initial Setup
```bash
$ cd Rummy_RL/Federated\ Rummy/
$ python reset.py
```
### Starting Socketio Server
```bash
$ python Server/run_socketio.py
```
### Starting FTP Server
```bash
$ python Server/ftp_server.py
```
### Starting Clients
```bash
$ python Client_A/client.py
$ python Client_B/client.py
$ python Client_C/client.py    
```

## Self-Play Agent
```bash
$ python Rummy\ PPO/main.py
```

## Demonstration

### Federated Learning Agents


### Self-Play Agent
![ezgif com-gif-maker](https://user-images.githubusercontent.com/36446402/136848216-c9977dcc-d3c5-48ec-bbd0-71c8ff124b1e.gif)

