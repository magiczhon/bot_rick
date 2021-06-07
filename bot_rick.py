import pandas as pd
import re
import compress_fasttext
from gensim.matutils import hellinger

def get_ans(model, question, dialog_df):
    min_dist = 100
    index_ans = 0
    current_question_vector = model[question]
    for i in range(len(dialog_df)):
        tmp = hellinger(current_question_vector, dialog_df.iloc[i]["question_vector"])
        if tmp < min_dist:
            index_ans = i
            min_dist = tmp
    if min_dist == 100:
        print("WTF Morty?!")
    print(index_ans)
    return dialog_df.iloc[index_ans]["rick_answer"]

def get_df(model):
    df = pd.read_csv("RickAndMortyScripts.csv")
    q_a = {"question": [],
    "question_vector": [],
    "rick_answer": []}

    for i in range(1, len(df)):
        if df.iloc[i]["name"] == "Rick":
            processed_sentences = re.sub('[^a-zA-Z]', ' ', df.iloc[i - 1]["line"])
            processed_sentences = re.sub(r'\s+', ' ', processed_sentences)
            processed_sentences = processed_sentences.lower().strip()
            q_a["question"].append(processed_sentences)

            question_vector = model[processed_sentences]
            q_a["question_vector"].append(question_vector)

            q_a["rick_answer"].append(str(df.iloc[i]["line"]).strip())

    dialog_df = pd.DataFrame(q_a)
    return dialog_df

def processed_question(line):
    processed_question = re.sub('[^a-zA-Z]', ' ', line)
    processed_question = re.sub(r'\s+', ' ', processed_question).strip()
    return processed_question

def main():
    print("run")
    small_model = compress_fasttext.models.CompressedFastTextKeyedVectors.load('ft_freqprune_100K_20K_pq_100.bin')
    dialog_df = get_df(small_model)

    #question = "it's a joke?"
    #question = "i'm sad boy"
    #print("Enter question to Rick:")
    while(1):
        question = processed_question(input())

        answer = get_ans(small_model, question, dialog_df)
        print(answer)


if __name__ == "__main__":
    main()