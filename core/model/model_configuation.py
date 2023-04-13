import os

import torch


def get_yolov5():
    # local best.pt
    model = torch.hub.load(os.path.join(os.getcwd(), "yolov5"), 'custom',
                           path=os.path.join(os.getcwd(), "model", "best.pt"),
                           source='local')  # local repo
    model.conf = 0.5
    return model
