# 修改任意文件的时间属性
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time  # 可以忽视这个 Time 报错（运行程序还是没问题的）
import time, os


def modifyFileTime(filePath, CreateTime, ModifyTime, AccessTime, offset):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param filePath: 文件路径名
    :param CreateTime: 创建时间
    :param ModifyTime: 修改时间
    :param AccessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    try:
        fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes_, accessTimes_, modifyTimes_ = GetFileTime(fh)

        format = "%Y-%m-%d %H:%M:%S"  # 时间格式

        createTimes = Time(time.mktime(timeOffsetAndStruct(CreateTime, format, offset[0]))) if CreateTime != "" else createTimes_
        accessTimes = Time(time.mktime(timeOffsetAndStruct(AccessTime, format, offset[2]))) if AccessTime != "" else accessTimes_
        modifyTimes = Time(time.mktime(timeOffsetAndStruct(ModifyTime, format, offset[1]))) if ModifyTime != "" else modifyTimes_

        SetFileTime(fh, createTimes, accessTimes, modifyTimes) if CreateTime != "" or AccessTime != "" or ModifyTime != "" else None
        CloseHandle(fh)
        return 0
    except:
        return 1


def timeOffsetAndStruct(times, format, offset):
    return time.localtime(time.mktime(time.strptime(times, format)) + offset)


if __name__ == '__main__':
    print("欢迎使用文件时间修改系统：")
    while True:
        dir_path = input("请输入文件所在目录的绝对路径（输入0退出）：")
        fNames = dir_path.replace('\\', '/', 100) if os.path.isdir(dir_path) else "./" if dir_path == "" else None
        if fNames:
            for filename in os.listdir(fNames):
                if not filename.startswith('~$') and not os.path.isdir(filename):
                    fName = os.path.join(dir_path, filename).replace('\\', '/')
                    print("")
                    print(f"要修改文件 {filename} 的时间属性")
                    # 需要自己配置
                    cTime = input("请输入要修改为的文件创建时间（格式为 2022-02-13 16:51:02）：")  # 创建时间
                    mTime = input("请输入要修改为的文件修改时间（格式为 2022-03-02 09:01:03）：")  # 修改时间
                    aTime = input("请输入要修改为的文件访问时间（格式为 2022-03-02 09:05:04）：")  # 访问时间

                    offset = (0, 1, 2)  # 偏移的秒数（不知道干啥的）

                    # 调用函数修改文件创建时间，并判断是否修改成功
                    r = modifyFileTime(fName, cTime, mTime, aTime, offset)
                    if r == 0:
                        print('修改完成')
                    elif r == 1:
                        print('修改失败')
        elif dir_path == "0":
            print("欢迎再次使用文件时间修改系统！")
            break
        else:
            print("您输入路径有误，请重新输入：")
