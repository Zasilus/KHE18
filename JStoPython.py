import cgi
import RMPLookup

form = cgi.FieldStorage()
search_term = form.getvalue('searchbox')
lookup = RMPLookup()
json = lookup.build_function(class_code=search_term)

print(json)