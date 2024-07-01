
from dataset.basedataset import BaseDataset_rgbt

class RGBT234(BaseDataset_rgbt):
    def __init__(self, gt_path='gt_file/RGBT234/rgbt234_gt/') -> None:
        super().__init__(gt_path)

        self.name = 'RGBT234'

        # 挑战属性
        self.BC = "BC"
        self.CM = "CM"
        self.DEF = "DEF"
        self.FM = "FM"
        self.HO = "HO"
        self.LI = "LI"
        self.LR = "LR"
        self.MB = "MB"
        self.NO = "NO"
        self.TC = "TC"
        self.PO = "PO"
        self.SC = "SC"

    def get_attr_list(self):
        
        return ["BC","CM","DEF","FM","HO","LI","LR","MB","NO","TC","PO","SC"]