import os
import json


# 接收path与Original_file
def writeRelo(path, Original_file, Remote_login_account, Service_Provider="天翼云盘"):
    """

    :param path:路径
    :param Original_file:自身（原本）文件名
    :param Service_Provider:服务商
    :param Client_or_Web:客户端还是网页还是两者都可以
    :param Remote_login_account:
    :return:
    """
    global linkfilename
    quanname = os.path.join(path, Original_file)
    # # 判断是文件还是目录
    Directory_or_file = "f" if os.path.isfile(quanname) else "d"
    Size = getSize_t(os.path.getsize(quanname))
    # 提取出原文件类型
    extension = Original_file.split(".")[-1]
    item = {
        "Original_file": Original_file,
        "Service_Provider": Service_Provider,
        "Remote_login_account": Remote_login_account,
        "Directory_or_file": Directory_or_file,
        "Size": Size,
        "Main_file_extension": extension
    }
    # 链接文件（文件链接后缀为cllo）
    linkfilename = quanname + ".cllo"
    if os.path.exists(linkfilename) and not cover:
        # 如果已经有此链接文件了，并且没开启覆盖，则不重新执行了
        print("遇到了个已经存在链接文件的文件，且没有开启处理")
    else:
        # 否则重新执行
        print("覆盖/新建")
        with open(linkfilename, "w+") as f:
            f.write(json.dumps(item, ensure_ascii=False, indent=4))
    if remove:
        os.remove(quanname)


def getSize_t(size):
    for i in unit:
        if size < 1024:
            return ("{}" + i).format(round(size, 2))
        else:
            size /= 1024


def run(path):
    global recursivenum
    listdir = os.listdir(path)
    for name in listdir:
        # 根据文件名判断是不是已创建的文件链接
        quanpath = os.path.join(path, name)
        if os.path.isfile(quanpath):
            if ".cllo" not in name:
                print("正常文件：" + name)
                writeRelo(path, name, info)
                print("写入链接文件成功")
                # 如果是文件，则创建文件链接
            else:
                print("遇到的已完成的链接文件：" + name)
        elif os.path.isdir(quanpath):
            # 如果是目录
            if recursive and recursivenum < recursiveMaxnum:
                # 如果是目录，且开启了递归执行
                # 如果开递归处理了，并且小于最大递归层数
                print("进入下一层")
                recursivenum += 1
                # 如果不是文件，则执行
                run(quanpath)
            elif recursive:
                # 如果仅仅可以递归，但是不能再次递归了
                # 不能再深入的时候就把目录给处理
                writeRelo(path, name, info)
                ...
            else:
                if processdir:
                    print("遇到目录，处理")
                    writeRelo(path, name, info)
                else:
                    print("遇到目录，但未开启处理")
                    continue
            # # 其余情况正常处理
            # writeRelo(path, name, "手机号-187540******")
        print("返回上一层")
        recursivenum -= 1


if __name__ == "__main__":
    # input("将会删除文件，请注意，不允许请按Ctrl+C")
    # 设置字节计量单位
    unit = ["B", "KB", "MB", "GB", "TB"]
    # 设置是否递归执行
    recursive = True
    # 如果没有开启递归，那么遇到目录是否处理
    processdir = False
    # 若开启递归，则深入多少层停止深入
    recursiveMaxnum = 1
    # 如果已有链接文件，是否用新的进行覆盖
    cover = True
    # 设置创建完成文件链接之后（或者存在链接文件）删除文件
    remove = False

    # 递归层数初始化
    recursivenum = 0

    info="手机号-187540******"
    path = r""
    run(path)
