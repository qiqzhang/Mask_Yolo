# # full assembly of the sub-parts to form the complete net
import torch as th
from unet.unet_parts4 import *
import torch.nn as nn



resnet = resnet34()
resnet.load_state_dict(th.load('E:\Person_detection\Pytorch-UNet\\checkpoint\\pretrain\\resnet34-333f7ec4.pth'))
resnet.eval()



class UNet(nn.Module):
    def __init__(self, n_channels, n_classes):
        super(UNet, self).__init__()
        self.resnet = resnet
        self.up1 = up(512, 256, [1, 2, 4, 6])
        self.up2 = up(256, 128, [1, 2, 4, 6])
        self.up3 = up(128, 64, [2, 4, 6, 8])
        self.up4 = up(64, 64, [2, 4, 6, 8])
        self.outc = outconv(64, n_classes)
        self.loc = locconv(64)
        # self.conf = confconv(64)

    def forward(self, x):
        x1, x2, x3, x4, x5 = self.resnet(x)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x_1 = self.up4(x, x1)
        cls = self.outc(x_1)
        loc = self.loc(x_1)
        # conf = self.conf(x_1)
        return cls, loc, x_1