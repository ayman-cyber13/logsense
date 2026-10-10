import streamlit as st
import ollama

st.set_page_config(page_title="LogSense", page_icon="🛡️", layout="wide")

EXAMPLES = {
    "SSH brute force": "Failed password for root from 185.220.101.4 port 52144 ssh2 (x47 in 60 seconds)",
    "Suspicious PowerShell": "powershell.exe -nop -w hidden -enc JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0AA==",
    "Port scan": "Firewall: 203.0.113.9 attempted connections to ports 21,22,23,80,443,3389,8080 in 5 seconds - DROPPED",
    "Normal login": "User ayman logged in successfully from 192.168.1.15 at 09:02",
}

with st.sidebar:
    st.header("About")
    st.write("LogSense explains security logs in simple language.")
    st.write("**Model:** Llama 3.2 3B (open-weight)")
    st.write("**Runtime:** Ollama (100% local)")
    st.header("Try an example")
    choice = st.selectbox("Example logs", ["-"] + list(EXAMPLES))

st.title("🛡️ LogSense")
st.caption("AI-powered security log explainer, running fully on your laptop")

left, right = st.columns(2)

with left:
    log = st.text_area("Paste log or alert", value=EXAMPLES.get(choice, ""), height=250)
    go = st.button("🔍 Explain", type="primary")

with right:
    st.subheader("Analysis")
    if go and log.strip():
        prompt = f"""You are a SOC analyst assistant.
Explain this log to a beginner. Use exactly this format:
1. What happened
2. Severity (Low/Medium/High) and why
3. Possible attack type (MITRE ATT&CK if known)
4. What to do next

Log:
{log}"""
        with st.spinner("Analyzing..."):
            r = ollama.chat(model="llama3.2:3b",
                            messages=[{"role": "user", "content": prompt}])
        st.markdown(r["message"]["content"])
    else:
        st.info("Result yahan dikhega.")