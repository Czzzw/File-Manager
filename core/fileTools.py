"""文件处理集合"""

import os
import re


def updateNfo(filePath, match, new_content):
    if new_content is None or match is None:
        print('要改动内容不能为空')
        return
    # match和new_content判断是否为空字符串，如果是空字符串弹出对话框让用户确认
    if match == '' or new_content == '':
        result = input('要改动内容不能为空，是否继续？(y/n):')
        if result == 'n':
            return
    # 读取路径下的.nfo类型文件，如果有子文件夹继续递归处理
    if os.path.isdir(filePath):
        for item in os.listdir(filePath):
            itemPath = os.path.join(filePath, item)
            updateNfo(itemPath, match, new_content)

    # 如果是.nfo文件，则更新文件内容
    elif os.path.isfile(filePath) and filePath.endswith(".nfo"):
        with open(filePath, "r", encoding="utf-8") as f:
            content = f.read()
            # print(filePath, '\n', content, '\n')
        # 匹配标签的正则表达式
        reString = '(<' + match + '>)(.*?)(</' + match + '>)'
        pattern = re.compile(reString, re.DOTALL)
        # 替换标签之间的内容，写入文件中
        new_file_content = pattern.sub(r'\1' + new_content + r'\3', content)
        with open(filePath, "w", encoding="utf-8") as f:
            # print(filePath, '更改后：\n', new_file_content, '\n')
            f.write(new_file_content)

if __name__ == '__main__':
    filePath = r'C:\Users\Czzzw\Desktop\测试'
    updateNfo(filePath, 'actor', 'fdfd')


