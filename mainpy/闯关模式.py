import datetime
import json
import os
import random

from UI界面 import (
    print_title,
    get_guess,
    print_guess_result,
    clear_screen
)
from 存档位置 import load_unlock_status

# 动态存档文件路径（包含时间戳）
timestamp = datetime.datetime.now().strftime("%Y%m%d")
SAVE_FILE = f"../saves/adventure_save_{timestamp}.json"


# 玩家类
class Player:
    def __init__(self):
        # 固定初始属性
        self.hp = 100
        self.max_hp = 100
        self.strength = 10
        self.defense = 5
        self.level = 1
        self.exp = 0
        self.current_map = None
        self.current_level = 1
        self.completed_levels = []
        self.current_room = None

    def show_stats(self):
        print(f"\n玩家属性：")
        print(f"生命值：{self.hp}/{self.max_hp}")
        print(f"力量：{self.strength}")
        print(f"防御力：{self.defense}")
        print(f"等级：{self.level}")
        print(f"经验值：{self.exp}")

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        return amount

    def gain_exp(self, exp):
        self.exp += exp
        if self.exp >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.strength += 3
        self.defense += 2
        print(f"\n恭喜升级！当前等级：{self.level}")

    def increase_stats(self, strength=0, defense=0, max_hp=0):
        self.strength += strength
        self.defense += defense
        self.max_hp += max_hp
        self.hp = self.max_hp

    def save_progress(self, map_id, level_id, completed_rooms):
        save_data = {
            "player": {
                "hp": self.hp,
                "max_hp": self.max_hp,
                "strength": self.strength,
                "defense": self.defense,
                "level": self.level,
                "exp": self.exp
            },
            "current_map": map_id,
            "current_level": level_id,
            "completed_levels": self.completed_levels,
            "completed_rooms": completed_rooms
        }

        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

        print(f"\n游戏进度已保存！")

    def load_progress(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            player_data = save_data.get("player", {})
            self.hp = player_data.get("hp", 100)
            self.max_hp = player_data.get("max_hp", 100)
            self.strength = player_data.get("strength", 10)
            self.defense = player_data.get("defense", 5)
            self.level = player_data.get("level", 1)
            self.exp = player_data.get("exp", 0)

            self.current_map = save_data.get("current_map")
            self.current_level = save_data.get("current_level", 1)
            self.completed_levels = save_data.get("completed_levels", [])

            return save_data.get("completed_rooms", [])
        return []


class Enemy:
    def __init__(self, name, hp, strength, defense, exp_reward, enemy_type="normal"):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.strength = strength
        self.defense = defense
        self.exp_reward = exp_reward
        self.enemy_type = enemy_type

    def show_stats(self):
        print(f"\n敌人：{self.name}")
        print(f"生命值：{self.hp}/{self.max_hp}")
        print(f"力量：{self.strength}")
        print(f"防御力：{self.defense}")

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage


difficulty_database = {
    '简单': {'range': 250, 'ordinary_rate': 0.6, 'minions_rate': 0.3, 'luck_rate': 0.1},
    '普通': {'range': 500, 'ordinary_rate': 0.5, 'minions_rate': 0.45, 'luck_rate': 0.05},
    '困难': {'range': 750, 'ordinary_rate': 0.4, 'minions_rate': 0.57, 'luck_rate': 0.03},
    '地狱': {'range': 1000, 'ordinary_rate': 0.3, 'minions_rate': 0.69, 'luck_rate': 0.01}
}

enemy_database = {
    "slime": {
        "name": "数字史莱姆",
        "hp": 30,
        "strength": 8,
        "defense": 2,
        "exp_reward": 25,
        "enemy_type": "normal"
    },
    "goblin": {
        "name": "计算哥布林",
        "hp": 45,
        "strength": 12,
        "defense": 4,
        "exp_reward": 40,
        "enemy_type": "normal"
    },
    "wolf": {
        "name": "算法野狼",
        "hp": 60,
        "strength": 15,
        "defense": 6,
        "exp_reward": 55,
        "enemy_type": "normal"
    },
    "orc": {
        "name": "逻辑兽人",
        "hp": 80,
        "strength": 18,
        "defense": 8,
        "exp_reward": 70,
        "enemy_type": "normal"
    },
    "forest_boss": {
        "name": "森林守护者",
        "hp": 150,
        "strength": 25,
        "defense": 12,
        "exp_reward": 200,
        "enemy_type": "boss"
    },
    "mountain_boss": {
        "name": "山脉巨人",
        "hp": 200,
        "strength": 30,
        "defense": 15,
        "exp_reward": 300,
        "enemy_type": "boss"
    },
    "maze_boss": {
        "name": "迷宫之主",
        "hp": 250,
        "strength": 35,
        "defense": 18,
        "exp_reward": 400,
        "enemy_type": "boss"
    },
    "castle_boss": {
        "name": "算法之王",
        "hp": 300,
        "strength": 40,
        "defense": 20,
        "exp_reward": 500,
        "enemy_type": "boss"
    }
}

maps = {
    1: {
        "name": "数字森林",
        "description": "充满数字谜题的森林，适合新手探索",
        "difficulty": "简单",
        "levels": 3,
        "unlocked": True,
        "boss": "forest_boss"
    },
    2: {
        "name": "数学山脉",
        "description": "高耸的山脉，挑战更复杂的数字游戏",
        "difficulty": "普通",
        "levels": 4,
        "unlocked": False,
        "boss": "mountain_boss"
    },
    3: {
        "name": "逻辑迷宫",
        "description": "复杂的迷宫，需要敏锐的逻辑思维",
        "difficulty": "困难",
        "levels": 5,
        "unlocked": False,
        "boss": "maze_boss"
    },
    4: {
        "name": "算法城堡",
        "description": "终极挑战，只有真正的数字大师才能征服",
        "difficulty": "地狱",
        "levels": 6,
        "unlocked": False,
        "boss": "castle_boss"
    }
}


def generate_levels_for_map(map_id):
    levels = []
    map_info = maps.get(map_id)
    if not map_info:
        return levels

    rooms_count = difficulty_database[map_info['difficulty']]['range']

    for i in range(1, map_info['levels'] + 1):
        level = {
            "id": i,
            "name": f"关卡{i}",
            "description": f"这是{map_info['name']}的第{i}个关卡",
            "completed": False,
            "difficulty": "简单" if i <= 2 else "普通" if i <= 4 else "困难" if i <= 6 else "地狱",
            "rooms": [],
            "rooms_count": rooms_count
        }
        levels.append(level)

    return levels


def generate_rooms_for_level(level, map_info):
    rooms = []

    room_types = {
        "普通": difficulty_database[map_info['difficulty']]['ordinary_rate'] *
                difficulty_database[map_info['difficulty']]['range'],
        "小怪": difficulty_database[map_info['difficulty']]['minions_rate'] *
                difficulty_database[map_info['difficulty']]['range'],
        "幸运": difficulty_database[map_info['difficulty']]['luck_rate'] * difficulty_database[map_info['difficulty']][
            'range'],
        "boss": 1
    }

    for i in range(1, difficulty_database[map_info['difficulty']]['range'] + 1):
        room_type = random.choices(
            ["普通", "小怪", "幸运", "boss"],
            weights=[room_types["普通"], room_types["小怪"], room_types["幸运"], room_types["boss"]]
        )[0]

        battle_range = difficulty_database[map_info['difficulty']]['range']
        enemy = None
        if room_type == "小怪":
            enemy = random.choice(list(enemy_database.keys()))

        room = {
            "id": i,
            "name": f"房间{i}",
            "completed": False,
            "room_type": room_type,
            "description": f"这是{map_info['name']}的第{level['id']}个关卡的第{i}个房间",
            "battle_range": battle_range,
            "difficulty": level["difficulty"],
            "enemy": enemy
        }
        rooms.append(room)
    return rooms


def adventure_mode(saved_data=None):
    player = Player()

    if saved_data:
        completed_levels = saved_data.get('completed_levels', [])
        if isinstance(completed_levels, list):
            player.completed_levels = completed_levels

    while True:
        map_choice = select_map()
        if map_choice == 0:
            return

        player.current_map = map_choice
        levels = generate_levels_for_map(map_choice)

        while True:
            show_levels_info(map_choice, levels, player)

            print("\n请输入关卡号进入（输入0返回地图选择）：")
            try:
                level_choice = int(input("输入：").strip())

                if level_choice == 0:
                    break
                elif 1 <= level_choice <= len(levels):
                    current_level = levels[level_choice - 1]
                    player.current_level = level_choice

                    rooms = generate_rooms_for_level(current_level, maps[map_choice])
                    completed_rooms = []

                    while True:
                        clear_screen()
                        print_title(f"{maps[map_choice]['name']} - 共有{len(rooms)}个房间")
                        player.show_stats()

                        print("\n请输入房间号进入挑战（输入0返回关卡选择，输入s查看属性，输入save保存进度）：")
                        room_input = input("输入：").strip()

                        if room_input.lower() == 's':
                            player.show_stats()
                            continue
                        elif room_input.lower() == 'save':
                            player.save_progress(map_choice, level_choice, completed_rooms)
                            continue

                        try:
                            room_choice = int(room_input)

                            if room_choice == 0:
                                break
                            elif 1 <= room_choice <= len(rooms):
                                if room_choice in completed_rooms:
                                    print(f"\n房间{room_choice}已经完成！")
                                    input("\n按回车键继续...")
                                    continue

                                challenge_result = start_room_challenge(map_choice, current_level,
                                                                        rooms[room_choice - 1], player)
                                if challenge_result:
                                    completed_rooms.append(room_choice)
                                    print(
                                        f"""\n恭喜你完成了{maps[map_choice]['name']} - {current_level['name']}的第{room_choice}个房间！""")

                                    if rooms[room_choice - 1]["room_type"] == "boss":
                                        player.completed_levels.append(level_choice)
                                        print(f"\n🎉 恭喜你完成了整个{current_level['name']}！")

                                        player.save_progress(map_choice, level_choice, completed_rooms)

                                        input("\n按回车键继续...")
                                        break

                                    if player.hp <= 0:
                                        print("\n💀 游戏结束！你被击败了！")
                                        input("\n按回车键返回主菜单...")
                                        return
                            else:
                                print("输入无效，请输入有效房间号")
                        except ValueError:
                            print("输入无效，请输入数字")

                        input("\n按回车键继续...")
                else:
                    print("输入无效，请输入有效关卡号")
            except ValueError:
                print("输入无效，请输入数字")

            input("\n按回车键继续...")


def select_map():
    while True:
        print_title("闯关挑战 - 地图选择")

        unlock_status = load_unlock_status()
        unlocked_maps = unlock_status.get("levels_unlocked", [1])

        print("可用地图：")
        available_maps = []
        for map_id, map_info in maps.items():
            if map_id in unlocked_maps or map_info["unlocked"]:
                available_maps.append(map_info)
                status = "[已解锁]" if map_id in unlocked_maps or map_info["unlocked"] else "[未解锁]"
                print(f"{map_id}. {map_info['name']} {status}")
                print(f"   难度：{map_info['difficulty']} | 关卡数：{map_info['levels']}")
                print(f"   {map_info['description']}")
                print()

        print("0. 返回")

        try:
            choice = int(input("请选择地图 (0-" + str(len(available_maps)) + "): "))
            if choice == 0:
                return 0
            elif 1 <= choice <= len(available_maps):
                return list(maps.keys())[choice - 1]
            else:
                print("输入无效，请输入有效数字")
        except ValueError:
            print("输入无效，请输入数字")

        input("\n按回车键继续...")


def show_levels_info(map_id, levels, player):
    map_info = maps.get(map_id)
    if not map_info:
        return

    print_title(f"{map_info['name']} - 关卡信息")

    print("关卡列表：")
    for level in levels:
        if not isinstance(player.completed_levels, list):
            player.completed_levels = []

        status = "[已完成]" if level["id"] in player.completed_levels else "[未完成]"
        print(f"{level['id']}. {level['name']} {status}")
        rooms_count = level.get('rooms_count', difficulty_database[map_info['difficulty']]['range'])
        print(f"   难度：{level['difficulty']} | 房间数：{rooms_count}")
        print(f"   {level['description']}")
        print()


def start_room_challenge(map_id, level, room, player):
    map_info = maps.get(map_id)
    if not map_info:
        return False

    print_title(f"{map_info['name']} - {level['name']} - {room['name']}")
    print(f"房间类型：{room['room_type']}")
    print(f"难度：{room['difficulty']}")
    if room["room_type"] == "小怪" or room["room_type"] == "boss":
        print(f"战斗范围：1 ~ {room['battle_range']}")
    print(f"{room['description']}")
    print()

    if room["room_type"] == "小怪" or room["room_type"] == "boss":
        enemy_id = room.get('enemy')
        if enemy_id and enemy_id in enemy_database:
            enemy_data = enemy_database[enemy_id]
            enemy = Enemy(
                name=enemy_data['name'],
                hp=enemy_data['hp'],
                strength=enemy_data['strength'],
                defense=enemy_data['defense'],
                exp_reward=enemy_data['exp_reward'],
                enemy_type=enemy_data['enemy_type']
            )
            return minions_battle(room['battle_range'], enemy, player, map_id, level, room)
        return False
    elif room["room_type"] == "幸运":
        return luck_room(player, map_id, level, room)
    elif room["room_type"] == "普通":
        return True

    return False


def minions_battle(battle_range, enemy, player, map_id, level, room):
    map_info = maps.get(map_id)
    if not map_info:
        return False

    if not enemy:
        return False

    print_title(f"{map_info['name']} - {level['name']} - {room['name']}")
    print(f"你遇到了{enemy.name}！")
    enemy.show_stats()
    player.show_stats()

    input("\n准备就绪！按回车键开始战斗...")

    while True:
        clear_screen()
        print_title(f"{map_info['name']} - {level['name']} - {room['name']}")
        print("\n" + "=" * 50)
        print("你的回合：")
        print(f"敌人：{enemy.name} | 生命值：{enemy.hp}/{enemy.max_hp}")
        print(f"你：生命值：{player.hp}/{player.max_hp}")
        print("=" * 50)

        range_min, range_max = 1, battle_range
        target = random.randint(range_min, range_max)

        print(f"\n战斗挑战：")
        print(f"请输入{range_min}-{range_max}之间的数字！")

        attempts = 0
        while True:
            guess = get_guess(range_min, range_max)
            attempts += 1

            print_guess_result(guess, target)

            if range_min <= guess <= range_max:
                distance = abs(guess - target)
                if distance == 0:
                    damage = player.strength + random.randint(3, 7)
                elif distance <= 3:
                    damage = player.strength + random.randint(1, 4)
                else:
                    damage = max(1, player.strength - distance // 5)

                actual_damage = enemy.take_damage(damage)
                print(f"\n🎯 攻击命中！对{enemy.name}造成了{actual_damage}点伤害！")

                damage = enemy.strength + random.randint(1, 3)
                actual_damage = player.take_damage(damage)
                print(f"\n💥 敌人攻击！你受到了{actual_damage}点伤害！\n")

                if player.hp <= 0:
                    print("\n💀 你被击败了！")
                    return False

                if enemy.hp <= 0:
                    print(f"\n🏆 你击败了{enemy.name}！")
                    player.gain_exp(enemy.exp_reward)

                    if enemy.enemy_type == "boss":
                        print("\n🎉 Boss奖励！获得大量属性提升！")
                        player.increase_stats(strength=10, defense=5, max_hp=50)
                        player.heal(100)
                    else:
                        player.heal(random.randint(5, 15))

                    return True

                continue
            else:
                print(f"\n⚠️ 输入不在范围内！必须输入{range_min}-{range_max}之间的数字！")
                damage = enemy.strength + random.randint(1, 3)
                actual_damage = player.take_damage(damage)
                print(f"\n💥 敌人趁机攻击！你受到了{actual_damage}点伤害！")
                if player.hp <= 0:
                    print("\n💀 你被击败了！")
                    return False
                continue

        if enemy.hp > 0:
            print("\n" + "=" * 50)
            print("敌人回合：")
            damage = enemy.strength + random.randint(1, 3)
            actual_damage = player.take_damage(damage)
            print(f"{enemy.name}攻击了你，造成了{actual_damage}点伤害！")
            print(f"你的生命值：{player.hp}/{player.max_hp}")
            print("=" * 50)

            if player.hp <= 0:
                print("\n💀 你被击败了！")
                return False

        return False


def luck_room(player, map_id, level, room):
    map_info = maps.get(map_id)
    if not map_info:
        return False

    print_title(f"{map_info['name']} - {level['name']} - {room['name']}")
    print("欢迎来到幸运房！")
    print("你获得属性提升！")

    boost_type = random.choice(["strength", "defense", "max_hp"])
    boost_amount = random.randint(2, 5)

    if boost_type == "strength":
        player.increase_stats(strength=boost_amount)
        print(f"力量提升了{boost_amount}点！")
    elif boost_type == "defense":
        player.increase_stats(defense=boost_amount)
        print(f"防御力提升了{boost_amount}点！")
    else:
        player.increase_stats(max_hp=boost_amount * 5)
        print(f"生命值上限提升了{boost_amount * 5}点！")

    heal_amount = random.randint(10, 25)
    player.heal(heal_amount)
    print(f"恢复了{heal_amount}点生命值！")

    return True


def continue_adventure(saved_data):
    print_title("继续闯关游戏")
    print(f"正在加载存档...")

    map_name = saved_data.get('map_name', '未知')
    current_level = saved_data.get('current_level', 1)
    completed_levels = saved_data.get('completed_levels', [])
    if not isinstance(completed_levels, list):
        completed_levels = []

    print(f"地图：{map_name}")
    print(f"当前关卡：{current_level}")
    print(f"已完成关卡：{completed_levels}")

    input("\n按回车键开始游戏...")

    adventure_mode(saved_data)
