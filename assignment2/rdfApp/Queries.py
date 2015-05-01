import rdflib
from rdflib import ConjunctiveGraph, Namespace

__author__ = 'Hugo Silva'

filePathRDF = "E:\\WS trab2\\Semantic-web-rdf-app\\assignment2\\dados\\dados.n3"
# list countrys
FBNAMESPACE = Namespace("<http://ws_60015_76169.com/")
g = ConjunctiveGraph()
g.parse(filePathRDF, format="n3")
qres = g.query("""SELECT ?country ?name
     WHERE <http://ws_60015_76169.com/country> <http://xmlns.com/work/name> ?name
      """
)
for x in qres:
    print("a")



'''BORDONHOS
def listTypes (graph, namespace, type):
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



'''
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