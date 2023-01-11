#Kata - https://www.codewars.com/kata/51e056fe544cf36c410000fb

def top_3_words(text):
    other_chars = '#\/,.?!:;_-'
    for char in other_chars:
        text = text.replace(char,' ')

    words = text.lower().split()
    frequncy = {word: words.count(word) for word in words}
    sort_freq = sorted(frequncy.items(), key=lambda item: item[1], reverse = True)
    return [key for key, item in sort_freq[:3] if key.count('\'') != len(key)]