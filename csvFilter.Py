import csv  

 
 
def writeArticle(fileName,row):
    with open(fileName, 'a', encoding="utf-8",newline='') as f:
        writer = csv.writer(f,delimiter = '~')
        writer.writerow(row)
  