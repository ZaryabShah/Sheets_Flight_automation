// Simple test to check what we actually get from Delta API
const Scrappey = require('scrappey-wrapper');

async function testDelta() {
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
        
        // Now try the API with the post method directly
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
                    }
                }
            },
            query: `query ($offerSearchCriteria: OfferSearchCriteriaInput!) {
              gqlSearchOffers(offerSearchCriteria: $offerSearchCriteria) {
                offerResponseId
              }
            }`
        };

        console.log('🔄 Testing POST to Delta API...');
        
        // Try using the post method from scrappey-wrapper
        const result = await scrappey.post({
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
                "Transactionid": "test-" + Date.now(),
                "X-App-Type": "shop-mach"
            },
            postData: JSON.stringify(payload)
        });
        
        console.log('📄 Result keys:', Object.keys(result));
        if (result.solution) {
            console.log('📄 Solution keys:', Object.keys(result.solution));
            console.log('📄 Response headers:', result.solution.responseHeaders);
            console.log('📄 Response preview:', String(result.solution.response).substring(0, 500));
        }
        
        // Clean up
        await scrappey.destroySession(session.session);
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
}

testDelta();
