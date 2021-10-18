import csv  

def writeMovies(fileName,row):
    with open(fileName, 'a', encoding="utf-8",newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

 
def readMovies(fileName):
    with open(fileName, 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        return list(reader)

 
def writeArticle(fileName,row):
    with open(fileName, 'a', encoding="utf-8",newline='') as f:
        writer = csv.writer(f,delimiter = '~')
        writer.writerow(row)
  