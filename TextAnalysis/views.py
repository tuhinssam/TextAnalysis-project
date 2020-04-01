from django.http import HttpResponse
from django.shortcuts import render
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def welcome(request):
    return HttpResponse('<h1>Hello welcome to Django!</h1>')
'''
'''
def homepage(request):
    return render(request, 'home.html')

def aboutpage(request):
    return render(request, 'about.html')

def anaysetext(request):
    fulltext = request.GET['fulltext']
    wordscount = len(fulltext.split())
    #get top 5 frequent words
    top_freqnt_words =  wordFreqCount(" ".join(remove_stopwords(fulltext)))
    
    sentiment_dict = sentence_sentiment(fulltext)
    
    return render(request,'count.html', {'fulltext':fulltext,
    'wordcount':wordscount,
    'top_freqnt_words':top_freqnt_words,
    'sentiment_dict':sentiment_dict})

def wordFreqCount(inputtxt):
    word_tokens = word_tokenize(inputtxt)
    fdist = FreqDist()
    for token in word_tokens:
        fdist[token.lower()] += 1
    return fdist.most_common()[:5]

def sentence_sentiment(inputtxt):
    sentiment_dict = {}
    sia = SentimentIntensityAnalyzer()
    sentences = sent_tokenize(inputtxt)

    for sentence in sentences:
        lst = []
        ss = sia.polarity_scores(sentence)
        #print("Sentence: ", sentence)
        for k in sorted(ss):
            lst.append({k : ss[k]})
            #print('{0}: {1}, '.format(k, ss[k]), end='')
        sentiment_dict[sentence] = lst
    return sentiment_dict

def remove_stopwords(inputtext):
    english_stopwords = stopwords.words('english')
    new_stopwords =english_stopwords + [',','.','"',':','``']
    wo_stopword = []
    words = word_tokenize(inputtext)
    
    for word in words:
        if word not in new_stopwords:
            wo_stopword.append(word)
    return wo_stopword

