import urllib.request, urllib.error, urllib.parse
from re import findall

url = 'https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/'

response = urllib.request.urlopen(url)
webContent = response.read()
html = webContent.decode()
ndata= findall("<a href=\"(.*)?\"\sclass=\"unstyled articleLink\">\s(.*)?</a>",html)
count = 0
for item in ndata:
    count +=1
    print(item[1])

f = open('samplehtml.txt', 'wb')
f.write(webContent)
f.close

