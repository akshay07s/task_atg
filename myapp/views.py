from django.shortcuts import render
from django.http import HttpResponse
from .models import URLModel
from .forms import URLForm
import requests
from bs4 import BeautifulSoup
import re

# Create your views here.
def frequency(request):
    form = URLForm()

    return render(request,'myapp/frequency.html',{'form':form})

def result(request):
    
    if request.method == 'POST':

        url = request.POST['url']
        context = {}

        if URLModel.objects.filter(url=url).exists():

            context['message'] = "URL Already Exists! Data from DataBase"

        else:

            context['message'] = "New URL!"

            try:
                # get request from url
                r = requests.get(url)

            except:
                return HttpResponse('Invalid URL')

            urlobj = URLModel.objects.create(url = url)
            
            # fetching data from url
            soup = BeautifulSoup(r.content, 'html.parser')

            # converting html to list
            list1 = soup.get_text(" ", strip=True).lower().split()

            common_words = ['the', 'at', 'there', 'some', 'my', 'of', 'be', 'use', 'her', 'than', 'and', 'this', 'an', 'would', 'first', 'a', 'have', 'each', 'make', 'water', 'to', 'from', 'which', 'like', 'been', 'in', 'or', 'she', 'him', 'call', 'is', 'one', 'do', 'into', 'who', 'you', 'had', 'how', 'time', 'oil', 'that', 'by', 'their', 'has', 'its', 'it', 'word', 'if', 'look', 'now', 'he', 'but', 'will', 'two', 'find', 'was', 'not', 'up', 'more', 'long', 'for', 'what', 'other', 'write', 'down', 'on', 'all', 'about', 'go', 'day', 'are', 'were', 'out', 'see', 'did', 'as', 'we', 'many', 'number', 'get', 'with', 'when', 'then', 'no', 'come', 'his', 'your', 'them', 'way', 'made', 'they', 'can', 'these', 'could', 'may', 'i', 'said', 'so', 'people', 'part','me','our']

            # remove non-alphabetic characters from start and end of words
            index=0
            while index<len(list1):
                list1[index] = re.sub("^\W|\W$","",list1[index])
                if list1[index]=="":
                    list1.pop(index)
                index+=1

            # removing common words from list
            list2 = [x for x in list1 if x not in common_words]

            # removing repeated words and forming a new list 
            list3= list(set(list2))
            
            # sorting according to count and storing first 10
            wordlist = sorted(list3, key = lambda x : list2.count(x), reverse = True)[0:10]

            # storing count of first 10
            countlist = []

            for word in wordlist:
                countlist.append(str(list2.count(word)))

            # adding values to model instance
            urlobj.tenwords = ", ".join(wordlist)
            urlobj.wordcount = ", ".join(countlist)
            urlobj.save()

        context['ten_words'] = zip(URLModel.objects.get(url=url).tenwords.split(", ") ,URLModel.objects.get(url=url).wordcount.split(", "))

    return render(request,'myapp/result.html',context)    