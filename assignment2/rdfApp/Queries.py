import rdflib
from rdflib import ConjunctiveGraph, Namespace
from rdfApp import converter

__author__ = 'Hugo Silva'


# Queries functions

# List Countrys
def f1(graph):
    qres = """
        PREFIX pred: <http://xmlns.com/work/>
        SELECT ?countryID ?name
        WHERE {
            ?countryID pred:name ?name .
            ?countryID pred:countryID ?id .
        }
        ORDER BY (?name)
    """
    return graph.query(qres)

# List Players
def f2(graph):
    qres = """
        PREFIX pred: <http://xmlns.com/work/>
        SELECT ?playerID ?name
        WHERE {
            ?playerID pred:name ?name .
            ?playerID pred:playerID ?id .
        }
        ORDER BY (?name)
    """
    return graph.query(qres)

# List player information
def f3(graph, str):
    qres = """
        PREFIX pred: <http://xmlns.com/work/>
        SELECT ?playerID ?name ?position ?age ?nameTeam ?team_presences ?nameClub
        WHERE {
            ?playerID pred:name ?name FILTER regex(?name, '""" + str + """', "i").
            ?playerID pred:playerID ?id .
            ?playerID pred:age ?age .
            ?playerID pred:position ?position .
            ?playerID pred:in_team ?in_team .

            ?in_team pred:name ?nameTeam .

            ?playerID pred:team_presences ?team_presences .
            ?playerID pred:in_club ?in_club .

            ?in_club pred:name ?nameClub .
        }
    """
    return graph.query(qres)

# List Clubs from one country that have players of the same country and went to world cup
# example: List Portuguese Clubs with Portuguese players that went to world cup
def f4(graph, str):
    qres = """
        PREFIX pred: <http://xmlns.com/work/>
        SELECT ?clubName ?playerName
        WHERE {

            ?country pred:name ?nameC FILTER regex(?nameC, '""" + str + """',"i").
            ?country pred:countryID ?countryID .

            ?player pred:playerID ?playerID .
            ?player pred:in_team ?country .
            ?player pred:in_club ?club .
            ?player pred:name ?playerName .

            ?club pred:clubID ?clubID .
            ?club pred:from_country ?country .
            ?club pred:name ?clubName .
        }
        ORDER BY (?name)
    """
    return graph.query(qres)

# List Players from one Team
def f5(graph, str):
    qres = """
        PREFIX pred: <http://xmlns.com/work/>
        SELECT ?playerID ?name
        WHERE {
            ?country pred:name ?nameC FILTER regex(?nameC, '""" + str + """',"i") .
            ?playerID pred:in_team ?country .
            ?playerID pred:name ?name .
        }
        ORDER BY (?name)
    """
    return graph.query(qres)

# List Players from one Team
def f6(graph, str):
    qres = """
        PREFIX pred: <http://xmlns.com/work/>
        SELECT ?playerID ?name
        WHERE {
            ?clubID pred:name ?nameC FILTER regex(?nameC, '""" + str + """').
            ?playerID pred:in_club ?clubID.
            ?playerID pred:name ?name.
        }
        ORDER BY (?name)
    """
    return graph.query(qres)

# Get country name inserting club name
def f7(graph, str):
    qres = """
        PREFIX pred: <http://xmlns.com/work/>
        SELECT ?nameC ?countryName
        WHERE {
            ?club pred:name ?nameC FILTER regex(?nameC, '""" + str + """',"i").
            ?club pred:from_country ?country .
            ?country pred:name ?countryName .
        }
    """
    return graph.query(qres)