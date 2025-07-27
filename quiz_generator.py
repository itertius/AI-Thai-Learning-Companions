from pythainlp.tokenize import word_tokenize
import random

def generate_vocab_quiz(text):
    word = word_tokenize(text, engine="newmm")
    vocab = list(set([w for w in word if len(w)>1]))
    random.shuffle(vocab)

    quizzes = []
    for word in vocab[:5]:
        choices = random.sample(vocab, min(3, len(vocab)-1))
        if word not in choices:
            choices.append(word)
        random.shuffle(choices)
        quizzes.append({
            "question": f"คำว่า '{word}' แปลว่าอะไร?",
            "choices": choices,
            "answer": word
        })
    return quizzes