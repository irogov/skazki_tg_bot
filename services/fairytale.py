import random, asyncio
from services.fairytale_properties import enemies_by_hero_expanded, magic_items_expanded
from openai import AsyncOpenAI
from services.fairytale_properties import groups
from config.config import load_config

config = load_config()
deepseek_key = config.ai

def get_hero_villain():
    res = random.choice(list(enemies_by_hero_expanded.items()))
    hero = res[0]
    villain = random.choice(res[1])
    return hero, villain

def get_magic_item():
    res = random.choice(list(magic_items_expanded.items()))
    item = res[0]
    use = res[1]
    return item, use

def get_query(group: int) -> str:
    query_cl = groups[group]
    hero, villain = get_hero_villain()
    item, use = get_magic_item()
    preface = "Напиши русскую сказку. Используй схему Проппа. Верни только сказку без упоминаний функций Проппа."
    characters = f'Главным героем должен быть {hero}, его соперником должен быть {villain}'
    magic_items = f'Магический предмет (не обязательный): {item} ({use})'
    age = f"Для возраста: {query_cl['min_age']} - {query_cl['max_age']}."
    length = f"Длинна: {query_cl['min_char']} - {query_cl['max_char']} слов."
    specials = f"Особенности: {query_cl['specials']}."
    query = f'{preface} {characters} {magic_items} {age} {length} {specials}'
    return query, group
        
async def get_story(group: int, client: AsyncOpenAI):
    # client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
    query, new_group = get_query(group)
    messages = [{"role": "user", "content": query}]
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    ) 
    return response.choices[0].message.content, new_group

# Функция, возвращающая строку с текстом страницы и её размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    end_signs = ',.!:;?'
    counter = 0
    if len(text) < start + size:
        size = len(text) - start
        text = text[start:start + size]
    else:
        if text[start + size] == '.' and text[start + size - 1] in end_signs:
            text = text[start:start + size - 2]
            size -= 2
        else:
            text = text[start:start + size]
        for i in range(size - 1, 0, -1):
            if text[i] in end_signs:
                break
            counter = size - i
    page_text = text[:size - counter]
    page_size = size - counter
    return page_text, page_size


# Функция, формирующая словарь книги
def prepare_book(text: str, page_size: int = 4000):
    book = {}
    f = text
    page_count = 1
    start = 0
    while start < len(f):
        page_text, size = _get_part_text(f, start, page_size)
        book[page_count] = page_text.lstrip()
        page_count += 1
        start += size
    return book
