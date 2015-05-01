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
















#--------------------LIXO----------------------------
'''
# QUERY NOT WORKING-------------------------------------------->
def f3(graph, namespace, playerName):
    ns = Namespace(namespace)
    #"PREFIX pred: <http://xmlns.com/work/>"
    qres = "SELECT ?playerID ?name ?age ?position ?teamName ?teamPresences ?clubName" \
           "WHERE {" \
           "?playerID ?name pred:playerID ?id ." \
           "?playerID ?name pred:name "+playerName+" ." \
                                                   "}"

    return graph.query(qres, initNs={'pred':ns})
'''

#BORDONHOS
'''def listTypes (graph, namespace, type):
    ns = Namespace(namespace)
qry = "SELECT ?Descricao ( Count (*) as ?count) " \
      " WHERE {" \
      " ?s pf:" + type + " ?Tipo . " \
                         " ?Tipo pf:description ?Descricao ." \
                         "}" \
                         "GROUP BY ?Descricao " \
                         "ORDER BY DESC (?count)"
results = graph.query( qry, initNs={'pf':ns})
return results'''


'''PREFIX countrySubject = "<http://ws_60015_76169.com/country"
FROM graph
SELECT ?name
WHERE {
?country countrySubject:id ?name .
}'''



''' #Tiago
def query1(graph, namespace, predicate):
# namespace = URI - link (URI diretamente e deve dar, penso eu)
# predicate = URI (onde esta pf:ns metes o URI)
def predicateCount (graph, namespace, predicate):
    ns = Namespace(namespace)
    qry = "SELECT (COUNT(pf:" + predicate + ") as ?pCount) " \
                                            " WHERE {" \
                                            "?s pf:" + predicate + " ?o ." \
                                                                   "    } "

    results = graph.query( qry, initNs={'pf':ns})
    return results
'''