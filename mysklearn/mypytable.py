# TODO: copy your mypytable.py solution from PA2-PA7 here


import copy
import csv
#from tabulate import tabulate # uncomment if you want to use the pretty_print() method
# install tabulate with: pip install tabulate

# required functions/methods are noted with TODOs
# provided unit tests are in test_mypytable.py
# do not modify this class name, required function/method headers, or the unit tests
class MyPyTable:
    """Represents a 2D table of data with column names.

    Attributes:
        column_names(list of str): M column names
        data(list of list of obj): 2D data structure storing mixed type data.
            There are N rows by M columns.
    """

    def __init__(self, column_names=None, data=None):
        """Initializer for MyPyTable.

        Args:
            column_names(list of str): initial M column names (None if empty)
            data(list of list of obj): initial table data in shape NxM (None if empty)
        """
        if column_names is None:
            column_names = []
        self.column_names = copy.deepcopy(column_names)
        if data is None:
            data = []
        self.data = copy.deepcopy(data)

    # def pretty_print(self):
    #     """Prints the table in a nicely formatted grid structure.
    #     """
    #     print(tabulate(self.data, headers=self.column_names))

    def get_shape(self):
        
        """Computes the dimension of the table (N x M).
        
        Returns:
            int: number of rows in the table (N)
            int: number of cols in the table (M)
        """
        return len(self.data), len(self.column_names)

    def get_column(self, col_identifier, include_missing_values=True):
        
        col  = []
        col_index = self.column_names.index(col_identifier)
        for row in self.data:
            col.append(row[col_index])
    
        """Extracts a column from the table data as a list.
        
        Args:
            col_identifier(str or int): string for a column name or int
                for a column index
            include_missing_values(bool): True if missing values ("NA")
                should be included in the column, False otherwise.

        Returns:
            list of obj: 1D list of values in the column

        Notes:
            Raise ValueError on invalid col_identifier
        """
        return col

    def convert_to_numeric(self):
        """Try to convert each value in the table to a numeric type (float).

        Notes:
            Leave values as is that cannot be converted to numeric.
        """
        for row in range(len(self.data)):
            for i in range(len(self.data[row])):
                try: 
                    self.data[row][i] = float(self.data[row][i])
                    #attempts to convert to float, pass if fails
                except ValueError:
                    pass

                    
               
                
                
                

    def drop_rows(self, row_indexes_to_drop):
        
        """Remove rows from the table data.

        Args:
            row_indexes_to_drop(list of int): list of row indexes to remove from the table data.
        """
        row_indexes_to_drop.sort(reverse=True)
        #sorts indices
        for row in row_indexes_to_drop:
            self.data.pop(row)
        #removes rows with said indices
                

    def load_from_file(self, filename):
        """Load column names and data from a CSV file.

        Args:
            filename(str): relative path for the CSV file to open and load the contents of.

        Returns:
            MyPyTable: return self so the caller can write code like
                table = MyPyTable().load_from_file(fname)

        Notes:
            Use the csv module.
            First row of CSV file is assumed to be the header.
            Calls convert_to_numeric() after load
        """
      
        inFile = open(filename, 'r')
        reader = csv.reader(inFile)
        header = [] 
        table = []
        #opens and reads file and then created header and data table
        num = 0

        for value in reader:
            if num != 0:
                table.append(value)
            else:
                header = value
            num +=1
        #differentiates between headers and data
        inFile.close()

        self.column_names = header
        self.data = table
        #puts header and data into table
        self.convert_to_numeric()
        #converts applicable valujes to numeric
        return self

    def save_to_file(self, filename):
        """Save column names and data to a CSV file.

        Args:
            filename(str): relative path for the CSV file to save the contents to.

        Notes:
            Use the csv module.
        
        """
        outFile = open(filename, 'w')
        writer = csv.writer(outFile)
        writer.writerow(self.column_names)
        writer.writerows(self.data)
        #writes out headers and data to a csv file


    def find_duplicates(self, key_column_names):
        """Returns a list of indexes representing duplicate rows.
        Rows are identified uniquely based on key_column_names.

        Args:
            key_column_names(list of str): column names to use as row keys.

        Returns
            list of int: list of indexes of duplicate rows found

        Notes:
            Subsequent occurrence(s) of a row are considered the duplicate(s).
                The first instance of a row is not considered a duplicate.
        """
        index_holder = []
        table = []

        for i in key_column_names:
            index_holder.append(self.column_names.index(i))
        #creates list of column indices
        for row in self.data:
            table.append(tuple(row[i] for i in index_holder))
        
        
            #checks for duplicates and then returns list of the indexes of the duplicates
        return [j for j, x in enumerate(table) if x in table[:j]]




    def remove_rows_with_missing_values(self):
        """Remove rows from the table data that contain a missing value ("NA").
        """
        self.data = [i for i in self.data if "NA" not in i]
              #checks if rows have missing values and then removes them if they do      

    def replace_missing_values_with_column_average(self, col_name):
        """For columns with continuous data, fill missing values in a column
            by the column's original average.

        Args:
            col_name(str): name of column to fill with the original average (of the column).
        """
        col = self.column_names.index(col_name)
        cleaned = [row[col] for row in self.data if row[col] != "NA"]
        #finds rows that dont have missing values
        average = sum(cleaned)/len(cleaned) 
        #computes average for selected column
        self.data = [[row[i] if i != col or row[i] != "NA" else average for i in range(len(row))] for row in self.data]
        #applies average to rows with NA values
        
                
        

    def compute_summary_statistics(self, col_names):
        """Calculates summary stats for this MyPyTable and stores the stats in a new MyPyTable.
            min: minimum of the column
            max: maximum of the column
            mid: mid-value (AKA mid-range) of the column
            avg: mean of the column
            median: median of the column

        Args:
            col_names(list of str): names of the numeric columns to compute summary stats for.

        Returns:
            MyPyTable: stores the summary stats computed. The column names and their order
                is as follows: ["attribute", "min", "max", "mid", "avg", "median"]

        Notes:
            Missing values should in the columns to compute summary stats
                for should be ignored.
            Assumes col_names only contains the names of columns with numeric data.

        """
        header = ["attribute", "min", "max", "mid", "avg", "median"]
        table = []
        #assigns lists
        for col in col_names:
            stats = []
            values = self.get_column(col, False)
            #gets seleected column and does not include missing values

            if not values == []:
                values.sort()

                stats.append(col)
                #adds attributes

                stats.append(min(values))
                #finds max

                stats.append(max(values))
                #finds min

                stats.append((max(values) + min(values)) / 2)
                #finds middle value

                stats.append(sum(values) / len(values))
                # finds mean

                if len(values) % 2 == 0:
                    stats.append((values[int((len(values) -1) / 2)] + values[int(((len(values) -1) / 2) + 1)]) / 2)
                    #median for even number of values
                else:
                    stats.append(values[int((len(values)-1)/2)])
                    #median for odd values
                #finds median
                table.append(stats)
                #appends values to table
        return MyPyTable(header, table)



    def perform_inner_join(self, other_table, key_column_names):
        """Return a new MyPyTable that is this MyPyTable inner joined
            with other_table based on key_column_names.

        Args:
            other_table(MyPyTable): the second table to join this table with.
            key_column_names(list of str): column names to use as row keys.

        Returns:
            MyPyTable: the inner joined table.
        """
        table1 = []
        table2 = []
        values = []

        header = copy.deepcopy(self.column_names)
        
        for i in other_table.column_names:
            try:
                key_column_names.index(i)
            except ValueError:
                header.append(i)
        #checks other table for specified columns to join on
        
        
        
        try:
            for name in key_column_names:
                table1.append(self.column_names.index(name))
                table2.append(other_table.column_names.index(name))

                #Appends column names to both tables
        except:
            pass
       
       
       
       
        else:
            for rows in self.data:
                for rows2 in other_table.data:
                    equal = True
                    #sets values as equal
                   
                   
                    for j in range(len(key_column_names)):
                        value1 = rows[table1[j]]
                        value2 = rows2[table2[j]]
                        if value1 != value2:
                            equal = False
                            #tests if values in 2 tables are equal, changes to false if false
                            break
                    
                    
                    if equal == True:
                        row = copy.deepcopy(rows)
                        for k in range(len(rows2)):
                            try:
                                table2.index(k)
                            except ValueError:
                                row.append(rows2[k])
                        #if true, appends values to new row after deep copy
                        values.append(row)
                        #appends rows to data


        return MyPyTable(header, data = values) 
        

    def perform_full_outer_join(self, other_table, key_column_names):
        """Return a new MyPyTable that is this MyPyTable fully outer joined with
            other_table based on key_column_names.

        Args:
            other_table(MyPyTable): the second table to join this table with.
            key_column_names(list of str): column names to use as row keys.

        Returns:
            MyPyTable: the fully outer joined table.

        Notes:
            Pad the attributes with missing values with "NA".

        """
        table1 = []
        table2 = []
        values = []

        header = copy.deepcopy(self.column_names)
        
        for i in other_table.column_names:
            try:
                key_column_names.index(i)
            except ValueError:
                header.append(i)
        #checks other table for specified columns to join on
        
        
        
        try:
            for name in key_column_names:
                table1.append(self.column_names.index(name))
                table2.append(other_table.column_names.index(name))

                #Appends column names to both tables
        except:
            pass
       
       
       
       
        else:
            for rows in self.data:
                for rows2 in other_table.data:
                    equal = True
                    #sets values as equal
                   
                   
                    for j in range(len(key_column_names)):
                        value1 = rows[table1[j]]
                        value2 = rows2[table2[j]]
                        if value1 != value2:
                            equal = False
                            #tests if values in 2 tables are equal, changes to false if false
                            break
                    
                    
                    if equal == True:
                        row = copy.deepcopy(rows)
                        for k in range(len(rows2)):
                            try:
                                table2.index(k)
                            except ValueError:
                                row.append(rows2[k])
                        #if true, appends values to new row after deep copy
                        values.append(row)
                        #appends rows to data


                # I did not know what to do past the inner join
        return MyPyTable(header, data = values) 


       

        


#if __name__ == "__main__":
