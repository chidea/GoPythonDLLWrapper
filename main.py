# coding=utf-8
#from urllib.request import urlopen
from lxml import html
import requests

import re
from time import sleep

from urllib.request import urlopen
from urllib.parse import urlencode

from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By

chrome = webdriver.Chrome()
chrome.implicitly_wait(10)

def link(fname, url):
  fname += '.url'
  with open(fname, 'w') as f:
    f.write('[{000214A0-0000-0000-C000-000000000046}]\n\
Prop3=19,2\n\
[InternetShortcut]\n\
IDList=\n\
URL=' + url + '\n\
IconIndex=13\n\
HotKey=0\n\
IconFile=%WINDIR%\system32\SHELL32.dll')
  print('saved to', fname)

def source(fname, frame=''):
  global chrome
  if frame:
    chrome.switch_to.frame(frame)
  with open(fname, 'w', encoding='utf-8') as f:
    f.write(chrome.page_source)
  if frame:
    chrome.switch_to.default_content()
  print('saved to', fname)

def screenshot(fname, frame=''):
  from PIL import Image, ImageFile
  global chrome
  wh=chrome.execute_script('return window.innerHeight')
  ww=chrome.execute_script('return window.innerWidth')
  th=chrome.execute_script('return %s.body.parentNode.scrollHeight'%(frame if frame else 'document',))
  #tw=chrome.execute_script('return %s.body.parentNode.scrollWidth'%frame)
  img=Image.new('RGB', (ww, th))
  for sh in range(0, th, wh):
    chrome.execute_script('%s.scroll(0,%d)'%(frame if frame else 'window', sh))
    sleep(.1)
    p=ImageFile.Parser()
    p.feed(chrome.get_screenshot_as_png())
    t=p.close()
    if th-sh<wh: # end of screenshot is smaller than screen
      t=t.crop((0,wh-(th-sh),ww,wh))
      img.paste(t, (0,sh,ww,th))
    else:
      img.paste(t, (0,sh,ww,sh+wh))
    t.close()
  img.save(fname)
  print('saved to', fname)

pat1 = re.compile(r'http://cafe.naver.com/(.+)/(.+)')
def parse_naver_cafe(r):
  global chrome
  l = r.xpath('//*[@id="ArticleSearchResultArea"]/li/dl')
  l.reverse()
  for dl in l:
    link = dl.xpath('dt/a')[0]
    title = link.text_content()
    link = link.attrib['href']
    content_sum = dl.xpath('dd[1]')[0]
    date = content_sum.text.strip()
    content_sum = content_sum.xpath('dd')[0].text_content()
    fname = date[:-1] + '-' + '-'.join(pat1.match(link).groups())
    try:
      print(date, link, title, content_sum)
    except UnicodeEncodeError:
      pass
    chrome.get(link)
    chrome.find_element_by_id('denyNamelessLayer')
    #chrome.switch_to.frame(chrome.find_element_by_id('cafe_main'))
    #try:
    #  chrome.implicitly_wait(1)
    #  chrome.find_element_by_id('basisElement')
    #  chrome.switch_to.default_content()
    if len(chrome.window_handles) > 1 :
      chrome.switch_to.window(chrome.window_handles[-1])
      chrome.close()
      chrome.switch_to.window(chrome.window_handles[0])
    else:
      screenshot(fname + '.png')
      source(fname + '.htm', 'cafe_main')
    #except selenium.common.exceptions.NoSuchElementException:
    #  pass

  #'//*[@id="ArticleSearchResultArea"]/li[1]/dl/dd[2]'
  #for l in links:
  #  print(l)

pat2=re.compile(r'http://blog.naver.com/([^?]+)\?Redirect=Log&logNo=([^&]+)&from=section')
def parse_naver_blog(r):
  global chrome
  l = r.xpath('//*[@id="blogSearchForm"]/div[2]/ul[3]/li')
  l.reverse()
  for dl in l:
    link = dl.xpath('h5/a')[0]
    title = link.text_content()
    link = link.attrib['href']
    content_sum = dl.xpath('div[2]/div/a')[0].text_content()
    date = dl.xpath('div[1]/span[2]')[0].text[:10]
    fname = date + '-'
    try:
      fname += '-'.join(pat2.match(link).groups())
    except:
      fname += link[7:].replace('/','-').replace('?', '-')
    try:
      print(date, link, title, content_sum)
    except UnicodeEncodeError:
      pass
    chrome.get(link)
    mainframe='mainFrame'
    try:
      chrome.find_element_by_id('hiddenFrame')
    except:pass
    try:
      chrome.switch_to.frame('mainFrame')
    except:
      mainframe='screenFrame'
      chrome.switch_to.frame(mainframe)
      chrome.switch_to.frame('mainFrame')
    try:
      # open reply box
      chrome.find_element(By.XPATH, '//*[@id="printPost1"]/tbody/tr/td[2]/div[contains(@class, "post-btn")]/div[3]/strong[1]/a').click()
    except: pass
    chrome.switch_to.default_content()
    if mainframe != 'mainFrame':
      chrome.switch_to.frame(mainframe)
    screenshot(fname + '.png', 'mainFrame')
    source(fname + '.htm', 'mainFrame')

sites = {
    'http://section.cafe.naver.com/ArticleSearch.nhn':{
        'parse':parse_naver_cafe,
        'data':{
            'sortBy':1,
            'searchBy':0,
            'duplicate':'false',
          },
        'q':'query',
        'page':'page',
        'lastpage':100
      },
    'http://section.blog.naver.com/sub/SearchBlog.nhn':{
        'parse':parse_naver_blog,
        'data':{
            'type':'post',
            'option.orderBy':'date',
            #'term':'',
            #'option.startDate':'',
            #'option.endDate':''
          },
        'q':'option.keyword',
        'page':'option.page.currentPage',
        'lastpage':100
      }
  }
if __name__ == '__main__':
  from sys import argv
  if not argv[1].startswith('http://') or not argv[1].startswith('https://'):
    argv[1] = 'http://' + argv[1]
  chrome.get(argv[1]) # target page
  sleep(1) # or implicit/explicit wait for AJAX be done
  fname = argv[1][7:].replace('/','-').replace('?', '-')
  screenshot(fname + '.png')
  source(fname + '.htm')
  link(fname, argv[1])
  chrome.close()
  exit()
  from os import listdir
  from os.path import join
  from os.path import isfile
  from PIL import Image
  #for f in listdir('blog.naver.com/done'):
  #  if not f.endswith('.png'): continue
  #  if Image.open(join('blog.naver.com/done',f)).size[1] <= 2000:
  #    print(f)
  #exit()
  while True:
    for s in sites:
      fname = input()
      url = fname[11:].split('-')
      if len(url) > 2 :
          url = ['-'.join(url[:-1]), url[-1]]
      if url[0].find('.') == -1:
        url ='http://blog.naver.com/' + url[0] + '\?Redirect=Log&logNo=' + url[1] + '&from=section'
      else:
        url = 'http://' + url[0] + '/' + url[1]
      print(fname, url)
      chrome.get(url)
      sleep(1)
      mainframe='mainFrame'
      try:
        chrome.switch_to.frame('mainFrame')
      except:
        mainframe='screenFrame'
        chrome.switch_to.frame(mainframe)
        chrome.switch_to.frame('mainFrame')
      try:
        # open reply box
        chrome.find_element(By.XPATH, '//*[@id="printPost1"]/tbody/tr/td[2]/div[contains(@class, "post-btn")]/div[3]/strong[1]/a').click()
      except: pass
      sleep(.2)
      chrome.switch_to.default_content()
      if mainframe != 'mainFrame':
        chrome.switch_to.frame(mainframe)
      screenshot(fname + '.png', 'mainFrame')
      #source(fname + '.htm', 'cafe_main')
  exit() 
  for f in listdir('blog.naver.com'):
    if not f.endswith('.png'): continue
    #if f.find('-blog.me-') == 10:
    #  nf = f[:-4].split('-')
    #  nf = '-'.join([nf[0], nf[2] + '.' + nf[1], nf[3]]) + f[-4:]
    #  rename(join('blog.naver.com', f), join('blog.naver.com', nf))
    if Image.open(join('blog.naver.com',f)).size[1] > 1000:
      url = f[11:-4].split('-')
      if len(url) > 2 :
          url = ['-'.join(url[:-1]), url[-1]]
      if url[0].find('.') == -1:
        url ='http://blog.naver.com/' + url[0] + '\?Redirect=Log&logNo=' + url[1] + '&from=section'
      else:
        url = 'http://' + url[0] + '/' + url[1]
      print(f, url)
      chrome.get(url)
      sleep(1)
      mainframe='mainFrame'
      try:
        chrome.switch_to.frame('mainFrame')
      except:
        mainframe='screenFrame'
        chrome.switch_to.frame(mainframe)
        chrome.switch_to.frame('mainFrame')
      try:
        # open reply box
        chrome.find_element(By.XPATH, '//*[@id="printPost1"]/tbody/tr/td[2]/div[contains(@class, "post-btn")]/div[3]/strong[1]/a').click()
      except: pass
      chrome.switch_to.default_content()
      if mainframe != 'mainFrame':
        chrome.switch_to.frame(mainframe)
      screenshot(f, 'mainFrame')
  exit()
  for f in listdir('cafe.naver.com'):
    if not f.endswith('.png'): continue
    if Image.open(join('cafe.naver.com',f)).size[1] > 2000:
      url = f[11:-4].split('-')
      url = 'http://cafe.naver.com/' + url[0] + '/' + url[1]
      chrome.get(url)
      screenshot(f)
  exit()
  while True:
    for s in sites:
      fname = input()
      url = fname[11:].split('-')
      url = 'http://cafe.naver.com/' + url[0] + '/' + url[1]
      chrome.get(url)
      chrome.find_element_by_id('denyNamelessLayer')
      screenshot(fname + '.png')
      #source(fname + '.htm', 'cafe_main')
  exit() 
  kwd = input('Keyword>')
  for s in sites:
    d=sites[s]['data']
    d[sites[s]['q']] = kwd
    for i in range(sites[s]['lastpage'], 0, -1):
      d[sites[s]['page']] = i
      sites[s]['parse'](html.fromstring(urlopen(s +'?'+ urlencode(d)).read().decode()))
      #chrome.get(s.format(i))
      #chrome.find_element_by_id('ArticleSearchResultArea')
      #sites[s](html.fromstring(chrome.page_source.encode('utf-8')))
      #sites[s](html.fromstring(requests.get(s.format(i)).content))
