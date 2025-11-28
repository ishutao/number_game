import json
import os
from datetime import datetime

DEFAULT_SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../saves')
SAVE_FILE_EXT = '.sav'
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game_config.json')
UNLOCK_STATUS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'unlock_status.json')

GAME_TYPE_GUESS_NUMBER = 1
GAME_TYPE_BOSS_CHALLENGE = 2
GAME_TYPE_LEVEL_CHALLENGE = 3


def ensure_save_dir_exists():
    if not os.path.exists(DEFAULT_SAVE_DIR):
        os.makedirs(DEFAULT_SAVE_DIR)


def get_save_file_path(save_name):
    ensure_save_dir_exists()
    return os.path.join(DEFAULT_SAVE_DIR, f"{save_name}{SAVE_FILE_EXT}")


def get_all_saves():
    ensure_save_dir_exists()
    saves = []
    for file in os.listdir(DEFAULT_SAVE_DIR):
        if file.endswith(SAVE_FILE_EXT):
            saves.append(file[:-len(SAVE_FILE_EXT)])
    return saves


def load_config():
    default_config = {
        "encryption_enabled": True,
        "encryption_key": "数字游戏默认密钥",
        "auto_save": True,
        "max_save_slots": 10
    }

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        return default_config

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        return default_config


def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存配置文件失败: {e}")
        return False


def load_unlock_status():
    default_status = {
        "levels_unlocked": [1],
        "all_unlocked": False,
        "last_updated": datetime.now().isoformat()
    }

    if not os.path.exists(UNLOCK_STATUS_FILE):
        with open(UNLOCK_STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_status, f, ensure_ascii=False, indent=2)
        return default_status

    try:
        with open(UNLOCK_STATUS_FILE, 'r', encoding='utf-8') as f:
            status = json.load(f)
            for key, value in default_status.items():
                if key not in status:
                    status[key] = value
            return status
    except Exception as e:
        print(f"加载解锁状态失败: {e}")
        return default_status


def save_unlock_status(status):
    status['last_updated'] = datetime.now().isoformat()
    try:
        with open(UNLOCK_STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存解锁状态失败: {e}")
        return False


def unlock_all_levels():
    status = load_unlock_status()
    status['all_unlocked'] = True
    status['levels_unlocked'] = list(range(1, 11))
    return save_unlock_status(status)


def lock_all_levels():
    status = load_unlock_status()
    status['all_unlocked'] = False
    status['levels_unlocked'] = [1]
    return save_unlock_status(status)


def is_level_unlocked(level_id):
    status = load_unlock_status()
    return status['all_unlocked'] or level_id in status['levels_unlocked']


def unlock_level(level_id):
    status = load_unlock_status()
    if level_id not in status['levels_unlocked']:
        status['levels_unlocked'].append(level_id)
        status['levels_unlocked'].sort()
        return save_unlock_status(status)
    return True
