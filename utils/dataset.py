import numpy as np
import pandas as pd
import os
import re

from statistic import stat_para_nums
from statistic import stat_sen_nums
from statistic import calc_tokens_use_google_genai
from easse.sari import corpus_sari


# 从wiki——aoto中加载对齐的简化doc，nums可以指定一次加载多少对数据
# path  = "F:\自然语言处理学习\dataset\wiki_auto_plan\wikiauto_docs_test.csv"
def load_wiki_doc(path=os.path.abspath(os.path.join(os.getcwd(), "..")) + r"\data\wiki-auto\wikiauto_docs_test.csv",
                  nums=1, random_seed=10):
    # 读取csv文件
    path = r"F:\自然语言处理学习\dataset\wiki_auto_plan\wikiauto_docs_test.csv"
    df = pd.read_csv(path)
    complex_col = df['complex']
    simple_col = df['simple']

    # num = 0
    # flag = 0
    # for i in complex_col:
    #     num += 1
    #     tokens = calc_tokens(i)
    #     if tokens >= 300:
    #         flag += 1
    #     print("========")
    # print(num)
    # print(flag)

    # 随机生成nums个随机数
    np.random.seed(random_seed)
    random_index = np.random.randint(0, len(complex_col), nums)
    # 从df中取出对应的数据
    complex_doc = complex_col[random_index]
    simple_doc = simple_col[random_index]
    return complex_doc.tolist(), simple_doc.tolist()

"""

"""
# path = "F:\自然语言处理学习\dataset\newsela_share_2020\newsela_share_2020\documents\articles"
def load_newsela_doc(
        path=os.path.abspath(os.path.join(os.getcwd(), "..")) + r"\data\newsela\articles\\",
        nums=1, random_seed=10):
    # 读取path下的所有文件
    path =r"F:\自然语言处理学习\dataset\newsela_share_2020\newsela_share_2020\documents\articles\\"
    file_list = os.listdir(path)
    # 构造正则表达式，找到所有以“0.txt”结尾的文件名
    pattern = re.compile(r'.*0.txt')
    raw_file_list = list(filter(lambda x: pattern.match(x), file_list))
    # print(len(raw_file_list))
    # 拿到当前文件后面的4个文件（根据在file_list中的索引）
    doc_list = []
    for file in raw_file_list:
        index = file_list.index(file)
        temp_list = file_list[index:index + 5]
        # 检查temp_list中的文件名前缀是否一致
        prefix = file.split('-')[0]
        if len(temp_list) < 5:
            continue
        else:
            flag = 0
            for i in range(1, 5):
                if prefix != temp_list[i].split('-')[0]:
                    print(f"文件名前缀不一致！{prefix}<--------->{temp_list[i].split('-')[0]}")
                    flag = 1
                    break  # !!!
            if flag == 1:
                continue
        if len(temp_list) == 5:
            doc_list.append(temp_list)
    # 随机生成nums个随机数
    np.random.seed(random_seed)
    if nums > len(doc_list):
        nums = len(doc_list)
    random_index = np.random.randint(0, len(doc_list), nums)
    # 从list中取出对应的数据
    doc_list = np.array(doc_list)[random_index]
    # print(doc_list.shape)
    # print(doc_list)
    # 读取对应的文件内容
    content_list = []
    for i in range(len(doc_list)):
        temp_list = []
        for j in range(len(doc_list[i])):
            with open(path + doc_list[i][j], 'r', encoding='utf-8') as f:
                temp_list.append(f.read())
        content_list.append(temp_list)
    return doc_list, content_list


import csv


def write_list_to_csv(data_list, csv_file):
    with open(csv_file, 'w') as f:
        writer = csv.writer(f)
        for row in data_list:
            writer.writerow(row)


if __name__ == '__main__':

    wiki_doc_complex, wiki_doc_simple = load_wiki_doc(nums=2000)
    newsela_names, newsela_docs = load_newsela_doc(nums=2000)

    wiki_avg_token = 0
    newsela_avg_token = 0

    for i in range(len(wiki_doc_complex)):
        wiki_avg_token += calc_tokens_use_google_genai(wiki_doc_complex[i])
        newsela_avg_token += calc_tokens_use_google_genai(newsela_docs[i][0])
    wiki_avg_token /= len(wiki_doc_complex)
    newsela_avg_token /= len(newsela_docs)
    print("wiki_avg_token: ", wiki_avg_token)
    print("newsela_avg_token: ", newsela_avg_token)

    # As there is no consensus on what is “long”, we consider it to mean documents of several thousands of tokens in length

    wiki_dataset = []
    newsela_a = []
    newsela_b = []

    complex_col = wiki_doc_complex
    simple_col = wiki_doc_simple
    nums = 0
    avg_paras_a = 0
    avg_paras_b = 0
    avg_sents_a = 0
    avg_sents_b = 0
    avg_words_a = 0
    avg_words_b = 0
    for i, j in zip(complex_col, simple_col):
        if 500 > calc_tokens_use_google_genai(i) > 300:
            if nums == 1000:
                break
            nums += 1
            # print(i)
            # print("=========")
            # print(j)
            wiki_dataset.append((i, j))
            paras_a = stat_para_nums(i)
            paras_b = stat_para_nums(j)
            avg_paras_a += paras_a
            avg_paras_b += paras_b

            sents_a = stat_sen_nums(i)
            sents_b = stat_sen_nums(j)
            avg_sents_a += sents_a
            avg_sents_b += sents_b

            words_a = calc_tokens_use_google_genai(i)
            words_b = calc_tokens_use_google_genai(j)
            avg_words_a += words_a
            avg_words_b += words_b

    print(nums)
    write_list_to_csv(wiki_dataset, 'wiki_dataset.csv')
    print(avg_words_a / nums)
    print(avg_words_b / nums)
    print(avg_sents_a / nums)
    print(avg_sents_b / nums)
    print(avg_paras_a)
    print(avg_paras_b)

    docs = newsela_names
    contents = newsela_docs
    numa = 0
    numb = 0

    all_para_a = 0
    all_para_b = 0
    all_sent_a = 0
    all_sent_b = 0
    all_word_a = 0
    all_word_b = 0
    sari1 = 0
    sari2 = 0
    sari3 = 0
    sari4 = 0
    sari5 = 0
    length_list = []
    for doc, content in zip(docs, contents):

        v0 = content[0]
        v1 = content[1]
        v2 = content[2]
        v3 = content[3]
        v4 = content[4]

        if calc_tokens_use_google_genai(v0) <= 1000:
            numa += 1
            all_para_a += stat_para_nums(v0)
            all_para_b += stat_para_nums(v1 + v2 + v3 + v4) / 4
            all_sent_a += stat_sen_nums(v0)
            all_sent_b += stat_sen_nums(v1 + v2 + v3 + v4) / 4
            all_word_a += calc_tokens_use_google_genai(v0)
            all_word_b += calc_tokens_use_google_genai(v1 + v2 + v3 + v4) / 4

            if numa >= 500:
                continue
            else:
                newsela_a.append([v0, v1, v2, v3, v4])


        else:
            if calc_tokens_use_google_genai(v0) <= 2000:

                numb += 1

                if numb >= 500:
                    continue
                else:
                    newsela_b.append([v0, v1, v2, v3, v4])

                list1, raw_sari = corpus_sari([v0], [v0], [[v1], [v2], [v3], [v4]])
                list2, ref1_sari = corpus_sari([v0], [v1], [[v1], [v2], [v3], [v4]])
                list3, ref2_sari = corpus_sari([v0], [v2], [[v1], [v2], [v3], [v4]])
                list4, ref3_sari = corpus_sari([v0], [v3], [[v1], [v2], [v3], [v4]])
                list5, ref4_sari = corpus_sari([v0], [v4], [[v1], [v2], [v3], [v4]])
                sari1 += raw_sari
                sari2 += ref1_sari
                sari3 += ref2_sari
                sari4 += ref3_sari
                sari5 += ref4_sari

    print(numa)
    write_list_to_csv(newsela_a, 'newsela_a.csv')
    write_list_to_csv(newsela_b, 'newsela_b.csv')
    print(all_para_a / numa)
    print(all_para_b / numa)
    print(all_sent_a / numa)
    print(all_sent_b / numa)
    print(all_word_a / numa)
    print(all_word_b / numa)
    for li in length_list:
        print(li)
        print("---------------")
