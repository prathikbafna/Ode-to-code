#!/usr/bin/env python
# coding: utf-8

# In[65]:



# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

# get_ipython().system('pip install tesseract-ocr')
# get_ipython().system('pip install pytesseract')


# In[66]:

km = None
flag = None

import nltk
import pytesseract
import shutil
import os
import random
try:
 from PIL import Image
except ImportError:
 import Image
from sklearn.cluster import KMeans
import numpy as np
import base64
from nltk.corpus import wordnet

import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'


# In[67]:

def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    


def clean_text(text):
    # lower text
    text = text.lower()
    # tokenize text and remove puncutation
    text = [word.strip(string.punctuation) for word in text.split(" ")]
    # remove words that contain numbers
    text = [word for word in text if not any(c.isdigit() for c in word)]
    # remove stop words
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    # remove empty tokens
    text = [t for t in text if len(t) > 0]
    # pos tag text
    pos_tags = pos_tag(text)
    # lemmatize text
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    # remove words with only one letter
    text = [t for t in text if len(t) > 1]
    # join all
    text = " ".join(text)
    return(text)


# In[68]:

#obtained using ml model
my_weights ={
    'acute': 2,
    'shortness': 4,
    'fall': 4, 'died': 2, 'rash': 2, 'packed': 2, 'skin': 4, 'or': 0, 'condition': 6, 'ptx': 4, 'nosocomial': 2, 'rupture': 4, 'GPLA': 4, 'aspiration': 2, 'oversedation': 4, 'somnolent': 4, 'perforation': 4, 'surgery': 8, 'time': 10, 'nsicu': 4, 'hemorrhage': 4, 'heel': 6, 'sepsis': 4, 'consultations': 8, 'wound': 6, 'Past': 4, 'deep': 2, 'decubitus': 2, 'overload': 2, 'hyperkalemia': 4, 'pneumonia': 4, 'x-ray': 6, 'number': 6, 'failure': 4, 'diagnosis': 10, 'medicine': 2, 'decubiti': 2, 'hypoglycemia': 4, 'dissection': 6, 'room': 8, 'operating': 6, 'gender': 8, 'od': 2, 'ccu': 4, 'clostridium': 4, 'wet': 2, 'Health': 10, 'error': 0, 'mistakenly': 0, 'consult': 8, 'resuscitation': 4, 'reopen': 0, 'fell': 0, 'eruption': 4, 'Diet': 4, 'transferred': 0, 'next': 0, 'rbc': 4, 'delirium': 4, 'Investigation': 6, 'subtherapeutic': 6, 'tube': 4, 'icu': 6, 'transfer': 0, 'chest': 4, 'Attending': 4, 'infection': 6, 'required': 0, 'hyperglycemia': 4, 'dka': 2, 'vein': 6, 'distress': 4, 'signature': 10, 'admission': 10, 'reaction': 6, 'physician': 10, 'Date': 10, 'fluids': 6, 'family': 6, 'of': 0, 'Reason': 4, 'findings': 0, 'renal': 2, 'lethargic': 2, 'mistake': 0, 'complicated': 4, 'drug': 6, 'birth': 8, 'maternity': 4, 'discharge': 10, 'allergic': 6, 'sedated': 4, 'accident': 6, 'acquired': 0, 'after': 4, 'Wound': 6, 'post': 6, 'op': 6, 'pneumothorax': 4, 'supratherapeutic': 4, 'MLC': 2, 'ICU': 6, 'treatment': 10, 'drop': 0, 'agitation': 2, 'ulcer': 4, 'hospital': 10, 'respiratory': 4, 'desaturation': 4, 'dropped': 0, 'identifier': 0, 'ward': 10, 'laceration': 2, 'sugars': 4, 'overdose': 6, 'history': 8, 'death': 2, 'summary': 10, 'breath': 4, 'Method': 4, 'referral': 4, 'operation': 6, 'Unit': 4, 'volume': 0, 'hematoma': 4, 'contact': 8, 'status': 6, 'difficile': 2, 'age': 10, 'telemetry': 2, 'bed': 10, 'transfusion': 4, 'Patient': 10, 'blood': 6, 'hypoxia': 4, 'Provided': 0, 'hospitalization': 8, 'slipped': 0, 'postoperative': 6, 'FIR': 4, 'complication': 6, 'mental': 4, 'Address': 8, 'expired': 0, 'discontinued': 6, 'syncopy': 4, 'hypotension': 4, 'low': 2, 'Examination': 6, 'nonresponsive': 2, 'reopening': 2, 'pressure': 2, 'line': 2, 'unresponsive': 2, 'Consultant': 8, 'hallucinations': 4, 'micu': 4, 'the': 0, 'Instructions': 4, 'Operating': 6, 'Source': 4, 'fluid': 4, 'iv': 4, 'sore': 4, 'appointment': 6, 'medication': 8, 'admit': 8, 'name': 10, 'polypharmacy': 4, 'Procedures': 4, 'trauma': 4, 'hypoxemia': 4, 'accidentally': 4, 'RTA': 4, 'thrombosis': 4
}

def returnSum(dict1,dict2):
    sum = 0
    for i in dict1:
        gg = dict1[i] *dict2[i]
        sum = sum + gg

    return sum

# In[72]:
def init():
  final=[]
  data_path = 'assets\\project'
  categories=os.listdir(data_path)
  for category in categories:
    folder_path=os.path.join(data_path,category)
    img_names = os.listdir(folder_path)        
          
    for img_name in img_names:
      img_path=os.path.join(folder_path,img_name)
      
      extractedInformation = pytesseract.image_to_string(Image.open(img_path))
      pdf_data=clean_text(extractedInformation).split()
      my_file = open('assets/my_keywords.txt',"r")
      k = my_file.read().split()
      k = set(k)
      dict_keywords={}
          
      for i in k:
        if i == 'ï»¿discharge':
          dict_keywords['discharge']=0
        else:        
          dict_keywords[i]=0
          
      for i in dict_keywords:
        if i in pdf_data:
          dict_keywords[i]+=1
      final.append(returnSum(dict_keywords,my_weights))
    final=[]
    
  
  km =KMeans(n_clusters = 2)
  x=final
  y=[]
  for i in range(1,len(x)+1):
    y.append(i)

  combined = np.vstack((x, y)).T
  km.fit(combined)

  y_p = km.fit_predict(combined)

  for1 = sum([i for i in range(len(x)) if y_p[i] == 1])

  for0 = sum([i for i in range(len(x)) if y_p[i] == 0])

  if for1 > for0 : flag = 1
  else : flag = 0
      
  # print(flag)

  # for i in range(len(x)):
  #   print(str(y_p[i])+ "   " +str(x[i]))





  
  
# file = open('assets/binary.txt', 'r')
# byte = file.read()
# file.close()
  
# decodeit = open('input.jpeg', 'wb')
# decodeit.write(base64.b64decode((byte)))
# decodeit.close()
# img_path='input.jpeg'


# # In[88]:


# extractedInformation = pytesseract.image_to_string(Image.open(img_path))
# pdf_data=clean_text(extractedInformation).split()
# my_file = open('assets/my_keywords.txt',"r")
# k = my_file.read().split()
# k = set(k)
# dict_keywords={}
        
# for i in k:    
#   if i == 'ï»¿discharge':
#     dict_keywords['discharge']=0
#   else:        
#     dict_keywords[i]=0
        
# for i in dict_keywords:
#   if i in pdf_data:
#     dict_keywords[i]+=1
# print(km.predict([[returnSum(dict_keywords,my_weights),1]]))


def validate(image):

  
  
  decodeit = open('input.jpeg', 'wb')
  decodeit.write(base64.b64decode((image)))
  decodeit.close()
  img_path='input.jpeg'

  extractedInformation = pytesseract.image_to_string(Image.open(img_path))
  pdf_data=clean_text(extractedInformation).split()
  my_file = open('assets/my_keywords.txt',"r")
  k = my_file.read().split()
  k = set(k)
  dict_keywords={}
  for i in k:
    dict_keywords[i]=0
        
  for i in dict_keywords:
    if i in pdf_data:
      dict_keywords[i]+=1
  m=(km.predict([[returnSum(dict_keywords,my_weights),1]]))

  if m==[flag]:
    return "Invalid"

  return "Valid"