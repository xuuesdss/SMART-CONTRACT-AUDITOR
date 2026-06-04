import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Smart Contract Auditor",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Smart Contract Security Auditor")
st.caption("基于 LangGraph + Slither + Qwen 的智能合约自动化审计系统")

uploaded_file = st.file_uploader("上传 Solidity 合约文件", type=["sol"])

if uploaded_file:
    st.code(uploaded_file.read().decode("utf-8"), language="solidity")
    uploaded_file.seek(0)  # 重置指针，后面 POST 还要用

    if st.button("🚀 开始审计", type="primary"):
        with st.spinner("正在分析合约，请稍候..."):
            try:
                response = requests.post(
                    f"{API_URL}/audit",
                    files={"file": (uploaded_file.name, uploaded_file, "text/plain")}
                )
                result = response.json()
            except Exception as e:
                st.error(f"请求失败：{e}")
                st.stop()

        if result.get("status") != "success":
            st.error("审计失败，请检查后端日志")
            st.stop()

        # ── 结果展示 ──────────────────────────────────────
        st.divider()

        # 风险评分
        raw_score = result.get("risk_score",0)
        try:
            score = int(raw_score)
        except (ValueError,TypeError):
            score = 0
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("安全评分", f"{score} / 100")
        col2.metric("🔴 High",   sum(1 for f in result["findings"] if f["severity"] == "High"))
        col3.metric("🟡 Medium", sum(1 for f in result["findings"] if f["severity"] == "Medium"))
        col4.metric("🟢 Low",    sum(1 for f in result["findings"] if f["severity"] == "Low"))

        # 漏洞列表
        st.subheader("🔍 漏洞发现")
        if result["findings"]:
            for f in result["findings"]:
                color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(f["severity"], "⚪")
                with st.expander(f"{color} [{f['severity']}] {f['name']}"):
                    st.write(f["description"])
        else:
            st.success("未发现漏洞")

        # 完整报告
        st.subheader("📄 审计报告")
        st.markdown(result["final_report"])

        st.download_button(
            label="⬇️ 下载报告 (.md)",
            data=result["final_report"],
            file_name="audit_report.md",
            mime="text/markdown"
        )