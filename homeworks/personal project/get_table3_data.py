import json
import os
import collections
import numpy

# 设置测试文件夹
TEST_FOLDER = 'C:/Users/hp/OneDrive/Desktop/2/AgentGroup/AgentGroup-main/storage/succession/test_version_5'

action_history_dir = os.path.join(TEST_FOLDER, 'action_history')

# 收集所有评估数据
results = collections.defaultdict(list)

if os.path.isdir(action_history_dir):
    for json_file in os.listdir(action_history_dir):
        with open(os.path.join(action_history_dir, json_file), encoding='utf-8') as f:
            for json_line in f:
                data = json.loads(json_line)
                action_type = data['action_type']
                action = data['action']
                
                if action_type.startswith('### EVALUATION'):
                    # 提取 agent response 和 ground truth
                    if 'agent response:' in action and 'ground truth:' in action:
                        agent_response = action.split('agent response: ')[-1].split('[SEP]')[0].strip()
                        ground_truth = action.split('ground truth: ')[-1].strip()
                        results[action_type].append((agent_response, ground_truth))

# 计算各项指标
print("="*70)
print("DeepSeek (test_version_5) - 详细评估数据")
print("="*70)

# 定义指标名称映射
metric_names = {
    "### EVALUATION ACTION SPACE": "CS (Action Space准确率)",
    "### EVALUATION ACTION HISTORY": "BUS (Action History准确率)",
    "### EVALUATION CHAT ROUND": "RUS (Round理解准确率)",
    "### EVALUATION RELATIONSHIP LENGTH": "NoR-L (Relationship长度准确率)",
    "### EVALUATION BELIEF LENGTH": "NoB-L (Belief长度准确率)",
    "### EVALUATION RELATIONSHIP VALUE": "NoR-V (Relationship值准确率)",
    "### EVALUATION BELIEF VALUE": "NoB-V (Belief值准确率)",
    "### EVALUATION NUMBER OF CHARACTER": "NoC (角色数准确率)",
    "### EVALUATION NUMBER OF RESOURCE": "NoR (资源数准确率)"
}

# 计算并打印结果
for metric, name in metric_names.items():
    if metric in results:
        data = results[metric]
        correct = 0
        total = len(data)
        
        for agent_resp, gt in data:
            # 尝试提取数字比较
            try:
                # 提取 agent 响应中的数字
                agent_nums = []
                for part in agent_resp.split():
                    try:
                        agent_nums.append(int(part))
                    except:
                        pass
                
                # 提取 ground truth 中的数字
                gt_nums = []
                for part in gt.split():
                    try:
                        gt_nums.append(int(part))
                    except:
                        pass
                
                # 比较
                if agent_nums and gt_nums:
                    if agent_nums[0] == gt_nums[0]:
                        correct += 1
                # 如果是列表比较
                elif agent_resp == gt:
                    correct += 1
            except:
                if agent_resp == gt:
                    correct += 1
        
        accuracy = correct / total if total > 0 else 0
        print(f"{name}: {accuracy:.4f} ({correct}/{total})")
    else:
        print(f"{name}: N/A (0/0)")

print()
print("="*70)
print("详细统计")
print("="*70)

# 统计每种类型的数量
for metric, name in metric_names.items():
    if metric in results:
        print(f"{name}: {len(results[metric])} 条记录")

