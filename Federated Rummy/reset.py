import os

if not os.path.exists('Server/global_ckpt'):
    os.makedirs('Server/global_ckpt')

if not os.path.exists('Server/incoming_ckpts/actors'):
    os.makedirs('Server/incoming_ckpts/actors')

if not os.path.exists('Server/incoming_ckpts/critics'):
    os.makedirs('Server/incoming_ckpts/critics')

if not os.path.exists('Client_A/local_ckpts'):
    os.makedirs('Client_A/local_ckpts')

if not os.path.exists('Client_B/local_ckpts'):
    os.makedirs('Client_B/local_ckpts')

if not os.path.exists('Client_C/local_ckpts'):
    os.makedirs('Client_C/local_ckpts')


dir = 'Server/incoming_ckpts/actors'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'Server/incoming_ckpts/critics'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'Server/global_ckpt'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'Client_A/local_ckpts'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'Client_B/local_ckpts'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'Client_C/local_ckpts'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))