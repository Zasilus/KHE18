from bs4 import BeautifulSoup
import requests
import re

class ProfessorInfo:
    def make_artsci_prof_dept_list(self):

        # Download html file of faculty and department info
        page = requests.get("http://artsci.case.edu/about-the-college/faculty-directory/")
        soup = BeautifulSoup(page.content, 'html.parser')

        # Scrape for faculty names and their department
        full_faculty_data = soup.findAll('div', {'class': 'col-md-3 directory-data'})
        dept_data = soup.findAll('div', {'class': 'col-md-2 directory-data'})

        faculty_info = []
        i = 0
        j = 0
        while (i < len(full_faculty_data)):
            name = full_faculty_data[i].find('a').text
            department = dept_data[j].text.strip()
            dict = {
                "Department": department,
                "Name": name
            }
            faculty_info.append(dict)
            i += 2
            j += 1
        return faculty_info
    def make_cs_prof_list(self):

        page = requests.get("http://engineering.case.edu/eecs/faculty-staff")
        soup = BeautifulSoup(page.content, 'html.parser')
        full_cs_data = soup.findAll('div', {'class':"content clear-block"})
        full_cs_data = full_cs_data[0].find_all('ul')
        list_of_professors = []
        list_of_professors.append('Erman Ayday')
        for ul_tag in full_cs_data:
            a_ref = ul_tag.find_all('a')
            for a_tags in a_ref:
                professor = a_tags.text
                professor = professor.replace("\xa0", " ")
                professor = professor.split(", ")[0]
                professor = professor.split(" - ")[0]

                professor = re.sub(r'".*"', " ", professor)
                professor = professor.split(" ")
                while len(professor) > 2:
                    del professor[1]
                professor = " ".join(professor)
                if (professor != "Assistant Professor") & (professor != " "):
                    list_of_professors.append(professor)
        #print(full_cs_data)
        return list_of_professors

    def make_eciv_prof_list(self):
        list_of_professors = []
        core_faculty = requests.get("http://engineering.case.edu/eciv/faculty")
        soup = BeautifulSoup(core_faculty.content, 'html.parser')
        core_faculty_data = soup.findAll('div', {'class':"content clear-block"})
        core_faculty_data = soup.findAll('p')
        trimmed_faculty_data = []
        #split_core_faculty_data = "".join(core_faculty_data)
        #split_core_faculty_data = split_core_faculty_data.split("<hr>")
        for para in core_faculty_data:

            if len(para.findAll('strong')) != 0:
                trimmed_faculty_data.append(para.findAll('strong'))
        print(core_faculty_data)

def main():
    professor_info = ProfessorInfo()
    professor_info.make_emae_prof_list()



if __name__ == '__main__':
    main()
