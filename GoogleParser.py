import requests
import os
from bs4 import BeautifulSoup
import threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

hashes = {'й': '%D0%B9', 'ц': '%D1%86', 'у': '%D1%83', 'к': '%D0%BA', 'е': '%D0%B5', 
          'н': '%D0%BD', 'г': '%D0%B3', 'ш': '%D1%88', 'щ': '%D1%89', 'з': '%D0%B7', 
          'х': '%D1%85', 'ъ': '%D1%8A', 'ф': '%D1%84', 'ы': '%D1%8B', 'в': '%D0%B2', 
          'а': '%D0%B0', 'п': '%D0%BF', 'р': '%D1%80', 'о': '%D0%BE', 'л': '%D0%BB', 
          'д': '%D0%B4', 'ж': '%D0%B6', 'э': '%D1%8D', 'я': '%D1%8F', 'ч': '%D1%87', 
          'с': '%D1%81', 'м': '%D0%BC', 'и': '%D0%B8', 'т': '%D1%82', 'ь': '%D1%8C', 
          'б': '%D0%B1', 'ю': '%D1%8E', 'Й': '%D0%99', 'Ц': '%D0%A6', 'У': '%D0%A3', 
          'К': '%D0%9A', 'Е': '%D0%95', 'Н': '%D0%9D', 'Г': '%D0%93', 'Ш': '%D0%A8', 
          'Щ': '%D0%A9', 'З': '%D0%97', 'Х': '%D0%A5', 'Ъ': '%D0%AA', 'Ф': '%D0%A4', 
          'Ы': '%D0%AB', 'В': '%D0%92', 'А': '%D0%90', 'П': '%D0%9F', 'Р': '%D0%A0', 
          'О': '%D0%9E', 'Л': '%D0%9B', 'Д': '%D0%94', 'Ж': '%D0%96', 'Э': '%D0%AD', 
          'Я': '%D0%AF', 'Ч': '%D0%A7', 'С': '%D0%A1', 'М': '%D0%9C', 'И': '%D0%98', 
          'Т': '%D0%A2', 'Ь': '%D0%AC', 'Б': '%D0%91', 'Ю': '%D0%AE', ' ': '%20',
          'І': '%D0%86', ',': '%2C'}

def calc_hash(orig_string,hash_string):
    hashes = {}
    for i in range(len(orig_string)):
         hashes[orig_string[i]] = hash_string[i*6:(i*6)+6]
    return hashes

def write_files(urls,dir,verify_certificates = True):#gets and writes files   
    global hashes
    for url in urls:
        try:            
            file_bytes = requests.get(url,verify = verify_certificates).content
            file_name = os.path.basename(url)
            
            for letter,hash in hashes.items():
                while hash in file_name:
                    file_name = file_name.replace(hash,letter)

            file = open(dir+file_name,'wb')
            file.write(file_bytes)
            file.close()
        except:
            pass

class GoogleParser():
    #Parser for google
    def __init__(self,verify_certificates = True):
        self.verify = verify_certificates
        self.session = requests.Session()
        
        self.session.get('https://www.google.com/')

    def prepare_request(self,name):
        '''
        just prepares request for other functions
        '''
        parsed_name = name.replace(' ','+')
        while parsed_name.find(' ') != -1:
            parsed_name = parsed_name.replace(' ','+')
        return parsed_name

    def get_page(self,request,offset=0):
        '''
        Gets page with searching results
        request - search request for google
        '''
        offset_str = str(offset)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0','Referer':'https://www.google.com/'}
        page = self.session.get(f'https://www.google.com/search?q={request}&start={offset_str}',headers = headers)
        return page.text

    def parse_urls(self,page):
        '''
        Parses urls in page
        '''
        to_return = []
        soup = BeautifulSoup(page,'html.parser')
        try:
            response_block = soup.find('div',{'class':'srg'})
            for div in response_block.find_all('div',{'class':'r'}):
                try:
                    to_return.append(div.a.get('href'))
                except:
                    continue
        except:
            pass
        return to_return
    
    def get_urls(self,request,pages = 0):
        '''
        That function allows you get all urls from google
        request - search request to google
        pages - how many pages do we parse, if 0 will be parse all pages
        '''

        prepared_request = self.prepare_request(request)

        urls = []

        counter = 0
        while True:
            page = self.get_page(prepared_request,counter*10)#Google returns 10 sites per request
            purls = self.parse_urls(page)

            if purls == []:
                break

            for url in purls:
                urls.append(url)
                          
            counter += 1
            if counter == pages:
                break

        return urls
    
    def download_files(self, request, dir = '.\\', pages = 0):
        '''
        That function allows you download all files google find
        request - search request to google
        dir - directory where files will be saved
        pages - how many pages do we parse, if 0 will be parse all pages
        '''
     
        try:
            os.mkdir(dir)
        except:
            pass

        prepared_request = self.prepare_request(request)
        
        threads = []
        counter = 0
        while True:
            page = self.get_page(prepared_request,counter*10)#Google returns 10 sites per request
            urls = self.parse_urls(page)

            if urls == []:
                break
            else:
                threads.append(threading.Thread(target = write_files, args = (urls,dir,self.verify)))
                threads[len(threads)-1].start()
            counter += 1
            if counter == pages:
                break

        for thread in threads:#checking threads
            if thread.is_alive():
                thread.join()
        return True


#hashes.update(hs)
#print(hashes)
#input()

if __name__ == '__main__':
    print('Downloading started')
    parser = GoogleParser(False)
    request = input('Request for Google: ')
    print(parser.get_urls(request))
    #parser.download_files(request,dir = '.\\txts\\')
    print('Downloading done')

