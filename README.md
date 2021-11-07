# Rummy_RL

A Proximal Policy Optimization(PPO) based agent that learns to play rummy by playing against itself.

## How the game works
The rules of Gin Rummy are quite simple. For the 3 player format utilized in this repo, we assign each player a hand of 10 cards from a shuffled deck. The game starts with a card from the remaining deck placed on the "table". The goal of the game is for the player to form 3 sets from the hand. A set can either be a running set of cards with consecutive values or a set of duplicate valued cards. The player must form 3 such sets with 4 cards in one of the set and 3 in the other two. Towards this, the player can either take the card on the table or take a new card from the remaining deck and must place a card from the current hand back onto the table. Hence, before and after each turn, a player can have only 10 cards. The game goes turnwise and we declare the end of the game to have occured if there is a winner or if the deck runs out.

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

