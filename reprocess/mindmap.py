import ollama

def Qwen_Chat(prompt_text,system_text):
    prompt_text = prompt_text.replace('\n\n', '\n')
    if system_text == '':
        res = ollama.chat(model="qwen2.5:72b-instruct", messages=[
                        {"role": "user", "content": prompt_text}], keep_alive='1h', options={"num_ctx": 20480,"num_predict":-1})
    else:
        res = ollama.chat(model="qwen2.5:72b-instruct", messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": prompt_text}], keep_alive='1h', options={"num_ctx": 20480, "num_predict": -1})
    result = res['message']['content']
    result = result.replace('\n\n', '\n')
    return result

sys_text = """
你是一位专业的书籍内容分析专家，擅长从文本中提取关键信息并生成结构化的思维导图。请根据提供的书本解读稿，生成一个清晰分层的结构化思维导图数据：
提取规则：
根节点：书籍的核心主题，作为导图的标题。
一级节点：书籍的主要论点。
二级节点：重要子主题或分论点。
三级节点：具体论据、方法、解释。
层级限制：最多支持四级节点，避免过度细分。
内容限制：不要包含任何案例、人名信息等非结构化内容，只提取书籍的核心观点和论据。三级论点应详细展开，不要过于简单。
----格式要求----
请以json的格式输出，格式如下：
{
  "name" : "核心主题",
      "children": [
        {
          "name": "主要论点1",
          "children": [
            {
              "name": "分论点1",
              "children": [
                { "name": "具体论据/方法/解释" },
                { "name": "具体论据/方法/解释" }
                ...
              ]
            },
            {
              "name": "分论点2",
              "children": [
               ...
              ]
            }
          ]
        },
        {
          "name": "主要论点2",
          "children": [
            ...
          ]
        }
      ]
}
"""

booktext = f""""""
Qwen_Chat(booktext, sys_text)