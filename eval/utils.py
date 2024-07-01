import numpy as np

def load_text(path):
    return load_text_numpy(path, delimiter=[',', ' ', '\t'])

def load_text_numpy(path, delimiter=' ', dtype=np.float32):
    if isinstance(delimiter, (tuple, list)):
        for d in delimiter:
            try:
                ground_truth_rect = np.loadtxt(path, delimiter=d, dtype=dtype)
                return ground_truth_rect
            except:
                pass

        raise Exception('Could not read file {}'.format(path))
    else:
        ground_truth_rect = np.loadtxt(path, delimiter=delimiter, dtype=dtype)
        return ground_truth_rect


def ltwh_2_ltrb(rect):
    rect[2] += rect[0]
    rect[3] += rect[1]
    return rect


def ltrb_2_ltwh(rect):
    rect[2] -= rect[0]
    rect[3] -= rect[1]
    return rect

def corner_2_ltrb(rect):
    return [rect[0], rect[1], rect[2], rect[5]]

def corner_2_ltwh(rect):
    return [rect[0], rect[1], rect[2]-rect[0], rect[5]-rect[1]]


def serial_process(fun, *serial):
    res = []
    if len(serial)==1:
        for item in zip(*serial):
            if isinstance(item, tuple):
                item = item[0]
            res.append(fun(item))
    if len(serial)==2:
        for item1, item2 in zip(*serial):
            # if isinstance(item1, tuple):
            #     item1 = item1[0];item2 = item2[0]
            res.append(fun(item1, item2))
    return res


def CLE(rect1, rect2):
    """ caculate center location error
    Args:
        rect1: (x1, y1, x2, y2)
        rect2: (x1, y1, x2, y2)
    Returns:
        center location error
    """
    cp1 = [(rect1[2]+rect1[0])/2., (rect1[3]+rect1[1])/2.]
    cp2 = [(rect2[2]+rect2[0])/2., (rect2[3]+rect2[1])/2.]
    d = ((cp1[0]-cp2[0])**2 + (cp1[1]-cp2[1])**2)**0.5
    return d


def IoU(rect1, rect2):
    """ caculate interection over union
    Args:
        rect1: (x1, y1, x2, y2)
        rect2: (x1, y1, x2, y2)
    Returns:
        iou
    """
    # overlap
    x1, y1, x2, y2 = rect1[0], rect1[1], rect1[2], rect1[3]
    tx1, ty1, tx2, ty2 = rect2[0], rect2[1], rect2[2], rect2[3]

    xx1 = np.maximum(tx1, x1)
    yy1 = np.maximum(ty1, y1)
    xx2 = np.minimum(tx2, x2)
    yy2 = np.minimum(ty2, y2)

    ww = np.maximum(0, xx2 - xx1)
    hh = np.maximum(0, yy2 - yy1)

    area = (x2-x1) * (y2-y1)
    target_a = (tx2-tx1) * (ty2 - ty1)
    inter = ww * hh
    iou = inter / (area + target_a - inter)
    return iou