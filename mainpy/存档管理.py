import base64
import hashlib
import json
import os
import shutil
from datetime import datetime, timedelta

from 存档位置 import (
    DEFAULT_SAVE_DIR,
    SAVE_FILE_EXT,
    get_save_file_path,
    get_all_saves,
    ensure_save_dir_exists
)

ENCRYPTION_KEY = b'digitalgameencryptionkey!'


def generate_key():
    return hashlib.sha256(ENCRYPTION_KEY).digest()


def xor_encrypt(data, key):
    extended_key = (key * ((len(data) // len(key)) + 1))[:len(data)]
    return bytes(a ^ b for a, b in zip(data, extended_key))


def encrypt_data(data, key):
    encrypted = xor_encrypt(data, key)
    return base64.b64encode(encrypted)


def decrypt_data(encrypted_data, key):
    raw_data = base64.b64decode(encrypted_data)
    return xor_encrypt(raw_data, key)


def load_saved_game(save_name):
    file_path = get_save_file_path(save_name)
    if not os.path.exists(file_path):
        print(f"错误：存档 '{save_name}' 不存在")
        return None

    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        try:
            key = generate_key()
            decrypted_content = decrypt_data(content, key)
            save_data = json.loads(decrypted_content.decode('utf-8'))
        except Exception:
            try:
                save_data = json.loads(content.decode('utf-8'))
                print(f"警告：存档 '{save_name}' 未加密，建议重新保存以启用加密保护")
            except json.JSONDecodeError:
                print(f"错误：存档 '{save_name}' 格式错误或已损坏")
                return None

        return save_data
    except Exception as e:
        print(f"错误：加载存档 '{save_name}' 时发生错误: {e}")
    return None


def save_game(save_name, game_data):
    file_path = get_save_file_path(save_name)

    save_data = {
        **game_data,
        'save_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'last_modified': datetime.now().isoformat(),
        'encrypted': True
    }

    try:
        json_data = json.dumps(save_data, ensure_ascii=False, indent=2)

        key = generate_key()
        encrypted_data = encrypt_data(json_data.encode('utf-8'), key)

        with open(file_path, 'wb') as f:
            f.write(encrypted_data)

        print(f"游戏 '{save_name}' 已成功加密保存")
        return True
    except Exception as e:
        print(f"错误：保存游戏 '{save_name}' 时发生错误: {e}")
        return False


def delete_saved_game(save_name):
    file_path = get_save_file_path(save_name)
    if not os.path.exists(file_path):
        print(f"错误：存档 '{save_name}' 不存在")
        return False

    try:
        os.remove(file_path)
        print(f"存档 '{save_name}' 已成功删除")
        return True
    except Exception as e:
        print(f"错误：删除存档 '{save_name}' 时发生错误: {e}")
        return False


def list_saves_with_details():
    saves = []
    save_names = get_all_saves()

    for save_name in save_names:
        file_path = get_save_file_path(save_name)
        try:
            file_stats = os.stat(file_path)
            created_time = datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            modified_time = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            file_size = f"{file_stats.st_size / 1024:.2f} KB"

            save_data = load_saved_game(save_name)

            save_info = {
                'name': save_name,
                'game_name': save_data.get('game_name', '未知游戏') if save_data else '未知游戏',
                'save_time': save_data.get('save_time', modified_time) if save_data else modified_time,
                'file_size': file_size,
                'created_time': created_time,
                'modified_time': modified_time,
                'difficulty': save_data.get('difficulty') if save_data else None,
                'attempts_used': save_data.get('attempts_used') if save_data else None,
                'attempts_remaining': save_data.get('attempts_remaining') if save_data else None,
                'encrypted': save_data.get('encrypted', False) if save_data else False
            }
            saves.append(save_info)

        except Exception as e:
            save_info = {
                'name': save_name,
                'game_name': '未知游戏',
                'save_time': '未知',
                'file_size': '未知',
                'created_time': '未知',
                'modified_time': '未知',
                'encrypted': '未知'
            }
            saves.append(save_info)

    saves.sort(key=lambda x: x['modified_time'], reverse=True)
    return saves


def rename_save(old_name, new_name):
    if not old_name or not new_name:
        print("错误：存档名称不能为空")
        return False

    old_path = get_save_file_path(old_name)
    new_path = get_save_file_path(new_name)

    if not os.path.exists(old_path):
        print(f"错误：存档 '{old_name}' 不存在")
        return False

    if os.path.exists(new_path):
        print(f"错误：存档 '{new_name}' 已存在")
        return False

    try:
        os.rename(old_path, new_path)
        print(f"存档已从 '{old_name}' 重命名为 '{new_name}'")
        return True
    except Exception as e:
        print(f"错误：重命名存档时发生错误: {e}")
        return False


def copy_save(source_name, target_name):
    if not source_name or not target_name:
        print("错误：存档名称不能为空")
        return False

    source_path = get_save_file_path(source_name)
    target_path = get_save_file_path(target_name)

    if not os.path.exists(source_path):
        print(f"错误：源存档 '{source_name}' 不存在")
        return False

    if os.path.exists(target_path):
        overwrite = input(f"存档 '{target_name}' 已存在，是否覆盖？(y/n): ").lower()
        if overwrite != 'y':
            print("已取消复制操作")
            return False

    try:
        save_data = load_saved_game(source_name)
        if not save_data:
            print(f"错误：无法加载源存档 '{source_name}'")
            return False

        return save_game(target_name, save_data)
    except Exception as e:
        print(f"错误：复制存档时发生错误: {e}")
        return False


def delete_all_saves():
    confirm = input("警告：确定要删除所有存档吗？此操作不可恢复！(y/n): ").lower()
    if confirm != 'y':
        print("已取消删除操作")
        return False

    save_names = get_all_saves()
    if not save_names:
        print("当前没有存档可删除")
        return True

    deleted_count = 0
    for save_name in save_names:
        if delete_saved_game(save_name):
            deleted_count += 1

    print(f"已删除 {deleted_count}/{len(save_names)} 个存档")
    return deleted_count == len(save_names)


def clean_old_saves(days=30, keep_min=3):
    save_list = list_saves_with_details()
    if not save_list:
        print("当前没有存档可清理")
        return True

    cutoff_date = datetime.now() - timedelta(days=days)

    save_list.sort(key=lambda x: datetime.strptime(x['modified_time'], '%Y-%m-%d %H:%M:%S'), reverse=True)

    to_delete = []
    for i, save in enumerate(save_list):
        if i < keep_min:
            continue

        modified_time = datetime.strptime(save['modified_time'], '%Y-%m-%d %H:%M:%S')
        if modified_time < cutoff_date:
            to_delete.append(save['name'])

    if not to_delete:
        print("没有需要清理的旧存档")
        return True

    print(f"将删除 {len(to_delete)} 个旧存档")
    print("要删除的存档：")
    for save_name in to_delete:
        print(f"  - {save_name}")

    confirm = input("确认要删除这些旧存档吗？(y/n): ").lower()
    if confirm != 'y':
        print("已取消清理操作")
        return False

    deleted_count = 0
    for save_name in to_delete:
        if delete_saved_game(save_name):
            deleted_count += 1

    print(f"已成功清理 {deleted_count}/{len(to_delete)} 个旧存档")
    return deleted_count == len(to_delete)


def backup_all_saves():
    ensure_save_dir_exists()

    backup_dir = os.path.join(DEFAULT_SAVE_DIR, 'backups')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'backup_{timestamp}')
    os.makedirs(backup_path)

    save_names = get_all_saves()
    if not save_names:
        print("当前没有存档可备份")
        # 即使没有存档，也要创建一个空的备份目录作为标记
        with open(os.path.join(backup_path, 'empty_backup.txt'), 'w', encoding='utf-8') as f:
            f.write(f"备份创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("此备份不包含任何存档文件")
        print(f"已创建空备份：{backup_path}")
        return True

    backed_up_count = 0
    for save_name in save_names:
        source_path = get_save_file_path(save_name)
        target_path = os.path.join(backup_path, f"{save_name}{SAVE_FILE_EXT}")
        try:
            shutil.copy2(source_path, target_path)
            backed_up_count += 1
        except Exception as e:
            print(f"错误：备份 '{save_name}' 时发生错误: {e}")

    with open(os.path.join(backup_path, 'backup_info.txt'), 'w', encoding='utf-8') as f:
        f.write(f"备份创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"备份的存档数量: {backed_up_count}\n")
        f.write(f"总存档数量: {len(save_names)}\n")
        if backed_up_count < len(save_names):
            f.write("警告：部分存档备份失败")

    print(f"已成功备份 {backed_up_count}/{len(save_names)} 个存档到 {backup_path}")
    return backed_up_count == len(save_names)


def verify_all_saves():
    save_names = get_all_saves()
    if not save_names:
        print("当前没有存档需要验证")
        return True

    valid_count = 0
    invalid_count = 0
    unencrypted_count = 0
    invalid_saves = []
    unencrypted_saves = []

    print("开始验证存档完整性...")
    for save_name in save_names:
        file_path = get_save_file_path(save_name)
        print(f"验证存档: {save_name}...")

        if not os.path.exists(file_path):
            print(f"  - 错误：文件不存在")
            invalid_count += 1
            invalid_saves.append(save_name)
            continue

        if os.path.getsize(file_path) == 0:
            print(f"  - 错误：文件为空")
            invalid_count += 1
            invalid_saves.append(save_name)
            continue

        try:
            save_data = load_saved_game(save_name)
            if not save_data:
                print(f"  - 错误：无法解析存档数据")
                invalid_count += 1
                invalid_saves.append(save_name)
                continue

            required_fields = ['save_time']
            missing_fields = [field for field in required_fields if field not in save_data]

            is_encrypted = save_data.get('encrypted', False)
            encryption_status = "已加密" if is_encrypted else "未加密"

            if missing_fields:
                print(f"  - 警告：缺少必要字段: {', '.join(missing_fields)}")
                print(f"  - 加密状态: {encryption_status}")
                valid_count += 1
            else:
                print(f"  - 有效")
                print(f"  - 加密状态: {encryption_status}")
                valid_count += 1

            if not is_encrypted:
                unencrypted_count += 1
                unencrypted_saves.append(save_name)

        except Exception as e:
            print(f"  - 错误：验证失败: {e}")
            invalid_count += 1
            invalid_saves.append(save_name)

    print("\n验证完成！")
    print(f"总存档数: {len(save_names)}")
    print(f"有效存档: {valid_count}")
    print(f"无效存档: {invalid_count}")
    print(f"未加密存档: {unencrypted_count}")

    if unencrypted_saves:
        print("\n未加密存档列表:")
        for save_name in unencrypted_saves:
            print(f"  - {save_name}")
        print("\n建议: 重新保存这些存档以启用加密保护")

    if invalid_saves:
        print("\n无效存档列表:")
        for save_name in invalid_saves:
            print(f"  - {save_name}")
        print("\n建议: 考虑删除这些无效存档以避免潜在问题")

    return invalid_count == 0


default_save_name = "default"
DEFAULT_SAVE_NAME = default_save_name


def batch_encrypt_saves():
    saves = list_saves_with_details()
    unencrypted_saves = [save for save in saves if not save.get('encrypted', False)]

    if not unencrypted_saves:
        print("所有存档都已经加密")
        return True

    print(f"找到 {len(unencrypted_saves)} 个未加密的存档")
    print("要加密的存档列表：")
    for save in unencrypted_saves:
        print(f"  - {save['name']}")

    confirm = input("\n确认要加密这些存档吗？(y/n): ").lower()
    if confirm != 'y':
        print("已取消加密操作")
        return False

    success_count = 0
    for save in unencrypted_saves:
        print(f"\n正在加密存档: {save['name']}...")
        # 加载存档数据
        save_data = load_saved_game(save['name'])
        if save_data:
            # 重新保存以加密
            if save_game(save['name'], save_data):
                success_count += 1
                print(f"  - 成功加密")
            else:
                print(f"  - 加密失败")
        else:
            print(f"  - 无法加载存档，跳过")

    print(f"\n加密完成！")
    print(f"成功加密: {success_count}/{len(unencrypted_saves)} 个存档")
    return success_count == len(unencrypted_saves)


def manage_saves():
    while True:
        from UI界面 import saves_management_menu, clear_screen

        choice = saves_management_menu()

        if choice == 0:
            break
        elif choice == 1:
            clear_screen()
            print("=" * 50)
            print("                    存档列表")
            print("=" * 50)
            saves = list_saves_with_details()
            if not saves:
                print("当前没有存档文件")
            else:
                print(f"{'存档名称':<20} {'游戏类型':<15} {'保存时间':<20} {'文件大小':<10} {'加密状态':<8}")
                print("-" * 73)
                for save in saves:
                    encrypted_status = "已加密" if save.get('encrypted', False) else "未加密" if save.get(
                        'encrypted') is not None else "未知"
                    print(
                        f"{save['name']:<20} {save['game_name']:<15} {save['save_time']:<20} {save['file_size']:<10} {encrypted_status:<8}")
            print("=" * 50)
            input("按回车键继续...")

        elif choice == 2:
            clear_screen()
            print("=" * 50)
            print("                    重命名存档")
            print("=" * 50)
            saves = list_saves_with_details()
            if not saves:
                clear_screen()
                print("当前没有存档文件")
                input("\n按回车键继续...")
                continue
            else:
                print(f"{'序号':<5}{'存档名称':<20} {'游戏类型':<15} {'保存时间':<20} {'文件大小':<10} {'加密状态':<8}")
                print("-" * 73)
                for save in saves:
                    encrypted_status = "已加密" if save.get('encrypted', False) else "未加密" if save.get(
                        'encrypted') is not None else "未知"
                    print(
                        f"{saves.index(save) + 1}: {save['name']:<20} {save['game_name']:<15} {save['save_time']:<20} {save['file_size']:<10} {encrypted_status:<8}")
            print("=" * 50)

            old_name = input("请输入要重命名的存档名称: ")
            if old_name.isnumeric():
                old_name = f"{saves[int(old_name) - 1]['name']}"
            new_name = input("请输入新的存档名称: ")
            rename_save(old_name, new_name)
            input("\n按回车键继续...")

        elif choice == 3:
            clear_screen()
            print("=" * 50)
            print("                    复制存档")
            print("=" * 50)
            saves = list_saves_with_details()
            if not saves:
                clear_screen()
                print("当前没有存档文件")
                input("\n按回车键继续...")
                continue
            else:
                print(f"{'序号':<5}{'存档名称':<20} {'游戏类型':<15} {'保存时间':<20} {'文件大小':<10} {'加密状态':<8}")
                print("-" * 73)
                for save in saves:
                    encrypted_status = "已加密" if save.get('encrypted', False) else "未加密" if save.get(
                        'encrypted') is not None else "未知"
                    print(
                        f"{saves.index(save) + 1}: {save['name']:<20} {save['game_name']:<15} {save['save_time']:<20} {save['file_size']:<10} {encrypted_status:<8}")
            print("=" * 50)
            source_name = input("请输入要复制的存档名称: ")
            if source_name.isnumeric():
                source_name = f"{saves[int(source_name) - 1]['name']}"
            target_name = input("请输入新的存档名称: ")
            copy_save(source_name, target_name)
            input("\n按回车键继续...")

        elif choice == 4:
            clear_screen()
            print("=" * 50)
            print("                    删除存档")
            print("=" * 50)

            print("1. 删除指定存档")
            print("2. 删除所有存档")
            sub_choice = input("请选择操作 (1-2): ")

            if sub_choice == '1':
                clear_screen()
                print("=" * 50)
                print("                    删除存档")
                print("=" * 50)
                saves = list_saves_with_details()
                if not saves:
                    clear_screen()
                    print("当前没有存档文件")
                    input("\n按回车键继续...")
                    continue
                else:
                    print(
                        f"{'序号':<5}{'存档名称':<20} {'游戏类型':<15} {'保存时间':<20} {'文件大小':<10} {'加密状态':<8}")
                    print("-" * 73)
                    for save in saves:
                        encrypted_status = "已加密" if save.get('encrypted', False) else "未加密" if save.get(
                            'encrypted') is not None else "未知"
                        print(
                            f"{saves.index(save) + 1}: {save['name']:<20} {save['game_name']:<15} {save['save_time']:<20} {save['file_size']:<10} {encrypted_status:<8}")
                save_name = input("请输入要删除的存档名称: ")
                if save_name.isnumeric():
                    save_name = f"{saves[int(save_name) - 1]['name']}"
                delete_saved_game(save_name)
            elif sub_choice == '2':
                delete_all_saves()
            input("\n按回车键继续...")

        elif choice == 5:
            clear_screen()
            print("=" * 50)
            print("                    清理旧存档")
            print("=" * 50)
            try:
                days = int(input("请输入要保留的天数 (默认30天): ") or "30")
                keep_min = int(input("请输入要保留的最少存档数量 (默认3个): ") or "3")
                clean_old_saves(days, keep_min)
            except ValueError:
                print("输入无效，使用默认值")
                clean_old_saves()
            input("\n按回车键继续...")

        elif choice == 6:
            clear_screen()
            print("=" * 50)
            print("                    备份所有存档")
            print("=" * 50)
            backup_all_saves()
            input("\n按回车键继续...")

        elif choice == 7:
            clear_screen()
            print("=" * 50)
            print("                    验证存档完整性")
            print("=" * 50)
            verify_all_saves()
            input("\n按回车键继续...")

        elif choice == 8:
            clear_screen()
            print("=" * 50)
            print("                    批量加密存档")
            print("=" * 50)
            batch_encrypt_saves()
            input("\n按回车键继续...")
