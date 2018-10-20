from bs4 import BeautifulSoup
import requests


class ProfessorInfo:
    def make_prof_dept_list(self):

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

def main():
    prompt = ProfessorInfo()
    prompt.make_prof_dept_list()

if __name__ == '__main__':
    main()
