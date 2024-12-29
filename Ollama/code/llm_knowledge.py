# 参照郭震原创文章内容
import requests
from whoosh.index import open_dir, create_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser, OrGroup, WildcardPlugin
from docx import Document
import os
import streamlit as st
import jieba


# Function to query the Qwen-7B model via Ollama's API
def query_qwen(prompt):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "qwen2",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"


# Function to extract text from a .docx file
def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


# Function to initialize or open the Whoosh index
# 初始化索引
def initialize_index():
    schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))  # 设置 stored=True
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
        return create_in("indexdir", schema)
    else:
        return open_dir("indexdir")


# Function to add a .docx document to the Whoosh index
# 将文档内容分词并添加到索引
def add_document_to_index(ix, file_path, title):
    content = read_docx(file_path)
    with ix.searcher() as searcher:
        # 检查是否已有相同标题的文档
        existing_docs = [hit["title"] for hit in searcher.documents()]
        if title in existing_docs:
            print(f"文档 \"{title}\" 已存在，跳过索引。")
            return

    writer = ix.writer()
    writer.add_document(title=title, content=content)
    writer.commit()
    print(f"Indexed DOCX: {title}")


# Function to search the knowledge base
def search_knowledge_base(ix, query):
    with ix.searcher() as searcher:
        query_parser = QueryParser("content", ix.schema, group=OrGroup.factory(0.9))
        query_parser.add_plugin(WildcardPlugin())  # 添加通配符支持
        segmented_query = " ".join(jieba.cut(query))  # 分词查询
        user_query = query_parser.parse(f"*{segmented_query}*")  # 使用通配符
        print(f"分词后的模糊查询：{user_query}")  # 调试输出
        results = searcher.search(user_query, limit=3)
        return [
            {"title": hit["title"], "content": hit["content"]}
            for hit in results
        ]


# Streamlit app to combine the knowledge base and Qwen-7B
def main():
    st.title("LLM&Whoosh")

    # Initialize or open the Whoosh index
    ix = initialize_index()

    # Upload a .docx file
    uploaded_file = st.file_uploader("上传一个 .docx 文件以添加到知识库", type="docx", label_visibility='visible')
    if uploaded_file:
        file_path = f"uploaded_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # 检查并添加文档
        add_document_to_index(ix, file_path, title=uploaded_file.name)
        st.write(f"文件 \"{uploaded_file.name}\" 已处理！")

    # Input from user
    query = st.text_input("请输入你的问题：")
    if query:
        results = search_knowledge_base(ix, query)

        if results:
            st.write("知识库结果：")
            seen_contents = set()
            filtered_results = []
            for result in results:
                if result['content'] not in seen_contents:
                    seen_contents.add(result['content'])
                    filtered_results.append(result)
            for result in filtered_results:
                st.write(f"标题：{result['title']}")
                st.write(f"内容：{result['content']}")
            st.markdown('<p style="color:blue;">Qwen-7B 正在深度分析查询内容...</p>', unsafe_allow_html=True)
            llm_response = query_qwen("请对下面内容进行深度分析： "+results[0]['content'])
            st.write(f"Qwen2 回答：{llm_response}")
        else:
            st.write("在个人知识库文件里未找到相关内容，切换到大模型 Qwen2...")
            prompt = f"用户的问题是：\"{query}\"\n请根据常识和推理回答。"
            llm_response = query_qwen(prompt)
            st.write(f"Qwen2 回答：{llm_response}")


if __name__ == "__main__":
    main()
