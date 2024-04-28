import sys
import math
import json, operator

def distanceCalculator(latitude1,longitude1,latitude2, longitude2):
    return math.sqrt(((latitude1-latitude2)**2) + ((longitude1-longitude2)**2))


def averageAge(json_data):

    sumAge = 0
    
    for i in json_data:
        sumAge+= i['age']
    
    average = sumAge // len(json_data)

    return average

def averageDistance(longitude1,latitude1, json_data):
    
    sumDistance = 0
    
    for i in json_data:
        longitude2=i['location']['longitude']
        latitude2=i['location']['latitude']

        sumDistance+= distanceCalculator(longitude1,latitude1,longitude2,latitude2)
    
    average = sumDistance / len(json_data)

    return average

def averageAcceptedOffers(json_data):

    sumAcepOffers = 0
    
    for i in json_data:
        sumAcepOffers+= i['accepted_offers']
    
    average = sumAcepOffers // len(json_data)

    return average


def averageCancelledOffers(json_data):
    
    sumCanOffers = 0
    
    for i in json_data:
        sumCanOffers+= i['canceled_offers']
    
    average = sumCanOffers // len(json_data)

    return average


def averageReplyTime(json_data):
    
    sumReplyTime = 0
    
    for i in json_data:
        sumReplyTime+= i['average_reply_time']
    
    average = sumReplyTime / len(json_data)

    return average




def weightAge(age,average):
    if age <= average:
        return 0.1
    else:
        finalWeight = (average/age)*0.1
    return finalWeight

def weightDistance(latitudeOffice,longitudeOffice,latitudeClient,longitudeClient,average):
    
    distanceClient = distanceCalculator(latitudeOffice,longitudeOffice,latitudeClient,longitudeClient)
    if distanceClient <= average:
        return 0.1
    else:
        finalWeight = (average/distanceClient)*0.1
        return finalWeight

def weightAcceptedOffers(acceptedOffers,average):
    if acceptedOffers >= average:
        return 0.3
    else:
        finalWeight = (acceptedOffers/average)*0.3
        return finalWeight

def weightCancelledOffers(cancelledOffers,average):
    
    if cancelledOffers <= average:
        return 0.3
    else:
        finalWeight = (average/cancelledOffers)*0.3
        return finalWeight

def weightReplyTime(replyTime,average):
    
    if replyTime <= replyTime:
        return 0.2
    else:
        finalWeight = (average/replyTime)*0.2
        return finalWeight



def priorityClients(collectionData, beginningAverageOffers):
    
    divitionClients = 2

    listaRetorno = []

    while True:

        for i in collectionData:

            acceptedOffers = i['accepted_offers']
            cancelledOffers = i['canceled_offers']
            clientOffers = acceptedOffers + cancelledOffers

            if (clientOffers < (initialAverageOffers/divitionClients)):

                listaRetorno.append(i)
        
        if (len(listaRetorno) < 10):
            break
        
        else:
            
            listaRetorno = []
            divitionClients = divitionClients*2

    return listaRetorno
        




if (len(sys.argv)!= 3):
    print("Escriba los parametros de la localizacion de Fixat's ")
else:

    json_data_inicial = ""

    listaSalida =[]

    with open("taxpayers.json") as json_file:
        json_data_inicial = json.load(json_file)

    dataAverageAgeClient = averageAge(json_data_inicial)
    dataAverageDistanceClient = averageDistance(float(sys.argv[2]),float(sys.argv[1]), json_data_inicial)
    dataAverageAcceptedOffersClient = averageAcceptedOffers(json_data_inicial)
    dataAverageCancelledOffersClient = averageCancelledOffers(json_data_inicial)
    dataAverageReplyTimeClient  = averageReplyTime(json_data_inicial)


    json_data_with_score = []

    for i in json_data_inicial:
        client = i
        weightAgeClient = weightAge(client['age'],dataAverageAgeClient)
        weightDistanceClient = weightDistance(float(sys.argv[2]),float(sys.argv[1]),client['location']['latitude'],client['location']['longitude'],dataAverageDistanceClient)
        weightAcceptedOffersClient = weightAcceptedOffers(client['accepted_offers'],dataAverageAcceptedOffersClient)
        weightCancelledOffersClient = weightCancelledOffers(client['canceled_offers'],dataAverageCancelledOffersClient)
        weightReplyTimeClient = weightReplyTime(client['average_reply_time'],dataAverageReplyTimeClient)
        finalWeight = weightAgeClient + weightDistanceClient + weightAcceptedOffersClient + weightCancelledOffersClient + weightReplyTimeClient
        score = 10 * finalWeight
        client['score'] = round(score)
        json_data_with_score.append(client)
    
    json_data_with_score.sort(key=operator.itemgetter('score'))

    initialAverageOffers = averageAcceptedOffers(json_data_inicial) + averageCancelledOffers(json_data_inicial)

    listaPriority = priorityClients(json_data_with_score, initialAverageOffers)

    elementosFaltantes = 10 - len(listaPriority)

    listaFaltantes = []

    for i in range(1,elementosFaltantes+1):
        listaFaltantes.append(json_data_with_score[-i])
    
    listaSalida = listaPriority + listaFaltantes

    print(json.dumps(listaSalida, indent=2))

    
    


    
