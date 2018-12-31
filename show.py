# -*- coding: utf-8 -*-
# __Author__: Sdite
# __Email__ : a122691411@gmail.com

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.rcParams['savefig.dpi'] = 300 #图片像素
plt.rcParams['figure.dpi'] = 130 #分辨率
# 默认的像素：[6.0,4.0]，分辨率为100，图片尺寸为 600&400
# 指定dpi=200，图片尺寸为 1200*800
# 指定dpi=300，图片尺寸为 1800*1200

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体 SimHei为黑体
mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def showPic(fileName, schoolNames):
    data = pd.read_excel(fileName)

    for schoolName in schoolNames:
        # 获取该学校的数据
        school = data[data['学校名'] == schoolName]

        # 该学校的数据按评估来分类
        schoolGroupByAss = school[['专业名', '评估']].groupby(['评估'])

        # 用来存放各个评估等级的专业名， 共九个等级
        majorData = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
        ]
        # 九个等级的映射表
        map_dic = {
            'A+': 0,
            'A': 1,
            'A-': 2,
            'B+': 3,
            'B': 4,
            'B-': 5,
            'C+': 6,
            'C': 7,
            'C-': 8
        }
        n_rows = 0  # 保存所有等级中最多专业名的等级的 数量
        for k, v in schoolGroupByAss:
            major = list(v['专业名'])  # 某个等级的所有专业名
            n_rows = max(n_rows, len(major))  # 判断该等级的 专业数量是不是最多
            majorData[map_dic[k]].extend(major)  # 存放各个等级数据

        assessment = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']
        emptyList = []

        # 新建一个存放各个等级专业的list表, 并对二维list表填充到列数相同
        newMajorData = majorData.copy()
        for row in range(9):
            newMajorData[row] = majorData[row] + [''] * (n_rows - len(majorData[row]))

            if not any(newMajorData[row]):
                emptyList.append(row)

        offset = 0
        for e in emptyList:
            newMajorData.pop(e - offset)
            assessment.pop(e - offset)
            offset += 1
        num = 9 -offset

        newMajorData = list(zip(*newMajorData))  # 二维list表转置

        # 存放绘图数据的表, 长度为9行n_rows列,
        # 9行表示9个等级
        # 这个二维表1表示有一个专业在这个等级, 0表示没有, 主要用于后续绘图
        pltData = np.zeros((num, n_rows))
        for i in range(num):
            pltData[i] = [x < len(majorData[i]) for x in range(n_rows)]

        # 二维表转置
        pltData = pltData.T
        index = np.arange(num)
        bar_width = 0.01
        y_offset = np.zeros(num) + 0.3    # y轴偏移量

        plt.figure()
        for row in range(n_rows):
            for col in range(num):
                # 将文字画在表上
                plt.text(index[col], y_offset[col], newMajorData[row][col], ha='center', size=7,
                        bbox=dict(boxstyle="round", ec=(1., 0.5, 0.5), fc=(1., 0.8, 0.8), ))
            y_offset += pltData[row] + 3

        plt.bar(index, y_offset, bar_width, color='w')
        for col in range(num):
            # 将文字画在表上
            plt.text(index[col], -5, assessment[col], ha='center', size=10,
                    bbox=dict(boxstyle="round", ec=(1., 0.5, 0.5), fc=(1., 1, 1), ))

        plt.axis('off')
        plt.title(schoolName + ' 评估表')
    plt.show()


if __name__ == '__main__':
    schoolNames = sys.argv[1:]
    showPic('GetSomeData/schoolRank.xlsx', schoolNames)
