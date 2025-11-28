import random
import time

from UI界面 import (
    difficulty_menu,
    print_guess_number_start,
    get_guess,
    print_guess_result,
    print_game_over,
    ask_play_again
)
from 存档位置 import (
    GAME_TYPE_GUESS_NUMBER,
    is_level_unlocked
)
from 继续游戏 import save_game

DIFFICULTY_SETTINGS = {
    1: {'name': '简单', 'range': 250},
    2: {'name': '普通', 'range': 500},
    3: {'name': '困难', 'range': 750},
    4: {'name': '地狱', 'range': 1000}
}


def guess_number_game():
    while True:
        # 选择难度
        diff_choice = difficulty_menu()

        if diff_choice == 0:
            break

        if diff_choice > 1 and not is_level_unlocked(diff_choice):
            print(f"\n❌ 错误：难度等级 {diff_choice} 尚未解锁！")
            print("请先完成前面的难度等级解锁新内容。")
            time.sleep(2)
            continue

        settings = DIFFICULTY_SETTINGS[diff_choice]
        difficulty_name = settings["name"]
        range_max = settings["range"]

        print_guess_number_start(difficulty_name, range_max)

        target_number = random.randint(1, range_max)
        attempts_used = 0
        is_won = False

        while True:
            guess = get_guess(1, range_max)
            attempts_used += 1

            print_guess_result(guess, target_number)

            if guess == target_number:
                is_won = True
                break

        print_game_over(is_won, target_number, range_max, attempts_used)

        if is_won:
            game_state = {
                'game_type': GAME_TYPE_GUESS_NUMBER,
                'game_name': '猜数字',
                "difficulty": diff_choice,
                "difficulty_name": difficulty_name,
                "target_number": target_number,
                "attempts_used": attempts_used,
                "is_won": is_won,
                "score": (range_max - attempts_used) * 100
            }
            save_game(GAME_TYPE_GUESS_NUMBER, game_state)

        if not ask_play_again():
            break


def continue_guess_number(saved_data):
    try:
        game_state = saved_data.get('game_state', {})
        difficulty = game_state.get('difficulty', 2)
        difficulty_name = game_state.get('difficulty_name', '普通')
        attempts_used = game_state.get('attempts_used', 0)
        is_won = game_state.get('is_won', False)
        target_number = game_state.get('target_number', random.randint(1, 500))
        range_max = DIFFICULTY_SETTINGS.get(difficulty, {}).get('range', 500)

        print(f"\n=== 继续游戏 ===")
        print(f"难度：{difficulty_name}")
        if is_won:
            print(f"恭喜您！您之前猜对了数字 {target_number}！")
        else:
            print(f"您之前猜的数字是 {target_number}，请继续猜数字游戏。")
        print(f"数字范围：1-{range_max}")
        print(f"已使用尝试次数：{attempts_used}")

        attempts = attempts_used

        while not is_won:
            guess = get_guess(1, range_max)
            attempts += 1

            print_guess_result(guess, target_number, attempts_used)

            if guess == target_number:
                is_won = True
                break

        print_game_over(is_won, target_number, range_max, attempts_used)

        if is_won:
            game_state = {
                'game_type': GAME_TYPE_GUESS_NUMBER,
                'game_name': '猜数字',
                "difficulty": difficulty,
                "difficulty_name": difficulty_name,
                "target_number": target_number,
                "attempts_used": attempts_used,
                "is_won": is_won,
                "score": (range_max - attempts_used) * 100
            }
            save_game(GAME_TYPE_GUESS_NUMBER, game_state)

        if ask_play_again():
            guess_number_game()

        return True
    except Exception as e:
        print(f"加载游戏失败: {e}")
        input("按回车键返回...")
        return False
