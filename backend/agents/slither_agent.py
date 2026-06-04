import subprocess
import json
from backend.schemas import AuditState

def slither_node(state: AuditState) -> AuditState:
    print("[Slither] 开始静态分析...")
    
    result = subprocess.run(
        ["slither", state["contract_path"], "--json", "-"],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    # Slither 会同时输出到 stdout 和 stderr
    # 优先解析 stdout，失败则从 stderr 里找 JSON
    for output in [result.stdout, result.stderr]:
        try:
            parsed = json.loads(output)
            state["slither_result"] = parsed
            detectors = parsed.get("results", {}).get("detectors", [])
            print(f"[Slither] 发现 {len(detectors)} 个问题")
            return state
        except (json.JSONDecodeError, ValueError):
            continue
    
    # 两个都解析失败
    print(f"[Slither] 解析失败")
    print(f"stdout: {result.stdout[:300]}")
    print(f"stderr: {result.stderr[:300]}")
    state["slither_result"] = {"error": "parse failed", "results": {}}
    return state