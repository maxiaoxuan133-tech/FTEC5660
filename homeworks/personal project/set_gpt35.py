import json
import os
import re

# 读取所有角色文件并修改engine为gpt3.5-turbo
chars_dir = "C:/Users/hp/OneDrive/Desktop/2/AgentGroup/AgentGroup-main/storage/succession/initial_version/characters"

for filename in os.listdir(chars_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(chars_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 修改engine为gpt3.5-turbo
        data['engine'] = 'gpt3.5-turbo'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Modified: {filename} -> engine: gpt3.5-turbo")

print("\nAll characters updated to use GPT-3.5-Turbo!")

