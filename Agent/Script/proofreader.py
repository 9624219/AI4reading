import ollama
from utils.chat import Deepseek_Generate


async def case_feedback3(raw_doc,last_topic):
    prompt_sys = f"""你是一个内容校对员，你的任务是按以下要求审查生成的案例列表。
----要求----
1. 案例与章节的核心主题直接相关，它不是一个偏离主旨的次要故事或无关情境。
2. 案例反映了章节内容的不同方面或观点。
3. 案例符合章节的逻辑结构，案例中的因果关系清晰。
如果所有的主题都符合要求，请仅返回“是”。若存在不满足的情况，请返回“否”，并给出具体的修改意见。
"""
    prompt_text = f"""----章节内容----
章节内容：{raw_doc}
----案例列表----
"""
    topic_str  = ""
    cur = 1
    for key,value in last_topic.items():
        topic_str += f"""案例 {cur}: {value}; 
"""
        cur += 1
    prompt_text += topic_str
    prompt_text = prompt_text.replace('\n\n','\n')
    result = Deepseek_Generate(prompt_text, prompt_sys)
    return result


def organize_case_feedback(raw_doc,full_case,case_demonstrate,case_expansion,organize_text):
    result_dict = {}
    prompt_sys = f"""你是一个内容校对员，你的任务是根据输入的信息评价整合文本的质量，按以下要求审查案例信息。
----要求----
检视整合文本中的分析部分是否充分，支撑材料是否能够有力地佐证案例及核心主题。论证部分应该解释清楚“为什么”和“怎么样”，而不仅仅是表面上的描述。
如果给出的案例符合要求，请仅返回“是”。若存在不满足的情况，请返回“否”，并根据章节内容和要求给出具体的修改意见，修改意见不能包含修改后的文本。
"""
    for key, value in organize_text.items():
        prompt_text = f"""----章节内容----
{raw_doc}
----主题----
{key}
----案例信息----
{full_case[key]}
----案例解释----
{case_demonstrate[key]}
----案例拓展----
{case_expansion[key]}
----整合文本----
{value}
"""
        result = Deepseek_Generate(prompt_text, prompt_sys)
        if result.startswith('是'):
            result_dict[key] = '是'
        else:
            result_dict[key] = result
    return result_dict



async def organize_case_feedback_content(raw_doc,full_case,case_demonstrate,case_expansion,organize_text):
    result_dict = {}
    prompt_sys = f"""你是一个内容校对员，你的任务是根据输入的信息评价整合文本的内容是否完整，请按以下要求审查案例信息。
----要求----
1. 核心主题是否完整呈现？主要论点是否明确传达？检查文本是否完整传达了章节的核心主题或主要论点。
2. 支持性信息是否充足？是否有足够的背景信息、数据、案例或证据来支撑主要论点？
----
如果给出的案例符合要求，请仅返回“是”。若存在不满足的情况，请返回“否”，并根据章节内容和要求给出具体的修改意见，修改意见不能包含修改后的文本。
"""
    for key, value in organize_text.items():
        prompt_text = f"""----章节内容----
{raw_doc}
----主题----
{key}
----案例信息----
{full_case[key]}
----案例解释----
{case_demonstrate[key]}
----案例拓展----
{case_expansion[key]}
----整合文本----
{value}
"""
        result = Deepseek_Generate(prompt_text, prompt_sys)
        if result.startswith('是'):
            result_dict[key] = '是'
        else:
            result_dict[key] = result
    return result_dict

'''
整合文本内容的逻辑是否清晰
'''


async def organize_case_feedback_logic(raw_doc,full_case,case_demonstrate,case_expansion,organize_text):
    result_dict = {}
    prompt_sys = f"""你是一个内容校对员，你的任务是根据输入的信息评价整合文本内容的逻辑与结构，按以下要求审查案例信息。
----要求----
1. 段落顺序是否合理？评估各个段落或部分的顺序是否合乎逻辑。开头是否有效引入主题，中间部分是否按照由浅入深或由一般到具体的逻辑展开，结尾是否有总结或升华。
2. 案例的因果关系是否清晰？是否能够清晰地表达事件的发展过程和结果。
3. 过渡语句是否合理？检查每个段落之间的过渡是否自然。是否有足够的过渡语句或逻辑桥梁，将不同部分有机连接？
如果给出的案例符合要求，请仅返回“是”。若存在不满足的情况，请返回“否”，并根据章节内容和要求给出具体的修改意见，修改意见不能包含修改后的文本。
"""
    for key, value in organize_text.items():
        prompt_text = f"""----章节内容----
{raw_doc}
----主题----
{key}
----案例信息----
{full_case[key]}
----案例解释----
{case_demonstrate[key]}
----案例拓展----
{case_expansion[key]}
----整合文本----
{value}
"""
        result = Deepseek_Generate(prompt_text, prompt_sys)
        if result.startswith('是'):
            result_dict[key] = '是'
        else:
            result_dict[key] = result
    return result_dict


async def organize_case_feedback_enlightening(raw_doc,full_case,case_demonstrate,case_expansion,organize_text):
    result_dict = {}
    prompt_sys = f"""你是一个内容校对员，你的任务是根据输入的信息评价整合文本的启发性，按以下要求审查案例信息。
----要求----
1. 内容是否包括情感共鸣？内容是否通过故事、案例或情感化的描述激发听众的情感反应，让他们在感性层面产生认同或反思？
2. 讲稿是否不仅局限于具体案例，还能够抽象出普遍性原则，帮助听众在其他情境中运用这些知识？
如果给出的案例符合要求，请仅返回“是”。若存在不满足的情况，请返回“否”，并根据章节内容和要求给出具体的修改意见，修改意见不能包含修改后的文本。
"""
    for key, value in organize_text.items():
        prompt_text = f"""----章节内容----
{raw_doc}
----主题----
{key}
----案例信息----
{full_case[key]}
----案例解释----
{case_demonstrate[key]}
----案例拓展----
{case_expansion[key]}
----整合文本----
{value}
"""
        result = Deepseek_Generate(prompt_text, prompt_sys)
        if result.startswith('是'):
            result_dict[key] = '是'
        else:
            result_dict[key] = result
    return result_dict




async def organize_refine(raw_doc,full_case,case_demonstrate,case_expansion,organize_text,feedback):
    prompt_sys = f"""你是一个书本解读者，你已经通过整合案例信息与书本内容得到了内容解读的草稿，并收到了修改建议。你的任务是对照修改建议，将草稿进行完善。仅返回修改后的整合文本，不要返回任何无关文字。"""
    new_dict = {}
    wrong_key = []
    for key, value in feedback.items():
        if feedback[key].startswith('是'):
            new_dict[key] = organize_text[key]
            continue
        else:
            wrong_key.append(key)
            prompt_text = f"""----章节内容----
{raw_doc}
----主题----
{key}
----案例----
{full_case[key]}
----案例论证----
{case_demonstrate[key]}
----案例拓展----
{case_expansion[key]}
----整合草稿----
{organize_text[key]}
----修改建议----
{feedback[key]}
"""
            result = Deepseek_Generate(prompt_text, prompt_sys)
            new_dict[key] = result
    wrong_key_str = "<".join(wrong_key)
    return new_dict,wrong_key_str


async def oral_feedback(organize_text,oral_text):
    result_dict = {}
    prompt_sys = f"""你是一个专业的书本解读者，负责以深入浅出的解读方式，帮助听众轻松领悟书中精华，给工作、生活、学习带来帮助和启发。
你的任务是根据输入的信息评价口语化改写文本是否满足解读需求，确保讲稿生动、流畅、且能够引起听众兴趣。
----要求----
1. 是否避免了书面化、复杂或生硬的句式？使用的词汇和表达方式，听众能否轻松理解？
2. 句子是否听起来自然，轻松，信息之间是否过渡自然，衔接流畅？是否通过短句、停顿和口语常用的词汇，增加了语气的节奏感？
3. 是否通过提问、类比或互动性语言，鼓励听众代入和思考？是否让听众感觉你是在和他们对话，而不是单向灌输？
如果给出的案例符合要求，请仅返回“是”。若存在不满足的情况，请返回“否”，并根据章节内容和要求给出具体的修改意见，修改意见不能包含修改后的文本。
"""
    for key, value in oral_text.items():
        prompt_text = f"""----主题----
{key}
----主题内容----
{organize_text[key]}
----口语化改写文本----
{value}"""
        result = Deepseek_Generate(prompt_text, prompt_sys)
        if result.startswith('是'):
            result_dict[key] = '是'
        else:
            result_dict[key] = result
    return result_dict

# async def oral_refine(raw_doc,organize_text,oral_text,feedback):
async def oral_refine(raw_doc,organize_text,oral_text,feedback):
    prompt_sys = f"""你是一个书本解读者，你已经对主题内容进行了口语化改写，并收到了修改建议。你的任务是对照修改建议，将口语化改写文本进行完善，确保讲稿生动、流畅、且能够引起听众兴趣。请仅返回修改后的口语化改写文本，不要返回任何无关文字。"""
    new_dict = {}
    wrong_key = []
    for key, value in feedback.items():
        if feedback[key].startswith('是'):
            new_dict[key] = organize_text[key]
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


async def final_feedback_consistent(raw_doc,final_text):
    prompt_sys = f"""你是一个专业的书本解读者，负责以深入浅出的解读方式，帮助听众轻松领悟书中精华，给工作、生活、学习带来帮助和启发。
你的任务是根据章节内容评价讲稿是否满足解读要求，确保讲稿生动、流畅、且能够引起听众兴趣。
----要求----
1. 案例之间是否有清晰的过渡句或过渡段落？过渡是否帮助听众从一个话题顺利过渡到另一个话题？ 如果发现部分转折不自然，可以添加过渡句或引导语。
2. 每个观点、每个案例是否自然引出下一个部分？听众是否能无意识地跟随你的思路推进？
如果给出的案例符合要求，请仅返回“是”。若存在不满足的情况，请返回“否”，并根据章节内容和要求给出具体的修改意见，修改意见不能包含修改后的文本。
"""
    prompt_text = f"""----章节内容----
{raw_doc}
----讲稿----
{final_text}"""
    result = Deepseek_Generate(prompt_text, prompt_sys)
    if result.startswith('是'):
        return '是'
    else:
        return result

async def final_feedback_expression(raw_doc,final_text):
    prompt_sys = f"""你是一个专业的书本解读者，负责以深入浅出的解读方式，帮助听众轻松领悟书中精华，给工作、生活、学习带来帮助和启发。
你的任务是根据章节内容评价讲稿是否满足解读要求，确保讲稿生动、流畅、且能够引起听众兴趣。
----要求----
1. 语言是否简洁易懂，避免使用过于复杂的词汇或长句子？如果用词较为复杂，可以通过替换简单词汇来改善
2. 语言是否具有亲和力，能够让听众感到轻松，像是朋友之间的对话？可以通过加入一些日常用语、幽默感和个性化的表达，使讲稿更具亲和力。
3. 语言是否有足够的生动性，能够通过比喻、类比等手法使复杂的概念更容易理解？可以加入一些幽默或情感色彩，避免纯粹的学术性或教条性语言。
如果给出的案例符合要求，请仅返回“是”。若存在不满足的情况，请返回“否”，并根据章节内容和要求给出具体的修改意见，修改意见不能包含修改后的文本。
"""
    prompt_text = f"""----章节内容----
{raw_doc}
----讲稿----
{final_text}"""
    result = Deepseek_Generate(prompt_text, prompt_sys)
    if result.startswith('是'):
        return '是'
    else:
        return result

def final_feedback_inspiration(raw_doc,final_text):
    prompt_sys = f"""你是一个专业的书本解读者，负责以深入浅出的解读方式，帮助听众轻松领悟书中精华，给工作、生活、学习带来帮助和启发。
你的任务是根据章节内容评价讲稿是否满足解读要求，确保讲稿生动、流畅、且能够引起听众兴趣。
----要求----
1. 讲稿是否包含能引发听众思考的问题？这些问题是否贴近听众的实际工作或生活场景？
2. 讲稿是否给出了清晰的行动建议或指导，能够帮助听众解决实际问题？
3. 讲稿是否与听众产生互动，听众是否能参与其中，感到自己是讲解的一部分？讲稿是否传递了情感，让听众感到共鸣和触动？
如果给出的案例符合要求，请仅返回“是”。若存在不满足的情况，请返回“否”，并根据章节内容和要求给出具体的修改意见，修改意见不能包含修改后的文本。
"""
    prompt_text = f"""----讲稿----
{final_text}"""
    result = Deepseek_Generate(prompt_text, prompt_sys)
    if result.startswith('是'):
        return '是'
    else:
        return result

async def final_refine(final_text,feedback):
    if feedback.startswith('是'):
        return final_text,"是"
    else:
        prompt_sys = f"""你是一个专业的书本解读者，负责以深入浅出的解读方式，帮助听众轻松领悟书中精华，给工作、生活、学习带来帮助和启发。
你已经得到了章节讲稿的草稿，并收到了修改建议。你的任务是对照修改建议，将草稿进行完善，确保讲稿生动、流畅、且能够引起听众兴趣。请仅返回修改后的口语化改写文本，文本中不要包含任何如“大家好”等问候语，不要返回任何无关文字。"""
        prompt_text = f"""----草稿----
{final_text}
----修改反馈----
{feedback}"""
        result = Deepseek_Generate(prompt_text, prompt_sys)
        return result,"否"


async def compare_result(Lines,result1,result2):
    prompt_sys = f"""你是一个专业的书本解读者，负责以深入浅出的解读方式，帮助听众轻松领悟书中精华，给工作、生活、学习带来帮助和启发。
你的任务是比较两份讲稿，判断哪一份更符合解读要求。
----要求----
1. 案例之间有清晰的过渡句或过渡段落。过渡能够帮助听众从一个话题顺利过渡到另一个话题。
2. 每个观点、每个案例能够自然引出下一个部分，听众能够跟随你的思路推进。
3. 讲稿语言简洁易懂，避免使用过于复杂的词汇或长句子。
4. 讲稿语言具有亲和力，能够让听众感到轻松，像是朋友之间的对话。讲稿中含有日常用语、幽默感和个性化的表达。
5. 讲稿语言有足够的生动性，能够通过比喻、类比等手法使复杂的概念更容易理解。讲稿加入一些幽默或情感色彩，避免纯粹的学术性或教条性语言。
----返回格式----
如果讲稿1更符合要求，请返回“讲稿1”；如果讲稿2更符合要求，请返回“讲稿2”；并说明理由。
"""
    prompt_text = f"""----章节内容----
{Lines}
----讲稿1----
讲稿1：{result1}
----讲稿2----
讲稿2：{result2}"""
    result = Deepseek_Generate(prompt_text, prompt_sys)
    if result.startswith('讲稿2'):
        return '讲稿2'
    else:
        return '讲稿1'