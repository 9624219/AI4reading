from utils.chat import Qwen_Generate
import ollama
prompt_sys = f"""你是一个经验丰富的书本解读者。你的任务是在两个章节之间插入一段过渡语句，以确保内容的连贯性和逻辑性。你需要确保过渡语句自然流畅，能够有效地连接两个章节，使听众在听到过渡语句后能够顺利理解两个章节之间的关系。
你可以采用如下步骤：
1. 简要回顾一下上一章的关键点或重要事件。这可以帮助读者巩固记忆，并为接下来的内容做铺垫。指出即将讨论的主题或即将发生的事件，建立一种期待感。
2. 引入下一章：说明下一章的主题，并点明它与上一章的联系。
3. 过渡语句应该满足口语化的要求，避免使用过于正式或复杂的词汇和句式，以确保听众能够轻松理解。
4. 直接输出一个自然的过渡语句来承接两部分内容。
----输出要求----
请务必生成纯文本格式的内容，不能带有任何形式的标题或项目符号列表。
"""
text1 = ""
text2 = ""
prompt_text = f"""----前一章内容----
{text1}
----本章内容----
{text2}
----过渡----
"""
prompt_text = prompt_text.replace('\n\n', '\n')
res = ollama.generate(model="qwen2.5:72b-instruct", prompt=prompt_text, system=prompt_sys, keep_alive="1h",options={"num_ctx": 8192,"num_predict":-1})
result = res['response']
result = result.replace('\n\n', '\n')
print(result)
