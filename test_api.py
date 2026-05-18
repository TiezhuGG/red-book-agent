import requests
import json

# 测试诊断 API
print("=== 测试诊断 API ===")
try:
    response = requests.post(
        "http://localhost:8000/api/diagnose",
        data={
            "title": "懒人食谱｜5分钟搞定的美味",
            "content": "今天给大家分享一个超级好吃的食谱！做法非常简单，食材也很容易买到。",
            "category": "food",
            "tags": "美食,食谱,家常菜"
        }
    )
    response.encoding = "utf-8"
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n=== 响应数据结构 ===")
        print(f"overall_score: {data.get('overall_score')}")
        print(f"grade: {data.get('grade')}")
        print(f"radar_data: {json.dumps(data.get('radar_data', {}), ensure_ascii=False)}")
        print(f"suggestions 数量: {len(data.get('suggestions', []))}")
        print(f"agent_opinions 数量: {len(data.get('agent_opinions', []))}")
        print(f"simulated_comments 数量: {len(data.get('simulated_comments', []))}")
        print(f"debate_summary: {data.get('debate_summary', '')[:100]}...")
        
        # 检查每个 Agent 的意见
        print("\n=== Agent 意见 ===")
        for op in data.get('agent_opinions', []):
            print(f"- {op.get('agent_name')}: {op.get('dimension')} - 分数: {op.get('score')}")
            if op.get('issues'):
                print(f"  问题: {op['issues'][:2]}")
            if op.get('simulated_comments'):
                print(f"  模拟评论数: {len(op['simulated_comments'])}")
        
        # 检查建议
        print("\n=== 优化建议 ===")
        for i, s in enumerate(data.get('suggestions', [])):
            print(f"{i+1}. [{s.get('priority')}] {s.get('description', '')[:50]}...")
            
    else:
        print(f"错误响应: {response.text}")
        
except Exception as e:
    print(f"请求失败: {e}")

# 测试优化建议 API
print("\n\n=== 测试优化建议 API ===")
try:
    response = requests.post(
        "http://localhost:8000/api/optimize",
        json={
            "title": "测试美食笔记标题",
            "content": "今天给大家分享一个超级好吃的食谱！",
            "category": "food",
            "issues": '[{"description":"标题不够吸引人"}]',
            "suggestions": '[{"description":"优化标题"}]',
            "overall_score": 60
        }
    )
    response.encoding = "utf-8"
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"original_score: {data.get('original_score')}")
        print(f"plans 数量: {len(data.get('plans', []))}")
        for i, plan in enumerate(data.get('plans', [])):
            print(f"{i+1}. {plan.get('strategy')}: {plan.get('optimized_title')[:30]}... (分数: {plan.get('score')})")
    else:
        print(f"错误响应: {response.text}")
        
except Exception as e:
    print(f"请求失败: {e}")
