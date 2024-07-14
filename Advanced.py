from transformers import pipeline
from translator import *
import re

pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-emotion-multilabel-latest", top_k = 3)

emotions = {
    'anger' : '🤬',
    'anticipation' : '😯',
    'disgust' : '😖',
    'fear' : '😱',
    'joy' : '🤗',
    'love' : '🌸',
    'optimism' : '😌',
    'pessimism' : '😒',
    'sadness' : '😔',
    'surprise' : '😳',
    'trust' : '🤝'
}

texts = [
        "Ты выглядишь потрясающе!",
        "Я очень боюсь собак.",
        "Моя собака вчера умерла.",
        "Я тебя больше не люблю!",
        "Я бы хотел умереть прямо сейчас.",
        "Я думаю, что люблю тебя...",
        "Я НЕНАВИЖУ ТЕБЯ!",
        "Может быть, моя ненависть лишь плод моих фантазий и мне стоит простить тебя? Все таки ты то еще быдло!"
         ]

import re

def TranslateToEnglishApart(Phrase):

    PhraseApart = re.findall(r"[\w']+|[.,!?;]", Phrase)
    # print(PhraseApart)
    part = ''
    check = True
    PhraseFilter = []
    for literal in PhraseApart:
        if literal not in {'?', '.', '!', ';'}:
            if check is False: 
                PhraseFilter.append(part)
                part = ''
                check = True
            if literal == ',': part += (literal)
            else: part += (' ' + literal)
            # print(part)
            
            
        else:
            check = False
            part += literal
    PhraseFilter.append(part)
    PhraseFilter[0] = PhraseFilter[0].strip()

    # print(PhraseFilter)
    if len(PhraseFilter) > 1:
        # for 
        return [''.join([translate_ru_to_en(phrase) for phrase in PhraseFilter])]
    else:
        return [translate_ru_to_en(Phrase)]

# print(TranslateToEnglishApart("Может быть, моя ненависть лишь плод моих фантазий и мне стоит простить тебя?.. Все таки ты то еще быдло!"))


def Response(Phrase):

    PhraseApart = TranslateToEnglishApart(Phrase)
    
    texts_en = [translate_ru_to_en(phrase) for phrase in PhraseApart]
    results = pipe(texts_en)

    for text, result in zip(texts_en, results):
        EmotionsAll = [emotions[res['label']] if res['score'] > 0.5 else None for res in result]
        EmotionsFilter = list(filter( lambda x:  x if x is not None else x , EmotionsAll))
        print(text, ' ' , EmotionsFilter)    
    return EmotionsFilter if EmotionsFilter != [] else ['😐']
    # print(results)
# for Phrase in texts:
#     print(Response(Phrase))

Response("Может быть, моя ненависть лишь плод моих фантазий и мне стоит простить тебя?.. Все таки ты то еще быдло! Я все еще люблю тебя, но ты глубоко ранил мои чувства.")