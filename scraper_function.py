# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 08:20:26 2019

@author: DELL
"""

from bs4 import BeautifulSoup
import bs4 as bs
import urllib.request
import numpy as np    
import pandas as pd 
import re 
from urllib.parse import quote  
import time
from selenium import webdriver
from datetime import date
import os


            
def scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, hd='h',
                clean=False, firstTime=False, selenium1=False, it_num=0, encod=0,
                start_para=0, end_para=None, numb=0,numb2=0, show=1):   

    
    url1=url
    filename=p+".xlsx"  
    filename2="list_link_old_"+p+".npy"
    print()
    print(url)

    if not firstTime:   
        set_link_old =set(np.load(filename2))
        #print(filename)
        d2 = pd.read_excel(filename)
        til=d2['title']
        set_title=set(til)
        print("Records:", len(til))
    else:
        print("First Time list")
        tt=[]
        np.save(filename2 , tt)
        set_link_old =set(np.load(filename2))
        set_title=set()
        til=[]
        
    set_link=set()
    dpp=0
    
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options )
    driver.set_page_load_timeout(50)
    
    
    flag=True
    print("OK ",end=" ")
    try:
       
        if selenium1:
                        # use this for javascript wrapper pages
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'lxml')#res, 'lxml')
            driver.quit()
        else:
            # use this for non-javascript wrapper pages
            r = urllib.request.Request(url, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
            source = urllib.request.urlopen(r,timeout=100)
            soup = bs.BeautifulSoup(source,'lxml')
        print("OK ")
        ###########################################################################
        x=soup.body#find('div', {"class": ["mainAreaPeace" ]})
        #x=soup.find('div', {"class": ["column--primary" ]})
        for url in x.findAll('a'):
            if "http" in str(url.get('href')):
                lik=str(url.get('href'))
            else:
                lik=url2+str(url.get('href'))
            if lik not in set_link_old: 
                set_link.add(lik)
                #print(lik)
    
    except:
        flag=False
        print("TimeOut")
        

    ###############################################################################
    
    print("Number of new links is: ",len(set_link))
    copy_set_link=set_link.copy()
    
    
    ###############################################################################
    ##################       Page Scrape       ####################################
    ###############################################################################
    
    listAll=[]
    xx=0
    
    '''
    while len(set_link)>700:
        url=set_link.pop()
        xx=xx+1
        print(xx)
    '''
    set_link2=set()    
    
    while flag==True and len(set_link)>0:
        listSmall=[]
        xt=set_link.pop()
        xx=xx+1
        if xx==it_num:break
        if show: print(xx,end=" ")
        try:
            list_url=re.split("/",xt)
            if encod==0:url= xt
            if encod==1:url= "/".join(list_url[:-1])+"/"+quote(list_url[-1])
            if encod==2:url= "/".join(list_url[:-2])+"/"+quote(list_url[-2])+"/"+list_url[-1] # yamm7
            if encod==3:url= "/".join(list_url[:-2])+"/"+quote(list_url[-2])+"/"+quote(list_url[-1])
        except:
            if show:print("----format----")

        
        #print(url)
        try:
            r = urllib.request.Request(url, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
            if show:print("OK ", end=" ")
            source = urllib.request.urlopen(r, timeout = 15)
            if show:print("OK ", end=" ")
            soup = bs.BeautifulSoup(source,'lxml')
            if show:print("OK ")
        except:
            if show:print("Time Out")
            continue
            
        try:  
            ################################# To change ############################
            #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            x=[]
            for  tu_dicts in set_tu_dicts1 :
                x=soup.findAll(tu_dicts[0],tu_dicts[1])
                if x!=[]:break
           
            try:
                lis1=[]
                for i in x[0].findAll('a'):
                    tex=re.findall("[\w ]+",i.text)[0].strip()
                    lis1.append(tex)
                text1="_".join(lis1)
                #if text1=="": text1="__"
                text1=re.findall("[\w ]+",text1)[0].strip()
            except:
                if x!=[] and x[0].text !="":
                    text1=re.findall("[\w ]+",re.sub("[\n ]+"," ",x[0].text))[0].strip()  
                else:
                    text1="_"
            #if text1=="" and x[0].text !="":
            #        text1=x[0].text.strip()
            #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            
            if hd=='h': 
                x1=soup.find('h2')#, {"class": ["main-title"]})  
                x2=soup.find('h1')
                if x1 != None and x2 != None:
                    text2=x1.text.strip()+"++"+x2.text.strip()
                elif x1 !=None:
                    text2=x1.text.strip()
                else:
                    text2=x2.text.strip()
            elif hd=='div':
                tu_dicts= set_tu_dicts1[-1]
                x=soup.find(tu_dicts[0],tu_dicts[1])
                text2=x.text.strip().strip("\n")
            else:
                x=soup.find(hd)
                text2=x.text.strip()
            #text2=x.text.strip()
            
            #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            
            today = date.today()
            text3=str(today)
            

            #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            lis4=[]
            x=[]
            for  tu_dicts in set_tu_dicts2 :
                x=soup.findAll(tu_dicts[0],tu_dicts[1])
                if x!=[]:break
            #print(x)
            for paragraph in x[0].findAll('p'):
                t=paragraph.text
                lis4.append(t)
                
            text4="\n".join(lis4[start_para:end_para])
            
    
            #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            x=[]
            for  tu_dicts in set_tu_dicts3 :
                x=soup.findAll(tu_dicts[0],tu_dicts[1])
                if x!=[]:break
            #print(x)   
            if x==[]: 
                text5=""
            else:
                lis1=[]
                for i in x[numb].findAll('a'):
                     tex=re.findall("[\w ]+",i.text)[numb2].strip().strip("#").replace("_"," ")
                     lis1.append(tex)
                text5="_".join(lis1)
                
    
            ################################# end change ############################
            #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            
            text6="/".join(url.split('/',3)[:3])+"/"
            text7=url.split('/',3)[3]
            
            if text2 in set_title:
                dpp=dpp+1
                continue
            #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
            listSmall.append(text1)
            listSmall.append(text2)
            listSmall.append(text3)
            listSmall.append(text4)
            listSmall.append(text5)
            listSmall.append(text6)
            listSmall.append(text7)
            listAll.append(listSmall)
            #if xx%100==0:
            #    df = pd.DataFrame(listAll, columns =['category', 'title','time','text','keywords']) 
            #    df.to_excel(filename)#, encoding='utf-8') 
            set_link2.add(xt)
    
        except Exception as e: 
            if show:print("bad Format")
            if show:print(e)
            
                
            
           
     
    d1 = pd.DataFrame(listAll, columns =['category', 'title','time','text','keywords','url1','url2']) 
    
    if not firstTime:
        df1=pd.concat([d1, d2],  axis=0, ignore_index=True, sort=False )
    else:
        df1=pd.concat([d1],  axis=0, ignore_index=True, sort=False )
        print("First Time")
    
     
    df=df1[['category', 'title','time','text','keywords','url1','url2']]
    
    df.to_excel(filename)#, encoding='utf-8') 
    df.to_csv(filename+'_csv')
    
    
    print("The total Number of the records: ",len(df)) 
    print("The Number of the duplicate title: ",dpp) 
    
    set_link_old= set_link_old | set_link2
    
    np.save(filename2 , list(set_link_old))
    
    
    if clean: set_link_old= set_link_old | set_link2|copy_set_link
    
    np.save(filename2 , list(set_link_old))
    return len(df),len(til)
    
###################################################################################


###################################################################################
flag=1
clean=True
show=0
ln_total=0
dp_total=0

start=time.time()

if flag:
    url="http://alrai.com/"
    url2="http://alrai.com"
    p="alrai"
    set_tu_dicts1=[('div', {"class": [ "titlepage"]}),('div', {"class": [ "title-2 padd10px"]}) ]
    set_tu_dicts2=[('div', {"class": ["articleBody desc-1 selectionShareable"]}), ('div', { "class":["articleBody"]})]
    set_tu_dicts3=[('div', {"class": [ "keywordsDiv"]})  ]
    selenium1=False#True
    encod=3
    hd='div'
    
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd,
            numb=-1,numb2=-1, show=show)

    ln_total=ln_total+ln
    dp_total=dp_total+dp
############################################################################################### 

if flag:
    url="https://www.masrawy.com/"
    url2="https://www.masrawy.com"
    p="masrawy"
    set_tu_dicts1=[('nav', {"class": [ "breadcrumb"]}) ]
    set_tu_dicts2=[('div', {"id": ["ArticleDetails details"]}), ('div', { "class":["ArticleDetails details"]})]
    set_tu_dicts3=[('div', {"class": [ "keywordsDiv"]})  ]
    selenium1=False#True
    encod=0
    hd='h1'
    
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd,
            numb=-1,numb2=-1, show=show)
    
    ln_total=ln_total+ln
    dp_total=dp_total+dp
############################################################################################### 
if flag:
    url="https://www.youm7.com/"
    url2="https://www.youm7.com"
    p="youm7"
    set_tu_dicts1=[('div', {"class": [ "breadcumb"]}) ]
    set_tu_dicts2=[('div', {"id": ["articleBody"]}), ('div', { "class":["detail body"]})]
    set_tu_dicts3=[('div', {"class": [ "tags"]})  ]
    selenium1=False#True
    encod=2
    hd='h1'
    
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean,  selenium1=selenium1, it_num=0,encod=encod, hd=hd,show=show)

    ln_total=ln_total+ln
    dp_total=dp_total+dp
###############################################################################################    
if flag:
    url="https://arabi21.com/"
    url2="https://arabi21.com"
    p="arabi21"
    set_tu_dicts1=[('div', {"class": [ "breadCrum21 row"]}) ]
    set_tu_dicts2=[('div', {"id": ["documentcontainer"]}), ('div', { "class":["detail body"]})]
    set_tu_dicts3=[('div', {"class": [ "tags21"]})  ]
    selenium1=False#True
    encod=0
    hd='h1'
    
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean,  selenium1=selenium1, it_num=0,encod=encod, hd=hd,show=show)
    
    ln_total=ln_total+ln
    dp_total=dp_total+dp
###############################################################################################    
if flag:
    url="http://almanar.com.lb/"
    url2=""
    p="almanar"
    set_tu_dicts1=[('div', {"class": [ "article-categories"]}) ]
    set_tu_dicts2=[('div', {"id": ["documentcontainer"]}), ('div', { "class":["article-content"]})]
    set_tu_dicts3=[('div', {"class": [ "article-tags"]}) ]
    selenium1=False
    encod=0
    hd='h2'
    
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd,show=show)
    
    ln_total=ln_total+ln
    dp_total=dp_total+dp
###############################################################################################

if flag:
    url="https://www.aljazeera.net/"
    url2="https://www.aljazeera.net"
    p="aljazeera"
    
    set_tu_dicts1=[('nav', {"class": ["nav-path"]}), ('div', {"class": [ "sportBreadcrumb"]}),
                   ('div', {"class": [ "blogger-info-detail"]}) ]
              
    set_tu_dicts2=[('div', {"id": ["DynamicContentContainer","DynamicContentContainer "]}),
                   ('div', { "class":["body-content","body-content clearfix " ]})]
    
    set_tu_dicts3=[('div', {"class": ["tags", "article-tags" ,"keyWord_Contaner"]})]
    selenium1=False
    encod=0
    hd='h'
    
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd,show=show)
    
    ln_total=ln_total+ln
    dp_total=dp_total+dp    
###############################################################################################


if flag:
    url="https://www.alalamtv.net/"
    url2="https://www.alalamtv.net"
    p="alalamtv"
    
    
    
    set_tu_dicts1=[('div', {"class": [ "row news-detail-tag lg-zerro-lr-margin"]})  ]
              
    set_tu_dicts2=[('div', {"id": ["DynamicContentContainer","DynamicContentContainer "]}),
                   ('div', { "class":["detail body"]})]
    
    set_tu_dicts3=[('div', {"class": [ "row news-detail-tag lg-zerro-lr-margin"]}) ]
    selenium1=False#True
    encod=1
    hd='h1'
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd, numb=1,show=show)
        
    ln_total=ln_total+ln
    dp_total=dp_total+dp
###############################################################################################

if flag:
    url="https://www.alarabiya.net/"
    url2="https://www.alarabiya.net"
    p="alarabiya"
    
    set_tu_dicts1=[('div', {"class": [ "breadcrumbs"]})  ]
              
    set_tu_dicts2=[('div', {"id": ["body-text"]}),
                   ('div', { "class":["detail body"]})]
    
    set_tu_dicts3=[('div', {"class": ["box tags" ]}) ]
    selenium1=True#False
    encod=1
    hd='h1'
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd,show=show)
        
    ln_total=ln_total+ln
    dp_total=dp_total+dp
###############################################################################################
if flag:
    url='https://arabic.euronews.com/'
    url2='https://arabic.euronews.com'
    p="euronews"
    set_tu_dicts1=[('div', {"class": [ "c-breadcrumbs--scroll row column hide-for-small-only"]})  ]
    set_tu_dicts2=[('div', {"class": ["column small-12 medium-10 xlarge-11 js-responsive-iframes-container", "c-article-content js-article-content article__content selectionShareable"]})  ]
    set_tu_dicts3=[('div', {"class": ["row column" ]}) ]
    selenium1=False
    encod=0
    hd='h1'
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd,show=show)
        
    ln_total=ln_total+ln
    dp_total=dp_total+dp
###############################################################################################
if flag:
    url='https://www.cnbcarabia.com/'
    url2='https://www.cnbcarabia.com'
    p="cnbcarabia"
    set_tu_dicts1=[('div', {"class": [ "box-title"]})  ]  
    set_tu_dicts2=[('div', {"class": ["article-content margin-fix"]})  ]
    set_tu_dicts3=[('div', {"class": ["blog-box-tags","btn btn-primary btn-xs tags" ]}) ]
    selenium1=False
    encod=1
    hd='h1'
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd,show=show)
        
    ln_total=ln_total+ln
    dp_total=dp_total+dp
###############################################################################################
if flag:
    url='https://www.bbc.com/arabic/'
    url2='https://www.bbc.com'
    p="bbc"
    set_tu_dicts1=[('div', {"class": [ "box-title"]})  ]  
    set_tu_dicts2=[('div', {"class": ["story-body__inner"]})  ]#"story-body",
    set_tu_dicts3=[('div', {"class": [ "tags-container"]}) ] #,('u1', {"class": ["tags-list" ]})
    selenium1=False
    encod=0
    hd='h1'
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd,show=show)
        
    ln_total=ln_total+ln
    dp_total=dp_total+dp
###############################################################################################
if flag:

    url="https://arabic.rt.com/"
    url2="https://arabic.rt.com"
    p="rt"
    set_tu_dicts1=[('div', {"class": ["time-public"]})  ]  
    set_tu_dicts2=[('div', {"class": ["text js-text js-mediator-article"]}) ,('div', { "class":["detail body"]}) ]
    set_tu_dicts3=[('div', {"class": ["news-tags news-tags_article" ]}) ] #,('u1', {"class": ["tags-list" ]})
    selenium1=False
    encod=0
    hd='h1'
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd,show=show)    
        
    ln_total=ln_total+ln
    dp_total=dp_total+dp
###############################################################################################
if flag:

    url="https://www.skynewsarabia.com/"
    url2="https://www.skynewsarabia.com"
    p="skynewsarabia"
    set_tu_dicts1=[('div', {"class": ["time-public"]})  ]  
    set_tu_dicts2=[('div', {"class": ["row article article-content"]})]# ,('div', { "class":["detail body"]}) ]
    set_tu_dicts3=[('div', {"class": ["article-tags noprint" ]}) ] #,('u1', {"class": ["tags-list" ]})
    selenium1=False  #True
    encod=1
    hd='h1'
    ln, dp = scrape_site(url,url2, p, set_tu_dicts1,set_tu_dicts2, set_tu_dicts3, 
            clean=clean, selenium1=selenium1, it_num=0,encod=encod, hd=hd,show=show)     
        
    ln_total=ln_total+ln
    dp_total=dp_total+dp
###############################################################################################
end=time.time()
   
print()
print("The Number of the new records at all sites: ",ln_total-dp_total) 
print("The total Number of the records at all sites: ",ln_total) 
print("the total time  :", (end-start)/60)

## search for the lastest version of chromedriver and paste it in the place of the old one or go to https://chromedriver.chromium.org/downloads
## in the folder C:\Users\DELL\Anaconda3
## to see the required version go to chrome://settings/help