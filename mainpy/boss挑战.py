from datetime import datetime
from random import randint

from UI界面 import clear_screen, print_title
from 存档位置 import GAME_TYPE_BOSS_CHALLENGE
# 导入存档相关模块
from 存档管理 import save_game

DEFAULT_EXIT_COMMANDS = ['q', 'qw', 'quit', 'exit']

ENEMY_DATA = {
    '简单': {
        'boss': {
            'name': '巨型史莱姆王', 'hp': 50, 'defense': 2, 'accuracy': 0.7, 'type': 'boss',
            'skill': '分裂攻击', 'skill_desc': '有20%几率连续攻击两次'
        }
    },
    '普通': {
        'boss': {
            'name': '哥布林王', 'hp': 80, 'defense': 3, 'accuracy': 0.8, 'type': 'boss',
            'skill': '召唤增援', 'skill_desc': '有30%几率恢复10点生命值'
        }
    },
    '困难': {
        'boss': {
            'name': '黑暗巫师', 'hp': 120, 'defense': 4, 'accuracy': 0.85, 'type': 'boss',
            'skill': '黑暗魔法', 'skill_desc': '有25%几率造成双倍伤害'
        }
    },
    '地狱': {
        'boss': {
            'name': '远古巨龙', 'hp': 200, 'defense': 5, 'accuracy': 0.75, 'type': 'boss',
            'skill': '龙息喷吐', 'skill_desc': '有20%几率造成三倍伤害，同时恢复20点生命值'
        }
    }
}


def create_game_config(hp, range_max, game_mode, luck_rate, exit_commands=None):
    if exit_commands is None:
        exit_commands = DEFAULT_EXIT_COMMANDS

    return {
        'hp': hp,
        'range_max': range_max,
        'game_mode': game_mode,
        'luck_rate': luck_rate,
        'exit_commands': exit_commands,
        'enemy_data': ENEMY_DATA
    }


def update_range(min_num, max_num, guess, target_num):
    try:
        guess_num = int(guess)
        if target_num > guess_num > min_num:
            return guess_num, max_num
        elif target_num < guess_num < max_num:
            return min_num, guess_num
    except ValueError:
        pass
    return min_num, max_num


def create_battle_scene(enemy_type, enemy_name):
    if enemy_type == 'boss':
        return f"\n⚠️ ⚠️ ⚠️ 终极挑战！你来到了{enemy_name}的领地！这将是一场艰难的战斗！⚠️ ⚠️ ⚠️"
    else:
        return f"\n战斗开始！你遇到了敌人：{enemy_name}"


def boss_battle(config):
    # 从配置中提取参数
    player_hp = config['hp']
    range_max = config['range_max']
    game_mode = config['game_mode']
    exit_commands = config.get('exit_commands', DEFAULT_EXIT_COMMANDS)
    enemy_data = config.get('enemy_data', ENEMY_DATA)

    if game_mode in enemy_data:
        current_enemies = enemy_data[game_mode]
        enemy = current_enemies['boss']
    else:
        enemy = {
            'name': '神秘怪物',
            'hp': randint(10, 30),
            'type': 'minion'
        }

    clear_screen()
    print_title(f"boss挑战 - {enemy['name']}")
    print(f"\n=== 战斗开始 ===")
    print(f"敌人信息：{enemy['name']} (HP: {enemy['hp']})")
    print(f"你的状态：生命值: {player_hp}")

    if 'skill' in enemy:
        print(f"Boss技能：{enemy['skill']} - {enemy['skill_desc']}")

    enemy_hp = enemy['hp']
    attack_count = 0
    damage_taken = 0

    target_num = randint(1, range_max)
    min_num = 1
    max_num = range_max

    print(create_battle_scene('boss' if enemy.get('type') == 'boss' else 'minion', enemy['name']))
    print(f"战斗规则：根据你的猜测和敌人血量决定战斗结果")
    print(f"初始数字范围：{min_num}~{max_num}")

    while player_hp > 0 and enemy_hp > 0:
        user_input = input(f"\n请输入你猜的数字（范围是{min_num}~{max_num}），你的血量：{player_hp}，敌人血量：{enemy_hp}：")

        if user_input.lower() in exit_commands:
            print("游戏已退出")
            return {'success': False, 'remaining_hp': player_hp, 'enemy_hp': enemy_hp, 'target_num': target_num,
                    'min_num': min_num, 'max_num': max_num}

        try:
            guess_num = int(user_input)
            if not (min_num <= guess_num <= max_num):
                print("数字超出范围！")
                player_hp -= 10
                continue
        except ValueError:
            print("请输入有效的数字！")
            continue

        if guess_num == target_num:
            print("🎉 恭喜你猜对了！给予敌人致命一击！")
            enemy_hp = 0
            break
        else:
            min_num, max_num = update_range(min_num, max_num, user_input, target_num)

            attack_count += 1
            print(f"第{attack_count}次攻击：")

            distance = abs(guess_num - target_num)
            damage_dealt = max(10, 50 - distance * 2)
            enemy_hp -= damage_dealt
            print(f"⚔️ 你发动了攻击，造成{damage_dealt}点伤害！敌人剩余血量：{enemy_hp}")

            player_damage = 5
            player_hp -= player_damage
            damage_taken += player_damage
            print(f"⚡ 敌人反击！你受到{player_damage}点伤害！剩余血量：{player_hp}")

    if player_hp <= 0:
        print(f"\n💀 战斗失败！你被{enemy['name']}击败了！")
        print(f"正确答案是：{target_num}")
        return {'success': False, 'remaining_hp': 0, 'attack_count': attack_count, 'damage_taken': damage_taken,
                'enemy_name': enemy['name']}
    else:
        print(f"\n🎉 战斗胜利！你成功击败了{enemy['name']}！")
        print(f"战斗统计：")
        print(f"- 攻击次数：{attack_count}次")
        print(f"- 受到伤害：{damage_taken}点")
        print(f"- 剩余生命值：{player_hp}点")

        return {'success': True, 'remaining_hp': player_hp, 'attack_count': attack_count, 'damage_taken': damage_taken,
                'enemy_name': enemy['name']}


def start_boss_challenge(save_data=None):
    boss_choices = {
        '1': {'name': '巨型史莱姆王', 'difficulty': '简单'},
        '2': {'name': '哥布林王', 'difficulty': '普通'},
        '3': {'name': '黑暗巫师', 'difficulty': '困难'},
        '4': {'name': '远古巨龙', 'difficulty': '地狱'}
    }

    clear_screen()
    print_title("boss挑战 - 选择boss")
    print("\n请选择要挑战的Boss:")
    for key, boss in boss_choices.items():
        print(f"{key}. {boss['name']} ({boss['difficulty']})")
    print(f"\n输入{DEFAULT_EXIT_COMMANDS}退出")

    while True:
        choice = input("\n请选择Boss (1-4): ").strip()
        if choice in boss_choices:
            selected_boss = boss_choices[choice]
            player_hp = 50
            range_max = 250
            break
        elif choice.lower() in DEFAULT_EXIT_COMMANDS:
            print("游戏已退出")
            return False
        else:
            print("无效的选择，请重新输入。")

    try:
        game_config = create_game_config(player_hp, range_max, selected_boss['difficulty'], 0.05)

        save_name = f"boss_{selected_boss['name']}_{datetime.now().strftime('%Y%m%d')}"
        game_data = {
            'game_type': GAME_TYPE_BOSS_CHALLENGE,
            'game_name': 'Boss挑战',
            'difficulty': selected_boss['difficulty'],
            'boss_name': selected_boss['name'],
            'player_hp': player_hp,
            'range_max': range_max,
            'start_time': datetime.now().isoformat()
        }

        save_game(save_name, game_data)
        print(f"\n游戏已保存为: {save_name}")

        result = boss_battle(game_config)

        game_data['end_time'] = datetime.now().isoformat()
        game_data['success'] = result.get('success', False)
        game_data['remaining_hp'] = result.get('remaining_hp', 0)
        game_data['attack_count'] = result.get('attack_count', 0)
        game_data['damage_taken'] = result.get('damage_taken', 0)
        game_data['enemy_name'] = result.get('enemy_name', '')

        save_game(save_name, game_data)

        if result and result.get('success'):
            print("\n🎉 游戏胜利！")
            save_game(save_name, game_data)
            print(f"\n游戏已保存为: {save_name}")
        else:
            print("\n💀 游戏失败！")

        while True:
            play_again = input("\n是否重新开始游戏？(y/n): ").strip().lower()
            if play_again == 'y':
                return start_boss_challenge()
            elif play_again == 'n':
                print("感谢游玩，再见！")
                return result.get('success', False)
            else:
                print("请输入 'y' 或 'n'")

    except Exception as e:
        print(f"游戏过程中发生错误: {str(e)}")
        input("按回车键退出...")
        return False
    except KeyboardInterrupt:
        print("\n游戏被中断")
        return False


def continue_boss_challenge(save_data):
    difficulty = save_data.get('difficulty', '普通')
    player_hp = 50
    range_max = 250

    game_config = create_game_config(player_hp, range_max, difficulty, 0.05)

    clear_screen()
    print(f"\n=== 继续Boss挑战 ===")
    print(f"难度: {difficulty}")
    print(f"剩余生命值: {player_hp}")
    print(f"数字范围: 1~{range_max}")
    if 'boss_name' in save_data:
        print(f"挑战Boss: {save_data['boss_name']}")

    result = boss_battle(game_config)

    save_data['end_time'] = datetime.now().isoformat()
    save_data['success'] = result.get('success', False)
    save_data['remaining_hp'] = result.get('remaining_hp', 0)
    save_data['attack_count'] = result.get('attack_count', 0)
    save_data['damage_taken'] = result.get('damage_taken', 0)
    save_data['enemy_name'] = result.get('enemy_name', '')

    save_name = save_data.get('save_name', f"boss_{difficulty}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    save_game(save_name, save_data)

    return result.get('success', False)


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("            Boss挑战模式            ")
    print("=" * 50)
    print("在Boss挑战模式中，你将面对强大的Boss！")
    print("玩家固定血量：50")
    print("数字范围：1~250")
    print("输入正确的数字将直接击败敌人！")
    print("=" * 50)

    start_boss_challenge()
