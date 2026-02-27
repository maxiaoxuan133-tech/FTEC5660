import json
import os

# 读取所有角色文件并修改engine为deepseek
chars_dir = "C:/Users/hp/OneDrive/Desktop/2/AgentGroup/AgentGroup-main/storage/succession/initial_version/characters"

for filename in os.listdir(chars_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(chars_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 修改engine为deepseek
        data['engine'] = 'deepseek'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Modified: {filename} -> engine: deepseek")

print("\nAll characters updated to use DeepSeek!")
