# -*- coding: utf-8 -*-
# __Author__: Sdite
# __Email__ : a122691411@gmail.com

import random
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体 SimHei为黑体
mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率


def GetWordCloud(fileName):
    mask = np.array(Image.open("../images/mask.jpg"))  # 蒙版图

    data = pd.read_excel(fileName)
    text = dict(data['学校名'].value_counts())  # 自己计算好词频

    # 生成一个词云图像
    wc = WordCloud(background_color='white', mask=mask, max_font_size=100).generate_from_frequencies(text)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('../images/wordcloud.jpg', dpi=300)
    plt.show()


if __name__ == '__main__':
    GetWordCloud('schoolRank.xlsx')
