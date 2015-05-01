package main;

import java.io.File;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Scanner;

/**
 * Created by Hugo Silva on 30/04/2015.
 */

public class ParseCSV {

    static HashSet<String> country_list = new HashSet<String>();
    static HashMap<String, String> country_map = new HashMap<String, String>();
    static HashMap<String, String> club_map = new HashMap<String, String>(); // <Nome do clube, countryID>
    static HashMap<String, String> clubID_map = new HashMap<String, String>(); // <clubID, nome do clube> --- CLUBES REPETIDOS
    static HashMap<String, String> newClubID_map = new HashMap<String, String>(); // <clubID, nome do clube> -- SEM clubes repetidos :D
    static HashMap<String, String> team_map = new HashMap<String, String>();
    static HashMap<String, String> player_map = new HashMap<String, String>();

    static StringBuilder country_csv = new StringBuilder();
    static StringBuilder club_csv = new StringBuilder();
    static StringBuilder player_csv = new StringBuilder();
    static StringBuilder team_csv = new StringBuilder();
    static StringBuilder dados_csv = new StringBuilder();

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);

        //Objetivo: ler ficheiro original WM 2014.csv e converter para um ficheiro csv em formato de triples

        File filePath = new File(new File(System.getProperty("user.dir")).getParent() + "\\dados\\WM 2014.csv");
        File filePath1 = new File(new File(System.getProperty("user.dir")).getParent() + "\\dados\\dados.csv");

        StringBuilder sb = read.ReadFile.fileToStringBuilder(filePath.toString());

// COUNTRY ---------------------------------------------------------------------
        String[] lines = sb.toString().split("\\n");
        for (String line : lines) {
            String[] lineData = line.split(",");
            String club_country = lineData[11];

            //guardar paises (Country)
            saveCountry(club_country);
        }

        Iterator country_iterator = country_list.iterator();
        int i = 0;
        while (country_iterator.hasNext()) {
            i++;
            String countryName = (String) country_iterator.next();
            country_map.put("country/" + i, countryName); //colocar nomes dos paises e respectivos ids num hashmap
            generate_tripleStore(country_csv, "country/" + i, "countryID", Integer.toString(i));
            generate_tripleStore(country_csv, "country/" + i, "name", countryName);
        }

// CLUB ------------------------------------------------------------------------
        int i2 = 0;
        for (String line : lines) {
            i2++;
            String[] lineData = line.split(",");
            String player_club_name = lineData[10];
            String club_country = lineData[11];

            saveClubData(player_club_name, club_country);
            saveOldClubDataID("club" + i2, player_club_name); //vai gravar clubes repetidos, por isso vamos criar um novo HashSet para eliminar esses dados repetidos
        }

        Iterator club_iterator = club_map.entrySet().iterator();
        int i1 = 0;
        while (club_iterator.hasNext()) {
            i1++;
            Map.Entry pair = (Map.Entry) club_iterator.next();
            String clubName = (String) pair.getKey();
            String clubCountryID = (String) pair.getValue();
            generate_tripleStore(club_csv, "club/" + i1, "clubID", Integer.toString(i1));
            generate_tripleStore(club_csv, "club/" + i1, "name", clubName);
            generate_tripleStore(club_csv, "club/" + i1, "from_country", clubCountryID);
        }

// PLAYER ----------------------------------------------------------------------
        //<idclub, nome club> - hashmap usado para ligar o player ao club.
        HashSet<String> getClubsName = new HashSet<String>();
        getClubsName.addAll(clubID_map.values());

        Iterator clubsID_iterator = getClubsName.iterator();
        int i4 = 0;
        while (clubsID_iterator.hasNext()) {
            i4++;
            newClubID_map.put("club/" + i4, (String) clubsID_iterator.next());
        }

        int i3 = 0;
        for (String line : lines) {
            i3++;
            String[] lineData = line.split(",");
            String team_name = lineData[1];
            String player_position = lineData[3];
            String player_name = lineData[4];
            String player_age = lineData[8];
            String player_team_presences = lineData[9];
            String player_club_name = lineData[10];

            savePlayerData("player/" + i3, player_name);
            generate_tripleStore(player_csv, "player/" + i3, "playerID", Integer.toString(i3));
            generate_tripleStore(player_csv, "player/" + i3, "name", player_name);
            generate_tripleStore(player_csv, "player/" + i3, "age", player_age);
            generate_tripleStore(player_csv, "player/" + i3, "position", player_position);
            generate_tripleStore(player_csv, "player/" + i3, "in_team", (String) getKeyFromValue(country_map, team_name));
            generate_tripleStore(player_csv, "player/" + i3, "team_presences", player_team_presences);
            generate_tripleStore(player_csv, "player/" + i3, "in_club", (String) getKeyFromValue(newClubID_map, player_club_name));
        }

// TEAM ------------------------------------------------------------------------
        int i5 = 0;
        for (String line : lines) {
            String[] lineData = line.split(",");
            String team_group = lineData[0];
            String team_name = lineData[1];
            String player_name = lineData[4];
            String player_is_captain = lineData[12];

            if (player_is_captain.equalsIgnoreCase("TRUE")) {
                saveTeamData(team_name, player_name);
                i5++;
                generate_tripleStore(team_csv, "team/" + i5, "teamID", Integer.toString(i5));
                generate_tripleStore(team_csv, "team/" + i5, "group", team_group);
                generate_tripleStore(team_csv, "team/" + i5, "from_country", (String) getKeyFromValue(country_map, team_name));
                generate_tripleStore(team_csv, "team/" + i5, "captain", (String) getKeyFromValue(player_map, player_name));
            }
        }

        //stringbuilder geral com todos os dados
        dados_csv.append(country_csv);
        dados_csv.append(club_csv);
        dados_csv.append(player_csv);
        dados_csv.append(team_csv);

        //escrever dados organizados
        write.WriteFile.stringBuilderToFile(dados_csv, filePath1.toString());
    }

    public static void saveCountry(String countryName) {
        country_list.add(countryName);
    }

    //grava nome do clube e sua localizacao
    public static void saveClubData(String clubName, String country) {
        club_map.put(clubName, (String) getKeyFromValue(country_map, country));
    }

    //grava id do clube e o seu nome
    public static void saveOldClubDataID(String clubID, String clubName) {
        clubID_map.put(clubID, clubName);
    }

    public static Object getKeyFromValue(HashMap hm, Object value) {
        for (Object o : hm.keySet()) {
            if (hm.get(o).equals(value)) {
                return o;
            }
        }
        return null;
    }

    public static boolean verifyDuplicates(HashMap hm, Object value) {
        for (Object o : hm.keySet()) {
            if (o.equals(value)) {
                return true;
            }
        }
        return false;
    }

    public static void savePlayerData(String playerID, String playerName) {
        player_map.put(playerID, playerName);
    }

    public static void saveTeamData(String teamName, String playerCaptain) {
        team_map.put(teamName, (String) getKeyFromValue(player_map, playerCaptain));
    }

    public static void generate_tripleStore(StringBuilder sb, String subject, String predicate, String object) {
        sb.append(subject).append(",").append(predicate).append(",").append(object).append("\n");
    }
}
