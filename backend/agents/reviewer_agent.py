import json
import os
from openai import OpenAI
from backend.schemas import AuditState

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def reviewer_node(state: AuditState) -> AuditState:
    print("[Reviewer] Qwen 开始分析漏洞...")
    
    detectors = state["slither_result"].get("results", {}).get("detectors", [])
    
    findings_text = json.dumps(detectors, indent=2, ensure_ascii=False)
    
    prompt = f"""你是一名资深智能合约安全审计专家。

以下是 Slither 静态分析发现的问题：
{findings_text}

请对每个问题：
1. 用简洁中文解释漏洞原理
2. 说明潜在攻击场景
3. 给出具体修复建议
4. 标注风险等级：High / Medium / Low

输出格式：
## [漏洞名称] - [风险等级]
**原理：** ...
**攻击场景：** ...
**修复建议：** ...

---
"""
    
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
    
    state["review_result"] = response.choices[0].message.content
    print("[Reviewer] 分析完成")
    return state