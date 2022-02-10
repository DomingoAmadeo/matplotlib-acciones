import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime
import os
import pandas as pd
import numpy as np

#Funciones

def inputQuantity():
    while True:
        try:
            x = int(input("Ingrese cuantas empresas desea graficar (1/2):"))
            if x not in range (1,3):
                print (msgError)
                continue
            else:
                return x
        except ValueError:
            print(msgError)
            continue

def companySelection(companiesList):
    print("Elegir de la siguiente lista de empresas:")    
    for idx, company in enumerate(companiesList):
        print(f"{idx+1}. {company}")
    
    while True:
        try:
            companyIndex = int(input(f"Seleccione una empresa via su ID numérico (1-{len(companiesList)}): "))
            if companyIndex not in range (1,len(companiesList)+1):
                print(msgError)
                continue
            else:
                return companiesList[companyIndex-1]
        except ValueError:
            print(msgError)
            continue

def inputDate(str, arg):

        year = []
        months = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

        print (f"Seleccione el {arg} de {str}:")
        
        if arg == "año":
            for i in range (2001,2021):
                year.append(i)
            for idx, number in enumerate(year):
                print(f"{idx+1}. {number}")
            dateList = year
        elif arg == "mes":
            for idx, month in enumerate(months):
                print(f"{idx+1}. {month}")
            dateList = [i for i in range (1,13)]            
        while True:
            inputDateValue = input(f"Seleccione el {arg} de {str} de operaciones (por defecto, {str} de datos):")
            if inputDateValue != "":
                try:
                    inputDateValue = int(inputDateValue)
                    
                    if inputDateValue not in range (1,len(dateList)+1):
                        print(msgError)
                        continue
                    else:
                        return dateList[inputDateValue-1]
                except ValueError:
                    print(msgError)
                    continue
            else:
                return ""

def plotFormat(defaultStart, defaultEnd):
    startingDate = str(inputDate("inicio","año")) + "-" + str(inputDate("inicio","mes")) + "-01"
    endingDate = str(inputDate("finalización","año")) + "-" + str(inputDate("finalización","mes")) + "-01"
    try:
        startFormatted = dates.date2num(datetime.strptime(startingDate,'%Y-%m-%d'))
    except ValueError:
        startFormatted = dates.date2num(datetime.strptime(defaultStart,'%Y-%m-%d'))
    try:
        endFormatted = dates.date2num(datetime.strptime(endingDate,'%Y-%m-%d'))
    except ValueError:
        endFormatted = dates.date2num(datetime.strptime(defaultEnd,'%Y-%m-%d'))
    if startFormatted > endFormatted:
        return [endFormatted, startFormatted]        
    return [startFormatted, endFormatted]

def graphPrompt():
    print("\n¿Desea graficar la informacion seleccionada? \n1. Grafico discretizado \n2. No graficar")
    while True:
        try:
            answer = int(input())
            if answer not in range (1,4):
                print(msgError)
                continue
            else:
                break
        except ValueError:
            print(msgError)
            continue
    return answer

def graphIntersections(valueListOne,dateListOne,valueListTwo,dateListTwo):
    intersection_Indexes = getIntersections(valueListOne,dateListOne,valueListTwo,dateListTwo)
    if intersection_Indexes == 0:
        return
    intersection_Values = []
    intersection_Dates = []
    for i in intersection_Indexes:
        intersection_Values.append(valueListTwo[i])
        intersection_Dates.append(dateListTwo[i])
    plt.plot(intersection_Dates, intersection_Values, 'm*', label='Intersecciones')


    datesFormatted = [(dates.num2date(i)).strftime('%Y-%m-%d') for i in intersection_Dates]
    datadict = {
        "Fechas" : datesFormatted,
        "Valores" : intersection_Values
    }

    return datadict

def getIntersections(valueOne,dateOne,valueTwo,dateTwo):
    overlappingPeriod = sorted(list(set(dateOne) & set(dateTwo)))
    if len(overlappingPeriod) < 1:
        return 0
    dateOne_Overlap = []
    dateTwo_Overlap = []
    for i in overlappingPeriod:
        dateOne_Overlap.append(dateOne.index(i))
        dateTwo_Overlap.append(dateTwo.index(i))
    count = 0
    idxs = []
    if valueOne[dateOne_Overlap[0]] < valueTwo[dateTwo_Overlap[0]]:
        count +=1
    for i in range (len(dateOne_Overlap)):
        if valueOne[dateOne_Overlap[i]] < valueTwo[dateTwo_Overlap[i]] and count%2 == 0:
            count += 1
            idxs.append(dateTwo_Overlap[i])
        elif valueOne[dateOne_Overlap[i]] > valueTwo[dateTwo_Overlap[i]] and count%2 == 1:
            count += 1
            idxs.append(dateTwo_Overlap[i])
    return idxs

def createIntersectionXLSX(intersectionDict, nameOne, nameTwo):
    nameList = [nameOne[:-4], nameTwo[:-4]]    
    nameList.sort()

    intersection_path = f'data\\intersections'
    if not os.path.exists(intersection_path):
        os.makedirs(intersection_path)

    pd.DataFrame(intersectionDict).to_excel(f"data\\intersections\\{nameList[0]}-{nameList[1]}.xlsx")

def createGrowthXLSX(endDate, companyValues, companyPeriod, companyName):
    dateRange, labels = growthPeriod(endDate)    
    sizes = valueIncrease(dateRange, companyValues, companyPeriod)
    yearly = sum(sizes)
    data = {
        "Mes" : labels + ["Anual"],
        "Crecimiento" : sizes + [yearly]
    }

    growth_path = 'data\\growth'
    if not os.path.exists(growth_path):
        os.makedirs(growth_path)

    pd.DataFrame(data).to_excel(f"data\\growth\\{companyName[:-4]}.xlsx")

def growthPeriod(endDate):
    dateToDate = dates.num2date(endDate)
    dateToString = dateToDate.strftime('%Y-%m')
    pieStartDate = dateToString
    newYear = str(int(pieStartDate[2:4])-1)
    if len(newYear) == 1:
        newYear = '0' + newYear
    pieProperStartDate = pieStartDate[:2] + newYear + pieStartDate[4:]
    pieProperEndDateFormat = dates.date2num(datetime.strptime(dateToString,'%Y-%m')) - 1
    pieProperStartDateFormat = dates.date2num(datetime.strptime(pieProperStartDate,'%Y-%m'))

    months = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    lastMonth =  months[int(dateToDate.strftime('%m')) - 2]
    reversedMonths = months[::-1]
    indexOfLastMonth = reversedMonths.index(lastMonth)
    arrangedMonths = reversedMonths[indexOfLastMonth:] + reversedMonths[:indexOfLastMonth]
    
    return [pieProperStartDateFormat,pieProperEndDateFormat], arrangedMonths

def valueIncrease(timeRange,listOfValues,listOfDays):
    periods = monthSegmentation(timeRange[1],timeRange[0], [])
    monthlyGrowth = []
    for i in periods:
        x = i[1]
        while x not in listOfDays:
            x -= 1
        firstIndex = listOfDays.index(x)
        y = i[0]
        while y not in listOfDays:
            y -= 1
        secondIndex = listOfDays.index(y)

        monthlyGrowth.append(listOfValues[firstIndex]-listOfValues[secondIndex])
    
    return monthlyGrowth

def monthSegmentation(plotDateEnd, plotDateStart, answer):
    dateToDate = dates.num2date(plotDateEnd)
    dateToString = dateToDate.strftime('%Y-%m')
    dateToPlotStartMonth = dates.date2num(datetime.strptime(dateToString,'%Y-%m'))
            
    dateToPlotEndPreviousMonth = dateToPlotStartMonth - 1
    answer += [[dateToPlotStartMonth,plotDateEnd]]
    if plotDateStart >= dateToPlotStartMonth:        
        return answer

    answer = monthSegmentation(dateToPlotEndPreviousMonth, plotDateStart, answer)
    return answer


# 

msgError = "Input inválido, ingrese un número válido"

print("Bienvenido al graficador de acciones.")

companyQuantity = inputQuantity()

dataList = os.listdir("data")
for i in dataList:
    if i[-4:] != ".csv":
        dataList.remove(i)

firstCompanyName = companySelection(dataList)
firstCompanyData = pd.read_csv(f"data\\{firstCompanyName}").to_dict("list")
firstCompanyDate = firstCompanyData['date']
firstCompanyDate_plot = [dates.date2num(datetime.strptime(firstCompanyDate[i],'%Y-%m-%d')) for i in range (len(firstCompanyDate))]
firstCompanyValue = firstCompanyData['open']

startDate = min(firstCompanyDate)
endDate = max(firstCompanyDate)
valueRange = [min(firstCompanyValue),max(firstCompanyValue)]


if companyQuantity == 2:
    dataList.remove(firstCompanyName)
    secondCompanyName = companySelection(dataList)
    secondCompanyData = pd.read_csv(f"data\\{secondCompanyName}").to_dict("list")
    secondCompanyDate = secondCompanyData['date']
    secondCompanyDate_plot = [dates.date2num(datetime.strptime(secondCompanyDate[i],'%Y-%m-%d')) for i in range (len(secondCompanyDate))]
    secondCompanyValue = secondCompanyData['open']

    startDate = min(startDate,min(secondCompanyDate))
    endDate = max(endDate,max(secondCompanyDate))
    valueRange += [min(secondCompanyValue),max(secondCompanyValue)]

graphPeriod = plotFormat(startDate, endDate)
valueRange_Plot = [min(valueRange)/10,max(valueRange)*1.1]

createGrowthXLSX(graphPeriod[1], firstCompanyValue, firstCompanyDate_plot, firstCompanyName)

if companyQuantity == 2:
    createGrowthXLSX(graphPeriod[1], secondCompanyValue, secondCompanyDate_plot, secondCompanyName)

drawGraph = graphPrompt()

if drawGraph == 1:
    plt.figure(figsize=(12, 4))
    plt.subplot(2,1,1)
    plt.plot_date(firstCompanyDate_plot, firstCompanyValue, 'g--', xdate=True, ydate=False, label=f'{firstCompanyName}'[:-4])
    if companyQuantity == 2:
        plt.plot_date(secondCompanyDate_plot, secondCompanyValue, 'b-', xdate=True, ydate=False, label=f'{secondCompanyName}'[:-4])
        intersectionDict = graphIntersections(firstCompanyValue,firstCompanyDate_plot,secondCompanyValue,secondCompanyDate_plot)   
        createIntersectionXLSX(intersectionDict,firstCompanyName,secondCompanyName)       
    plt.ylabel('Valores')
    plt.axis([graphPeriod[0], graphPeriod[1],valueRange_Plot[0],valueRange_Plot[1]])
    plt.title('Valor Acciones')
    plt.grid()
    plt.legend()

    plt.subplot(2, 3, 4)
    pieDf1 = pd.read_excel(f"data\\growth\\{firstCompanyName[:-4]}.xlsx")
    pieDf1Filtered = pieDf1[(pieDf1['Mes'] != 'Anual') & (pieDf1['Crecimiento'] > 0)]
    pieDf1Filtered = pieDf1Filtered.to_dict("list")


    labels = pieDf1Filtered['Mes']
    sizes = pieDf1Filtered['Crecimiento']
    explode = [0 for i in labels]
    explode[0] = 0.1
    explode[1] = 0.1

    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',  startangle=90, pctdistance=0.75, labeldistance=1.1, radius= 1)
    

    if companyQuantity == 2:
        pieDf2 = pd.read_excel(f"data\\growth\\{secondCompanyName[:-4]}.xlsx")
        pieDf2Filtered = pieDf2[(pieDf2['Mes'] != 'Anual') & (pieDf2['Crecimiento'] > 0)]
        pieDf2Filtered = pieDf2Filtered.to_dict("list")

        plt.subplot(2, 3, 5)

        plt.title('Comparacion de crecimiento sobre el ultimo año')

        sizeOne = pieDf1 [pieDf1['Mes'] == 'Anual']
        sizeOne= sizeOne.to_dict("records")

        sizeTwo = pieDf2 [pieDf2['Mes'] == 'Anual']
        sizeTwo= sizeTwo.to_dict("records")
        

        labels = (firstCompanyName[:-4], secondCompanyName[:-4])

        sizes = [sizeOne[0]['Crecimiento'], sizeTwo[0]['Crecimiento']] 

        for i in range (2):
            if sizes[i] < 0:
                sizes[i] = 0

        plt.pie(sizes, labels=labels, autopct='%1.01f%%',  startangle=90)


        plt.subplot(2, 3, 6)
        labels = pieDf2Filtered['Mes']
        sizes = pieDf2Filtered['Crecimiento']
        explode = [0 for i in labels]
        explode[0] = 0.1
        explode[1] = 0.1

        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',  startangle=90, pctdistance=0.75, labeldistance=1.1, radius= 1)

    plt.show()

