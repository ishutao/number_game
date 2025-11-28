import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_title(title="数字游戏"):
    clear_screen()
    print("=" * 50)
    print(f"{' ' * 15}{title}{' ' * 15}")
    print("=" * 50)
    print()


def print_menu(options, title="请选择"):
    print_title(title)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")


def main_menu():
    options = [
        "开始游戏",
        "继续游戏",
        "游戏详情",
        "存档管理",
        "设置菜单"
    ]
    print_menu(options, "主菜单")
    print("0. 退出游戏")
    print()

    while True:
        try:
            choice = int(input("请输入您的选择 (0-5): "))
            if 0 <= choice <= 5:
                return choice
            else:
                print("输入无效，请输入0-5之间的数字")
        except ValueError:
            print("输入无效，请输入数字")


def game_mode_menu():
    options = [
        "猜数字",
        "Boss挑战",
        "闯关挑战"
    ]
    print_menu(options, "选择游戏模式")
    print("0. 返回主菜单")
    print()

    while True:
        try:
            choice = int(input("请输入您的选择 (0-3): "))
            if 0 <= choice <= 3:
                return choice
            else:
                print("输入无效，请输入0-3之间的数字")
        except ValueError:
            print("输入无效，请输入数字")


def print_game_info():
    print_title("游戏详情")
    print("数字游戏包含以下几种模式：\n")
    print("1. 猜数字：")
    print("   系统随机生成一个数字，玩家需要在限定次数内猜中。")
    print("   根据猜测的准确度获得不同的分数奖励。\n")
    print("2. Boss挑战：")
    print("   面对强大的Boss，通过解决数字谜题来击败它。")
    print("   每个Boss有不同的难度和特殊能力。\n")
    print("3. 闯关挑战：")
    print("   包含多个关卡，每关有不同的数字游戏任务。")
    print("   随着关卡提升，难度逐渐增加。\n")
    input("按回车键返回主菜单...")


def print_no_saved_game():
    print_title()
    print("目前没有未完成的游戏存档！")
    print("请先开始一个新游戏。")
    input("\n按回车键返回主菜单...")


def print_game_selected(game_name):
    print_title(f"{game_name}")
    print(f"即将进入{game_name}模式...")
    print("游戏逻辑尚未实现，敬请期待！")
    input("\n按回车键返回...")


def print_thank_you():
    clear_screen()
    print("=" * 50)
    print(f"{' ' * 10}感谢您游玩数字游戏！{' ' * 10}")
    print(f"{' ' * 15}再见！{' ' * 15}")
    print("=" * 50)
    input("按回车键退出...")


def difficulty_menu():
    options = [
        "简单 (1-250)",
        "普通 (1-500)",
        "困难 (1-750)",
        "地狱 (1-1000)",
    ]
    print_menu(options, "选择难度")
    print("0. 返回")
    print()

    while True:
        try:
            choice = int(input("请输入您的选择 (0-4): "))
            if 0 <= choice <= 4:
                return choice
            else:
                print("输入无效，请输入0-4之间的数字")
        except ValueError:
            print("输入无效，请输入数字")


def print_guess_number_start(difficulty, range_max):
    print_title(f"猜数字游戏 - {difficulty}")
    print(f"游戏规则：")
    print(f"1. 系统将随机生成一个{1}-{range_max}之间的整数")
    print(f"2. 每次猜测后，系统会提示您的猜测是偏大还是偏小")
    print(f"3. 猜对后游戏结束")
    print()
    input("准备就绪！按回车键开始游戏...")


def get_guess(range_min, range_max):
    while True:
        try:
            guess = int(input(f"请输入您的猜测 ({range_min}-{range_max}): "))
            if range_min <= guess <= range_max:
                return guess
            else:
                print(f"请输入{range_min}-{range_max}之间的数字")
        except ValueError:
            print("输入无效，请输入数字")


def print_guess_result(guess, target):
    if guess < target:
        print(f"{guess} 太小了！")
    elif guess > target:
        print(f"{guess} 太大了！")
    else:
        print(f"恭喜您！猜对了！答案就是 {target}！")

    if guess != target:
        print()


def print_game_over(is_win, target, range_max, used_attempts):
    print("=" * 50)
    if is_win:
        print(f"{' ' * 15}恭喜获胜！{' ' * 15}")
        print(f"您用了 {used_attempts} 次就猜对了！")
        # 计算得分（根据剩余次数）
        remaining = range_max - used_attempts
        score = remaining * 100
        print(f"本次得分：{score} 分")
    else:
        print(f"{' ' * 15}游戏结束{' ' * 15}")
        print(f"很遗憾，您没有在限定次数内猜对。")
        print(f"正确答案是：{target}")
    print("=" * 50)
    print()


def ask_play_again():
    while True:
        choice = input("是否再玩一次？(y/n): ").lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("输入无效，请输入 y 或 n")


def boss_challenge_menu():
    clear_screen()
    options = [
        "开始Boss挑战"
    ]
    print(""""\n" + "=" * 50
            Boss挑战模式
        "=" * 50
        在Boss挑战模式中，你将面对强大的Boss！
        根据你的猜测和敌人血量决定战斗结果。
        "=" * 50""")
    print_menu(options, "Boss挑战模式")
    print("0. 返回主菜单")
    print()

    while True:
        try:
            choice = int(input("请输入您的选择 (0-1): "))
            if 0 <= choice <= 1:
                return choice
            else:
                print("输入无效，请输入0-1之间的数字")
        except ValueError:
            print("输入无效，请输入数字")


def saves_management_menu():
    clear_screen()
    options = [
        "查看存档列表",
        "重命名存档",
        "复制存档",
        "删除存档",
        "清理旧存档",
        "备份所有存档",
        "验证存档完整性",
        "批量加密未加密存档"
    ]
    print_menu(options, "存档管理")
    print("0. 返回主菜单")
    print()
    while True:
        try:
            choice = int(input("请选择操作 (0-9): "))
            if 0 <= choice <= 9:
                return choice
            else:
                print("输入无效，请输入0-9之间的数字")
        except ValueError:
            print("输入无效，请输入数字")
