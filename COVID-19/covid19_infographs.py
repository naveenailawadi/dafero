import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

MASTER_DIR = os.getcwd()

DATASET = 'novel-corona-virus-2020-dataset'

plt.close('all')


def create_time_chart(dataframe, ylabel):
    headers = list(dataframe.columns)

    start_col = headers.index('3/15/20')

    columns = headers[start_col:]

    value_list = []
    for column in columns:
        total = sum(dataframe[column])
        value_list.append(total)

    # plot = pd.DataFrame({'Values': value_list, ylabel: columns}).plot.bar(x=ylabel, y='Values', rot=0)

    plt.plot([f"{' ' * headers.index(header)}" for header in headers[start_col:]], value_list, color='#6c3376')
    plt.xlabel(' ')
    plt.ylabel(f"{ylabel} (3/15 - 4/5)")

    plt.savefig(f"{ylabel}.pdf")
    plt.close('all')


def build_gross():
    os.chdir()

    # create a USA-based time series of confirmed cases, deaths, and recoveries
    confirmed = pd.read_csv(DATASET)
    deaths = pd.read_csv('time_series_covid_19_deaths_US.csv')

    # general recoveries
    recoveries = pd.read_csv('time_series_covid_19_recovered.csv')
    # reassign recoveries to only the us
    recoveries = recoveries[recoveries['Country/Region'] == 'US']

    os.chdir(MASTER_DIR)

    os.mkdir('Gross Amounts')

    os.chdir('Gross Amounts')

    create_time_chart(confirmed, 'Amount of Confirmed US Coronavirus Cases')
    create_time_chart(deaths, 'Amount of Confirmed US Coronavirus Deaths')
    create_time_chart(recoveries, 'Amount of Confirmed US Coronavirus Recoveries')
    os.chdir(MASTER_DIR)
    return


# do it by age
def build_age_pie():
    os.chdir(DATASET)

    open_line_df = pd.read_csv('COVID19_open_line_list.csv', header=0)

    raw_ages = open_line_df['age']

    count20 = 0
    count40 = 0
    count60 = 0
    count80 = 0
    count_more = 0

    for value in raw_ages:
        try:
            num = int(value)
        except TypeError:
            continue
        except ValueError:
            continue

        # sort the nums into boxes
        if num < 20:
            count20 += 1
        elif num <= 40:
            count40 += 1
        elif num <= 60:
            count60 += 1
        elif num <= 80:
            count80 += 1
        else:
            count_more += 1

    age_boxes = ['< 20', '21-40', '41-60', '61-80', '81+']
    sizes = [count20, count40, count60, count80, count_more]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=age_boxes, autopct='  %1.0f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')

    os.chdir(MASTER_DIR)

    plt.title('Ages of People with Confirmed Cases as of 4/5', pad=10)

    plt.savefig("Age Pie Chart.pdf")
    plt.close('all')

    return


def build_symptoms_bar():
    os.chdir(DATASET)

    # get the symptoms from the dataset
    open_line_df = pd.read_csv('COVID19_open_line_list.csv', header=0)
    symptoms_raw = list(open_line_df['symptoms'])

    # list of symptoms as listed in order
    symptoms_long = ''

    # count the patients with symptoms
    symptoms_found = 0

    for symptom in symptoms_raw:
        temp = [i.split(';') for i in str(symptom).split(',')]
        for i in temp:
            symptoms_long += f" {str(i).replace('[', '').replace(']', '')}"

        if len(str(symptom)) > 4:
            symptoms_found += 1

    symptoms_list = symptoms_long.replace("'", '').split(' ')

    symptom_dict = {}

    for i in set(symptoms_list):
        symptom_dict[i] = symptoms_list.count(i)

    pneumonitis = symptom_dict['pneumonitis'] + symptom_dict['pneumonia']
    cough = symptom_dict['cough'] + symptom_dict['coughing']
    headache = symptom_dict['headache']
    sore_throat = symptom_dict['throat']
    fever = symptom_dict['fever'] + symptom_dict['Fever']

    # create bar chart
    symptoms = ['pneumonitis', 'cough', 'headache', 'sore throat', 'fever']
    symptom_counts = [pneumonitis, cough, headache, sore_throat, fever]
    y_pos = np.arange(len(symptoms))

    plt.bar(y_pos, symptom_counts)

    plt.xticks(y_pos, symptoms)

    # set colors for bar chart

    os.chdir(MASTER_DIR)

    plt.title(f'Symptoms Recorded in Sample of {symptoms_found} patients', pad=10)

    plt.savefig("Symptoms Bar Chart.pdf")
    plt.close('all')


if __name__ == '__main__':
    build_gross()
    build_age_pie()
    build_symptoms_bar()
