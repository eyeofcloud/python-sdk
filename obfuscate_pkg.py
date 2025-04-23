import os
from python_minifier import minify


def minify_folder(source_folder, target_folder):
    # 遍历源文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(source_folder):
        # 计算当前子文件夹在目标文件夹中的对应路径
        relative_path = os.path.relpath(root, source_folder)
        target_subfolder = os.path.join(target_folder, relative_path)
        # 如果目标子文件夹不存在，则创建它
        if not os.path.exists(target_subfolder):
            os.makedirs(target_subfolder)
        # 遍历当前子文件夹中的所有文件
        for file in files:
            if file.endswith('.py'):
                # 计算源文件和目标文件的完整路径
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_subfolder, file)
                # 读取源文件内容
                with open(source_file, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                # 对源文件内容进行混淆
                minified_code = minify(source_code)
                # 将混淆后的代码写入目标文件
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(minified_code)
                print(f"Minified {source_file} to {target_file}")


if __name__ == "__main__":
    # 假设 eyeofcloud 文件夹就在当前工作目录下
    source_folder = 'eyeofcloud'
    target_folder = 'eyeofcloud_obfuscated'
    minify_folder(source_folder, target_folder)
    