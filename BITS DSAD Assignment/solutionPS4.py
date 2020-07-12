import copy

dataFile = "inputPS4.txt"
commands = "promptsPS4.txt"
outputFile = "outputPS4.txt"

# To store the adjacency matrix
citiesTrainsAdjacencyMatrix = []  

# To store the trains relations to cities (To create Adjacency Matrix)
trainDictionary = {}

# To store list of Cities - Used for maintaining array order for adjacency matrix
citiesList = []

# To store the cities relations to trains (To create Adjacency Matrix)
citiesDictionary = {}

# Function to read input File
def readCityTrainfile():
  rawInputData = []
  data = open(dataFile, "r", encoding="utf-8")
  out = open(outputFile, "w", encoding="utf-8")

  size = 0
  
  for line in data:
    rawInputData.append(processLine(line))
    size += 1

  data.close()
  out.close()
  storeData(rawInputData)

# Function to show the summary of read data
def showAll(): 
  out = open(outputFile, "a", encoding="utf-8")
  out.write("-------- Function showAll() --------" + "\n\n\n")
  out.write("Total no. of freight trains: {0}\n".format(len(trainDictionary)))
  out.write("Total no. of cities: {0}".format(len(citiesList)) + "\n\n")
  
  # List of Trains
  out.write("List of freight trains:" + "\n\n")
  for train in trainDictionary:
    out.write(train + "\n")
  out.write("\n\n")

  # List of Cities
  out.write("List of cities:" + "\n\n")
  for city in citiesList:
    out.write(city + "\n")
  out.write("\n")

  out.write("------------------------------------" + "\n\n\n\n")
  out.close()


# Function to determine transport hub
def displayTransportHub():
  out = open(outputFile, "a", encoding="utf-8")
  mainTransportHub = ""
  listOfTrains = []
  noOfTrains = 0

  # Traverse through the Adjacency Matrix and determine city which has most number of trains
  for i, row in enumerate(citiesTrainsAdjacencyMatrix):
    tempTrainCount = 0
    tempTrainList = []
    for column in row:
      if (column != 0):
        tempTrainCount = tempTrainCount + 1
        tempTrainList.append(column)
    if tempTrainCount > noOfTrains:
      noOfTrains = tempTrainCount
      mainTransportHub = citiesList[i]
      listOfTrains = tempTrainList
    

  out.write("-------- Function displayTransportHub() --------" + "\n\n\n")
  out.write("Main transport hub: {0}\n".format(mainTransportHub))
  out.write("Number of trains visited: {0}".format(noOfTrains) + "\n\n")
  
  # List of Trains
  out.write("List of freight trains:" + "\n\n")
  for train in listOfTrains:
    out.write(train + "\n")
  out.write("\n")
  out.write("-------------------------------------------------" + "\n\n\n\n")
  out.close()


# Function to determine connected cities
def displayConnectedCities(train):
  citiesConnected = []

  # Traverse through the Adjacency Matrix and determine cities which are connected by the specified train
  for i, row in enumerate(citiesTrainsAdjacencyMatrix):
    for column in row:
      if (column != 0 and train == column):
        if (citiesList[i] not in citiesConnected):
          citiesConnected.append(citiesList[i])

  out = open(outputFile, "a", encoding="utf-8")
  out.write("-------- Function displayConnectedCities() -------" + "\n\n\n")
  out.write("Freight train number: {0}\n".format(train))
  out.write("Number of cities connected: {0}".format(len(citiesConnected)) + "\n\n")

  # List of cities
  out.write("List of cities connected directly by {0}:".format(train))
  if len(citiesConnected) > 0:
    out.write("\n\n")
    for city in citiesConnected:
      out.write(city + "\n")
    out.write("\n\n")
  else:
    out.write("No cities connected by train {0}\n\n".format(train))
  out.write("-------------------------------------------------" + "\n\n\n\n")
  out.close()


# Function to determine direct train between 2 cities
def displayDirectTrain(cityA, cityB):
  out = open(outputFile, "a", encoding="utf-8")
  result = "No. There is no direct train between provided cities"
  directTrainFound = False

  out.write("-------- Function displayDirectTrain(cityA, cityB) -------" + "\n\n\n")
  out.write("City A: {0}\n".format(cityA))
  out.write("City B: {0}".format(cityB) + "\n\n")
  
  # Traverse through the Adjacency Matrix and determine cities which are connected by the specified train
  # First determine if the cities are adjacent. 
  #   If yes, directly return the connecting train
  #   Else, find common train (via Intersection) between rows of adjacency matrix for the provided cities.
  if (cityA in citiesList) and (cityB in citiesList):
    trainNumber = findTrainBetweenAdjacentCities(cityA, cityB)
    if (trainNumber in trainDictionary):
      result = "Yes, " + trainNumber
    else:
      trainsPassingByCityA = set(citiesTrainsAdjacencyMatrix[citiesList.index(cityA)])
      trainsPassingByCityB = set(citiesTrainsAdjacencyMatrix[citiesList.index(cityB)])
      commonTrains = trainsPassingByCityA.intersection(trainsPassingByCityB)
      commonTrains.discard(0)
      if (len(commonTrains) > 0):
        result = "Yes, "
        for i, train in enumerate(commonTrains):
          result = result + train
          if i == len(commonTrains):
            result = result + ", "
  
  out.write("Package can be sent directly: {0}".format(result)  + "\n\n")
  out.write("-------------------------------------------------" + "\n\n\n\n")
  out.close()


# Function to determine direct train between 2 cities
def findServiceAvailable(cityA, cityB):
  out = open(outputFile, "a", encoding="utf-8")
  result = "No. There is no service available between provided cities"
  connectionList = []

  out.write("-------- Function findServiceAvailable(cityA, cityB) -------" + "\n\n\n")
  out.write("City A: {0}".format(cityA) + "\n")
  out.write("City B: {0}".format(cityB) + "\n\n")
  
  if (cityA in citiesList) and (cityB in citiesList):
    # Call Recursive function findAllConnectingCities to get all the paths.
    connectingCities = findAllConnectingCities(cityA, cityB)
    for i, city in enumerate(connectingCities):
      connectionList.append(city)
      if (i < len(connectingCities) - 1):
        connectionList.append(" > ")
        # Call findTrainBetweenAdjacentCities to get train between 2 adjacent stations.
        connectionList.append(findTrainBetweenAdjacentCities(connectingCities[i], connectingCities[i+1]))
        connectionList.append(" > ")

    if (len(connectionList) > 0):
      result = "Yes, "
      for item in connectionList:
        result = result + item

  out.write("Can the package be sent: {0}".format(result) + "\n\n")
  out.write("-------------------------------------------------" + "\n\n\n\n")
  out.close()


# Recursive DFS function which traverses through the connections and finds a connecting path between two stations
def findAllConnectingCities(startCity, endCity, cities=[]):
  
  if startCity not in citiesList:
    return None

  allRoutes = []
  cities = cities + [startCity]

  if startCity == endCity:
    return cities
 
  startCityIndex = citiesList.index(startCity)
  for i, train in enumerate(citiesTrainsAdjacencyMatrix[startCityIndex]):
    if train != 0:
      city = citiesList[i]
      if (city not in cities):
        newRoutes = findAllConnectingCities(city, endCity, cities)
        for route in newRoutes:
          allRoutes.append(route)

  return allRoutes

# Function to find train between 2 adjacent stations via Adjacency Matrix
def findTrainBetweenAdjacentCities(cityA, cityB):
  return citiesTrainsAdjacencyMatrix[citiesList.index(cityA)][citiesList.index(cityB)]
  
# Function to clean and process the input file records
def processLine(line):
  cleanedRecord = []
  tempRecord = line.replace("\n", "").split("/")
  for record in tempRecord:
    cleanedRecord.append(record.strip())
  return cleanedRecord

# Function to store data in AdjacencyMatrix format
def storeData(cleanedData):
  tempMatrix = []
  for record in cleanedData:
    trainDictionary[record[0]] = record[1:len(record)]

    for i, v in enumerate(record):
      if (i != 0):
        if v not in citiesDictionary:
          citiesDictionary[v] = []        
          citiesList.append(v)
          tempMatrix.append(0)
        citiesDictionary[v].append(record[0])

  for i in citiesList:
    citiesTrainsAdjacencyMatrix.append(copy.deepcopy(tempMatrix))

  for trainNumber in trainDictionary:
    cities = trainDictionary[trainNumber]
    previousCity = ''
    for i, city in enumerate(cities):
      noOfCities = len(cities)
      if (i != 0):
        city1 = previousCity
        city2 = city
        if (previousCity!='' and city1 != city2):
          citiesTrainsAdjacencyMatrix[citiesList.index(city1)][citiesList.index(city2)] = trainNumber
          citiesTrainsAdjacencyMatrix[citiesList.index(city2)][citiesList.index(city1)] = trainNumber
      previousCity = city

# Function to print AdjacencyMatrix for debugging purposes
def printcitiesTrainsAdjacencyMatrix():
  for row in citiesTrainsAdjacencyMatrix:
    for column in row:
      if (column == 0):
        print(column + "\t")
      else: print(column +  "\t")
      print()
    print()


# Read input file and store all data. Also create new output file
readCityTrainfile()

# Write the read data into the output file
showAll()

# read command file
cmdfile = open(commands, "r")

for instruction in cmdfile:
    fields = instruction.split(':')
    
    if  fields[0] == 'searchTransportHub' :
        displayTransportHub()
    elif fields[0] == 'searchTrain' :
        displayConnectedCities(fields[1].strip())
    elif fields[0] == 'searchCities' :
        displayDirectTrain(fields[1].strip(),fields[2].strip())
    elif fields[0] == 'ServiceAvailability' :
        findServiceAvailable(fields[1].strip(),fields[2].strip())
    else:
            f = open(outputFile, "a")
            f.write("\n-------- Valid command list --------\n")
            f.write("searchTransportHub:\n")
            f.write("searchTrain:< train number>\n")
            f.write("searchCities:<city a>:<city b>\n")
            f.write("ServiceAvailability:<city a>:<city b>\n")
           
            f.close()

cmdfile.close()