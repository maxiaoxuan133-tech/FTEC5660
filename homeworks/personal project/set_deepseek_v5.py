import json
import os

chars_dir = "C:/Users/hp/OneDrive/Desktop/2/AgentGroup/AgentGroup-main/storage/succession/test_version_5"

for filename in os.listdir(chars_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(chars_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['engine'] = 'deepseek'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Modified: {filename} -> engine: deepseek")

print("\nAll characters updated to use DeepSeek!")

