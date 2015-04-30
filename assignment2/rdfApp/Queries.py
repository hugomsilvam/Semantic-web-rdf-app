__author__ = 'Hugo Silva'

# list countrys
def query1(graph, namespace, predicate):
    print("a")


'''
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