import inspect
import os
import rdflib
from rdflib import ConjunctiveGraph
import sys
from rdfApp import converter, Queries


__author__ = 'Hugo Silva'

# procedure chosen to automatically the program read and create data files in a specific data directory outside the application directory
rdfAppDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
assignment2Dir = os.path.dirname(os.path.abspath(rdfAppDir))
dataDir = os.path.dirname(os.path.abspath(assignment2Dir))

filePathCSV = dataDir+"/dados/dados.csv"
filePathNT = dataDir+"/dados/dados.nt"
filePathXML = dataDir+"/dados/dados.xml"
filePathN3 = dataDir+"/dados/dados.n3"
filePathDB = dataDir+"/dados/dados.db"

c = converter.converter()

# Convert CSV file to NT file
print("Loading CSV data...")
c.convert_csv_to_nt(filePathCSV, filePathNT)
print("NT file created!")
# load (automatically) NT file to graph - function f2()
graph = c.read_NTfile_to_graph(filePathNT)
print("Graph created!")

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
    print("Conversion completed!")

# Convert NT file to N3 file
def f1_2():
    c.convert_NTfile_to_N3_format(filePathN3)
    print("Conversion completed!")

# Load NT file - probably will be deleted because we do the same in the beginning of the script
def f2():
    # insert data in graph (located in converter.py)
    # very important, the graph is in converter.py (self.graph)
    graph = c.read_NTfile_to_graph(filePathNT)

# Store data in DB (SQLite) - convert NT_file data in DB file
def f3():
    c.convert_NTfile_to_DB_format(filePathDB)
    print("Conversion completed!")


#-----------------Queries-----------------
# List countrys
def f4():
    results = Queries.f1(graph)
    for subject, name in results:
        print(name)
    print("Number of countrys: %d" %(len(results)))

# List Players name
def f5():
    results = Queries.f2(graph)
    for subject, name in results:
        print(name)
    print("Number of players: %d" %(len(results)))

def f6():
    a = 1

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
    4: f4,
    5: f5,
    6: f6,
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
    print("2. Load NT file (not needed...)")
    print("3. Store data in DB (SQLite)")
    print("4. List Countrys name")
    print("5. List Players name")
    print("6. List data from Player name")
    print("7. List clubs who have players playing in the world cup")
    print("8. Listar clubes cujo jogadores participarem no mundial de um determinado País")
    print("6. Listar jogadores de uma determinada Seleção")
    print("7. Listar jogadores de um determinado clube")
    print("8. Listar dados de um jogador com base em inferencias")
    print("9. Gerar ficheiro para visualizar o Grafo(.dot)")
    print("10. Gerar ficheiro para visualizar o Grafo(.dot) com dados de Portugal")
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