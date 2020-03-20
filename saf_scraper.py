from bs4 import BeautifulSoup
import requests
import re
import click

class SAFire:
    def __init__(self, session_id_ing):
        self.cookie = session_id_ing
        self.saf_ing_url = "https://saf.uandes.cl/ing/default/index"
        self.saf_url = "https://saf.uandes.cl"
    
    def session(self):
        """
        Returns a new session with login cookie
        """
        s = requests.Session()
        j = requests.cookies.RequestsCookieJar()
        j.set('session_id_ing', self.cookie)
        s.cookies = j
        return s
    
    def get_bs_of_url(self, url):
        """
        Parses site returning a BeautifulSoup object
        """
        req = self.session().get(url)
        html = req.text
        return BeautifulSoup(html, 'lxml')

    def extract_past_courses(self):
        """ 
        Generator thet returns a dictionary with keys name: course's name, url: course's full url
        """
        main_bs = self.get_bs_of_url(self.saf_ing_url)
        courses =  main_bs.find('div', {'id': 'past_semester'})
        for link in courses.find_all('a', {'class': 'list-group-item'}):
            course_name = self.__valid_filename(link.find('div', {'class': 'col-lg-12'}).contents[0])
            yield {'name': course_name, 'link': self.saf_url + link.attrs['href']}
    
    def extract_files_of_types(self, bs, file_types):
        """
        Returns a list of dictionaries with keys 'section_name' and 'files'.
        TODO: Refractor, this is bulky and multiconcern. Knows and does too much.
        """
        product = []
        main = bs.find('div', {'id': 'main-content'})
        sections = main.find_all('div', {'class': 'accordion-group'})
        for section in sections:
            section_name = self.__valid_filename(section.find('a', {'class': 'accordion-toggle'}).contents[1])
            files = []
            for file_ in section.find_all('a', {'data-content-type': 'file'}):
                file_url = self.saf_url + file_['href']
                file_extention = re.compile(r"\.([a-z]+)$", re.I).search(file_url)
                if file_extention and file_extention.group() in file_types:
                    file_name = self.__valid_filename(file_['data-content-name'] + file_extention.group())
                    files.append({'file_name': file_name, 'file_url': file_url})
            if len(files) > 0:
                product.append({'section_name': section_name, 'files': files})
        return product

    def __valid_filename(self, filename):
        valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(c for c in filename if c in valid_chars).strip()


@click.command()
@click.option('--cookie', '-c', help='REQUIRED: session_id_ing cookie from saf', required=True)
def print_all_material(cookie):
    c= SAFire(cookie)

    for course in c.extract_past_courses():
        course_sections = c.get_bs_of_url(course['link'])
        for section in c.extract_files_of_types(course_sections, ['.pdf', '.rar', '.zip', '.ppt', '.pptx', '.xls', '.xlsx', '.doc', '.docx']):
            for file_ in section['files']:
                print(f"{file_['file_url']}\n\tdir=./{course['name']}/{section['section_name']}\n\tout={file_['file_name']}")

if __name__ == "__main__":
    print_all_material()
