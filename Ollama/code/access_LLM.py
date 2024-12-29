# 2024-12-29
# 本地大模型简易交互界面，待完善
import requests
import streamlit as st

def query_qwen(prompt):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "qwen2",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

def main():
    st.title("本地大模型交互（Qwen2）")
    query = st.text_input("请输入你的问题：")
    if query:
        st.write("使用大模型 Qwen2查询中...")
        prompt = f"用户的问题是：\"{query}\"\n请根据常识和推理回答。"
        llm_response = query_qwen(prompt)
        st.write(f"Qwen2 回答：{llm_response}")

if __name__ == "__main__":
    main()
