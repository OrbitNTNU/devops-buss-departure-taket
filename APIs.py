import requests

# enturApi gives buss information 
# takes in id and number

def enturApi(id,number):
    # query tells entur api what we want to know acc time 72100
    query = """
    query {
        stopPlace(id: "NSR:StopPlace:ID-REPLACEMENT") {
        id
        name
        estimatedCalls(timeRange: 72100, numberOfDepartures: NUMBER-REPLACEMENT) {
            realtime
            aimedArrivalTime
            aimedDepartureTime
            expectedArrivalTime
            expectedDepartureTime
            actualArrivalTime
            actualDepartureTime
            date
            forBoarding
            forAlighting
            destinationDisplay {
            frontText
            }
            quay {
            id
            }
            serviceJourney {
            journeyPattern {
                line {
                id
                name
                transportMode
                }
            }
            }
        }
        }
    }
    """

    # replaces parts of the query and the wanted id and number
    query=query.replace("ID-REPLACEMENT",str(id))
    query=query.replace("NUMBER-REPLACEMENT",str(number))

    # a map which tells the api some more information
    headers = {
        "Content-Type": "application/json",
        "ET-Client-Name": "orbit-buss-ruter-tider" 
    }

    # we send the request with a post command
    response = requests.post(
        'https://api.entur.io/journey-planner/v3/graphql',
        headers=headers,
        json={'query': query}
    )

    responsejson=response.json()

    # checks if we got a sound answer from the api
    if responsejson["data"]["stopPlace"]==None:
        return f"Forespørselen var stopPlace == null"
    elif len(responsejson["data"]["stopPlace"]["estimatedCalls"])==0:
        return f"Forespørselen ga ikke nok busstopp"
    elif response.status_code == 200:
        # if we do, we return the respons as a json format
        return(response.json())        
    else:
        # if we don't we print a warning and return false
        return f"Forespørselen feilet med statuskode {response.status_code}"