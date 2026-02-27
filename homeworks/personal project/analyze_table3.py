import json
import re

# 读取action_history - DeepSeek test_version_5
with open('C:/Users/hp/OneDrive/Desktop/2/AgentGroup/AgentGroup-main/storage/succession/test_version_5/action_history/0000.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 统计各类评估
eval_types = {}
for line in lines:
    data = json.loads(line)
    action_type = data['action_type']
    if 'EVALUATION' in action_type:
        if action_type not in eval_types:
            eval_types[action_type] = {'correct': 0, 'total': 0}
        
        action = data['action']
        # 提取agent response和ground truth
        if 'agent response:' in action and 'ground truth:' in action:
            agent_response = action.split('agent response: ')[1].split('[SEP]')[0].strip()
            ground_truth = action.split('ground truth: ')[1].strip()
            
            eval_types[action_type]['total'] += 1
            
            # 提取数字进行比较
            def extract_number(s):
                # 尝试直接转换为数字
                try:
                    return int(s)
                except:
                    pass
                # 尝试从字符串中提取数字
                nums = re.findall(r'\d+', s)
                if nums:
                    return int(nums[0])
                return None
            
            agent_num = extract_number(agent_response)
            gt_num = extract_number(ground_truth)
            
            # 如果能提取到数字，比较数字；否则比较原始字符串
            if agent_num is not None and gt_num is not None:
                if agent_num == gt_num:
                    eval_types[action_type]['correct'] += 1
            elif agent_response == ground_truth:
                eval_types[action_type]['correct'] += 1

print("=" * 60)
print("论文 Table 3 指标对照")
print("=" * 60)

# 指标映射
metric_map = {
    '### EVALUATION ACTION SPACE': ('CS', 'Choose Space'),
    '### EVALUATION BELIEF VALUE': ('BUS', 'Belief Update Space'),
    '### EVALUATION RELATIONSHIP VALUE': ('RUS', 'Relation Update Space'),
    '### EVALUATION BELIEF LENGTH': ('NoB', '# of Belief need to update'),
    '### EVALUATION RELATIONSHIP LENGTH': ('NoR', '# of Relationship need to update'),
    '### EVALUATION ACTION HISTORY': ('NoA', '# of Action agent have received'),
    '### EVALUATION CHAT ROUND': ('NoCR', '# of Chat Round agent have received'),
    '### EVALUATION NUMBER OF CHARACTER': ('NoC', '# of Character in this game'),
    '### EVALUATION NUMBER OF RESOURCE': ('NoR2', '# of Resource in this game'),
}

# NoC = # of Character = 9 (C0000-C0008)
# NoR (第二个) = # of Resource = 5 (R0000-R0004)

print(f"\n{'指标':<15} {'论文符号':<10} {'描述':<35} {'准确率':<10}")
print("-" * 70)

for eval_type, (code, desc) in metric_map.items():
    if eval_type in eval_types:
        correct = eval_types[eval_type]['correct']
        total = eval_types[eval_type]['total']
        accuracy = correct / total if total > 0 else 0
        print(f"{code:<15} {desc:<35} {accuracy*100:.2f}%")
    else:
        print(f"{code:<15} {desc:<35} N/A")

print("-" * 70)
print(f"{'NoC':<15} {'# of Character in this game':<35} 9")
print(f"{'NoR':<15} {'# of Resource in this game':<35} 5")

print("\n" + "=" * 60)
print("详细统计")
print("=" * 60)
for eval_type, stats in eval_types.items():
    print(f"{eval_type}: {stats['correct']}/{stats['total']} = {stats['correct']/stats['total']*100:.2f}%")

