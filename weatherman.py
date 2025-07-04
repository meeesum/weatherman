import sys
import os

if len(sys.argv) <= 1 or len(sys.argv) < 4:
    sys.exit("Too less arguments\n")
elif len(sys.argv) == 4 or len(sys.argv) == 5:
    flag = sys.argv[1]
    input_date = sys.argv[2]
    path = sys.argv[3]
    path = path + ' ' + sys.argv[4]
else:
    sys.exit("Too many arguments received\n")

def combine_month_and_date(month, line):
    curr_date = line[0].split("-")
    curr_date = curr_date[2]
    date = month + ' ' + curr_date
    return date

def get_month(month_no):
    month_no = int(month_no)
    if month_no == 1:
        return 'Jan'
    elif month_no == 2:
        return 'Feb'
    elif month_no == 3:
        return 'Mar'
    elif month_no == 4:
        return 'Apr'
    elif month_no == 5:
        return 'May'
    elif month_no == 6:
        return 'Jun'
    elif month_no == 7:
        return 'Jul'
    elif month_no == 8:
        return 'Aug'
    elif month_no == 9:
        return 'Sep'
    elif month_no == 10:
        return 'Oct'
    elif month_no == 11:
        return 'Nov'
    elif month_no == 12:
        return 'Dec'
    else:
        sys.exit("Invalid Month Input")
    

if flag == '-e':
    lowest_temp = {
        'temp': 100,
        'date' : ""
    }
    highest_temp = {
        'temp' : 0,
        'date' : ""
    }
    max_humid = {
        'humidity' : 0,
        'date' : ""
    }
    filenames = os.listdir(path)

    data_found = False
    for file in filenames:
        if file.__contains__(input_date):
            data_found = True
            first_non_blank_skipped = False
            with open (path + '\\'+ file, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    if not first_non_blank_skipped:
                        first_non_blank_skipped = True
                        continue

                    clean = line.lstrip()
                    if not clean or clean.startswith("<"):
                         continue

                    currentline = line.split(",")
                    if currentline[1] and int(currentline[1]) > int(highest_temp['temp']): 
                        highest_temp["temp"] = int(currentline[1])
                        # extracting the current date
                        month = currentline[0].split("-")
                        month = month[1]
                        month = get_month(month)
                        full_date = combine_month_and_date(month, currentline)
                        highest_temp["date"] = full_date
                    if currentline[3] and int(currentline[3]) < lowest_temp.get("temp"):
                        lowest_temp["temp"] = int(currentline[3])
                        # extracting the current date
                        month = currentline[0].split("-")
                        month = month[1]
                        month = get_month(month)
                        full_date = combine_month_and_date(month, currentline)
                        lowest_temp["date"] = full_date
                    if currentline[8] and int(currentline[8]) >  max_humid.get("humidity"):
                        max_humid["humidity"] = int(currentline[8])
                        # extracting the current date
                        month = currentline[0].split("-")
                        month = month[1]
                        month = get_month(month)
                        full_date = combine_month_and_date(month, currentline)
                        max_humid["date"] = full_date

    if(data_found == False):
        sys.exit("No data found for the given arguments")
        
    print(f"Highest: {highest_temp['temp']}C on {highest_temp['date']}")
    print(f"Lowest: {lowest_temp['temp']}C on {lowest_temp['date']}")
    print(f"Humid: {max_humid['humidity']}% on {max_humid['date']}")

if flag == '-a':
    highest_avg = int(0)
    lowest_avg = int(0)
    avg_humidity = int(0)
    count_highest = int(0)
    count_lowest = int(0)
    count_humidty = int(0)

    month = get_month(input_date[-1::])
    filenames = os.listdir(path)

    data_found = False
    for file in filenames:
        if file.__contains__(month) and file.__contains__(input_date[0:4:]):
            data_found = True
            first_non_blank_skipped = False
            with open(path + '//' + file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    if not first_non_blank_skipped:
                        first_non_blank_skipped = True
                        continue
                    clean = line.lstrip()
                    if not clean or clean.startswith("<"):
                         continue
                    current_line = line.split(",")
                    if current_line[1]:
                        highest_avg += int(current_line[1])
                        count_highest += 1
                    if current_line[3]:
                        lowest_avg += int(current_line[3])
                        count_lowest += 1
                    if current_line[7]:
                        avg_humidity += int(current_line[7])
                        count_humidty += 1

    if(data_found == False):
        sys.exit("No data found for the given arguments")

    print(f"Highest Average: {int(highest_avg/count_highest)}C")
    print(f"Lowest Average: {int(lowest_avg/count_lowest)}C")
    print(f"Average Humidity: {int(avg_humidity/count_humidty)}%")

if flag == '-c':
    month = get_month(input_date[-1::])
    year = input_date[0:4:]
    highest_temp_line = ""
    highest_and_lowest_temp = {
    "highest_temp" : int(0),
    "lowest_temp" : int(100),
    "date" : "",
    }
    lowest_and_highest_temp = {
        "highest_temp" : int(0),
        "lowest_temp" : int(100),
        "date" : "",
    }
    highest_and_lowest_temp['date'] = month + ' ' + year

    filenames = os.listdir(path)

    data_found = False
    for file in filenames:
        if file.__contains__(month) and file.__contains__(input_date[0:4:]):
            data_found = True
            first_non_blank_skipped = False
            with open(path + "//" + file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    if not first_non_blank_skipped:
                        first_non_blank_skipped = True
                        continue

                    clean = line.lstrip()
                    if not clean or clean.startswith("<"):
                         continue
                    
                    current_line = line.split(",")
                    if current_line[1] and int(current_line[1]) > int(highest_and_lowest_temp['highest_temp']):
                        highest_and_lowest_temp['highest_temp'] = current_line[1]
                        highest_and_lowest_temp['lowest_temp'] = current_line[3]

                    if current_line[3] and int(current_line[3]) < int(lowest_and_highest_temp['lowest_temp']):
                        lowest_and_highest_temp['lowest_temp'] = current_line[3]
                        lowest_and_highest_temp['highest_temp'] = current_line[1]
        
    if(data_found == False):
        sys.exit("No data found for the given arguments")

    print(f"{highest_and_lowest_temp['date']}")
    print(f"01 ", end=" ")
    for i in range(int(highest_and_lowest_temp['highest_temp']) + 1):
        print("+", end="")
    print(f" {highest_and_lowest_temp['highest_temp']}C")

    print("01 ", end=" ")
    for i in range (int(highest_and_lowest_temp['lowest_temp']) + 1):
        print("+", end="")
    print(f" {highest_and_lowest_temp['lowest_temp']}C")

    print(f"02 ", end=" ")
    for i in range(int(lowest_and_highest_temp['highest_temp']) + 1):
        print("+", end="")
    print(f" {lowest_and_highest_temp['highest_temp']}C")

    print("02 ", end=" ")
    for i in range (int(lowest_and_highest_temp['lowest_temp']) + 1):
        print("+", end="")
    print(f" {lowest_and_highest_temp['lowest_temp']}C")

    
                    


                    

