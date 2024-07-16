"""文件处理集合"""
import mimetypes
import os
import re
import shutil
import time
import logging


logger = Logger()
CLogger = logger.get_common_logger()
SLogger = logger.get_special_logger()


def updateNfo(filePath, match, new_content=None):
    """
    更新.nfo文件
    :param filePath: 文件路径
    :param match: 匹配标签的正则表达式
    :param new_content: 新的标签内容
    :return:
    """
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
        # 获取文件所在文件夹名称
        path_parts = filePath.split(os.sep)
        # 返回倒数第二个层级的名称
        if len(path_parts) >= 2:
            new_content = path_parts[-2]
        else:
            return None
        print(new_content)
        # 匹配标签的正则表达式
        reString = '(<' + match + '>)(.*?)(</' + match + '>)'
        pattern = re.compile(reString, re.DOTALL)
        # 替换标签之间的内容，写入文件中
        new_file_content = pattern.sub(r'\g<1>' + new_content + r'\g<3>', content)
        with open(filePath, "w", encoding="utf-8") as f:
            # print(filePath, '更改后：\n', new_file_content, '\n')
            f.write(new_file_content)

def renameNfo(filePath):
    """
    重命名nfo文件
    指定一个路径，将路径下所有子文件夹中的所有nfo类型的文件，重命名为子文件夹名.nfo
    :param filePath:
    :return:
    """
    for root, dirs, files in os.walk(filePath):
        if not dirs:
            nfo_files = [file for file in files if file.endswith('.nfo')]
            if len(nfo_files) == 1:
                os.rename(os.path.join(root, nfo_files[0]), os.path.join(root, root.split('\\')[-1] + '.nfo'))
            else:
                print(root, '文件夹中存在多个nfo文件，请手动处理')
                continue

def is_video_file(filepath):
    """
    检查文件是否为视频文件
    :param filepath: 文件路径
    :return: 如果是视频文件返回True，否则返回False
    """
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type and mime_type.startswith('video/')

def check_mp4_and_nfo_files(directory_path, new_directory_path):
    """
    检查文件夹中是否存在nfo文件
    检查指定路径下的子文件夹，如果子文件夹中有.mp4文件但没有.nfo文件，则将该文件夹移动到指定路径下
    :param directory_path: 指定路径
    :param new_directory_path: 移动后的路径
    :return:
    """
    # 遍历指定路径下的子文件夹
    for root, dirs, files in os.walk(directory_path):
        mp4_files = [file for file in files if is_video_file(file)]
        nfo_files = [file for file in files if file.endswith('.nfo')]
        # 如果当前子文件夹中有.mp4文件但没有.nfo文件，挪到指定路径下
        # print(nfo_files)
        if mp4_files and not nfo_files:
            destination = os.path.join(new_directory_path, os.path.basename(root))
            print(destination)
            if os.path.exists(destination):
                continue
            shutil.move(root, destination)
            print(f"Directory '{root}' contains video files but no .nfo files.")

def check_poster_and_nfo_files(directory_path, new_directory_path):
    """
    检查文件夹中是否存在poster.jpg
    检查指定路径下的子文件夹，如果子文件夹中有.nfo文件但没有poster.jpg文件，则将该文件夹移动到指定路径下
    :param directory_path: 指定路径
    :param new_directory_path: 移动后的路径
    :return:
    """
    # 遍历指定路径下的子文件夹
    for root, dirs, files in os.walk(directory_path):
        jpg_files = [file for file in files if file.name == 'poster.jpg']
        nfo_files = [file for file in files if file.endswith('.nfo')]
        # 如果当前子文件夹中有.nfo文件但没有poster.jpg文件，挪到指定路径下
        # print(nfo_files)
        if jpg_files and not nfo_files:
            destination = os.path.join(new_directory_path, os.path.basename(root))
            print(destination)
            if os.path.exists(destination):
                continue
            shutil.move(root, destination)
            print(f"Directory '{root}' contains video files but no .nfo files.")

def renameDir(filePath):
    """
    重命名文件夹
    :param filePath:
    :return:
    """
    for root, dirs, files in os.walk(filePath):
        # 判断路径下是否存在子文件夹
        # (dirs是当前文件夹下的文件夹列表，如果没有子文件夹，dirs为空，空元组判断是当做false)
        if not dirs:
            # 获取文件夹中所有视频文件
            video_files = [file for file in files if is_video_file(file)]
            # 如果没有视频文件则continue
            if len(video_files) == 0:
                print(root, '：没有视频文件，跳过')
                continue
            # 如果只有一个视频文件，则重命名父目录的名字为视频文件名
            if len(video_files) == 1:
                print(root, '|', os.path.join(os.path.dirname(root), video_files[0].split('.')[0]))
                os.rename(root, os.path.join(os.path.dirname(root), video_files[0].split('.')[0]))
            # 有多个视频文件，如果名称类似，差异不超过2字符，则使用公共前缀作为父目录名
            if len(video_files) > 1:
                max_prefix = find_max_prefix(video_files)
                if max_prefix:
                    print(root, '|', os.path.join(os.path.dirname(root), max_prefix))
                    os.rename(root, os.path.join(os.path.dirname(root), max_prefix))

def renameTorrent(filePath):
    """
    重命名种子文件
    :param filePath:
    :return:
    """
    # 遍历指定路径下的子文件夹
    for root, dirs, files in os.walk(filePath):
        if not dirs:
            torrent_files = [file for file in files if file.endswith('.torrent')]
            if len(torrent_files) == 1:
                print(os.path.join(root, torrent_files[0]), os.path.join(root, root.split('\\')[-1] + '.torrent'))
                os.rename(os.path.join(root, torrent_files[0]), os.path.join(root, root.split('\\')[-1] + '.torrent'))
            else:
                print(root, ' | 种子文件不唯一，跳过')
                continue

def find_max_prefix(arr):
    """
    查找公共前缀
    :param arr: 文件列表
    :return: 最大公共前缀
    """
    if not arr:
        return "arr is empty or null"
    # arr = [os.path.splitext(s)[0].upper().replace(' ', '') for s in arr]
    arr = [os.path.splitext(s)[0] for s in arr]
    print(arr)
    max_prefix = arr[0]
    for s in arr[1:]:
        i = 0
        while i < len(max_prefix) and i < len(s) and max_prefix[i] == s[i]:
            i += 1
        max_prefix = max_prefix[:i]
    for file in arr:
        if len(file) - len(max_prefix) > 2:
            print('公共前缀:<' + max_prefix + '>,长度超过2')
            return False
    return max_prefix

def mkdir_and_movefile(filePath):
    """
    为视频文件创建文件夹
    扫描路径下视频文件，并创建同名的文件夹
    :param filePath:
    :return:
    """
    records = []
    fileList = [file for file in os.listdir(filePath)]
    # print(fileList)
    for file in fileList:
        # print(file)
        oldFilePath = os.path.join(filePath, file)
        newDir = os.path.splitext(oldFilePath)[0]
        if not os.path.exists(newDir):
            # print(newDir, '不存在，可以创建')
            os.makedirs(newDir)
        newFilePath = os.path.join(newDir, file)
        if not os.path.exists(newFilePath):
            # print(newFilePath, '不存在,可以移动')
            shutil.move(oldFilePath, newFilePath)
            print('移动记录：', oldFilePath, '————>', newFilePath)
            records.append({'oldFilePath': oldFilePath, 'newFilePath': newFilePath})
    user_input = input('y（确认移动），n（回滚）:')
    if user_input == 'y':
        print('确认移动')
        exit()
    elif user_input == 'n':
        for item in records:
            # print(item['newFilePath'], item['oldFilePath'])
            shutil.move(item['newFilePath'], item['oldFilePath'])


if __name__ == '__main__':
    start_time = time.time()
    filePath = r'C:\Users\Czzzw\Desktop\测试'
    # failed_path = r'E:\完美\0-刮削\failed'
    # renameTorrent(filePath)
    # renameDir(filePath)
    # check_mp4_and_nfo_files(filePath, failed_path)
    # renameNfo(filePath)
    # updateNfo(filePath, 'num', '1')
    # mkdir_and_movefile(filePath)









    end_time = time.time()
    print('程序运行时间：', (end_time - start_time) * 1000, 'ms')
