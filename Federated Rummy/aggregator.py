import os
import torch as T
from model import Agent

agent_a = Agent(11,(52,),n_epochs=5,name='A')
agent_b = Agent(11,(52,),n_epochs=5,name='B')
agent_c = Agent(11,(52,),n_epochs=5,name='C')

agent_a.load_models()
agent_b.load_models()
agent_c.load_models()

actor_a = agent_a.actor.state_dict()
actor_b = agent_b.actor.state_dict()
actor_c = agent_c.actor.state_dict()
actor_g = agent_a.actor.state_dict()

critic_a = agent_a.critic.state_dict()
critic_b = agent_b.critic.state_dict()
critic_c = agent_c.critic.state_dict()
critic_g = agent_a.critic.state_dict()


for layer in actor_g:
    actor_g[layer] = (actor_a[layer] + actor_b[layer] + actor_c[layer])/3

for layer in critic_g:
    critic_g[layer] = (critic_a[layer] + critic_b[layer] + critic_c[layer])/3


agent_global = Agent(11,(52,),n_epochs=5,name='G')

actor_global = agent_global.actor
actor_global.load_state_dict(actor_g)

critic_global = agent_global.critic
critic_global.load_state_dict(critic_g)

actor_global.save_checkpoint()
critic_global.save_checkpoint()
print('Done')