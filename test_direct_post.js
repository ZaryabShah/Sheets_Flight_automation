// Test direct POST request to Delta API
const Scrappey = require('scrappey-wrapper');

async function testDirectPost() {
    const scrappey = new Scrappey('CPLgrNtC9kgMlgvBpMLydXJU3wIYVhD9bvxKn0ZO8SRWPNJvpgu4Ezhwki1U');
    
    try {
        // Create session
        const session = await scrappey.createSession({
            proxy: { country: 'US' }
        });
        console.log('✅ Session created:', session.session);
        
        // Visit Delta.com first
        await scrappey.get({
            url: 'https://www.delta.com/',
            session: session.session
        });
        console.log('✅ Delta.com visited');
        
        // Prepare the payload
        const payload = {
            variables: {
                offerSearchCriteria: {
                    productGroups: [{ productCategoryCode: "FLIGHTS" }],
                    customers: [{ passengerTypeCode: "ADT", passengerId: "1" }],
                    offersCriteria: {
                        resultsPageNum: 1,
                        pricingCriteria: { priceableIn: ["CURRENCY"] },
                        preferences: { nonStopOnly: false, refundableOnly: false },
                        flightRequestCriteria: {
                            sortByBrandId: "BE",
                            searchOriginDestination: [{
                                departureLocalTs: "2025-08-21T00:00:00",
                                destinations: [{
                                    airportCode: "BCN",
                                    airportRadiusMileCnt: { unitOfMeasure: "MI", unitOfMeasureCnt: 100 }
                                }],
                                origins: [{
                                    airportCode: "MCO",
                                    airportRadiusMileCnt: { unitOfMeasure: "MI", unitOfMeasureCnt: 100 }
                                }]
                            }]
                        }
                    },
                    flightRequestCriteria: {
                        searchOriginDestination: [{
                            departureLocalTs: "2025-08-21T00:00:00",
                            destinations: [{
                                airportCode: "BCN",
                                airportRadiusMileCnt: { unitOfMeasure: "MI", unitOfMeasureCnt: 100 }
                            }],
                            origins: [{
                                airportCode: "MCO",
                                airportRadiusMileCnt: { unitOfMeasure: "MI", unitOfMeasureCnt: 100 }
                            }]
                        }]
                    }
                }
            },
            query: `query ($offerSearchCriteria: OfferSearchCriteriaInput!) {
  gqlSearchOffers(offerSearchCriteria: $offerSearchCriteria) {
    offerResponseId
    gqlOffersSets {
      originAirportCode
      offers {
        soldOut
        offerPricing {
          totalAmt {
            currencyEquivalentPrice {
              roundedCurrencyAmt
              formattedCurrencyAmt
            }
            milesEquivalentPrice {
              mileCnt
            }
          }
        }
        additionalOfferProperties {
          lowestFare
          offered
          discountAvailable
        }
      }
    }
    offerDataList {
      flexDestinationAirportCodes
      pricingOptions {
        pricingOptionDetail {
          currencyCode
        }
      }
      responseProperties {
        tripTypeText
      }
    }
  }
}`
        };

        console.log('🔄 Making direct POST request...');
        
        // Use sendRequest directly with proper headers
        const result = await scrappey.sendRequest({
            cmd: 'request.post',
            endpoint: 'request.post',
            url: 'https://offer-api-prd.delta.com/prd/rm-offer-gql',
            session: session.session,
            customHeaders: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Airline": "DL",
                "Applicationid": "DC", 
                "Authorization": "GUEST",
                "Channelid": "DCOM",
                "Origin": "https://www.delta.com",
                "Referer": "https://www.delta.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors", 
                "Sec-Fetch-Site": "same-site",
                "Transactionid": "test-" + Date.now(),
                "X-App-Type": "shop-mach"
            },
            requestBody: JSON.stringify(payload)
        });
        
        console.log('📄 Direct POST result keys:', Object.keys(result));
        if (result.solution) {
            console.log('📄 Status code:', result.solution.statusCode);
            console.log('📄 Response headers:', result.solution.responseHeaders);
            console.log('📄 Response:', result.solution.response);
            
            // Try to parse the response
            try {
                const jsonData = JSON.parse(result.solution.response);
                console.log('✅ Successfully parsed JSON:', JSON.stringify(jsonData, null, 2));
            } catch (e) {
                console.log('❌ Failed to parse as JSON:', e.message);
            }
        }
        
        // Clean up
        await scrappey.destroySession(session.session);
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
}

testDirectPost();
