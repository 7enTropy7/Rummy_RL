'''
This scipt deletes all models collected from previous iteration
'''

import os
 
dir = 'ckpt/actors'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'ckpt/critics'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))