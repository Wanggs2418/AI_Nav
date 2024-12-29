# Ollama_intro

> [Ollama](https://ollama.com/) | [Docs](https://github.com/ollama/ollama/tree/main/docs)

## 1. 帮助文档

**[Windows Documentation](https://github.com/ollama/ollama/blob/main/docs/windows.md)**

**[API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)**

### Getting Started

- [Quickstart](https://github.com/ollama/ollama/blob/main/README.md#quickstart)
- [Examples](https://github.com/ollama/ollama/blob/main/examples)
- [Importing models](https://github.com/ollama/ollama/blob/main/docs/import.md)
- [Linux Documentation](https://github.com/ollama/ollama/blob/main/docs/linux.md)
- **[Windows Documentation](https://github.com/ollama/ollama/blob/main/docs/windows.md)**
- [Docker Documentation](https://github.com/ollama/ollama/blob/main/docs/docker.md)

### Reference

- **[API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)**
- [Modelfile Reference](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
- [OpenAI Compatibility](https://github.com/ollama/ollama/blob/main/docs/openai.md)

### Resources

- [Troubleshooting Guide](https://github.com/ollama/ollama/blob/main/docs/troubleshooting.md)
- [FAQ](https://github.com/ollama/ollama/blob/main/docs/faq.md)
- [Development guide](https://github.com/ollama/ollama/blob/main/docs/development.md)



## 2. 轻量级个人知识库

使用 Ollama 本地部署开源大模型 + Whoosh 全文搜索引擎

### Ollama

[Ollama](https://ollama.com/) 

```cmd
# 显示ollama常用命令
ollama

# 下载大模型qwen7b到本地（注意大模型占用的内存大小）
# b表示10参数(w,b)，7b即共70亿参数的大模型
ollama pull qwen2:7b

# 查看已经安装的大模型
ollama list

# 删除
ollama rm qwen2:7b

# 显示模型的基本信息
ollama show qweb2:7b

# 本地运行大模型(注意电脑配置)
ollama run qwen2:7b
```

### Whoosh

> [Whoosh Docs](https://whoosh.readthedocs.io/en/latest/)

```cmd
# 下载
conda install whoosh
pip install docx
pip install streamlit
pip install jieba
```

Whoosh 是轻量级的全文搜索引擎库，无需依赖，通过纯 python 实现，用于快速本地索引和查询。流程可分为 3 步：

1. 初始化索引：调用 `initialize_index()` 创建或加载索引；
2. 添加文档：用户上传 `.docx` 文件后，调用 `add_documnet_to_index()` 将文档内容分词并存储到索引；
3. 执行搜索：用户输入查询关键字后，调用 `search_knowledge_base()` 检索索引；

```cmd
# 使用浏览器截面交互
streamlit run e:/AI_learning/00AI_Nav/Ollama/code/access_LLM.py
# 结合个人知识库进行交互
streamlit run e:/AI_learning/00AI_Nav/Ollama/code/llm_knowledge.py
```























