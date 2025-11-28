import base64
import json
import os
from datetime import datetime

from UI界面 import print_no_saved_game, print_game_selected
from 存档位置 import (
    get_save_file_path,
    get_all_saves,
    load_config,
    GAME_TYPE_GUESS_NUMBER,
    GAME_TYPE_BOSS_CHALLENGE,
    GAME_TYPE_LEVEL_CHALLENGE
)

DEFAULT_SAVE_NAME = "autosave"


def xor_encrypt(data, key):
    result = []
    for i in range(len(data)):
        result.append(chr(ord(data[i]) ^ ord(key[i % len(key)])))
    return ''.join(result)


def encrypt_data(data, key):
    json_data = json.dumps(data, ensure_ascii=False)
    encrypted = xor_encrypt(json_data, key)
    return base64.b64encode(encrypted.encode('utf-8')).decode('utf-8')


def decrypt_data(encrypted_data, key):
    try:
        decoded = base64.b64decode(encrypted_data.encode('utf-8')).decode('utf-8')
        decrypted = xor_encrypt(decoded, key)
        return json.loads(decrypted)
    except Exception as e:
        print(f"解密失败: {e}")
        return None


def check_saved_game(save_name=DEFAULT_SAVE_NAME):
    return os.path.exists(get_save_file_path(save_name))


def load_saved_game(save_name=DEFAULT_SAVE_NAME):
    if not check_saved_game(save_name):
        return None

    config = load_config()
    encryption_enabled = config.get('encryption_enabled', True)
    encryption_key = config.get('encryption_key', '数字游戏默认密钥')

    try:
        save_path = get_save_file_path(save_name)
        with open(save_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

            if encryption_enabled:
                return decrypt_data(content, encryption_key)
            else:
                return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError, Exception) as e:
        print(f"加载存档失败: {e}")
        return None


def continue_game(save_name=DEFAULT_SAVE_NAME):
    saved_data = load_saved_game(save_name)

    if not saved_data:
        print_no_saved_game()
        return False

    game_type = saved_data.get('game_type', '')
    game_modes = {
        GAME_TYPE_GUESS_NUMBER: "猜数字",
        GAME_TYPE_BOSS_CHALLENGE: "Boss挑战",
        GAME_TYPE_LEVEL_CHALLENGE: "闯关挑战"
    }

    game_name = game_modes.get(game_type, "未知游戏")

    print_game_selected(game_name)

    save_time = saved_data.get('save_time', '未知时间')
    print(f"存档时间: {save_time}")

    print(f"继续{game_name}游戏...")

    if game_type == GAME_TYPE_GUESS_NUMBER:
        from 猜数字 import continue_guess_number
        continue_guess_number(saved_data)
    elif game_type == GAME_TYPE_BOSS_CHALLENGE:
        from boss挑战 import continue_boss_challenge
        continue_boss_challenge(saved_data)
    elif game_type == GAME_TYPE_LEVEL_CHALLENGE:
        from 闯关模式 import continue_level_challenge
        continue_level_challenge(saved_data)
    else:
        print(f"未知游戏类型: {game_type}")

    return saved_data


def save_game(game_type, game_state, save_name=DEFAULT_SAVE_NAME):
    try:
        save_data = {
            'game_type': game_type,
            'game_state': game_state,
            'save_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        config = load_config()
        encryption_enabled = config.get('encryption_enabled', True)
        encryption_key = config.get('encryption_key', '数字游戏默认密钥')

        save_path = get_save_file_path(save_name)

        with open(save_path, 'w', encoding='utf-8') as f:
            if encryption_enabled:
                encrypted_data = encrypt_data(save_data, encryption_key)
                f.write(encrypted_data)
            else:
                json.dump(save_data, f, ensure_ascii=False, indent=2)

        print(f"游戏已成功保存到: {save_path}")
        return True
    except Exception as e:
        print(f"保存游戏失败: {e}")
        return False


def delete_saved_game(save_name=DEFAULT_SAVE_NAME):
    if check_saved_game(save_name):
        try:
            save_path = get_save_file_path(save_name)
            os.remove(save_path)
            print(f"存档已成功删除: {save_name}")
            return True
        except Exception as e:
            print(f"删除存档失败: {e}")
            return False
    return True  # 没有存档也算成功


def list_saves():
    saves = get_all_saves()
    if saves:
        print("\n可用存档:")
        for i, save in enumerate(saves, 1):
            save_data = load_saved_game(save)
            if save_data:
                game_type = save_data.get('game_type', '未知')
                save_time = save_data.get('save_time', '未知时间')
                game_modes = {
                    GAME_TYPE_GUESS_NUMBER: "猜数字",
                    GAME_TYPE_BOSS_CHALLENGE: "boss挑战",
                    GAME_TYPE_LEVEL_CHALLENGE: "闯关模式"
                }
                game_name = game_modes.get(game_type, "未知游戏")
                print(f"{i}. {save} - {game_name} ({save_time})")
            else:
                print(f"{i}. {save} - 无法读取")
    else:
        print("\n当前没有可用存档")
    return saves
