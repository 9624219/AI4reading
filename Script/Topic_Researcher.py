import ollama
from utils.chat import Deepseek_Generate

async def topic_demonstrate(raw_doc,case_json):
    result = {}
    for key, value in case_json.items():
        prompt_sys = f"""你是一个经验丰富的内容分析师，你的任务是根据输入的章节内容、核心主题与案例信息，在不偏离核心主题的前提下，解释案例是如何支撑主题的。
你可以按照以下步骤完成此任务：
----步骤----
1. 根据书本内容和核心主题，明确主题的核心思想。
2. 识别案例中支持主题的关键细节，找出案例中的支撑点。
3. 分析案例与主题的逻辑关系，建立因果逻辑。
4. 结合书中理论或观点进行解释。
----输出要求----
请务必生成纯文本格式的内容，不能带有任何形式的标题或项目符号列表。
"""
        prompt_text = f"""----章节内容----
{raw_doc}
----核心主题----
{key}
----案例信息----
{value}
"""
        prompt_text = prompt_text.replace('\n\n', '\n')
        res = Deepseek_Generate(prompt_text, prompt_sys)
        result[key] = res
    print(result)
    return result


async def topic_expansion(raw_doc,case_json,topic_demonstrate):
    result = {}
    for key, value in case_json.items():
        prompt_sys = f"""你是一个经验丰富的书本讲解者，你的任务是在不偏离章节内容和核心主题的前提下，对案例进行拓展，你必须确保扩展内容与核心主题相关。
你可以通过融入个人理解、引用与主题相关的观点或者名言、增加与核心主题契合的现代生活相关的内容等方式，来使内容更加丰富和深入，最终帮助听众获得更全面、更有深度的知识。
----输出要求----
请务必生成纯文本格式的内容，不能带有任何形式的标题或项目符号列表。
"""
        prompt_text = f"""----章节内容----
{raw_doc}
----核心主题----
{key}
----案例信息----
{value}
----案例论证----
{topic_demonstrate[key]}
"""
        prompt_text = prompt_text.replace('\n\n', '\n')
        res = Deepseek_Generate(prompt_text, prompt_sys)
        result[key] = res
    print(result)
    return result
