import json
import os
import argparse


def get_department_json(year):
    with open(f"../{year}-assets/department_description.json", "r", encoding="utf-8") as f:
        department_description = json.load(f)
    files = list(os.walk(f"../{year}-assets/members-photos"))[0][2]
    files = [i for i in files if i.endswith(".jpg")] # 过滤掉非jpg文件
    members = sorted([i.split(".")[0].split("-") for i in files])
    members_grouped = {}
    # 处理成员信息
    for department, name, position in members:
        if department not in members_grouped:
            members_grouped[department] = {"members": {}}
        members_grouped[department]["members"][name] = {
            "position": position,
            # 这个photoSrc其实前端用不到，但是这里保留用来放方便排序与返回图片的时候拼接路径。
            "photoSrc": "{}-{}-{}.jpg".format(department, name, position)
        }

    # 排序成员
    # 这里用负数是因为部员名字排序需要用到reverse=True，因此这里也把想要排在前面的职位的值设的更大
    order = {
        "主席": 0,
        "副主席": -1,
        "秘书": -2,
        "开发部部长": -3,
        "人事部部长": -4,
        "外联部部长": -5,
        "文体部部长": -6,
        "新媒体部部长": -7,
        "宣传部部长": -8,
        "学术部部长": -9,
        "职业发展部部长": -10,
        "研究生部部长": -11,
        "部长": -12,
        # 没有-13是因为这里给各种组长或其他职位留了个空位
        "部员": -14
    }
    for department, members_dict in members_grouped.items():
        members_grouped[department]["members"] = dict(
            sorted(members_grouped[department]["members"].items(),
                   key=lambda x: (
                       # 首先根据职位排序，如果职位在order里找不到就给默认值-11，说明这个人是部门内高于部员但是低于部长的职位。
                       order.get(x[1]["position"], -11),
                       # 然后根据名字排序。
                       x[1]["photoSrc"]
                   ), reverse=True)
        )

    for department, members_dict in members_grouped.items():
        department_description[department]["members"] = members_dict["members"]

            
    # 注意这里写入的是department.json而不是department_description.json。
    # 这是因为department_description.json是用来生成department.json的。
    with open(f"../{year}-assets/department.json", "w", encoding="utf-8") as f:
        json.dump(department_description, f, ensure_ascii=False, indent=4)
    print("脚本执行完毕")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process department JSON and photos.")
    parser.add_argument("year", type=str, help="year of the department photos")
    args = parser.parse_args()

    result = get_department_json(args.year)
    #print(result)
