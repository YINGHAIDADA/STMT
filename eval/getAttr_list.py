import os
from dataset import RGBT234
import numpy as np
from vis import draw_eao
import pickle

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.join(current_dir,"../") 

dataset = RGBT234()
bbox_type = 'ltwh'  # 'corner' / 'ltwh' / 'ltrb'
print(dataset.name)

idx = dataset.choose_serial_by_att('FM').astype(np.bool8)
print(idx)