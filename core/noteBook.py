
def makeDirs(filePath):
    """
    为路径下所有视频文件创建同名的文件夹
    """
    if os.path.isdir(filePath):
        for item in os.listdir(filePath):
            itemPath = os.path.join(filePath, item)
            if os.path.isdir(itemPath):
                continue
            if :
                os.mkdir(itemPath)

def moveFiles(filePath):
    """
    将路径下所有视频文件移动到同名的文件夹中
    """
    if os.path.isdir(filePath):
        for item in os.listdir(filePath):
            itemPath = os.path.join(filePath, item)
            if os.path.isdir(itemPath):
                continue
            os.rename(itemPath, os.path.join(itemPath, item))