uvicorn backend.main:app --reload
curl -X POST http://localhost:8000/audit \
  -F "file=@contracts/VulnerableBank.sol"
streamlit run frontend/app.py  