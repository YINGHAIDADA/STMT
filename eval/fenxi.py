import os
from dataset import RGBT234
import numpy as np
from vis import draw_eao
import pickle


current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.join(current_dir,"../") 

result_path = [
    ['APFNet', os.path.join(workspace_dir,"tracking_result/APFNet_rgbt234"), ""],
    ['DMCNet', os.path.join(workspace_dir,"tracking_result/DMCNet_rgbt234"), "DMCNet_"],
    ['ViPT', os.path.join(workspace_dir,"tracking_result/vipt_rgbt234"), ""],
    ['STMT', os.path.join(workspace_dir,"tracking_result/stmt_rgbt234"), "stmt_"],
    
]
# print(result_path)
dataset = RGBT234()
bbox_type = 'ltwh'  # 'corner' / 'ltwh' / 'ltrb'
print(dataset.name)
attr_sr_list = []
attr_pr_list = []

tracker_temp = []
met_pr = None
met_sr = None

for tracker_name, res_path, pretxt in result_path:
    print(tracker_name)
    attr_sr_list.append([])
    attr_pr_list.append([])
    attr_sr_list[-1].append(tracker_name)
    attr_pr_list[-1].append(tracker_name)

    fp = os.path.join(workspace_dir,"eval/result", tracker_name+'.pkl')
    if os.path.exists(fp):
        msr,mpr = pickle.load(open(fp, 'rb'))
    else:
        msr = dataset.SR(res_path, attr=dataset.ALL, bbox_type=bbox_type, pre=pretxt)
        mpr = dataset.PR(res_path, attr=dataset.ALL, bbox_type=bbox_type, pre=pretxt)
        pickle.dump([msr, mpr], open(os.path.join(workspace_dir,"eval/result", tracker_name+'.pkl'), 'wb'))
    print(tracker_name,'SR = ', msr.mean())
    print(tracker_name,'PR = ', mpr.mean(axis=0)[20])

    if "met" in tracker_name:
        met_pr = mpr[:,20]
        met_sr = msr.mean(axis=1)
    else:
        tracker_temp.append(
            {
                "name": tracker_name,
                "pr": mpr[:,20],
                "sr": msr.mean(axis=1)
            }
        )
    # 属性分析
    attr_sr = []
    attr_pr = []
    for item in dataset.get_attr_list():
        idx = dataset.choose_serial_by_att(item).astype(np.bool8)
        attr_sr.append(msr[idx].mean())
        attr_pr.append(mpr[idx].mean(axis=0)[20])
        
    attr_sr_list[-1].append(attr_sr)
    attr_pr_list[-1].append(attr_pr)
