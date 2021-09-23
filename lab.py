import math
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import warnings

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
        self.actions = [self.create_PopData, self.answer_a, self.answer_b, self.answer_c, self.answer_d,
                        self.answer_e_f, self.answer_g,
                        self.exit]
        # menu text for each of the actions above
        self.menu = ["Create PopData", "Answer A", "Answer B", "Answer C", "Answer D", "Answer E and F", "Answer G",
                     "Exit"]
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
        drop_table_query = "DROP VIEW if EXISTS  PopData;"
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

        drop_table_query = "DROP VIEW if EXISTS  PopData2;"
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
            if r[0] is not None and r[0] is not None:
                xs.append(float(r[0]))
                ys.append(float(r[1]))
            else:
                print("Dropped tuple ", r)

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

        return [xs, ys]

    def answer_c(self):
        [xs, ys] = self.query_c()
        regr = LinearRegression().fit(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
        score = regr.score(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
        a = regr.coef_[0][0]
        b = regr.intercept_[0]
        #print("a:", a)
        #print("b:", b)
        xp = [1980, 1990, 2000, 2010, 2020, 2030]
        yp = []
        for cell in xp:
            yp.append((int(a) * cell + b))

        #print("predicted population:", yp)

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
            query = 'INSERT INTO Prediction(name, country,population, year) VALUES ("' + str(
                entry[0]) + '","' + str(entry[1]) + '",' + str(entry[2] * entry[4] + entry[3]) + ',' + str(
                entry[4]) + ')'
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
        ymin = min(yvals)
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
            ourhypothesis = "that in general, big cities grow at higher rates than smaller ones"
            print("Hello! Our hypothesis is {}\n".format(ourhypothesis))
            print("1. Growth Analysis \n"
                  "2. Exit")

        try:
            choice = int(input())
            if choice < 1:
                print("Too low!")
                raise ValueError
            elif choice > 2:
                print("Too High!")
                raise ValueError
        except ValueError:
            print("Try again!")
            print()
            self.main_menu_g(1)

        if choice == 1:
            print("Lets analyze the growth!")
            self.Growth_Analysis()

        elif choice == 2:
            return

    def Growth_Analysis(self):
        while True:
            syntax_q = input("Do you want to see the syntax? y/n ")
            if syntax_q == "y":
                self.syntax_printer()

            big_city_size = input("How big do you consider a big city to be?")
            small_city_size = input("How big do you consider a small city to be?")

            bigx, bigy, smallx, smally = self.eval_city_growth(big_city_size, small_city_size)

            ylower = min([min(bigy), min(smally)])
            yupper = max([max(bigy), max(smally)])

            fig, axs = plt.subplots(1, 2)
            big_plot_label = "Growth Rate of cities where population > " + big_city_size
            small_plot_label = "Growth Rate of cities where population < " + small_city_size
            axs[0].plot(bigx, bigy, label=big_plot_label)
            axs[1].plot(smallx, smally, label=small_plot_label)

            axs[0].set_ylim(ylower, yupper)
            axs[1].set_ylim(ylower, yupper)

            fig.suptitle("Growth Rates of big and small cities")
            axs[0].legend(loc=1, fontsize=6)
            axs[1].legend(loc=2, fontsize=6)
            plt.show()

    def eval_city_growth(self, big_city_size, small_city_size):
        years_big, pop_big = self.get_big_cities(big_city_size)
        years_small, pop_small = self.get_small_cities(small_city_size)

        first_year = max([min(years_big), min(years_small)])
        last_year = min([max(years_big), max(years_small)])


        prev_year = None
        next_year = None
        growth_list_big = []
        while len(years_big) != 0:
            i = 0
            prev_year = next_year
            while prev_year == next_year:
                try:
                    prev_year = years_big[i]
                    next_year = years_big[i + 1]
                    i += 1
                except IndexError:
                    i += 1
                    break
            try:
                sliced = pop_big[:i]
            except IndexError:
                sliced = pop_big
                growth_list_big.append([years_big[0], np.average(sliced)])
                break

            growth_list_big.append([years_big[0], np.average(sliced)])
            pop_big = pop_big[i + 1:]
            years_big = years_big[i + 1:]

        prev_year = None
        next_year = None
        growth_list_small = []
        while len(years_small) != 0:
            i = 0
            prev_year = next_year
            while prev_year == next_year:
                try:
                    prev_year = years_small[i]
                    next_year = years_small[i + 1]
                    i += 1
                except IndexError:
                    i += 1
                    break
            try:
                sliced = pop_small[:i]
            except IndexError:
                sliced = pop_small
                growth_list_small.append([years_small[0], np.average(sliced)])
                break

            growth_list_small.append([years_small[0], np.average(sliced)])
            pop_small = pop_small[i + 1:]
            years_small = years_small[i + 1:]

        pop_big = list(zip(*growth_list_big))[1]
        year_big = list(zip(*growth_list_big))[0]
        pop_small = list(zip(*growth_list_small))[1]
        year_small = list(zip(*growth_list_small))[0]

        growth_big = []
        growth_small = []

        for i in range(len(pop_big)):
            try:
                if math.isinf(pop_big[i + 1] / pop_big[i]) is True or pop_big[i + 1] / pop_big[i] > 5:
                    pass
                else:
                    growth_big.append([year_big[i + 1], ((pop_big[i + 1] / pop_big[i]) - 1)])
            except IndexError:
                pass

        for i in range(len(pop_small)):
            try:
                if math.isinf(pop_small[i + 1] / pop_small[i]) is True or (
                        (pop_small[i + 1] / pop_small[i]) - 1) < -0.9 or ((pop_small[i + 1] / pop_small[i]) - 1) > 5:
                    pass
                else:
                    growth_small.append([year_small[i + 1], ((pop_small[i + 1] / pop_small[i]) - 1)])
            except IndexError:
                pass

        big_years = []
        small_years = []
        growth_big_final = []
        growth_small_final = []

        for elem in growth_big:
            big_years.append(elem[0])
            growth_big_final.append(elem[1])

        for elem in growth_small:
            small_years.append(elem[0])
            growth_small_final.append(elem[1])

        return big_years, growth_big_final, small_years, growth_small_final

    def get_big_cities(self, big_city_size):
        data = self.data_grabber("year", "population", None, "PopData", "population > " + big_city_size, None)
        return data

    def get_small_cities(self, small_city_size):
        data = self.data_grabber("year", "population", None, "PopData", "population < " + small_city_size, None)
        return data

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

        data2 = sorted(data, key=lambda x: x[0])
        zippeddata = zip(*data2)
        z = list(zippeddata)
        x = list(map(float, z[0]))
        y = list(map(float, z[1]))
        return x, y

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
