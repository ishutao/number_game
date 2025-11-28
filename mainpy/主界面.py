from UI界面 import (
    main_menu,
    game_mode_menu,
    print_game_info,
    print_game_selected,
    print_thank_you,
    saves_management_menu,
)
from boss挑战 import continue_boss_challenge, start_boss_challenge
from 存档位置 import unlock_all_levels, lock_all_levels, load_unlock_status
from 存档管理 import (
    list_saves_with_details,
    manage_saves
)
from 猜数字 import guess_number_game, continue_guess_number
from 继续游戏 import continue_game, load_saved_game
from 闯关模式 import adventure_mode, continue_adventure


def start_new_game():
    while True:
        # 显示游戏模式选择菜单
        mode_choice = game_mode_menu()

        if mode_choice == 0:
            break

        game_modes = {
            1: "猜数字",
            2: "Boss挑战",
            3: "闯关挑战"
        }

        if mode_choice == 1:
            guess_number_game()
        elif mode_choice == 2:
            start_boss_challenge()
        elif mode_choice == 3:
            adventure_mode()
        else:
            game_name = game_modes.get(mode_choice)
            print_game_selected(game_name)

        break


def settings_menu():
    while True:
        print("\n" + "=" * 50)
        print("                    设置菜单")
        print("=" * 50)
        print("1. 一键解锁所有关卡")
        print("2. 锁定所有关卡（除第一关外）")
        print("3. 查看解锁状态")
        print("4. 快速管理存档")
        print("0. 返回主菜单")
        print("=" * 50)

        try:
            choice = int(input("请输入您的选择 (0-4): "))

            if choice == 1:
                confirm = input("确定要解锁所有关卡吗？(y/n): ")
                if confirm.lower() == 'y':
                    if unlock_all_levels():
                        print("\n✓ 所有关卡已成功解锁！")
                    else:
                        print("\n✗ 解锁失败，请稍后重试。")
                else:
                    print("\n已取消操作。")

            elif choice == 2:
                confirm = input("确定要锁定所有关卡吗？这将重置您的游戏进度。(y/n): ")
                if confirm.lower() == 'y':
                    if lock_all_levels():
                        print("\n✓ 所有关卡已成功锁定，仅保留第一关可用。")
                    else:
                        print("\n✗ 锁定失败，请稍后重试。")
                else:
                    print("\n已取消操作。")

            elif choice == 3:
                status = load_unlock_status()
                print("\n当前解锁状态:")
                print(f"- 是否所有内容都已解锁: {'是' if status['all_unlocked'] else '否'}")
                print(f"- 已解锁关卡: {', '.join(map(str, status['levels_unlocked']))}")
                print(f"- 最后更新时间: {status['last_updated']}")

            elif choice == 4:
                saves_management_menu()

            elif choice == 0:
                break

            else:
                print("\n输入错误，请输入1-5之间的数字。")

        except ValueError:
            print("\n输入错误，请输入有效的数字。")

        input("\n按Enter键继续...")


def main():
    while True:
        choice = main_menu()

        if choice == 1:
            start_new_game()
        elif choice == 2:
            save_list = list_saves_with_details()
            if save_list:
                try:
                    print("\n可用存档:")
                    for i, save in enumerate(save_list, 1):
                        print(f"{i}. {save['name']} - {save['game_name']} ({save['save_time']})")

                    save_choice = int(input("\n请选择要加载的存档 (1-" + str(len(save_list)) + ", 0返回): "))
                    if 1 <= save_choice <= len(save_list):
                        save_name = save_list[save_choice - 1]['name']
                        print(f"\n正在加载存档: {save_name}")
                        saved_data = load_saved_game(save_name)
                        if saved_data:
                            game_type = saved_data.get('game_type', 0)
                            if game_type == 1:  # 猜数字游戏
                                continue_guess_number(saved_data)
                            elif game_type == 2:  # Boss挑战
                                continue_boss_challenge(saved_data)
                            elif game_type == 3:  # 闯关挑战
                                continue_adventure(saved_data)
                            else:
                                continue_game(save_name)
                    elif save_choice == 0:
                        continue
                except ValueError:
                    print("输入错误，加载默认存档。")

            saved_data = load_saved_game()
            if saved_data:
                game_type = saved_data.get('game_type', 0)
                if game_type == 1:
                    continue_guess_number(saved_data)
                elif game_type == 2:
                    continue_boss_challenge(saved_data)
                elif game_type == 3:
                    continue_adventure(saved_data)
                else:
                    continue_game()
            else:
                continue_game()

        elif choice == 3:
            print_game_info()

        elif choice == 4:
            manage_saves()

        elif choice == 5:
            settings_menu()

        elif choice == 0:
            print_thank_you()
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n游戏已中断")
    except Exception as e:
        print(f"发生错误: {e}")
        input("按回车键退出...")
