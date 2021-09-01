import ply.lex as lex
import urllib.request
import urllib.error
import urllib.parse
from re import findall
import ply.yacc as yacc
import re

resultDict = {}         #to store the result of the parser
CastDict = {}           #to store the cast and role details
# List of token names.   This is always required
tokens = (
    'MOVIETITLE',
    'DIRECTORS',
    'RUNTIME',
    'BOXOFFICE',
    'WRITERS',
    'PRODUCERS',
    'LANGUAGE',
    'STORY',
    'CAST',
    'ROLE',
    'CASTEND',
    'ANCHORSTART',
    'COMMA',
    'ANCHOREND',
    'DIVEND',
    'CONTENT',
)

#functions to extract information

def t_MOVIETITLE(t):
    r'\s*<h1\sslot=\"title\"\sclass=\"scoreboard__title\"\sdata-qa=\"score-panel-movie-title\">\s*'
    return t

def t_DIRECTORS(t):
    r'\s*<a\shref=\"(?:.*)?\"\sdata-qa=\"movie-info-director\">\s*'
    return t


def t_RUNTIME(t):
    r'\s*<div\sclass=\"meta-label\ssubtle\"\sdata-qa=\"movie-info-item-label\">Runtime:</div>\s*<div\sclass=\"meta-value\"\sdata-qa=\"movie-info-item-value\">\s*<time\sdatetime=\".*?\">\s*'
    return t


def t_BOXOFFICE(t):
    r'\s*<div\sclass=\"meta-label\ssubtle\"\sdata-qa=\"movie-info-item-label\">Box\sOffice(?:[\s\S]*?):</div>\s*<div\sclass=\"meta-value\"\sdata-qa=\"movie-info-item-value\">\s*'
    return t


def t_WRITERS(t):
    r'\s*<div\sclass=\"meta-label\ssubtle\"\sdata-qa=\"movie-info-item-label\">Writer:</div>\s*<div\sclass=\"meta-value\"\sdata-qa=\"movie-info-item-value\">\s*'
    return t




def t_PRODUCERS(t):
    r'\s*<div\sclass=\"meta-label\ssubtle\"\sdata-qa=\"movie-info-item-label\">Producer:</div>\s*<div\sclass=\"meta-value\"\sdata-qa=\"movie-info-item-value\">\s*'
    return t


def t_LANGUAGE(t):
    r'\s*<div\sclass=\"meta-label\ssubtle\"\sdata-qa=\"movie-info-item-label\">Original\sLanguage:</div>\s*<div\sclass=\"meta-value\"\sdata-qa=\"movie-info-item-value\">\s*'
    return t


def t_STORY(t):
    r'\s*<div\sid=\"movieSynopsis\"\sclass=\"movie_synopsis\sclamp\sclamp-6\sjs-clamp\"\sstyle=\"clear:both\"\sdata-qa=\"movie-info-synopsis\">\s*'
    return t


def t_CAST(t):
    r'\s*<span\sclass=\"characters\ssubtle\ssmaller\"\stitle=\"'
    return t


def t_ROLE(t):
    r'\">[\s]*<br/>[\s*]'
    return t

def t_CASTEND(t):
    r'[\s]*<br/>[\s*]'
    return t

def t_ANCHORSTART(t):
    r'\s*<a\shref=\".*?\">\s*'
    # print(t)
    return t


def t_COMMA(t):
    r'\s*,\s*'
    return t


def t_ANCHOREND(t):
    r'\s*</a>\s*'
    return t

def t_DIVEND(t):
    r'\s*</div>\s*'
    return t

def t_CONTENT(t):
    r'[a-zA-Z0-9\u00C0-\u017F\',\s$.(|)-:_`]+'
    t.value = (t.value).strip()
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# ----------------------Parser----------------------------------------------
def p_ss(p):
    '''
    ss : director
            | writer
            | producer
            | language
            | cast
            | story
            | boxoffice
            | runtime
            | movietitle
            | empty            
    '''
    # print(p[1])
    p[0] = p[1]


def p_movietitle(p):
    '''
    movietitle : MOVIETITLE CONTENT    
    '''
    p[0] = p[2]
    resultDict['Movie Name'] = p[2]


def p_director(p):
    '''
    director :  DIRECTORS CONTENT         
    '''
    p[0] = p[2]
    resultDict['Director'] = p[2]
    # print('Director: ', p[2])


def p_writer(p):
    '''
    writer : WRITERS f DIVEND
    '''
    p[0] = p[2]
    resultDict['Writer'] = p[2]
    # print('Writers: ', p[2])


def p_f_recurse(p):
    '''
    f : f COMMA ANCHORSTART CONTENT ANCHOREND
    '''
    p[0] = f'{p[1]}, {p[4]}'
    # print('1Writer: ', p[0])

# def p_f_recurse1(p):
#     '''
#     f : COMMA ANCHORSTART CONTENT ANCHOREND f
#     '''
#     p[0] = f'{p[3]}, {p[5]}'
#     print('Writer: ', p[0])

def p_f_term(p):
    '''
    f : ANCHORSTART CONTENT ANCHOREND
    '''
    p[0] = p[2]
    # print('2Writer: ', p[2])


# def p_f_prime_term(p):
#     '''
#     f_prime : ANCHORSTART CONTENT ANCHOREND
#     '''
#     p[0] = p[2]

def p_producer(p):
    '''
    producer : PRODUCERS g DIVEND
    '''
    p[0] = p[2]
    resultDict['Producer'] = p[2]
    print('Producers: ', p[2])


def p_g_recurse(p):
    '''
    g : g COMMA ANCHORSTART CONTENT ANCHOREND
    '''
    p[0] = f'{p[1]}, {p[4]}'
    print('1Producer: ', p[0])

# def p_f_recurse1(p):
#     '''
#     f : COMMA ANCHORSTART CONTENT ANCHOREND f
#     '''
#     p[0] = f'{p[3]}, {p[5]}'
#     print('Writer: ', p[0])

def p_g_term(p):
    '''
    g : ANCHORSTART CONTENT ANCHOREND
    '''
    p[0] = p[2]
    print('2Producer: ', p[2])
# def p_producer(p):
#     '''
#     producer : PRODUCERS CONTENT
#     '''
#     p[0] = p[2]
#     print('Producer: ', p[0])


def p_language(p):
    '''
    language : LANGUAGE CONTENT
    '''
    p[0] = p[2]
    resultDict['Language'] = p[0]
    # print('Language: ', p[0])


def p_cast(p):
    '''
    cast : CAST CONTENT ROLE CONTENT CASTEND
    '''
    p[0] = [2] 

    CastDict[p[2]]=p[4]
    resultDict['Cast'] = CastDict
    # print('Cast: ', p[2], ',', p[4])


def p_story(p):
    '''
    story : STORY CONTENT
    '''
    p[0] = p[2]
    resultDict['Story'] = p[2]
    # print('Story: ', p[2])


def p_boxoffice(p):
    '''
    boxoffice : BOXOFFICE CONTENT
    '''
    p[0] = p[2]
    resultDict['Boxoffice'] = p[2]
    # print('Boxoffice: ', p[2])


def p_runtime(p):
    '''
    runtime : RUNTIME CONTENT
    '''
    p[0] = p[2]
    resultDict['Runtime'] = p[2]
    # print('Runtime: ', p[2])


def p_empty(p):
    '''
    empty : 
    '''
    p[0] = None


def p_error(p):
    pass

#open the text file with the links
# f= open("rotten tomatoes movie genre link.txt","r")

# #store the links as (moviename, link) pairs
# linkDict = {}
# for i in range(1,11):
#     temp=f.readline()
#     temp1=f.readline()
#     linkDict[temp] = temp1
#     # print(cat)

# #Display the genre options
# for item in linkDict:
#     print(item)

# #take user input for genre
# print("Enter Genre: ")
# input_cat = input()
# flag = 0
# pattern = r'.*?'+input_cat+r'.*?'

# #check for the input genre in the dictionary
# for cat,lnk in linkDict.items():
#     if re.match(pattern,str(cat)):
#         flag = 1
#         url = str(linkDict[cat])
#         break
# if flag == 0:
#     print("Input error")
#     exit()
# # print(url)

# #load the html of the input genre top 100 movies page
# response = urllib.request.urlopen(url)
# webContent = response.read()
# html = webContent.decode()

# #get all the top 100 movie links and names
# ndata= findall("<a href=\"(.*)?\"\sclass=\"unstyled articleLink\">\s(.*)?</a>",html)
# rdata = ndata
# count = 0
# for item in ndata:
#     count +=1
#     print(str(item[1]).strip())
# # print(count)

# #take user input for movie name
# print("Enter Movie Name:")
# input_cat1=input()
# flag = 0
# for item in rdata:
#     # count +=1
#     if item[1].strip() == input_cat1.strip():
#         url= item[0]
#         flag =1
#         break

# if flag == 0:
#     print("Input error")
#     exit()
# # print("link", url)
# url = "https://www.rottentomatoes.com"+url 
# print("link", url)  
url = 'https://www.rottentomatoes.com/m/song_of_the_sea_2014'

response = urllib.request.urlopen(url)
webContent = response.read()
html = webContent.decode()
f = open('samplehtml.txt', 'wb')
f.write(webContent)
f.close()
# url = 'https://www.rottentomatoes.com/m/avengers_infinity_war'

# response = urllib.request.urlopen(url)
# webContent = response.read()
# html = webContent.decode()
f = open('samplehtml.txt', 'r')
html = ''.join(f.readlines())
# f.close()
logFile = open('logFile.txt', 'a')


def main():
    # f = open("samplehtml.txt", "r")
    
    lexer = lex.lex()
    parser = yacc.yacc()
    result = yacc.parse(input=html, lexer=lexer)
    # print('Result: ', result)
    # line = f.readline()
    # f.close()
    query = ['Movie Name','Director', 'Writer', 'Producer', 'Language', 'Cast', 'Story', 'Boxoffice', 'Runtime']
    print("Enter Query Field from the List:")

    for item in query:
        print(item)

    input_field = input()
    if input_field not in query:
        print("Input Error")
        exit()

    if input_field in resultDict:

        if input_field == 'Cast':
            for cast, role in CastDict.items():
                print(cast, ":", role)

        else:
            print(resultDict[input_field])
        outputLog = '\n' + input_cat + '\t' + str(resultDict['Movie Name']) + '\t' + input_field + '\t' + str(resultDict[input_field])
        logFile.write(outputLog)

    else:
        print("Query Field Unavailable")
        
if __name__ == "__main__":
    main()
