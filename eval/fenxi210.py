from rgbt import RGBT210
import os

rgbt210 = RGBT210()

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.join(current_dir,"../") 
# Register your tracker

rgbt210(
    tracker_name="STMT", 
    result_path=os.path.join(workspace_dir,"tracking_result/stmt/rgbt210"),
    prefix="stmt_")

# Evaluate multiple trackers
pr_dict = rgbt210.PR()
sr = rgbt210.SR()

for k,v in pr_dict.items():
    print(k)
    print(v[0])
    print(sr[k][0])
    print("")
