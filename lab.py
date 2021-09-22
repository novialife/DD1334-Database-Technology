import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import warnings
from time import sleep
warnings.filterwarnings('ignore')

try:
    input = raw_input
except NameError:
    pass


class Program:

    def __init__(self):  # PG-connection setup
        self.conn = sqlite3.connect('mondial.db')  # establish database connection
        self.cur = self.conn.cursor()  # create a database query cursor

        # specify the command line menu here
        self.actions = [self.create_PopData, self.answer_a, self.answer_b, self.answer_c, self.answer_d, self.answer_e_f, self.answer_g,
                        self.exit]
        # menu text for each of the actions above
        self.menu = ["Create PopData","Answer A", "Answer B", "Answer C", "Answer D", "Answer E and F", "Answer G", "Exit"]
        self.cur = self.conn.cursor()

    def print_menu(self):
        """Prints a menu of all functions this program offers.  Returns the numerical correspondant of the choice made."""
        for i, x in enumerate(self.menu):
            print("%i. %s" % (i + 1, x))
        return self.get_int()

    def get_int(self):
        """Retrieves an integer from the user.
        If the user fails to submit an integer, it will reprompt until an integer is submitted."""
        while True:
            try:
                choice = int(input("Choose: "))
                if 1 <= choice <= len(self.menu):
                    return choice
                print("Invalid choice.")
            except (NameError, ValueError, TypeError, SyntaxError):
                print("That was not a number, genious.... :(")

    def population_query(self):
        minpop = input("min_population: ")
        maxpop = input("max_population: ")
        print("minpop: %s, maxpop: %s" % (minpop, maxpop))
        try:
            query = "SELECT * FROM city WHERE population >=%s AND population <= %s" % (minpop, maxpop)
            print("Will execute: ", query)
            result = self.cur.fetchall()
            self.cur.execute(query)
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            connection1.rollback()
            exit()

        self.print_answer(result)

    def exit(self):
        self.cur.close()
        self.conn.close()
        exit()

    ##Our Code Start here
    # Question A:################################################################################################################################

    def create_PopData(self):
        drop_table_query = "Drop VIEW if EXISTS  PopData;"
        try:
            self.cur.execute(drop_table_query)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()

        query = "CREATE VIEW [PopData] AS SELECT Year, City AS Name, citypops.Population, citypops.Country, Longitude," \
                "Latitude, Elevation FROM citypops JOIN City ON (citypops.City=City.Name AND citypops.Country=City.Country);"
        try:
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()

        drop_table_query = "Drop table if EXISTS  PopData2;"
        try:
            self.cur.execute(drop_table_query)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()

        query = "CREATE VIEW[PopData2] AS SELECT Year, Name, Population, PopData.Country, Longitude, Latitude, " \
                "Elevation, Agriculture, Service, Industry, Inflation FROM PopData JOIN Economy " \
                "ON (PopData.Country = Economy.Country);"

        try:
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()

    def query_a(self):
        xy = "select year,  population From Popdata2";
        print("U1: (start) " + xy)
        try:
            self.cur.execute(xy)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()
        xs = []
        ys = []
        for r in data:
            # print("Considering tuple", r)
            if r[0] is not None and r[0] is not None:
                xs.append(float(r[0]))
                ys.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        print("year:", xs)
        print("population:", ys)
        return [xs, ys]

    def answer_a(self):
        [xs, ys] = self.query_a()
        plt.scatter(xs, ys)
        plt.savefig("figure.png")  # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out
        plt.close()

    # Question B:################################################################################################################################
    def query_b(self):
        xy = "SELECT year, SUM(population) FROM PopData2 GROUP BY year";
        print("U1: (start) " + xy)
        try:
            self.cur.execute(xy)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()
        xs = []
        ys = []
        for r in data:
            print("Considering tuple", r)
            if r[0] is not None and r[0] is not None:
                xs.append(float(r[0]))
                ys.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        print("year:", xs)
        print("sum(population):", ys)
        return [xs, ys]

    def answer_b(self):
        [xs, ys] = self.query_b()
        plt.scatter(xs, ys)
        plt.savefig("figure.png")  # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out
        plt.close()

    # Question C:################################################################################################################################
    def query_c(self):
        xy = "select year,  population From PopData2 where name ='New York'";
        print("U1: (start) " + xy)
        try:
            self.cur.execute(xy)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()
        xs = []
        ys = []
        for r in data:
            # print("Considering tuple", r)
            if r[0] is not None and r[0] is not None:
                xs.append(float(r[0]))
                ys.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        print("New York City:")
        print("year:", xs)
        print("population:", ys)
        return [xs, ys]

    def answer_c(self):
        [xs, ys] = self.query_c()
        regr = LinearRegression().fit(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
        score = regr.score(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
        a = regr.coef_[0][0]
        b = regr.intercept_[0]
        print("a:", a)
        print("b:", b)
        xp = [1980, 1990, 2000, 2010, 2020, 2030]
        yp = []
        for cell in xp:
            yp.append((int(a) * cell + b))

        print("predicted population:", yp)

        plt.plot(xp, yp, color='red', linewidth=3)
        plt.scatter(xs, ys)
        plt.savefig("figure.png")  # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out
        plt.close()

    # Question D:################################################################################################################################
    def query_create_table_linearprediction(self):
        drop_table_query = "Drop table if EXISTS  linearprediction;"
        try:
            self.cur.execute(drop_table_query)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()
        create_table_query = "CREATE TABLE linearprediction( name VARCHAR2(50) not NULL ,country VARCHAR2(50) not NULL ,a float not NULL ,b float not NULL ,score float not NULL, linearprediction CHECK (score >= 0) CHECK (1 >= score),								CONSTRAINT linearprediction PRIMARY KEY (name, country) );";
        try:
            self.cur.execute(create_table_query)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()

    def query_insert_table_linearprediction(self, cities, countries, a_values, b_values, score_values):
        create_table_query = "CREATE TABLE linearprediction( name VARCHAR2(50) not NULL ,country VARCHAR2(50) not NULL ,a float not NULL ,b float not NULL ,score float not NULL, CONSTRAINT linearprediction CHECK (score >= 0) CHECK (1 >= score),								CONSTRAINT linearprediction PRIMARY KEY (name, country) );";
        try:
            for i in range(len(cities)):
                if (str(score_values[i]) != "nan"):
                    sql = 'INSERT INTO linearprediction (name, country,a,b,score) VALUES ("' + str(
                        cities[i]) + '","' + str(countries[i]) + '",' + str(a_values[i]) + ',' + str(
                        b_values[i]) + ',' + str(score_values[i]) + ')'
                else:
                    sql = 'INSERT INTO linearprediction (name, country,a,b,score) VALUES ("' + str(
                        cities[i]) + '","' + str(countries[i]) + '",' + str(a_values[i]) + ',' + str(
                        b_values[i]) + ',' + str(0) + ')'

                self.cur.execute(sql)
                self.conn.commit()

        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()
        print("done!")

    def query_get_all_cities(self):
        xy = "select DISTINCT  name,  country From Popdata2"
        try:
            self.cur.execute(xy)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()
        xs = []
        ys = []
        for r in data:
            # print("Considering tuple", r)
            if (r[0] != None and r[0] != None):
                xs.append((r[0]))
                ys.append((r[1]))
            else:
                print("Dropped tuple ", r)
        return [xs, ys]

    def query_get_year_pop(self, city):
        xy = 'select year,  population From PopData2 where name = "' + city + '"';
        try:
            self.cur.execute(xy)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()
        xs = []
        ys = []
        for r in data:
            # print("Considering tuple", r)
            if (r[0] != None and r[1] != None):
                xs.append(float(r[0]))
                ys.append(float(r[1]))
            else:
                xs.append(0)
                ys.append(0)


        return [xs, ys]

    def answer_d(self):
        cities = []
        countries = []
        a_values = []
        b_values = []
        score_values = []
        [cities, countries] = self.query_get_all_cities()
        for city in cities:
            [xs, ys] = self.query_get_year_pop(city)
            regr = LinearRegression().fit(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
            score = regr.score(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
            a = regr.coef_[0][0]
            b = regr.intercept_[0]
            a_values.append(a)
            b_values.append(b)
            score_values.append(score)
        self.query_create_table_linearprediction()
        self.query_insert_table_linearprediction(cities, countries, a_values, b_values, score_values)
        # close()
        print("woopdityscoop")
    # Question E:################################################################################################################################
    def answer_e_f(self):
        """Prints a menu of all functions this program offers.  Returns the numerical correspondant of the choice made."""
        while True:
            if self.second_menu(0) is not None:
                break

    def main_menu(self, tries=0):
        if tries == 0:
            print()
            print("1. Create new prediction relation Prediction(name, country, population, year)\n2. Populate the "
                  "prediction table\n3. Visualize the predictions\n4. Exit")
        try:
            choice = int(input())
            if choice < 1:
                print("Too low!")
                raise ValueError
            elif choice > 4:
                print("Too High!")
                raise ValueError
        except ValueError:
            print("Try again!")
            print()
            self.second_menu(1)
        return choice

    def second_menu(self, tries):
        user_choice = self.main_menu(tries)

        if user_choice == 1:
            print("Creating new table Prediction and replacing old one if it exists")
            self.create_prediction_table()
        elif user_choice == 2:
            print("Populating table with predicted linear regression data")
            self.populating_table()
        elif user_choice == 3:
            print("Visualizing the predictions")
            self.visualization()
        elif user_choice == 4:
            return False

    def create_prediction_table(self):
        try:
            query = "DROP TABLE Prediction";
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            pass

        try:
            query = "CREATE TABLE Prediction(" \
                    "name TEXT NOT NULL," \
                    "country TEXT NOT NULL," \
                    "population TEXT NOT NULL," \
                    "year TEXT NOT NULL);"

            self.cur.execute(query)
            self.conn.commit()
            print("Done creating table!")
            print()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            return

    def populating_table(self):
        query = "SELECT linearprediction.name, linearprediction.country, a, b, PopData2.year " \
                "FROM linearprediction INNER JOIN PopData2 " \
                "ON linearprediction.name = PopData2.name and linearprediction.country = PopData2.country"
        try:
            self.cur.execute(query)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()


        for entry in data:
            print(entry)
            query = 'INSERT INTO Prediction(name, country,population, year) VALUES ("' + str(
                entry[0]) + '","' + str(entry[1]) + '",' + str(entry[2] * entry[4] + entry[3]) + ',' + str(entry[4]) + ')'
            print(query)
            try:
                self.cur.execute(query)
                self.conn.commit()
            except sqlite3.Error as e:
                print("Error message:", e.args[0])
                self.conn.rollback()
                exit()

    def visualization(self):
        query = "SELECT year, population, name " \
                "FROM Prediction " \
                "WHERE population > 0"
        try:
            self.cur.execute(query)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()
        print(data)
        data2 = sorted(data, key=lambda x: x[0])
        zippeddata = zip(*data2)
        foo = list(zippeddata)

        try:
            xvals = list(map(float, foo[0]))
            yvals = list(map(float, foo[1]))
            names = list(map(str, foo[2]))
        except IndexError:
            print("Empty table, populate it please!")
            return


        plt.scatter(xvals, yvals)

        xmax = xvals[int(np.argmax(yvals))]
        ymax = max(yvals)
        maxname = names[int(np.argmax(yvals))]
        xmin = xvals[int(np.argmin(yvals))]
        print(min(xvals))
        ymin = min(yvals)
        print(ymin)
        minname = names[int(np.argmin(yvals))]

        textmax = "Maximum Population, Year = {}, Population = {}, City = {}".format(int(xmax), int(ymax), maxname)
        textmin = "Minimum Population, Year = {}, Population = {}, City = {}".format(int(xmin), int(ymin), minname)

        plt.axhline(ymax, color='r', linestyle='-', label=textmax)
        plt.axhline(ymin, color='y', linestyle='-', label=textmin)

        mean = np.mean(yvals)
        plt.axhline(mean, color='g', linestyle='-', label='Mean = ' + str(int(mean)))

        plt.legend()
        plt.show()
        print("Going to back to main menu!")

    def answer_g(self):
        """Prints a menu of all functions this program offers.  Returns the numerical correspondant of the choice made."""
        while True:
            self.main_menu_g(0)

    def main_menu_g(self, tries=0):
        if tries == 0:
            print()
            ourhypothesis = "Insert Hypothesis here"
            print("Hello! Our hypothesis is {}\n".format(ourhypothesis))
            print("1. Analysis 1 \n"
                  "2. Analysis 2\n"
                  "3. Analysis 3\n"
                  "4. Exit")
        try:
            choice = int(input())
            if choice < 1:
                print("Too low!")
                raise ValueError
            elif choice > 4:
                print("Too High!")
                raise ValueError
        except ValueError:
            print("Try again!")
            print()
            self.main_menu_g(1)

        if choice == 1:
            print("Calls method 1")
            self.method1()
        elif choice == 2:
            print("Calls method 2")
            self.method2()
        elif choice == 3:
            print("Calls method 3")
            self.method3()
        elif choice == 4:
            return

    def method1(self):
        while True:
            syntax_q = input("Do you want to see the syntax? y/n ")
            if syntax_q == "y":
                self.syntax_printer()

            data = self.data_grabber("year", "population", None, "Prediction")
            sleep(5)
            if data is not True:
                break
        self.plotter(data, "scatter")

    def method2(self):
        self.syntax_printer()

    def method3(self):
        self.syntax_printer()

    def data_grabber(self, x_attr=None, y_attr=None, extras=None, table_name=None, where_condition=None, complex=None):
        if complex is not None:
            query = complex
        else:
            query_sel = "SELECT {}, {} ".format(x_attr, y_attr)
            if extras is not None:
                for extra in extras:
                    query_sel += ", " + extra
                query_sel += " "

            query_from = "FROM {} ".format(table_name)

            if where_condition is not None:
                where_statement = "WHERE " + where_condition
            else:
                where_statement = ""

            query_where = "{}".format(where_statement)

            query = query_sel + query_from + query_where

        print("Your query is: " + query)
        try:
            self.cur.execute(query)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            print("Try changing input parameters")
            print()
            return True

        return data

    def plotter(self, data, plot_type, extras=None, labels=None):

        print("Plotting!")
        data2 = sorted(data, key=lambda x: x[0])
        zippeddata = zip(*data2)
        z = list(zippeddata)
        try:
            x = list(map(float, z[0]))
            y = list(map(float, z[1]))
        except:
            print("Empty table, populate it please!")
            return

        fig, ax = plt.subplots()
        func = getattr(ax, plot_type)
        if labels is not None:
            func(x, y, label=labels[0])
        else:
            func(x,y)

        i = 1
        if extras is not None:
            for extra in z[2:]:
                extra = list(map(float, extra))
                func(x, extra, labels[i])
                i += 1

        plt.show()


    def syntax_printer(self):
        print("SYNTAX FOR FUNCTIONS IS:")
        print()
        print("FOR DATA_GRABBER:")
        print("str: x_attribute, str: y_attribute, list: ['extra1','extra2',...] extras are considered as y_attributes"
              ", str: table_name, str: where_condition"
              ", str: complex_query")
        print()
        print("FOR DATA PLOTTER:")
        print("data: data, str: matplotlib plot type, YES/NO: extras, list: ['label1','label2','label3',....]")
        print("DONT GET IT WRONG, THERE IS ALMOST NO ERROR HANDLING FOR INPUT PARAMETERS...... ;(")
        print()


    ##Our code end here
    def print_answer(self, result):
        print("-----------------------------------")
        for r in result:
            print(r)
        print("-----------------------------------")

    def run(self):
        while True:
            try:
                self.actions[self.print_menu() - 1]()
            except IndexError as e:
                print(e)
                print("Bad choice")
                continue


if __name__ == "__main__":
    db = Program()
    db.run()
