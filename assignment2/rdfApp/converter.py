import csv

__author__ = 'Hugo Silva'

'''
This script will convert csv format data (our original data) into rdf format data.
First, we analysed the exemplo.csv with one sample of relation tuples and then we create a .nt format file in RDF/NT following the exemplo.csv struture
Of course, all the dados.csv will be converted to RDF/NT (.nt format file) following the struture created in exemplo.nt.

Example: <http://ws_60015_76169.com/club/1> <http://xmlns.com/work/name> "Benfica".
Age Player and Team presences -> integer objects are writen in this form: "30"^^<http://www.w3.org/2001/XMLSchema#int>.
all the rest atributes are strings and ids.

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

    fileDados = "E:\\WS trab2\\Semantic-web-rdf-app\\assignment2\\dados\\dados.csv"
    fileDadosNT = "E:\\WS trab2\\Semantic-web-rdf-app\\assignment2\\dados\\dados.nt"
    xmlIntegerStruture = "^^<http://www.w3.org/2001/XMLSchema#int>"
    dotPoint = "."

    # save old subjects (ex: country5) and new subjects (ex: <http://ws_60015_76169.com/country5>)
    dictionary_sub_newSub = dict()

    # array to save new data
    arrayLines = []

    #--------------------------read file and save new data into arrayLines--------------------------
    f = open(fileDados, "r", encoding="utf8")
    linhas = csv.reader(f)
    for sub, pred, obj in linhas:
        newSub = "<http://ws_60015_76169.com/"+sub+">"
        newPred = "<http://ws_60015_76169.com/"+pred+">"
        newObj = "<http://ws_60015_76169.com/"+obj+">"

        # if obj its an ID
        if "country" in obj or "club" in obj or "player" in obj or "team" in obj:
            # verify if obj exists in dictionary
            if obj in dictionary_sub_newSub: # ex: if country5 in dictionary, newObj = <http://ws_60015_76169.com/country5>
                newObj = dictionary_sub_newSub[obj]
                print("%s %s %s%s" %(newSub, newPred, newObj, dotPoint))
                aux = str.format("%s %s %s%s" %(newSub, newPred, newObj, dotPoint))
                arrayLines.append(aux)

            else: # if not, save in dictionary (ex: country4 : <http://..../country4>)
                dictionary_sub_newSub[obj] = newObj
                print("%s %s %s%s" %(newSub, newPred, dictionary_sub_newSub[obj], dotPoint))
                aux = str.format("%s %s %s%s" %(newSub, newPred, dictionary_sub_newSub[obj], dotPoint))
                arrayLines.append(aux)

        # if obj its plain text (string), then save in dictionary the old subject and the new rdf subject
        else:
            # if obj values are integer, add xmlIntegerStrture to newObj
            if "team_presences" in pred or "age" in pred:
                integerTypeObj = "\""+obj+"\""+xmlIntegerStruture
                dictionary_sub_newSub[sub] = newSub
                print("%s %s %s%s" %(newSub, newPred, integerTypeObj, dotPoint))
                aux = str.format("%s %s %s%s" %(newSub, newPred, integerTypeObj, dotPoint))
                arrayLines.append(aux)

            else: # pred values are strings
                print("%s %s \"%s\"%s" %(newSub, newPred, obj, dotPoint))
                aux = str.format("%s %s \"%s\"%s" %(newSub, newPred, obj, dotPoint))
                arrayLines.append(aux)
    f.close()

    #--------------------------save new file with new data from arrayLines--------------------------
    f1 = open(fileDadosNT, "w", encoding="utf8")
    f1.write("\n".join(str(x) for x in arrayLines))
    f1.close()
