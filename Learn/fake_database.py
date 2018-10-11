# 使用shelve实现简易的数据库学生信息
import sys, shelve

path = r"E:\datapy\fake_database.dat"

def store_info(db):
    """
    让用户输入信息储存到shelve中
    :param db:
    :return:
    """
    IDnum = input("请输入学号：")
    # 用字典储存学生信息
    student = {}
    student["name"] = input("请输入姓名：")
    student["sex"] = input("请输入性别：")
    student["major"] = input("请输入专业：")
    db[IDnum] = student

def find_student(db):
    """
    通过学号，查看学生信息
    :param db:
    :return:
    """
    try:
        IDnum = input("请输入学号：")
        print("姓名:", db[IDnum]["name"])
        print("性别:", db[IDnum]["sex"])
        print("专业:", db[IDnum]["major"])
        print(db)
        print(type(db))
        print(type(db[IDnum]))
        print(type(db[IDnum]["name"]))
    except:
        print("没找到")


def help_info():
    print("目前有如下指令：")
    print("store:表示储存新的信息")
    print("find:查看已有信息")
    print("exit:退出系统")
    print("?:查看指令提示")

def enter_command():
    cmd = input("Enter command(? for help):")
    cmd = cmd.strip()
    return cmd

if __name__ == '__main__':
    database = shelve.open(path)
    try:
        while True:
            cmd = enter_command()
            if cmd == "store":
                store_info(database)
            elif cmd == "find":
                find_student(database)
            elif cmd == "exit":
                database.close()
                sys.exit()
            elif cmd == "?" or cmd == "？":
                help_info()
    except:
        database.close()

