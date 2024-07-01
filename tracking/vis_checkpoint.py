import torch

path = "/media/data3/pretrained_models/vitb_256_mae_ce_32x4_ep300/OSTrack_ep0300.pth.tar"

checkpoint = torch.load(path, map_location="cpu")

if "net" in checkpoint.keys():
    # checkpoint=checkpoint['net']
    print("有net")
else:
    print("mei有net")


param_dict_rgbt = dict()