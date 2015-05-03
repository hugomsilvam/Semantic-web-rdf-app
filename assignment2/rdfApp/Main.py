import inspect
import os
import rdflib
from rdflib import ConjunctiveGraph, URIRef, Literal
import sys
from rdfApp import converter, Queries, InferenceRule


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

# List Player information (name, age, position, team name, team presences, club name)
def f6():
    str = input("Name -> ")
    results = Queries.f3(graph, str)
    for subject, name, position, age, nameCC, team_presences, in_club, inferenceAge, inferenceTeam_presences in results:
        print(" Name:", name, "\n", " Position:", position, "\n", " Age:", age, "\n", " Team:", nameCC, "\n", " Presences:", team_presences, "\n", " Club:", in_club, "\n", " Inference Age:", inferenceAge, "\n", " Inference Team Presences:", inferenceTeam_presences, "\n")
    print("Number of players: %d" %(len(results)))

# List Clubs from one country that have players of the same country and went to world cup
# example: List Portuguese Clubs with Portuguese players that went to world cup
def f7():
    str = input("Country -> ")
    results = Queries.f4(graph, str)
    print(" Club name \t - Player Name")
    for clubName, playerName in results:
        print(" %s \t - %s"%(clubName,playerName))
    print("Number players : %d" %(len(results)))

# List Players from one Team
def f8():
    str = input("Country -> ")
    results = Queries.f5(graph, str)
    for subject, name in results:
        print(" Player name:", name)
    print("Number of players: %d" %(len(results)))

# List Players from one Club
def f9():
    str = input("Club -> ")
    results = Queries.f6(graph, str)
    for subject, name in results:
        print("Name:",name)
    print("Number of players: %d" %(len(results)))

# Get country name inserting club name
def f10():
    str = input("Club -> ")
    results = Queries.f7(graph, str)
    for clubName, countryName in results:
        print("Club name: %s \t Country name: %s" %(clubName, countryName))

#apply inferences to the players (inferenceAge, and inferenceTeamPresences)
def f11():
    print("In this function will be applied inference to all players. Inference to the player's age and to the player's team presences.\n"
          " - To the player's age: if the player has less than equal 24 years old => belongs to Sub 24 team, "
          "ELSE IF player has more than 32 years old => This is the last world cup to this player.\n"
          " - To the player's team presence: if the player has less than equal 10 team presences => This player it debuted recently for the Team, "
          "ELSE IF player has more than 35 team presences => This player it's a veteran of the Team\n")

    option = input("Do you want to apply inference? (Y or any other key to cancel): ")
    if option[0].lower() == 'y':
        # inference age
        results = InferenceRule.f1(graph)
        for sub, pred, obj in results:
            graph.add((sub, pred, Literal(obj)))

        # inference team presences
        results1 = InferenceRule.f2(graph)
        for sub, pred, obj in results1:
            graph.add((sub, pred, Literal(obj)))

        print("Inference applied with sucess!")
    else:
        print("Canceled by the user")

# Update RDF Files (NT, XML, N3, and DB Files
def f12():
    # create updated NT file
    graph.serialize(destination=filePathNT, format='nt')
    # create updated XML file
    graph.serialize(destination=filePathXML, format='pretty-xml')
    # create updated N3 file
    graph.serialize(destination=filePathN3, format='n3')

    # create updated DB file.
    # first, we have to remove DB file to prevent this error: sqlite3.OperationalError: table kb_bec6803d52_asserted_statements already exists
    os.remove(filePathDB)

    g = rdflib.ConjunctiveGraph('SQLite')
    g.open(filePathDB, create=True)
    for t in graph.triples((None, None, None)):
        g.add(t)
    g.commit()
    g.close()

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
    7: f7,
    8: f8,
    9: f9,
    10: f10,
    11: f11,
    12: f12,
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
    print("7. List Clubs from one country that have players of the same country and went to world cup")
    print("8. List Players from one Team")
    print("9. List Players from one Club")
    print("10. Get country name inserting club name")
    print("11. Apply Inferences in all graph")
    print("12. Update RDF Files (NT, XML, N3, and DB Files")
    print("0. Exit")
    str = input("Option -> ")
    option = readIntegerValue(str, 0, 12)
    if(isinstance(option,int)):
        menuOptions[option]()

