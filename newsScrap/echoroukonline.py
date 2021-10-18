import requests as req 
from bs4 import BeautifulSoup as bsoup
import time
import json
import sys
sys.path.append('../')
import csvFilter as csvF
import databaseConect as db
#max len 14740
def getArticlesUrls(urll,nPage):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win32; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    linksList=[]
    for p in range(1,nPage+1):
        
        response= req.get(urll+'/page/'+str(p) ,headers=headers)
        parsedRes=bsoup(response.content,'html.parser')
        section=parsedRes.find('section',attrs={'class':'ech-cgmn__main fx-1'})
        links=section.findAll('h3',attrs={'class':'ech-card__title'})
        print(urll)
        for link in links:
            url=link.find('a')['href']
            if db.isExistArticle(url):
                print('page'+str(p)+' '+str(len(linksList)))
                return linksList
            linksList.append(url)
         
        print('page'+str(p)+" "+str(len(linksList)))
        time.sleep(3) 
    return linksList   
     
      

def getArticleContent(articleUrl):
   
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
    response= req.get(articleUrl ,headers=headers)
    parsedRes=bsoup(response.content,'html.parser')
    content=parsedRes.find('div',attrs={'class':'ech-artx'})
    title=parsedRes.find('h1',attrs={'class':'ech-sgmn__title'}).contents[0]
    image=parsedRes.find('figure',attrs={'class':'ech-sgmn__figure'}).find('img') 
    if image != None :
        image=image['data-src']
    else :
        image='https://leverageedu.com/blog/wp-content/uploads/2020/01/article-writing-800x500.jpg'
    
    row=[]
    row.append(image)
    row.append(title)
    body=''
    for p in content.findAll('p'):
       body=body+'\n'+p.get_text()
    row.append(body)
    row.append('\nالمصدر : الشروق اونلاين ')
    return row

def publishContent(pageid,accessToken):
    print('\n****** echoroukonline ******\n')
    gurls=[
    'https://www.echoroukonline.com/algeria',
    'https://www.echoroukonline.com/world',
    'https://www.echoroukonline.com/economy',
    'https://www.echoroukonline.com/sport',
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
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win32; x64; rv:89.0) Gecko/20100101 Firefox/88.0"}
                response= req.post(urll ,headers=headers)
                parsedRes=bsoup(response.content,'html.parser')
                if db.isExistArticle(url) or len(message)> 14700:
                    continue 
                parsedRes=json.loads(parsedRes.string)
                db.insertArticle(url,parsedRes['id'],parsedRes['post_id'])
                print(parsedRes)
            except:
                continue

