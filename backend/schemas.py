from typing import TypedDict,Optional

class AuditState(TypedDict):
    contract_path:str
    contract_code:str
    slither_result:str
    review_result:str
    final_report:str