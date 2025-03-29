import ollama
from utils.chat import Deepseek_Generate
import json


def do_case_description(raw_doc,topics,brief):
    prompt_sys = f"""你是一个内容分析师，你的任务是根据输入的章节内容、主题及案例简介，在不偏离主题的前提下补全案例信息。补全案例时，确保内容不会因为细节过多而变得冗长或复杂。你需要确保故事易于理解，且保持清晰的结构。你可以按照以下步骤进行操作。
----步骤----
1. 回顾章节的主题，确保案例简介中的核心情节已经涵盖了章节内容中的重要部分。识别出哪些信息缺失，哪些部分需要补充。
2. 简要补充案例的背景信息，帮助听众更好地理解案例所处的情境。
3. 补充案例的关键细节，明确事件的结果及其对主题的影响。
4. 将补全后的案例信息以完整连贯的文本形式输出。
----格式要求----
你必须以不带任何格式信息的纯文本输出结果，不要返回任何提纲类信息。
"""
    prompt_text = f"""----章节内容----
{raw_doc}
----核心主题----
{topics}
----案例简介----
{brief}
"""
    prompt_text = prompt_text.replace('\n\n','\n')
    result = Deepseek_Generate(prompt_text, prompt_sys)
    print(result)
    return result

async def Case_Description(raw_doc,topics_json):
    case_dict = {}
    for key,value in topics_json.items():
        case = do_case_description(raw_doc, key, value)
        case_dict[key] = case
    print(case_dict)
    return case_dict



async def find_case(raw_doc):
    prompt_sys = f"""你是一个内容分析师，你的任务是根据输入的章节内容，选取紧扣章节主题和核心内容的重点案例。你可以采取以下步骤来完成任务。
----步骤----
1. 仔细阅读并理解章节内容，明确章节的核心主题与作者的观点。
2. 在章节中寻找与主题相关的、能引发听众共鸣的代表性案例，这些案例应能清晰地说明或支撑章节的主要论点。案例数量不大于3个。
3. 为每个案例提供一个核心主题，核心主题应准确反映案例的主要议题或作者试图传达的主要思想，具有抽象性、深刻性。
4. 为每个案例提供详细的描述，确保案例发展的顺序是清晰的，并且因果关系明确。
----格式要求----
请按以下格式将案例以JSON格式输出，不要包含任何格式信息。
核心主题1：案例内容
JSON格式的key为生成的核心主题，value为找到的案例内容。
"""
    prompt_text = f"""----章节内容----
{raw_doc}
"""
    prompt_text = prompt_text.replace('\n\n', '\n')
    result = Deepseek_Generate(prompt_text, prompt_sys)
    json_result = json.loads(result)
    print(json_result)
    return json_result

