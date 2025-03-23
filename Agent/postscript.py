from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="",
)
prompt_sys = f"""你是一个经验丰富的书本解读者。你的任务是根据输入的书本名称，后记内容，写一个简短、亲切、轻松、富有吸引力的结尾语。
你需要做到以下几点：
1. 语气必须是口语化、亲切的，贴近听众的生活和实际需求。内容必须通俗易懂，引起听众的共鸣。
2. 重申作者在后记中想要传达的主要思想或信息。指出任何特别重要的观点或结论，这可能是作者希望读者最后记住的信息。
3. 将后记中的要点与书的整体主题、论点或故事线相联系。强调后记如何加深对书中内容的理解，或者它揭示了哪些新的视角。
4. 分析后记对于理解该书及其时代背景的重要性。讨论这本书以及它的后记可能对读者、学术界或社会产生的长远影响。
5. 分享你作为解读者的个人感悟，说明这本书及后记对你个人的意义。
6. 用一句有力的话来结束讲稿，这句话应该能够概括整个演讲的精神，并且给听众留下深刻印象。
----输出要求----
请务必生成纯文本格式的内容，不能带有任何形式的标题或项目符号列表。
"""

prompt_text = ""
completion = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {'role': 'system', 'content': prompt_sys},
        {'role': 'user', 'content': prompt_text}
    ],
    temperature=1.3
)
res = completion.choices[0].message.content
res = res.replace('\n\n', '\n')
print(res)
