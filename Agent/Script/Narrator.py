import ollama
from utils.chat import Deepseek_Generate
import re




async def case_change_style(case_dict):
    result_dict = {}
    prompt_sys = f"""你是一个经验丰富的书本解读者，擅长以通俗易懂的解读方式，帮助听众轻松领悟书中精华。
你的任务是根据输入信息，将主题内容以口语化、第三人称的方式重新表达，使听众更易理解。你可以按照以下步骤完成任务。
----步骤----
1. 将书面语的长句子拆分为短小、易懂的句子，尽量少用复杂的修饰词。口语表达要自然、轻松，避免过于正式或复杂的语言结构。
2. 适当加入口语常用的词汇、短语和语气词，让表达显得更生活化。也可以用“嗯”“啊”等词填充对话空隙，模仿真实交流中的停顿。
3. 可以通过提问和假设场景引导听众思考，增强互动感。口语风格常常通过提问或与听众对话来激发兴趣。
4. 将以上内容整合成一个连贯的口语化段落，确保信息自然过渡、流畅衔接。
----格式要求----
你必须以不带任何格式信息的纯文本输出结果，不要返回任何提纲类信息。
"""
    for key, value in case_dict.items():
        prompt_text = f"""----核心主题----
{key}
----主题内容----
{value}
"""
        prompt_text = prompt_text.replace('\n\n', '\n')
        result = Deepseek_Generate(prompt_text, prompt_sys)
        result_dict[key] = result
    return result_dict


async def oral_refine(organize_text,oral_text,feedback):
    prompt_sys = f"""你是一个书本解读者，你已经对主题内容进行了口语化改写，并收到了修改建议。你的任务是对照修改建议，将口语化改写文本进行完善，确保讲稿生动、流畅、且能够引起听众兴趣。请仅返回修改后的口语化改写文本，不要返回任何无关文字。"""
    new_dict = {}
    wrong_key = []
    for key, value in feedback.items():
        if feedback[key].startswith('是'):
            new_dict[key] = oral_text[key]
            continue
        else:
            wrong_key.append(key)
            prompt_text = f"""----主题----
{key}
----主题内容----
{organize_text[key]}
----口语化改写文本----
{oral_text[key]}
----修改建议----
{feedback[key]}
"""
            result = Deepseek_Generate(prompt_text, prompt_sys)
            new_dict[key] = result
    wrong_key_str = "<".join(wrong_key)
    return new_dict,wrong_key_str
