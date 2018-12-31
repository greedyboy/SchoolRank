import pandas as pd


def CountAssessment(file_name):
    print('正在统计每个学校的各个评估的次数...')
    data = pd.read_excel(file_name)
    group = data.groupby(['学校名', '评估']).size().reset_index().rename(columns={0: '出现次数'})

    schools = set(data['学校名'])
    assessment = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']

    newData = {
        'A+': [],
        'A': [],
        'A-': [],
        'B+': [],
        'B': [],
        'B-': [],
        'C+': [],
        'C': [],
        'C-': []
    }
    index = schools

    for school in schools:
        for ass in assessment:
            times = group.loc[(group['学校名'] == school) & (group['评估'] == ass)].iloc[:, 2].values
            if len(times) == 0:
                newData[ass].append(0)
            else:
                newData[ass].append(times[0])

    df = pd.DataFrame(newData, columns=assessment, index=index).sort_values(by=assessment, ascending=False)
    df['总评价次数'] = sum([df[x] for x in assessment])
    df.to_excel('schoolAssementCount.xlsx')
    # df.to_csv('schoolAssementCount.csv')
    print('生成数据完成')


if __name__ == '__main__':
    CountAssessment('schoolRank.xlsx')
