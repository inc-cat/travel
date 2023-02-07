from matplotlib import pyplot
from datetime import date, timedelta
import csv


# counter for line on csv, used for skipping
csv_count = 0
# raw info is for milage only before being converted
raw_info = []
# predefined variable to be used below for first date
first_str = None


# reads csv file, line 0 is start date, bottom line are notes
with open("travel.csv") as csv_file:
    csv_data = list(csv.reader(csv_file))
    for csv_cycle in csv_data:
        if csv_count == 5:
            break
        elif csv_count == 0:
            first_str = csv_cycle[0]
        else:
            raw_info.append(csv_cycle)
        csv_count += 1


# turning strings into numbers (float/ int)
# index: 0 is on foot, 1 is bike, 2 is motor vehicle, 3 is rail
journey_data = []
for info_cycle in raw_info:
    current_data = []
    for numbers in info_cycle:
        if "." in numbers:
            current_data.append(float(numbers))
        else:
            current_data.append(int(numbers))
    journey_data.append(current_data)

# defining start date from first line of csv
first_date = date(int(first_str[0:4]), int(first_str[4:6]), int(first_str[6:8]))

# total days and x axis points for graphs
total_days = len(journey_data[0])
x_global = [i for i in range(total_days)]

# making a list for cumulative data from the journey data
# top_value used for highest graph point on y axis
journey_cumulative = []
top_value = 0
for journey_sum in journey_data:
    current_cumulative = []
    for mode_sum in journey_sum:
        if len(current_cumulative) == 0:
            current_cumulative.append(mode_sum)
            continue
        else:
            current_cumulative.append(current_cumulative[-1] + mode_sum)
    current_cumulative = [round(num, 3) for num in current_cumulative]
    if max(current_cumulative) > top_value:
        top_value = max(current_cumulative)
    journey_cumulative.append(current_cumulative)

# x_labels contains strings for xticks, for dates on graph
# month_bound contains month bounaries as ints for indexes
x_labels = []
month_bound = []
index_count = 0
month_label = int(first_str[4:6]) - 1
for date_label in range(total_days):
    current_date = first_date + timedelta(days=date_label)

    if current_date.month != month_label:
        month_label = current_date.month
        ins_str = current_date.strftime("%b '%y")
        month_bound.append(index_count)
        x_labels.append(ins_str)
    else:
        x_labels.append("")
    index_count += 1

# global graph for cumulative data
pyplot.figure(figsize=(10, 5), dpi=150)
pyplot.xlabel("Day")
pyplot.ylabel("Toal distance (miles)")
for month_lines in month_bound:
    pyplot.axvline(x=month_lines, ymin=0, ymax=1, color="#C8C8C8")
pyplot.plot(
    x_global, journey_cumulative[0], color="#000000", label="On foot"  # marker = 'x',
)
pyplot.plot(
    x_global, journey_cumulative[1], color="#4287f5", label="Bike"  # marker = 'x',
)
pyplot.plot(
    x_global, journey_cumulative[3], color="#EE7C0E", label="Rail"  # marker = 'x',
)
pyplot.plot(
    x_global,
    journey_cumulative[2],
    color="#e00f00",  # marker = 'x',
    label="Motor Vehicle",
)

pyplot.title("Travelling")
pyplot.ylim([0, top_value + 20])
pyplot.xlim([0, total_days])
pyplot.xticks(x_global, x_labels)
pyplot.legend()
pyplot.show()


global_averages = []
for add_averages in journey_data:
    current_average = []
    temp_numbers = []
    for indi_average in add_averages:
        temp_numbers.append(indi_average)
        current_average.append(sum(temp_numbers) / len(temp_numbers))
    current_average = [round(num, 3) for num in current_average]
    global_averages.append(current_average)

mode_strings = ["On Foot", "Bike", "Motor Vehicle", "Rail"]
graph_colours = ["#000000", "#4287f5", "#EE7C0E", "#e00f00"]

for mode_index in range(4):
    pyplot.figure(figsize=(10, 5), dpi=150)
    pyplot.xlabel("Day")
    pyplot.ylabel("Toal distance (miles)")
    pyplot.plot(
        x_global, global_averages[mode_index], color="#000000", label="Overall average"
    )
    pyplot.bar(
        x_global,
        journey_data[mode_index],
        color=graph_colours[mode_index],
        label=mode_strings[mode_index],
    )
    pyplot.title("Travelling")
    # pyplot.ylim([0, top_value + 20])
    # pyplot.xlim([0, total_days])
    pyplot.xticks(x_global, x_labels)
    pyplot.legend()
    pyplot.show()

total = journey_cumulative[0][-1] + journey_cumulative[1][-1] + journey_cumulative[2][-1] + journey_cumulative[3][-1]

print(f"Miles traveled on foot: {journey_cumulative[0][-1]}")
print(f"Miles traveled by bike: {journey_cumulative[1][-1]}")
print(f"Miles traveled by motor vehicle: {journey_cumulative[2][-1]}")
print(f"Miles traveled by rail: {journey_cumulative[3][-1]}")
print(f"Total miles travelled: {total}")

