# class code is the 4 char string class code, and professorList is a list of all
# Professors as well as their Department"
import requests
from bs4 import BeautifulSoup

class RMPLookup:

    def lookupprofessor(self, classcode, professorlist):
        departmentlist = self.getdepartmentlist(classcode,professorlist)
        for professor_name in departmentlist:
            professor_name.replace(" ", "+")
            baseurl = "http://www.ratemyprofessors.com"
            requestsurl ="http://www.ratemyprofessors.com/search.jsp?query=Case+Western+"+professor_name
            page = requests.get(requestsurl)
            soup = BeautifulSoup(page.content, 'html.parser')
            #soup = soup.encode("utf-8")
            new_soup = soup.find("li",{"class": "listing PROFESSOR"})
            a_ref = new_soup.find("a")
            print(professor_name)
            for char in a_ref['href']:
                baseurl+=str(char)
            print(baseurl)

    def getdepartmentlist(self,classcode, professorlist):
        departmentname = self.classcodetodepartment(classcode)
        departmentlist = filter(lambda department: department['Department'] == departmentname, professorlist)
        returnlist =[]
        for x in departmentlist:
            returnlist.append(x['Name'])
        return returnlist

    def classcodetodepartment(self,classCode):
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

def main():
    lookup = RMPLookup()
    genericlist = [{"Department": "Mathematics, Applied Mathematics and Statistics", "Name": "Christopher Butler"},
                   {"Department": "Chemistry", "Name": "Drew Myers"},
                   {"Department": "Mathematics, Applied Mathematics and Statistics", "Name": "Steven Izen"},
                   {"Department": "Physics", "Name": "Harsh Mathur"},
                   {"Department": "Dance", "Name": "Random Dude"},
                   {"Department": "Physics", "Name": "Some Covault dude"}
                   ]

    lookup.lookupprofessor("MATH", genericlist)
    #print(lookup.getdepartmentlist("CHEM", genericlist));
    #print(lookup.getdepartmentlist("DANC", genericlist));
if __name__ == '__main__':
    main()
