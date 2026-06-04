from datetime import datetime
from backend.schemas import AuditState

def report_node(state: AuditState) -> AuditState:
    print("[Report] 生成审计报告...")
    
    detectors = state["slither_result"].get("results", {}).get("detectors", [])
    
    # 统计风险等级
    high = sum(1 for d in detectors if d.get("impact") == "High")
    medium = sum(1 for d in detectors if d.get("impact") == "Medium")
    low = sum(1 for d in detectors if d.get("impact") == "Low")
    
    # 计算风险评分（简单规则）
    score = max(0, 100 - high * 25 - medium * 10 - low * 3)
    
    report = f"""# Smart Contract Audit Report

**生成时间：** {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**合约文件：** {state["contract_path"].split("/")[-1]}

---

## Executive Summary

| 风险等级 | 数量 |
|----------|------|
| 🔴 High   | {high} |
| 🟡 Medium | {medium} |
| 🟢 Low    | {low} |

**安全评分：{score} / 100**

---

## Findings

{state.get("review_result", "未发现需要人工审查的问题。")}

---

## Conclusion

{"⚠️ 该合约存在高危漏洞，建议修复后再部署。" if high > 0 else "✅ 未发现高危漏洞，建议仍在部署前进行人工复核。"}

---
*本报告由 Smart Contract Security Agent 自动生成*
"""
    
    state["final_report"] = report
    state["risk_score"] = str(score)
    print("[Report] 报告生成完成")
    return state