from backend.schemas import AuditState

def parser_node(state: AuditState) -> AuditState:
    with open(state["contract_path"],"r") as f:
        state["contract_code"] = f.read()
    print(f"[Parser] 读取合约,共{len(state['contract_code'])} 字节")
    return state