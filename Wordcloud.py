import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
text_from_file_with_apath = open('search and discovery3.txt').read()
wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all = True)
wl_space_split = " ".join(wordlist_after_jieba)
stop_words = open(r"Baidu Stopwords.txt",encoding ="utf-8").read().split("\n")
my_wordcloud = WordCloud(font_path = 'Songti.ttc', stopwords=stop_words, background_color="white").generate(wl_space_split)
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()



