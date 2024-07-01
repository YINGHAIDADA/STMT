import os
from dataset import RGBT234
import numpy as np
from vis import draw_eao
import pickle
from rgbt.utils import *

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.join(current_dir,"../") 

dataset = RGBT234()
bbox_type = 'ltwh'  # 'corner' / 'ltwh' / 'ltrb'
print(dataset.name)
attr_list = ("BC","CM","DEF","FM","HO","LI","LR","MB","NO","TC","PO","SC")
seqs_name = load_text("/media/data3/gt_file/RGBT234/attr_txt/SequencesName.txt", dtype=str)
gt_path = "/media/data3/gt_file/RGBT234/rgbt234_gt/"


# seq_list = ["balancebike","carLight","child4","cycle4","elecbike2","man22","run1","scooter","threeman","threewoman2","walkingtogetherright","manfaraway",]
# seq_list = ["run1","man22","elecbike2","carLight","balancebike","walkingtogetherright","bikeman","shake","man24","manfaraway","manoccpart","maninglass"]
seq_list = ["people","glass"]


res={}
for seq in seq_list:
    res[seq] =[]

for attr in attr_list:
    p = load_text(os.path.join(gt_path, '..', 'attr_txt', attr+'.txt'))
    attr_seqs = [seq_name for i,seq_name in zip(p, seqs_name) if i]
    for seq in seq_list:
        if seq in attr_seqs:
            res[seq].append(attr)

for k,v in res.items():
    print(k,": ",v)
