import urllib.request, urllib.error, urllib.parse
from re import findall
import re


f= open("rotten tomatoes movie genre link.txt","r")
cat=[1000]
link=[1000]
for i in range(1,10):
	temp=f.readline()
	cat.append(temp)
	temp1=f.readline()
	link.append(temp1)
	print(cat)
print("Enter Genre: ")
input_cat = input()
flag = 0
for i in range(1,10):
	pattern = r'.*?'+input_cat+r'.*?'
	if re.match(pattern,cat[i]):
		flag =1
		break
if flag == 0:
	print("Input error")
	exit()
print(link[i])
url = link[i]
response = urllib.request.urlopen(url)
webContent = response.read()
html = webContent.decode()
ndata= findall("<a href=\"(.*)?\"\sclass=\"unstyled articleLink\">\s(.*)?</a>",html)
rdata = ndata
count = 0
for item in ndata:
    count +=1
    print(item[0],item[1])
# print(count)
print("Enter Movie Name:")
input_cat1=input()
flag = 0
for item in rdata:
    # count +=1
    if item[1].strip() == input_cat1.strip():
    	url= item[0]
    	flag =1
    	break

if flag == 0:
	print("Input error")
	exit()
# print("link", url)
url = "https://www.rottentomatoes.com"+url 
print("link", url)  
# url = 'https://www.rottentomatoes.com/m/black_panther_2018'

response = urllib.request.urlopen(url)
webContent = response.read()
html = webContent.decode()
f = open('samplehtml.txt', 'wb')
f.write(webContent)
f.close()
# ndata= findall("<span\sclass=\"characters\ssubtle\ssmaller\"\stitle=\"(.*?)\">\s*<br/>\s*(.*?)\s*<br/>",html)
# for item in ndata:
# 	print(item[0].strip())
# 	print(item[1].strip())
# # print(ndata[0].strip())
# # print(ndata)

# # rdata= findall("<a href=\"(?:.*?)\">(.*?)</a>",ndata[0])
# # print(','.join(rdata))
# # for item in rdata:
# # 	print(item.strip())
