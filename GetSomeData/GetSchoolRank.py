# 获取数据的脚本

import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


def GetSchoolRank():
    print('正在获取数据中...')
    session = requests.Session()

    base_url = 'http://www.cdgdc.edu.cn/webrms/pages/Ranking/xkpmGXZJ2016.jsp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }

    res = session.get(url=base_url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    # 获取专业名+专业代码
    subjects = [e.text for e in soup.find_all('a', text=re.compile(r'\d\d\d\d'))]

    # 展开一个一个大类来获取专业名+专业代码
    for e in soup.find_all('a', {'href': re.compile('\?xkdm=\d\d')})[1:]:
        url = base_url + e['href'][16:]
        res = session.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        subjects.extend([ee.text for ee in soup.find_all('a', text=re.compile(r'\d\d\d\d'))])

    df = pd.DataFrame(columns=['学校代码', '学校名', '专业名', '评估'])
    for e in subjects:
        major_name = e[4:]
        major_code = e[:4]
        url = base_url + '?yjxkdm=%s' % major_code
        res = session.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        table = soup.find('table', dict(bgcolor="#c2d8e5", border="0", cellpadding="0", cellspacing="1",
                                        width="610px")).find_all('td')

        school_code_regular = re.compile(r' \d{5}')
        assessment = ''
        for row in table:
            text = row.text
            if school_code_regular.match(text):
                school_code, school_name = text.split('      ')
                school_code = school_code.replace(' ', '')
                school_name = school_name.replace(' ', '')

                df = df.append({'学校代码': school_code.replace('\n', '').strip(), '学校名': school_name.replace('\n', '').strip(), '专业名': major_name.replace('\n', '').strip(), '评估': assessment.replace('\n', '').strip()},
                               ignore_index=True)

            else:
                assessment = text

    df.to_excel('schoolRank.xlsx', index=None)
    # df.to_csv('schoolRank.csv', index=None)

    print('获取数据完成')


if __name__ == "__main__":
    GetSchoolRank()
