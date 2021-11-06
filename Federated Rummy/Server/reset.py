import os

dir = 'incoming_ckpts/actors'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'incoming_ckpts/critics'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'global_ckpt'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))