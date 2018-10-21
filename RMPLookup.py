# class code is the 4 char string class code, and professorList is a list of all
# Professors as well as their Department"
import requests
from bs4 import BeautifulSoup
from ProfessorInfo import ProfessorInfo
import json
from multiprocessing import Pool
from functools import partial
import sys
from operator import itemgetter

class RMPLookup:

    def look_up_professor(self, classcode, professorlist):
        departmentlist = self.getdepartmentlist(classcode, professorlist)
        url_list = []
        p = Pool(4)
        url_list = list(p.map(self.name_to_url, departmentlist))
        url_list = list(filter(None, url_list))
        #for professor_name in departmentlist:
         #   self.loop_invariant(professor_name,url_list)
        return url_list

    def name_to_url(self, professor_name):
        headers = {'User-Agent': 'Mozilla/5.0'}
        split_name = professor_name.split(" ")
        while (len(split_name) > 2):
            del split_name[1]
        professor_name = " ".join(split_name)
        professor_name.replace(" ", "+")
        baseurl = "http://www.ratemyprofessors.com"
        requestsurl = "http://www.ratemyprofessors.com/search.jsp?query=Case+Western+" + professor_name
        page = requests.get(requestsurl,headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        # soup = soup.encode("utf-8")
        find_professor = soup.find("li", {"class": "listing PROFESSOR"})
        if (find_professor != None):
            a_ref = find_professor.find("a")
            for char in a_ref['href']:
                baseurl += str(char)
            return baseurl


    def loop_invariant(self, professor_name, url_list):
        split_name = professor_name.split(" ")
        while(len(split_name) > 2):
            del split_name[1]
        professor_name = " ".join(split_name)
        professor_name.replace(" ", "+")
        baseurl = "http://www.ratemyprofessors.com"
        requestsurl = "http://www.ratemyprofessors.com/search.jsp?query=Case+Western+" + professor_name
        page = requests.get(requestsurl)
        soup = BeautifulSoup(page.content, 'html.parser')
        # soup = soup.encode("utf-8")
        find_professor = soup.find("li", {"class": "listing PROFESSOR"})
        if (find_professor != None):
            a_ref = find_professor.find("a")
            for char in a_ref['href']:
                baseurl += str(char)
            url_list.append(baseurl)
        return url_list


    def class_teaching_professor_list(self, class_code, url_list):
        p = Pool(4)
        func = partial(self.url_to_prof_info, class_code)

        list_of_dict = list(p.map(func, url_list))
        list_of_dict = list(filter(None,list_of_dict))
        list_of_dict.sort(key=itemgetter('rating'),reverse=True)
        json_output = json.dumps(list_of_dict)
        return json_output

    def url_to_prof_info(self, class_code, professor_url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(professor_url,headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        find_class = soup.find_all("span", {"class": "name"})
        is_teaching_class = False
        for span in find_class:
            class_name = span.find("span", {"class": "response"}).text
            if class_name == class_code:
                is_teaching_class = True
                break
        if is_teaching_class:
            prof_dict = self.scrap_difficulty_rating(soup)
            return prof_dict

    def scrap_difficulty_rating(self,soup):
        professor_name_span = soup.find("span", {"class": "pfname"}).text
        professor_name_span = professor_name_span.strip(' \t\n\r')
        professor_last_name_span = soup.find("span", {"class": "plname"}).text
        professor_last_name_span = professor_last_name_span.strip(' \t\n\r')
        prof_name = professor_name_span + " " + professor_last_name_span
        prof_scrap = soup.find_all("div", {"class": "grade"})
        prof_rating = prof_scrap[0].text.strip(' \t\n\r')
        prof_difficulty = prof_scrap[2].text.strip(' \t\n\r')
        prof_dict = { "name": prof_name, "rating": prof_rating, "difficulty": prof_difficulty}
        return prof_dict

    def getdepartmentlist(self, classcode, professorlist):
        if "EECS" in classcode:
            return professorlist
        departmentname = self.classcodetodepartment(classcode)
        departmentlist = filter(lambda department: department['Department'] == departmentname, professorlist)
        returnlist = []
        for x in departmentlist:
            returnlist.append(x['Name'])
        return returnlist

    def classcodetodepartment(self, classCode):
        classCode = classCode.lower();
        classdict = {
            "anth": "Anthropology",
            "arth": "Art History and Art",
            "astr": "Astrology",
            "biol": "Biology",
            "chem": "Chemistry",
            "clsc": "Classics",
            "cogs": "Cognitive Science",
            "danc": "Dance",
            "dmll": "Modern Languages and Literatures",
            "eeps": "Earth, Environmental and Planetary Sciences",
            "engl": "English",
            "hsty": "History",
            "math": "Mathematics, Applied Mathematics and Statistics",
            "musc": "Music",
            "phil": "Philosophy",
            "phys": "Physics",
            "posc": "Political Science",
            "pscl": "Psychological Sciences",
            "rlgn": "Religious Studies",
            "soci": "Sociology",
            "thtr": "Theater"
        }
        return classdict.get(classCode)

    def build_function(self, class_code):
        class_department = class_code[:4]
        prompt = ProfessorInfo()
        if class_department == "EECS":
            professor_list = prompt.make_cs_prof_list()
        else:
            professor_list = prompt.make_artsci_prof_dept_list()
        url_list = self.look_up_professor(class_department, professor_list)
        json_look_up = self.class_teaching_professor_list(class_code, url_list)
        return json_look_up


def main():
   # class_code = sys.argv[1]
    lookup = RMPLookup()
    json = lookup.build_function("EECS233")
    print(json)



if __name__ == '__main__':
    main()
