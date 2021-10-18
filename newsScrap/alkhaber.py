import requests as req 
from bs4 import BeautifulSoup as bsoup
import time
import json
import sys
sys.path.append('../')
import csvFilter as csvF
import databaseConect as db

def getArticlesUrls(urll,nPage):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win32; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    linksList=[]
    for p in range(1,nPage+1):
        response= req.get(urll+'?page='+str(p) ,headers=headers)
        parsedRes=bsoup(response.content,'html.parser')
        links=parsedRes.findAll('h3',attrs={'class':'panel-title'})
        print(urll)
        for link in links:
            if link.find('i') is None :
                url='https://www.elkhabar.com'+link.find('a')['href']
                if db.isExistArticle(url):
                    print('page'+str(p)+' '+str(len(linksList)))
                    return linksList
                linksList.append(url)
        print('page'+str(p)+" "+str(len(linksList)))
        time.sleep(3)   
    return linksList   
     
      

def getArticleContent(articleUrl):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win32; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    response= req.get(articleUrl ,headers=headers)
    parsedRes=bsoup(response.content,'html.parser')
    content=parsedRes.find('div',attrs={'id':'article_body_content'})
    title=parsedRes.find('div',attrs={'class':'panel-blog'}).find('h2',attrs={'class':'title'}).contents[0]
    image=parsedRes.find('div',attrs={'id':'article_img'}).find('img') 
    if image != None :
        image='https://www.elkhabar.com'+image['src']
    else :
        image='https://leverageedu.com/blog/wp-content/uploads/2020/01/article-writing-800x500.jpg'
    
    row=[]
    row.append(image)
    row.append(title)
    body=''
    for p in content.findAll('p'):
       body=body+'\n'+p.get_text()
    row.append(body)
    row.append('\nالمصدر : الخبر ')
    return row
def publishContent(pageid,accessToken):
    print('\n****** alkhaber ******\n')
    gurls=[
        'https://www.elkhabar.com/press/category/28/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D9%84%D9%88%D8%B7%D9%86/',
        'https://www.elkhabar.com/press/category/36/%D8%A7%D9%84%D8%B9%D8%A7%D9%84%D9%85/',
        'https://www.elkhabar.com/press/category/38/%D8%B1%D9%8A%D8%A7%D8%B6%D8%A9/',
        'https://www.elkhabar.com/press/category/27/%D9%85%D8%AC%D8%AA%D9%85%D8%B9/',
    ]
    for gurl in gurls:
        urls=getArticlesUrls(gurl,5)
        urls.reverse()
        for url in urls:
            try:
               
                row=getArticleContent(url)
                message=row[1]+row[2]+row[3]
                image=row[0]
                urll='https://graph.facebook.com/'+pageid+'/photos?url='+image+'&access_token='+accessToken+'&message='+message
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win32; x32; rv:88.0) Gecko/20100100 Firefox/88.0"}
                response= req.post(urll ,headers=headers)
                parsedRes=bsoup(response.content,'html.parser')
                if db.isExistArticle(url) or len(message)> 14700:
                    continue 
                parsedRes=json.loads(parsedRes.string)
                db.insertArticle(url,parsedRes['id'],parsedRes['post_id'])
                print(parsedRes)
            except:
                continue

