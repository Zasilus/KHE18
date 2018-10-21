# class code is the 4 char string class code, and professorList is a list of all
# Professors as well as their Department"
import requests
from bs4 import BeautifulSoup
from ProfessorInfo import ProfessorInfo
import json
import sys
import cgi

from flask import Flask
class RMPLookup:

    def look_up_professor(self, classcode, professorlist):
        departmentlist = self.getdepartmentlist(classcode, professorlist)
        url_list = []
        for professor_name in departmentlist:
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
            if (find_professor == None):
                continue
            else:
                a_ref = find_professor.find("a")
                for char in a_ref['href']:
                    baseurl += str(char)
                url_list.append(baseurl)
        return url_list

    def class_teaching_professor_list(self, class_code, url_list):
        list_of_dict = []
        for professor_url in url_list:
            page = requests.get(professor_url)
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
                list_of_dict.append(prof_dict)
        json_output = json.dumps(list_of_dict)
        return json_output


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
    form = cgi.FieldStorage()
    searchterm = form.getvalue("searchbox")
    lookup = RMPLookup()
    json = lookup.build_function(searchterm)
    return json

if __name__ == '__main__':
    main()
