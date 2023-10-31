from database_connection import DataBaseConn
from profile import Profile

class Lattes():
    def __init__(self):
        self.db = DataBaseConn()

    def __del__(self):
        del self.db

    def get_profile_by_lattes_id(self, lattesID):
        query = "Select * from researcher where lattesID = " + lattesID
        researcher = self.db.execute_query(query)
        query = "Select * from titualtion where researcherID = " + lattesID
        titulations = self.db.execute_query(query)
        query = "Select * from projects a join project_researchers b on a.projectID = b.projectID where b.researcherID = " + lattesID
        projects = self.db.execute_query(query)
        query = "Select * from research_lines a join research_line_researcher b on a.lineID = b.lineID where b.researcherID = " + lattesID
        lines = self.db.execute_query(query)
        profile = Profile()
        profile.researcher = researcher
        profile.titulations = titulations
        profile.projects = projects
        profile.lines = lines
        return profile