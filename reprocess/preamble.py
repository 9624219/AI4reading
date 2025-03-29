from utils.chat import Qwen_Generate
import ollama

from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="",
)

bookname = ""
prompt_sys = f"""你是一个经验丰富的书本解读者。你的任务是根据输入的书本名称，前言内容，写一个简短、亲切、轻松、富有吸引力的开头语，为后续章节内容的解读做铺垫。
你需要做到以下几点：
1. 开头语的语气必须是口语化、亲切的，贴近听众的生活和实际需求。内容必须通俗易懂，引起听众的共鸣。
2. 开头语必须清晰地指出书本的背景，要解决的问题，以及它对听众的意义。
3. 内容必须连贯，无明显的逻辑错误、突兀的转折或不合理的结构。
4. 结尾不能是呼吁性质的内容，不要出现任何形式的呼吁、号召或建议。能够顺利连接到后续章节内容的解读。
----输出要求----
请务必生成纯文本格式的内容，不能带有任何形式的标题或项目符号列表。
"""


raw_doc = open('', 'r', encoding='utf-8').read()
prompt_text = f"""----书本名称----
{bookname}
----前言----
{raw_doc}
"""
prompt_text = prompt_text.replace('\n\n', '\n')

completion = client.chat.completions.create(
    model="qwen2.5-72b-instruct",
    messages=[
        {"role": "system", "content": prompt_sys},
        {"role": "user", "content": prompt_text},
    ])
print(completion)
res = completion['choices'][0]['message']['content']
res = res.replace('\n\n', '\n')
print(res)