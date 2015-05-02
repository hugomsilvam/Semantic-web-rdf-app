__author__ = 'Hugo Silva'

# INFERENCE - player's age
# if a player age <= 24 -> belongs to Sub 24 team
# else if player age >= 32 -> This is the last world cup to this player
def f1(graph):
    qres = """
        PREFIX pred: <http://xmlns.com/work/>
        CONSTRUCT {
            ?player pred:ageInference ?inferenceValue
        }
        WHERE {
            ?player pred:playerID ?playerID .
            ?player pred:age ?age .
            BIND (IF((?age <= 24), "Belongs to the Sub-24 team", IF(?age > 32, "Last World cup to this player", "None")) AS ?inferenceValue) .
        }
    """
    return graph.query(qres)

# INFERENCE - player's team presences
# if player presences <= 10 -> This player it debuted recently for the Team.
# else if player presences >= 35 -> This player it's a veteran for the Team.
def f2(graph):
    qres = """
        PREFIX pred: <http://xmlns.com/work/>
        CONSTRUCT {
            ?player pred:inferenceTeam_presences ?inferenceValue
        }
        WHERE {
            ?player pred:playerID ?playerID .
            ?player pred:team_presences ?team_presences.
            BIND (IF((?team_presences <= 10), "This player it debuted recently for the Team", IF(?team_presences >= 35, "This player it's a veteran of the Team.", "None")) AS ?inferenceValue) .
        }
    """
    return graph.query(qres)