import os

dir = 'local_ckpts'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))