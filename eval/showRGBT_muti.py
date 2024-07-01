import cv2
import numpy as np
import rgbt
import os
import time
from PIL import Image
import matplotlib.pyplot as plt
 
COLORS = [
    (0, 255, 0),
    (0, 0, 255),
    (255, 0, 0),
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0),
    (0, 0, 128),
    (0, 128, 0),
    (128, 0, 0),
    (0, 128, 128),
    (128, 0, 128),
    (128, 128, 0)]


def read_image(img_file, cvt_code=cv2.COLOR_BGR2RGB):
    img = cv2.imread(img_file, cv2.IMREAD_COLOR)
    if cvt_code is not None:
        img = cv2.cvtColor(img, cvt_code)
    return img


def show_image(img, boxes=None, box_fmt='ltwh', colors=None,
               thickness=2, fig_n=1, delay=1, visualize=True,
               cvt_code=cv2.COLOR_RGB2BGR, frame_idx = None):
    if cvt_code is not None:
        img = cv2.cvtColor(img, cvt_code)
    
    # resize img if necessary
    max_size = 960
    if max(img.shape[:2]) > max_size:
        scale = max_size / max(img.shape[:2])
        out_size = (
            int(img.shape[1] * scale),
            int(img.shape[0] * scale))
        img = cv2.resize(img, out_size)
        if boxes is not None:
            boxes = np.array(boxes, dtype=np.float32) * scale
    
    if boxes is not None:
        assert box_fmt in ['ltwh', 'ltrb']
        boxes = np.array(boxes, dtype=np.int32)
        if boxes.ndim == 1:
            boxes = np.expand_dims(boxes, axis=0)
        if box_fmt == 'ltrb':
            boxes[:, 2:] -= boxes[:, :2]
        
        # clip bounding boxes
        bound = np.array(img.shape[1::-1])[None, :]
        boxes[:, :2] = np.clip(boxes[:, :2], 0, bound)
        boxes[:, 2:] = np.clip(boxes[:, 2:], 0, bound - boxes[:, :2])
        
        if colors is None:
            colors = COLORS
        colors = np.array(colors, dtype=np.int32)
        if colors.ndim == 1:
            colors = np.expand_dims(colors, axis=0)
        
        for i, box in enumerate(boxes):
            color = colors[i % len(colors)]
            pt1 = (box[0], box[1])
            pt2 = (box[0] + box[2], box[1] + box[3])
            img = cv2.rectangle(img, pt1, pt2, color.tolist(), thickness)
    
    if frame_idx!=None:
        cv2.putText(img, str(frame_idx), (8, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1., (205, 255, 255), 2)

    if visualize:
        winname = 'window_{}'.format(fig_n)
        cv2.imshow(winname, img)
        cv2.waitKey(delay)

    return img



if __name__=="__main__":
    # 选择跟踪器
    seq_list = ['maninglass']

    # settings.lasher_path = "/data/LasHeR/"
    # settings.vtuav_path= "/data/VTUAV/"
    # settings.gtot_path = '/data/GTOT/'
    # settings.rgbt210_path = "/data/RGBT210/"
    # settings.rgbt234_path = "/data/RGBT234/"
    # settings.gtot_dir = '/data/GTOT/'
    # 设置数据集
    root_path = "/media/data3/dataset/RGBT234/"
    dataset = rgbt.RGBT234()

    # 设置跟踪器
    dataset(tracker_name="STMT", 
            result_path="/media/data3/stmt/rgbt234",
            seqs=seq_list,
            prefix='stmt_')
    dataset(tracker_name="ViPT", 
            result_path="/media/data3/vipt_rgbt234",
            seqs=seq_list)
    dataset(tracker_name="APFNet", 
            result_path="/media/data3/APFNet_rgbt234",
            seqs=seq_list,
            bbox_type='corner')
    dataset(tracker_name="DMCNet", 
            result_path="/media/data3/DMCNet_rgbt234",
            seqs=seq_list,
            prefix='DMCNet_')

    
    # 生成legend
    # legend = np.ones([60, 650, 3])*255
    # cv2.putText(legend, 'GT', color=COLORS[0], org=(10, 40), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2)
    # for i, (tracker_name, color) in enumerate(zip(dataset.trackers.keys(), COLORS[1:])):
    #     cv2.putText(legend, tracker_name, color=color, org=((i+1)*120+10, 40), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2)
    # cv2.imwrite('/media/data3/eval/legend.jpg', legend)
    # 绘图
    for seq in seq_list:
        current_directory = os.getcwd()
        print("当前目录:", current_directory)
        save_img_path = os.path.join(current_directory,'eval', dataset.name, seq)
        save_img_path_v = os.path.join(current_directory,'eval', dataset.name, seq, 'v')
        save_img_path_i = os.path.join(current_directory,'eval', dataset.name, seq, 'i')
        if not os.path.exists(save_img_path):
            print("create result dir:", save_img_path)
            os.makedirs(save_img_path_v)
            os.makedirs(save_img_path_i)
        # else:
        #     continue
            
        imgs_path = os.path.join(root_path, seq)
        vimgs_path = os.path.join(imgs_path, "visible")
        iimgs_path = os.path.join(imgs_path, "infrared")
        img_path_list = (sorted(os.listdir(vimgs_path)), sorted(os.listdir(iimgs_path)))

        gt_boxes_v = dataset.seqs_gt[seq]['visible']
        gt_boxes_i = dataset.seqs_gt[seq]['infrared']
        box_fmt = 'ltwh'

        i=0
        for vimg_n, iimg_n, box_v, box_i in zip(*img_path_list, gt_boxes_v, gt_boxes_i):

            vimg_path = os.path.join(vimgs_path, vimg_n)
            iimg_path = os.path.join(iimgs_path, iimg_n)

            vimg = read_image(vimg_path)
            iimg = read_image(iimg_path)

            box_result = [v[seq][i] for v in dataset.trackers.values()]
            box_v_all = [box_v] + box_result
            box_i_all = [box_i] + box_result
            # cv2.imwrite(f'{save_img_path_v}/img_v_{i}.jpg', show_image(vimg, boxes=box_v_all,
            #                                                         box_fmt=box_fmt, fig_n="v", frame_idx=i))
            # cv2.imwrite(f'{save_img_path_i}/img_t_{i}.jpg', show_image(iimg, boxes=box_i_all,
            #                                                         box_fmt=box_fmt, fig_n="i", frame_idx=i))
            if i in [92,113,115,124,238,285]:
                cv2.imwrite(f'{save_img_path_v}/img_v_{i}.jpg', show_image(vimg, boxes=box_v_all,
                                                                        box_fmt=box_fmt, fig_n="v"))
                cv2.imwrite(f'{save_img_path_i}/img_t_{i}.jpg', show_image(iimg, boxes=box_i_all,
                                                                        box_fmt=box_fmt, fig_n="i"))
            else:
                show_image(vimg, boxes=box_v_all, box_fmt=box_fmt, fig_n="v", frame_idx=i)
                show_image(iimg, boxes=box_i_all, box_fmt=box_fmt, fig_n="i", frame_idx=i)
            i+=1