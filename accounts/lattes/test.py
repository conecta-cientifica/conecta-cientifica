from lattesadapter import LattesAdapter
from lattes import Lattes

adapter = LattesAdapter(Lattes())
profile = adapter.get_lattes_profile('8606503911561836')

print("Researcher: ")
print(profile.researcher.name)

print("Titulations: ")
for titulation in profile.titulations:
    print(titulation.university)
    print(titulation.title)
    print(titulation.formation_degree)

print("Projects: ")
for project in profile.projects:
    print(project.project_name)
    print(project.project_description)

print("Research lines: ")
for line in profile.lines:
    print(line.line_description)