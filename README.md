[![Linkedin](https://img.shields.io/badge/Linkedin-Anirudh%20Menon-success?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/anirudh-menon-0b7764170/)
[![Linkedin](https://img.shields.io/badge/Linkedin-Unnikrishnan%20Menon-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/unnikrishnan-menon-aa013415a/)

# Rummy_RL

This is an application of Federated Learning to train a Proximal Policy Optimization(PPO) based agent that learns to play Rummy by playing against itself.

## How the game works
The rules of Gin Rummy are quite simple. For the 3 player format utilized in this repo, we assign each player a hand of 10 cards from a shuffled deck. The game starts with a card from the remaining deck placed on the "table". The goal of the game is for the player to form 3 sets from the hand. A set can either be a running set of cards with consecutive values freom the same suit or a set of duplicate valued cards. The player must form 3 such sets with 4 cards in one of the set and 3 in the other two. Towards this, the player can either take the card on the table or take a new card from the remaining deck and must place a card from the current hand back onto the table. <br>
<br>
![Rummy21-5c196dbd46e0fb0001070811](https://user-images.githubusercontent.com/36445587/140691014-6531a8bc-da3c-4f57-8db8-3c064dc05354.jpg)

Hence, before and after each turn, a player can have only 10 cards. The game goes turnwise and we declare the end of the game to have occured if there is a winner or if the deck runs out.

## Wrapping the game into an environment
We utilize the pydealer library to maintain card, hands and deck objects. We globally maintain the values of the card on the "table" and the top card of the remaning deck. Each hand assigned to player is a Pydealer stack dealt from the shuffled deck. The hand is visualised as a 4x13 matrix where the rows are the suits and the columns represent the values. <br><br>

![Capture](https://user-images.githubusercontent.com/36445587/140718318-6112e868-2ea2-4ad7-90a0-bc9f48543b6c.JPG)

Thus it is easy to track and reward the agent for running sets which occur horizontally in the matrix and duplicate value sets which occur vertically.


## Self-Play Agent
Our first implementation is analogous to a dude pulling out 3 chairs on a Rummy table and sitting on the 3 chairs sequentially to play his best cards. This dude is a PPO agent. And it tries to win against itself. Kinda like Fight Club ;P

```bash
$ python Rummy\ PPO/main.py
```

## Federated Learning
But Rummy is played by different minds competing against each other. Now imagine that the players are friends outside the game and meet up after every game to discuss how they could have done better, and so our second implementation is a system where three separate instances of the model play each other and aggregate their experiences using Federated Learning. <br>
<br>
Federated learning is an approach that downloads the current model and computes an updated model at the device itself (edge computing) using local data. These locally trained models are then sent from the devices back to the central server where they are aggregated, i.e. averaging weights, and then a single consolidated and improved global model is sent back to the devices.<br>
<br>
![0_MMNglGw1zSpS86Yf](https://user-images.githubusercontent.com/36445587/140692368-f2729424-1dbb-4e1e-972a-4587d219fd82.png)


### Cloning
```bash
$ git clone https://github.com/7enTropy7/Rummy_RL.git
```
The following steps are to be followed inside the ```Federated Rummy``` subdirectory.

Note that training the PPO agent with Federated Learning will require ```5``` terminals.

### Initial Setup
In Terminal 1 execute the following to check for missing folders (if any) for storing models across the server and all clients: 
```bash
$ python reset.py
```
This also removes any old redundant checkpoint files that may be left over from previous training session.

### Starting Socketio Server
In Terminal 1, next execute the following command to fire up the Socketio Server.

```bash
$ python Server/run_socketio.py
```
### Starting FTP Server
In Terminal 2 run the following to start an FTP Server that manages model weights file transmission.

```bash
$ python Server/ftp_server.py
```
### Starting Clients
In Terminals 3,4 and 5 run one of the following commands each in the right order.
```bash
$ python Client_A/client.py
$ python Client_B/client.py
$ python Client_C/client.py    
```
Note that Federated training will only get initialized once all 3 clients are connected to the socket server.
## Demonstration

### Federated Learning Agents
![ezgif com-gif-maker](https://user-images.githubusercontent.com/36446402/140694721-4d23f8f0-ca5c-4f3e-8d66-5e422da52ee4.gif)
<br>
<br>
And we have a winner! The image below shows that the player obtained the required sets: Duplicate set (1 of Hearts, 1 of Diamonds and 1 of Spades), Running set (9, 10 and 11 of Spades) and another Running set (Jack, Queen and King of Clubs denoted by 11, 12 and 13 respectively)<br><br>

<img width="507" alt="Screenshot 2021-11-08 at 11 56 11 AM" src="https://user-images.githubusercontent.com/36446402/140694884-2428326d-559a-4fcf-b535-62874ab90868.png">

### Self-Play Agent
![ezgif com-gif-maker](https://user-images.githubusercontent.com/36446402/136848216-c9977dcc-d3c5-48ec-bbd0-71c8ff124b1e.gif)

# Authors
* [**Anirudh Rajiv Menon**](https://github.com/axe76)
* [**Unnikrishnan Menon**](https://github.com/7enTropy7)

# License
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

