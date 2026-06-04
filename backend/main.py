import os
import shutil
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.workflow import graph

load_dotenv()

app = FastAPI(title="Smart Contract Auditor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "/tmp/contracts"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/audit")
async def audit_contract(file: UploadFile):
    if not file.filename.endswith(".sol"):
        raise HTTPException(400, "只支持 .sol 文件")
    
    contract_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(contract_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    try:
        result = graph.invoke({
            "contract_path": contract_path,
            "contract_code": "",
            "slither_result": {},
            "review_result": "",
            "final_report": ""
        })
        
        detectors = result["slither_result"].get("results", {}).get("detectors", [])
        
        return {
            "status": "success",
            "risk_score": result.get("risk_score", "N/A"),
            "findings": [
                {
                    "name": d.get("check", "Unknown"),
                    "severity": d.get("impact", "Low"),
                    "description": d.get("description", "")
                }
                for d in detectors
            ],
            "final_report": result["final_report"]
        }
    
    except Exception as e:
        raise HTTPException(500, f"审计失败: {str(e)}")

@app.get("/health")
def health():
    return {"status": "ok"}