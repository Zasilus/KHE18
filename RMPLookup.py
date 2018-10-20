# class code is the 4 char string class code, and professorList is a list of all
# Professors as well as their Departmet"


def getdepartmentlist(classcode, professorlist):
    departmentname = classcodetodepartment(classcode)
    departmentlist = filter(lambda department: department['Department'] == departmentname, professorlist)
    returnlist =[]
    for x in departmentlist:
        returnlist.append(x['Name'])
    return returnlist


def classcodetodepartment(classCode):
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


if __name__ == '__main__':
    genericlist = [{"Department": "Mathematics, Applied Mathematics and Statistics","Name": "Christopher Butler"},
            {"Department": "Chemistry","Name": "Drew Myers"},
            {"Department": "Mathematics, Applied Mathematics and Statistics","Name": "Steven Izen"},
            {"Department": "Physics", "Name": "Harsh Mathur"},
            {"Department": "Dance", "Name": "Random Dude"},
            {"Department": "Physics", "Name": "Some Covault dude"}
            ]
    print(getdepartmentlist("MATH",genericlist));
    print(getdepartmentlist("CHEM",genericlist));
    print(getdepartmentlist("DANC",genericlist));
