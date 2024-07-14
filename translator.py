from transformers import MarianMTModel, MarianTokenizer

# Создаем объект токенизатора и модели для русского-английского
model_name_ru_en = "Helsinki-NLP/opus-mt-ru-en"
tokenizer_ru_en = MarianTokenizer.from_pretrained(model_name_ru_en)
model_ru_en = MarianMTModel.from_pretrained(model_name_ru_en)

# Функция перевода с русского на английский
def translate_ru_to_en(text):
    tokens = tokenizer_ru_en.prepare_seq2seq_batch([text], return_tensors="pt")
    translated = model_ru_en.generate(**tokens)
    translation = [tokenizer_ru_en.decode(t, skip_special_tokens=True) for t in translated]
    return translation[0]

# Теперь создаем объект токенизатора и модели для английского-русского
model_name_en_ru = "Helsinki-NLP/opus-mt-en-ru"
tokenizer_en_ru = MarianTokenizer.from_pretrained(model_name_en_ru)
model_en_ru = MarianMTModel.from_pretrained(model_name_en_ru)

# Функция перевода с английского на русский
def translate_en_to_ru(text):
    tokens = tokenizer_en_ru.prepare_seq2seq_batch([text], return_tensors="pt")
    translated = model_en_ru.generate(**tokens)
    translation = [tokenizer_en_ru.decode(t, skip_special_tokens=True) for t in translated]
    return translation[0]


    