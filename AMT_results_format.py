__author__ = 'mmadaio'

import csv
import math
from collections import defaultdict
import glob, os

batchNum = "batch5"    ## Change this to "test1" or "batch1" depending on what your files or folders are labeled as


def list_of_indices(a, item):
    b = []
    for num in range(len(a)):
        if a[num] == item:
            b.append(num)
    return b

def convert_csv_to_list(filename):
    """
    Converts cvs file to list of rows as lists.
    """
    output = []
    with open(filename, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            output.append(row)
    csvfile.close()
    return output

def hiits(filename):
    filename = convert_csv_to_list(filename)
    hiits = defaultdict(lambda: [])
    for num in range(1, len(filename)):
        hiits[filename[num][0]].append(filename[num])
    return hiits



os.chdir("2016_Study/{0}/".format(batchNum))  ## Change this folder name to whatever subdirectory your "VideoNameRef_*.csv" and AMT output file e.g. "Batch_2659126_batch_results" are in
for file in glob.glob("*.csv"):
    if file.endswith("results.csv"):
        print(file)
        hiits = hiits(file)
    else:
        print("Make sure your AMT output file ends with 'results.csv'")

def format_csv(hiits):
    csvs = []
    num_raters = []
    for hiit in hiits:
        row_count = 1
        title = ["Slice num", "# Raters", "src"]
        rows = []
        values = hiits[hiit]
        workers = []
        for row in values:
            workers.append(row[15])  ## column index of worker ID  -- CHANGE THIS IF NECESSARY
            print row[15]
        num_raters.append(len(workers))
        title += workers
        for num1 in range(33, 43):  ## change column indices of src links to those of the 10 video files being rated here -- CHANGE THIS IF NECESSARY
            print num1
            print values[0][num1]
            slice_src = values[0][num1]
            row = [row_count, 0, slice_src]
            for num2 in range(len(values)):
                row.append(values[num2][num1+20])
                if values[num2][num1] != "N/A":
                    row[1] += 1
            rows.append(row)
            row_count += 1
        rows.insert(0, title)
        csvs.append(rows)
    return csvs, num_raters

output, num_raters = format_csv(hiits)

def delete_raters_with_same_ratings(output, num_raters):
    new_output = [[] for num in range(len(output))]
    columns = []
    for num1 in range(3, len(output[0])):
        ratings = set([])
        for num2 in range(1, len(output)):
            try:
                ratings.add(int(output[num2][num1]))
            except:
                pass
        if len(ratings) == 1:
            columns.append(num1)
    for num1 in range(len(output[0])):
        for num2 in range(len(output)):
            if num1 in columns:
                pass
            else:
                new_output[num2].append(output[num2][num1])
    num_raters -= len(columns)
    for num in range(1, len(output)):
        new_output[num][1] = num_raters
    return new_output, num_raters





def inv_bias_rating(rows, num_raters):
    """
    Takes rows formatted as list of lists and calculates the majority rules inv.
    bias rating for each row of scores.
    """
    row_count = sum(1 for row in rows) - 1
    inv = [[0 for k in range(8)] for num in range(num_raters)]
    # store the annotators' names
    l = []
    for num in range(row_count):
        l.append([0 for k in range(num_raters)])
    first = True
    num1 = -1
   # print rows
    # obtaining matrix with scores alone
    summ = 0
    sum2 = 0
    summ = 0
    for row in rows:
        for num2 in range(num_raters):
            if first == True:
                first = False

            else:
                l[num1][num2] = row[num2 + 3]

        num1 += 1
    l_zipped = zip(*l)
    # number of times each rater uses each category.
    c = [[] for num in range(num_raters)]
    for num1 in range(num_raters):
        for num2 in range(8):
            c[num1].append(list(l_zipped[num1]).count(str(num2)))
    # inverse based bias correction
    for num in range(num_raters):
        for j in range(0, 8):
            try:
                inv[num][j] = float(1) / float(c[num][j])
            except ZeroDivisionError:
                inv[num][j] = 0
    scores = ["Inv. Bias-corrected Rating"]
    workers = ["Summary Rater"]
    # summing weights and determining category with maximum weight for each slice
    for num1 in range(0, row_count):
        print "num1"
        print num1
        q = [0 for num3 in range(num_raters)]
        for i in range(num_raters):

            for num2 in range(num_raters):
                print num2
                if l[num1][num2] == "N/A" or l[num1][num2] == '':
                    print "passed"
                    pass
                else:

                    print l[num1]
                   # print num2

                    print l[num1][num2]
                    q[num2] += inv[i][int(l[num1][num2])]
        if len(list_of_indices(l[num1], str(0))) >= 1:
            scores.append(str(0))
            workers.append(str(l[num1].index(str(0)) + 1))
        else:
            scores.append(l[num1][q.index(max(q))])
            workers.append(str(q.index(max(q)) + 1))
    return scores, workers

def create_empty_columns(headers, num_rows):
    """
    Given a list of headers, creates a list of lists, with each list being a column of the length
    of num_rows and the first element in each list being the header. The rest of list contains
    empty strings.
    """
    columns = [[] for header in headers]
    num = 0
    for header in headers:
        columns[num] = ['' for x in range(num_rows)]
        columns[num][0] = header
        num += 1
    return columns

def add_columns_to_rows(columns, rows):
    """
    Adds columns represented as lists to a list of lists in which each list represents a row.
    """
    # if adding just one column
    if type(columns[0]) != list:
        num = 0
        for row in rows:
            row.append(columns[num])
            num += 1
    # if adding multiple columns
    else:
        for column in columns:
            num = 0
            for row in rows:
                row.append(column[num])
                num += 1
    return rows

def order_by_slice_number(reference, rows):
    ordered = [rows[0]]
    val = 1
    reference = convert_csv_to_list(reference)
    for num in range(1, len(reference)):
        link = reference[num][1]
        for video in rows:
            if video[3] == link:
                video[0] = val
                ordered.append(video)
        val += 1
    return ordered

def convert_to_csv(rows, output_name):
    """
    Converts a list of lists with each list representing a row to a csv file.
    """
    with open(output_name, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)
    csvfile.close()

hiits = None

for num in range(len(output)):
    hiit = output[num]
    hiit, hiit_num_raters = delete_raters_with_same_ratings(hiit, num_raters[num])
    print "hiit-here"
    print hiit
    inv_bias_ratings = inv_bias_rating(hiit, hiit_num_raters)
    other_columns = create_empty_columns(["Std. Dev. Of Ratings", "Avg Rating"], sum(1 for row in hiit))
    columns_to_add = other_columns + list(inv_bias_ratings)
    hiit = add_columns_to_rows(columns_to_add, hiit)
    if hiits == None:
        hiits = hiit
    else:
        hiits += hiit
    convert_to_csv(hiit, "amt_irr" + str(num + 1) + ".csv")

def hiit_to_workers(hiits):
    hiit_to_workers = {}
    print "here0"
    for hiit in hiits:
        #print hiit
        if hiit[2] == "src":
            new_hiit = []
            for num in range(3, 8):
                if len(hiit[num]) > 1 and "Std." not in hiit[num]:
                    print "here"
                    #print hiit[num]
                    new_hiit.append(hiit[num])
                else:
                    break
        else:
           # print new_hiit
            hiit_to_workers[hiit[2]] = new_hiit
    return hiit_to_workers

def order_hiits(hiits, reference):
    new_hiits = []
    srcs = []
    for num in range(len(hiits)):
        srcs.append(hiits[num][2])
    with open(reference, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        print "start"
        num = 1
        first = True
        for row in reader:
            if row[5] == "U": ## If the usage type is "U" for "Used" (not "T" for "Training" or "M" for "Missing")
               # try:
                    new_row_index = srcs.index(row[4])
                    new_hiit = hiits[new_row_index]
                    if new_hiit[0] != "Slice num":
                        new_hiit[0] = num
                     #   print num
                        hiit_number = int(math.ceil(((new_row_index + 1) / 11.0)))
                        num_in_hiit = (new_row_index) % 11
                        new_hiit.insert(1, str(hiit_number) + "_" + str(num_in_hiit))
                        new_hiits.append(new_hiit)
                       # print new_hiits

                        num += 1
                    else:
                        pass
              #  except:
                    # print row[0]
               #     num += 1
        print "num1"
        print len(new_hiits)
    return new_hiits

def expand_hiits(hiits):
    hiit_to_workers_dict = hiit_to_workers(hiits)
   # print hiit_to_workers_dict
    print "num old hits"
    print "herere"
    new_hiits = order_hiits(hiits, "VideoNameRef_{0}.csv".format(batchNum))
    workers = set([])
    final = []
    for x in hiit_to_workers_dict:
        workers = workers.union(set(hiit_to_workers_dict[x]))
    num = 3
    for num in range(3, 8):
        if "Std." in hiits[0]:
            num += 1
            break
        else:
            num += 1
    title = [hiits[0][0]] + ["HIIT Number"] + hiits[0][1:3]+ list(workers) + hiits[0][num:]
    final.append(title)

    for num1 in range(len(new_hiits)):
        print "num hits"
        print len(new_hiits)
       # print new_hiits
        src = new_hiits[num1][3]
        print num1
        print src
        #print hiit_to_workers_dict[src]
        workers = hiit_to_workers_dict[src]
        num_workers = len(workers)
        new_hiit = ['N/A' for x in range(len(title))]
        new_hiit[0:4] = new_hiits[num1][0:4]
        new_hiit[-2:] = new_hiits[num1][-2:]
        new_hiit[-3] = ""
        print "here1"
       # print new_hiits[num1][:]
        #print num_workers
        for num2 in range(num_workers):
            index = title.index(hiit_to_workers_dict[src][num2])
            new_hiit[index] = new_hiits[num1][num2+4]
            print new_hiit[index]
        new_hiit[-1] = title.index(hiit_to_workers_dict[src][int(new_hiits[num1][-1]) - 1]) + 1 - 4
        final.append(new_hiit)
    return final

final_output = expand_hiits(hiits)
# for row in final_output:
#      print row

convert_to_csv(final_output, "{0}_results_formatted.csv".format(batchNum))  ## Change if you want a different output file name






def convert_to_csv2(rows, output_name):
    """
    Converts a list of lists with each list representing a row to a csv file.
    """
    with open(output_name, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            print(row[3:])
            writer.writerow(row[3:])
    csvfile.close()

for num in range(len(output)):

    hiit = output[num]
    hiit, hiit_num_raters = delete_raters_with_same_ratings(hiit, num_raters[num])
    if hiits == None:
        hiits = hiit
    else:
        hiits += hiit
    convert_to_csv2(hiit, "R_output_{0}/irr".format(batchNum) + str(num + 1) + ".csv")  ## Make sure you have a folder called "R_output_* (whatever you defined batchNum as above). If not, create it.