from random import seed
from random import randint
import sqlite3
import csv
import subprocess, os, platform 
import matplotlib.pyplot as plt






def create_database():

    
    first_value = randint(0,9)
    second_value = randint(0,9)

    order = input("Do you want to go first or second Adam (enter either 1 or 2): ")
    if order == "1": 
        adam_car = cars[first_value]

        fred_car = cars[second_value]

        print("Adam's Car is... " + adam_car)

        print("Fred's Car is... " + fred_car)

    elif order == "2":

        adam_car = cars[second_value]

        fred_car = cars[first_value]

        print("Fred's Car is... " + fred_car)

        print("Adam's Car is... " + adam_car)

    else:
        print("error")

    random_track = str(randint(1, 22))

    

    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()

        cursor.execute("select name from sqlite_master where name=?", ("tblTracks",))
        result = cursor.fetchall()

        if len(result) == 1:
            cursor.execute("""SELECT track_name from tblTracks where trackID==""" + random_track,)
            track_result = cursor.fetchall()

            if track_result == []:
                
                
                create_database()
            
            else: 

                print("The track you will be racing at is... ")
                print(track_result)

                track_check = int(input("Is this okay? (1 for yes, 2 for no) "))

                if track_check == 1:
                    cursor.execute("DELETE FROM tblTracks WHERE trackID==" + random_track,)
                    db.commit()

                else:
                    create_database()



            

            

            


        else: 
            cursor.execute("""CREATE table tblTracks
            (trackID integer,
            track_name string,
            primary key(trackID))""")

            for i in range(0, len(tracks)):
                
                cursor.execute("""INSERT INTO tblTracks(track_name)
                VALUES(?)""", (tracks[i],))
                db.commit()
                i = i + 1

            cursor.execute("""SELECT track_name from tblTracks where trackID==""" + random_track,)
            track_result = cursor.fetchall()

            cursor.execute("DELETE FROM tblTracks WHERE trackID==" + random_track,)
            db.commit()

            print("The track you will be racing at is... ")
            print(track_result)
    
    start()

def score_keeper():
    adam_score = int(input("What Position did Adam come? "))
    adam_add = int(input("How many simp points did Adam get for his car? "))
    adam_deduct = int(input("How many deduction points did Adam recieve? "))
    adam_total = 21 - adam_score
    adam_total = adam_total + adam_add - adam_deduct
    print("Adam recieves " + str(adam_total))

    fred_score = int(input("What Position did Fred come? "))
    fred_add = int(input("How many simp points did Fred get for his car? "))
    fred_deduct = int(input("How many deduction points did Fred recieve? "))
    fred_total = 21 - fred_score
    fred_total = fred_total + fred_add - fred_deduct
    print("Fred recieves " + str(fred_total))

    race_name = input("What track were you racing at? ")

    score_check = int(input("Is this information correct? (1 for yes, 2 for no) "))

    if score_check == 1:

        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()

            cursor.execute("select name from sqlite_master where name=?", ("tblScores",))
            result = cursor.fetchall()

            if len(result) == 1:
                cursor.execute("""INSERT INTO tblScores(race_name,adam_score,fred_score)
                VALUES(?,?,?)""", (race_name, adam_total, fred_total))
                db.commit()

            
            else: 
                cursor.execute("""CREATE table tblScores
                (raceID integer,
                race_name string,
                adam_score integer,
                fred_score integer,
                primary key(raceID))""")

                cursor.execute("""INSERT INTO tblScores(race_name,adam_score,fred_score)
                VALUES(?,?,?)""", (race_name, adam_total, fred_total))
                db.commit()


    
    else:
        score_keeper()
    
    start()


def total_scores():

    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()

        cursor.execute("select * from tblScores")
        a = cursor.fetchall()


        cursor.execute("SELECT sum(adam_score) FROM tblScores")
        adam_total = cursor.fetchall()

        cursor.execute("SELECT sum(fred_score) FROM tblScores")
        fred_total = cursor.fetchall()

        print("Adam's total score is " + str(adam_total))
        print("Fred's total score is " + str(fred_total))

        if adam_total > fred_total:
            print("Adam's in the lead! Little bitch...")
        
        else:
            print("Fred's in the lead! Fuck u Adam, Bitch")

    csv_open = int(input("Would you like to download this as a CSV file? (1 = yes, 2 = no) "))

    if csv_open == 1:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tblScores",)
            score_data = cursor.fetchall()
            score_data = [[j for j in i] for i in score_data]
            score_data.insert(0, ["Track ID", "Race Name", "Adam's Score", "Fred's Score"])
            with open('Scores.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(score_data)

    graph_open = int(input("Would you like me to display this in graphical form? (1=yes, 2=no) "))

    adam_graph_score = []
    fred_graph_score = []
    race_graph_score = []
    fred_total_graph = []
    adam_total_graph = []

    if graph_open == 1: 
        # with sqlite3.connect("database.db") as db:
        #     cursor = db.cursor()
        #     cursor.execute("SELECT adam_score FROM tblScores")
        #     adam_individual = cursor.fetchall()
        #     cursor.execute("SELECT fred_score FROM tblScores")
        #     fred_individual = cursor.fetchall()

        #     print(adam_individual[0][0])
        #     print(fred_individual)

        with sqlite3.connect("database.db") as db:
            a = 1
            adam_tracker = 0
            check = True
            cursor = db.cursor()
            while check == True:
                cursor.execute("SELECT adam_score FROM tblScores WHERE raceID =?", (a,))
                adam_temp_score = cursor.fetchall()
                if adam_temp_score == []:
                    check = False
                else:
                    adam_final_score = adam_temp_score
                
                
                # adam_temp_score = int(adam_temp_score[0][0])
                adam_graph_score.append(adam_final_score[0][0])
                adam_cumulative_score = adam_final_score[0][0]
                adam_tracker = adam_tracker + int(adam_cumulative_score)
                adam_total_graph.append(adam_tracker)
                

                a = a+1

        adam_graph_score.pop()
        adam_total_graph.pop()

        
        
        

        with sqlite3.connect("database.db") as db:
            a = 1
            fred_tracker = 0
            check = True
            cursor = db.cursor()
            while check == True:
                cursor.execute("SELECT fred_score FROM tblScores WHERE raceID =?", (a,))
                fred_temp_score = cursor.fetchall()
                if fred_temp_score == []:
                    check = False
                else:
                    fred_final_score = fred_temp_score
                
                
                # adam_temp_score = int(adam_temp_score[0][0])
                fred_graph_score.append(fred_final_score[0][0])
                fred_cumulative_score = fred_final_score[0][0]
                fred_tracker = fred_tracker + int(fred_cumulative_score)
                fred_total_graph.append(fred_tracker)
                

                a = a+1

        fred_graph_score.pop()
        fred_total_graph.pop()


        with sqlite3.connect("database.db") as db:
            a = 1
            check = True
            cursor = db.cursor()
            while check == True:
                cursor.execute("SELECT race_name FROM tblScores WHERE raceID =?", (a,))
                race_temp_score = cursor.fetchall()
                if race_temp_score == []:
                    check = False
                else:
                    race_final_score = race_temp_score
                
                
                # adam_temp_score = int(adam_temp_score[0][0])
                race_graph_score.append(race_final_score[0][0])
                a = a+1

        race_graph_score.pop()
        
        


        plt.plot(race_graph_score, fred_graph_score, color='g')
        plt.plot(race_graph_score, adam_graph_score, color='orange')
        plt.xlabel('Track Name')
        plt.ylabel('Points')
        plt.title("Fred = Green, Adam = Orange")
        plt.show()

        plt.plot(race_graph_score, fred_total_graph, color='g')
        plt.plot(race_graph_score, adam_total_graph, color="orange")
        plt.xlabel('Track Name')
        plt.ylabel('Points')
        plt.title("Cumulative Scores, Fred=Green, Adam=Orange")
        plt.show()

    start()

        
            



cars = ["Mercedes", "Ferrari", "Red Bull", "McLaren", "Renult", "Alpha Tauri", "Racing Point", "Alfa Romeo", "Haas", "Williams"]

tracks = ["Australia", "Bahrain", "Vietnam", "China", "Netherlands", "Spain", "Monaco", "Baku", "Canada", "France", "Austria", "GB", "Hungary", "Belgium", "Italy", "Singapore", "Russia", "Japan", "USA", "Mexico", "Brazil", "Abu Dabhi"]


def start():



    race_score = input("Would u like to start new race, input scores or find total score? (enter 1 for new race and 2 for scores, 3 for total) ")

    if race_score == "1": 
        create_database()


            
    elif race_score == "3":
        total_scores()

    



    elif race_score == "2":
        score_keeper()

    else:
        f= input("ERROR!!!")

    start()

start()



























