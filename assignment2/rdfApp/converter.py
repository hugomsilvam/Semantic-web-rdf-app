import csv
from rdflib import ConjunctiveGraph
import rdflib

__author__ = 'Hugo Silva'

'''
This script will convert csv format data (our original data) into rdf format data.
First, we analysed the exemplo.csv with one sample of relation tuples and then we create a .nt format file in RDF/NT following the exemplo.csv struture
Of course, all the dados.csv will be converted to RDF/NT (.nt format file) following the struture created in exemplo.nt.

Example: <http://ws_60015_76169.com/club/1> <http://xmlns.com/work/name> "Benfica".
Age Player and Team presences -> integer objects are writen in this form: "30"^^<http://www.w3.org/2001/XMLSchema#int>.
all the rest atributes are strings and ids (URIs).

-----------------Countrys example:-----------------
    <http://ws_60015_76169.com/country5> <http://xmlns.com/work/name> "Portugal".
    <http://ws_60015_76169.com/country44> <http://xmlns.com/work/name> "Uruguay".

    <http://ws_60015_76169.com/country3> <http://xmlns.com/work/name> "England".

-----------------Club example:-----------------
    <http://ws_60015_76169.com/club104> <http://xmlns.com/work/name> "Benfica".
    <http://ws_60015_76169.com/club104> <http://xmlns.com/work/from_country> <http://ws_60015_76169.com/country5>.

    <http://ws_60015_76169.com/club100> <http://xmlns.com/work/name> "West Bromwich Albion".
    <http://ws_60015_76169.com/club100> <http://xmlns.com/work/from_country> <http://ws_60015_76169.com/country3>.

-----------------Player example:-----------------
    <http://ws_60015_76169.com/player361> <http://xmlns.com/work/name> "MaxiPereira".
    <http://ws_60015_76169.com/player361> <http://xmlns.com/work/age> "30"^^<http://www.w3.org/2001/XMLSchema#int>.
    <http://ws_60015_76169.com/player361> <http://xmlns.com/work/position> "DF".
    <http://ws_60015_76169.com/player361> <http://xmlns.com/work/in_team> <http://ws_60015_76169.com/country44>.
    <http://ws_60015_76169.com/player361> <http://xmlns.com/work/team_presences> "89"^^<http://www.w3.org/2001/XMLSchema#int>.
    <http://ws_60015_76169.com/player361> <http://xmlns.com/work/in_club> <http://ws_60015_76169.com/club104>.

    <http://ws_60015_76169.com/player347> <http://xmlns.com/work/name> "Diego Lugano (c)".
    <http://ws_60015_76169.com/player347> <http://xmlns.com/work/age> "33"^^<http://www.w3.org/2001/XMLSchema#int>.
    <http://ws_60015_76169.com/player347> <http://xmlns.com/work/position> "DF".
    <http://ws_60015_76169.com/player347> <http://xmlns.com/work/in_team> <http://ws_60015_76169.com/country44>.
    <http://ws_60015_76169.com/player347> <http://xmlns.com/work/team_presences> "93"^^<http://www.w3.org/2001/XMLSchema#int>.
    <http://ws_60015_76169.com/player347> <http://xmlns.com/work/in_club> <http://ws_60015_76169.com/club100>.


-----------------Team example:-----------------
    <http://ws_60015_76169.com/team16> <http://xmlns.com/work/group> "D".
    <http://ws_60015_76169.com/team16> <http://xmlns.com/work/from_country> <http://ws_60015_76169.com/country44>.
    <http://ws_60015_76169.com/country44> <http://xmlns.com/work/captain> <http://ws_60015_76169.com/player347>
'''

class converter:


    def __init__(self):
        self.arrayLines = []
        self.graph = ConjunctiveGraph()

    def convert_csv_to_nt(self, filePathCSV, filePathNT):

        # array to save new data
        self.arrayLines = converter.read_csvFile_and_create_arrayLines(self, filePathCSV)

        converter.write_arrayLines_in_NTfile(self, self.arrayLines, filePathNT)

    #read NT file and create graph
    def read_NTfile_to_graph(self, filePathNT):
        return self.graph.parse(filePathNT, format="nt")

    # save NT file data into RDF/XML format
    def convert_NTfile_to_rdfXML_format(self, filePathXML):
        ofXML = open(filePathXML, "wb")
        ofXML.write(self.graph.serialize(format="pretty-xml"))
        ofXML.close()

    # save NT file data into N3 format
    def convert_NTfile_to_N3_format(self, filePathN3):
        ofN3 = open(filePathN3, "wb")
        ofN3.write(self.graph.serialize(format="n3"))
        ofN3.close()

    def convert_NTfile_to_DB_format(self, filePathDB):
        g = rdflib.ConjunctiveGraph('SQLite')
        g.open(filePathDB, create=True)
        for t in self.graph.triples((None, None, None)):
            g.add(t)
        g.commit()
        g.close()

    # get graph data
    def getGraph(self):
        return self.graph;


    # secondary function: read file and save new data into arrayLines
    def read_csvFile_and_create_arrayLines(self, filePathCSV):
        # save old subjects (ex: country5) and new subjects (ex: <http://ws_60015_76169.com/country5>)
        dictionary_sub_newSub = dict()

        # usable strings to concatenate in file.nt format
        xmlIntegerStruture = "^^<http://www.w3.org/2001/XMLSchema#int>"
        dotPoint = "."

        # array to save new data
        arrayLines = []

        f = open(filePathCSV, "r", encoding="utf8")
        linhas = csv.reader(f)
        for sub, pred, obj in linhas:
            newSub = "<http://ws_60015_76169.com/"+sub+">"
            newPred = "<http://xmlns.com/work/"+pred+">"
            newObj = "<http://ws_60015_76169.com/"+obj+">"

            # if obj its an ID
            if "country" in obj or "club" in obj or "player" in obj or "team" in obj:
                # verify if obj exists in dictionary
                if obj in dictionary_sub_newSub: # ex: if country5 in dictionary, newObj = <http://ws_60015_76169.com/country5>
                    newObj = dictionary_sub_newSub[obj]
                    #print("%s %s %s%s" %(newSub, newPred, newObj, dotPoint))
                    aux = str.format("%s %s %s%s" %(newSub, newPred, newObj, dotPoint))
                    arrayLines.append(aux)

                else: # if not, save in dictionary (ex: country4 : <http://..../country4>)
                    dictionary_sub_newSub[obj] = newObj
                    #print("%s %s %s%s" %(newSub, newPred, dictionary_sub_newSub[obj], dotPoint))
                    aux = str.format("%s %s %s%s" %(newSub, newPred, dictionary_sub_newSub[obj], dotPoint))
                    arrayLines.append(aux)

            # if obj its plain text (string), then save in dictionary the old subject and the new rdf subject
            else:
                # if obj values are integer, add xmlIntegerStrture to newObj
                if "team_presences" in pred or "age" in pred:
                    integerTypeObj = "\""+obj+"\""+xmlIntegerStruture
                    dictionary_sub_newSub[sub] = newSub
                    #print("%s %s %s%s" %(newSub, newPred, integerTypeObj, dotPoint))
                    aux = str.format("%s %s %s%s" %(newSub, newPred, integerTypeObj, dotPoint))
                    arrayLines.append(aux)

                else: # pred values are strings
                    #print("%s %s \"%s\"%s" %(newSub, newPred, obj, dotPoint))
                    aux = str.format("%s %s \"%s\"%s" %(newSub, newPred, obj, dotPoint))
                    arrayLines.append(aux)
        f.close()
        return arrayLines

    # secondary function: save new file with new data from arrayLines
    def write_arrayLines_in_NTfile(self, arrayLines, filePathNT):
        f = open(filePathNT, "w", encoding="utf8")
        f.write("\n".join(str(x) for x in arrayLines))
        f.close()
