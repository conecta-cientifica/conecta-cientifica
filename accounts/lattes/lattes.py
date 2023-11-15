from accounts.lattes.database_connection import DataBaseConn
from accounts.lattes.profile import Profile
from accounts.lattes.researcher import Researcher
from accounts.lattes.titulation import Titualation
from accounts.lattes.project import Project
from accounts.lattes.researchline import ResearchLine

class Lattes():
    def __init__(self):
        self.db = DataBaseConn()

    def __del__(self):
        del self.db

    def get_profile_by_lattes_id(self, lattesID):
        query = "Select lattesID, name from researcher where lattesID = " + lattesID
        query_result = self.db.execute_query(query)
        for reg in query_result:
            researcher = Researcher(reg[0], reg[1])
        query = "Select university, title, formation_degree, big_area, area, subarea, especialty from titulation where researcherID = " + lattesID
        query_result = self.db.execute_query(query)
        titulations = []
        for reg in query_result:
            titulation = Titualation(reg[0], reg[1], reg[2], reg[3], reg[4], reg[5], reg[6])
            titulations.append(titulation)
        query = "Select project_name, project_description from projects a join project_researchers b on a.projectID = b.projectID where b.researcherID = " + lattesID
        query_result = self.db.execute_query(query)
        projects = []
        for reg in query_result:
            project = Project(reg[0], reg[1])
            projects.append(project)
        query = "Select lineDescription from research_lines a join research_line_researcher b on a.lineID = b.lineID where b.researcherID = " + lattesID
        query_result = self.db.execute_query(query)
        lines = []
        for reg in query_result:
            line = ResearchLine(reg[0])
            lines.append(line)
        profile = Profile()
        profile.researcher = researcher
        profile.titulations = titulations
        profile.projects = projects
        profile.lines = lines
        return profile