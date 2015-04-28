import rdflib
from rdflib import ConjunctiveGraph
import sys
from rdfApp import converter


__author__ = 'Hugo Silva'

filePathCSV = "E:\\WS trab2\\Semantic-web-rdf-app\\assignment2\\dados\\dados.csv"
filePathNT = "E:\\WS trab2\\Semantic-web-rdf-app\\assignment2\\dados\\dados.nt"
filePathXML = "E:\\WS trab2\\Semantic-web-rdf-app\\assignment2\\dados\\dados.xml"
filePathN3 = "E:\\WS trab2\\Semantic-web-rdf-app\\assignment2\\dados\\dados.n3"
filePathDB = "E:\\WS trab2\\Semantic-web-rdf-app\\assignment2\\dados\\dados.db"

c = converter.converter()

# Convert CSV file to NT file
c.convert_csv_to_nt(filePathCSV, filePathNT)
# load (automatically) NT file to graph - function f2()
c.read_NTfile_to_graph(filePathNT)

# Convert NT file
def f1():
    print("1. Convert NT file to RDF/XML file")
    print("2. Convert NT file to N3 file")
    str = input("Option -> ")
    option = readIntegerValue(str, 1, 2)
    if(isinstance(option, int)):
        menuConvertOptions[option]()

# Convert NT file to RDF/ML file
def f1_1():
    c.convert_NTfile_to_rdfXML_format(filePathXML)

# Convert NT file to N3 file
def f1_2():
    c.convert_NTfile_to_N3_format(filePathN3)

# Load NT file - probably will be deleted because we do the same in the beginning of the script
def f2():
    # insert data in graph (located in converter.py)
    # very important, the graph is in converter.py (self.graph)
    c.read_NTfile_to_graph(filePathNT)

# Store data in DB (SQLite) - not working
def f3():
    # usar para a query
    '''graph = c.getGraph()

    g = rdflib.ConjunctiveGraph('SQLite')
    g.open(filePathDB, create=True)
    for t in graph.triples((None, None, None)):
        g.add(t)
    g.commit()
    g.close()'''
    print("not working yet...")

def f0():
    sys.exit()


menuConvertOptions = {
    1: f1_1,
    2: f1_2,
}

menuOptions = {
    1: f1,
    2: f2,
    3: f3,
    0: f0,
}

def readIntegerValue(str, min, max):
    try:
        number = int(str)
        if(number <= max and number >= min):
            return number
        else:
            print("Invalid Option!")
    except ValueError:
        print("No valid integer! Please try again ...")

while True:
    print("\n*** WorldCup 2014 - Brazil ***")
    print("1. Convert NT file")
    print("2. Load NT file")
    print("3. Store data in DB (SQLite)")
    print("0. Exit")
    str = input("Option -> ")
    option = readIntegerValue(str, 0, 10)
    if(isinstance(option,int)):
        menuOptions[option]()


#-----------------TESTES-----------------
    # get predicates list
    #lista = set(graph.predicates())
    #for a in lista:
    #    print(a)

    # get triple selection - maxi pereira
    #lista = _graph.triples((rdflib.URIRef('http://ws_60015_76169.com/player361'), None, None))
    #for a in lista:
    #    print(a)

    # namespaces in graph
    #for prefix, uri in graph.namespaces():
    #    print("%s - %s" %(prefix, uri))