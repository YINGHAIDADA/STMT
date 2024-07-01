from utils import *
import os

class BaseDataset_rgbt:
    def __init__(self, gt_path) -> None:
        self.gt_path = gt_path
        
        self.ALL='ALL'

        self.sequencesName = os.listdir(self.gt_path)

        self.gt_serial_v = {}
        self.gt_serial_i = {}
        for seq_name in self.sequencesName:
            serial_v = load_text(os.path.join(self.gt_path,seq_name,'visible.txt'))
            serial_i = load_text(os.path.join(self.gt_path,seq_name,'infrared.txt'))
            self.gt_serial_v[seq_name] = serial_process(ltwh_2_ltrb, serial_v)
            self.gt_serial_i[seq_name] = serial_process(ltwh_2_ltrb, serial_i)


    def bbox_type_trans(self, bbox_type_src, bbox_type_new):
        if bbox_type_src!=bbox_type_new:
            return eval(bbox_type_src+'_2_'+bbox_type_new)
        else:
            return lambda x:x


    def choose_serial_by_att(self, attr):
        if attr==self.ALL:
            return np.array([1]*len(self.sequencesName), dtype=np.float32)
        else:
            return load_text(os.path.join(self.gt_path, '..', 'attr_txt',attr+'.txt'))


    def SR(self, result_path, bbox_type='ltwh', thr=np.linspace(0, 1, 21), attr='ALL', pre=""):
        # calculate success rate

        # 选择序列
        eval_serials = self.choose_serial_by_att(attr)

        # 处理序列
        sr=[]
        for p,item in zip(eval_serials, self.sequencesName):
            if p:
                serial=load_text(os.path.join(result_path, pre+item+'.txt'))
                serial_v = self.gt_serial_v[item]
                serial_i = self.gt_serial_i[item]
                if bbox_type != 'ltrb':
                    fun = self.bbox_type_trans(bbox_type, 'ltrb')
                    serial = serial_process(fun, serial)
                res_v = np.array(serial_process(IoU, serial, serial_v))
                res_i = np.array(serial_process(IoU, serial, serial_i))
                res = np.maximum(res_v, res_i)

                sr_cell = []
                for i in thr:
                    sr_cell.append(np.sum(res>i)/len(res))
                sr.append(sr_cell)
                #print(item,":",np.array(sr_cell).mean())

        # 总结
        return np.array(sr)

    
    def PR(self, result_path, bbox_type='ltwh', thr=np.linspace(0, 50, 51), attr='ALL', pre=''):
        # calculate success rate

        # 选择序列
        eval_serials = self.choose_serial_by_att(attr)

        # 处理序列
        pr=[]
        for p,item in zip(eval_serials, self.sequencesName):
            if p:
                serial=load_text(os.path.join(result_path, pre+item+'.txt'))
                serial_v = self.gt_serial_v[item]
                serial_i = self.gt_serial_i[item]
                if bbox_type != 'ltrb':
                    fun = self.bbox_type_trans(bbox_type, 'ltrb')
                    serial = serial_process(fun, serial)
                res_v = np.array(serial_process(CLE, serial, serial_v))
                res_i = np.array(serial_process(CLE, serial, serial_i))
                res = np.minimum(res_v, res_i)

                pr_cell = []
                for i in thr:
                    pr_cell.append(np.sum(res<=i)/len(res))
                pr.append(pr_cell)
                # if np.array(pr_cell)[20]<0.5:
                #     print(item,":",np.array(pr_cell)[20])

        # 总结
        return np.array(pr)
    

    def USR(self, result_path1, result_path2, w=[20,1]):
        raise