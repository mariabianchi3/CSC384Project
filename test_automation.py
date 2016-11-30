###############################################################################
#	TEST AUTOMATION															  #
###############################################################################

#################################
#          Imports              #
#################################
#TODO: If we want to use this module then check that all necessary imports are
#      placed here!

#Generate random place types
def generateRandomPlaceTypes(numOfTypes):
	placeTypes = []
	for i in range(0, numOfTypes):
		placeTypes.append(generateRandomName(-1, True))
	return placeTypes



#Generate a list of random location names
def generateRandomLocationNames(numOfNames):
	locationNames = []
	for i in range(0, numOfNames):
		locationNames.append(generateRandomName(-1, False, True))
	return locationNames



#Generate a list of Place objects without descriptions from input list of strings
def generatePlaces(placeStrings):
	listOfPlaces = []
	for placeType in placeStrings:
		#Make the place code the first letter of the placeType string
		listOfPlaces.append(Place(placeType, placeType[0]))
	return listOfPlaces



#Generate a list of Location objects
def generateLocations(placeList, listOfNames):
	listOfLocations = []
	for name in listOfNames:
		place = random.randrange(0, len(placeList))
		listOfLocations.append(Location(name, placeList[place]))
	return listOfLocations


#Build a Place table where key isPlace object, and values are associated Location objects
def buildPlaceTable(db, locationList):
	db.createTable("Places", "Place", ["Place", "Location"])
	placeTable = db.tables["Places"]
	
	for location in locationList:
		placeTable.addValToKey(Place(location.pType, location.pCode, location.pDesc), location)
	

#Generate a list of POI objects from a placeTable
def generateRandomPOIs(placeTable, numOfPOIs, mapSize):
	i = 0
	pois = []
	usedPositions = []
	while i < numOfPOIs:
		x = y = None
		place = None
		name = None
		pos = None
		while (x == None and y == None) or pos in usedPositions:
			x = random.randrange(0, mapSize)
			y = random.randrange(0, mapSize)
			pos = Point(x, y)
		
		usedPositions.append(pos)
		
		while place is None:
			place = random.choice(list(placeTable.data.keys()))
			location = random.choice(list(placeTable.data[place]))
		
		pois.append(POI(location, pos))
		i += 1
	#print(pois)
	#print(usedPositions)
	#print(set(pois))
	return list(set(pois)) 

#TODO: Name not passed in? Not good.
#Build the POI Table from a list of POIs
def buildPOITable(db, poiList):
	db.createTable("poiTab", "Location Code", ["Location Code", "POI"])
	poiTab = db.tables["poiTab"]
	for poi in poiList:
		poiTab.addValToKey(poi.location.pCode, poi)

#Randomly generate a path: list of location types
def generateRandomPath(DB, poiTable):
	print("IN PATH GENERATION")
	print(poiTable)
	locTypes = list(poiTable.data.keys())
	print("ALL LOCATION TYPES: " + str(locTypes))
	numOfLocs = random.randrange(2, len(locTypes))
	
	path = []
	for loc in range(0, numOfLocs):
		locIndx = random.randrange(0, len(locTypes))
		print(locTypes[locIndx])
		path.append(locTypes[locIndx])
	return path

