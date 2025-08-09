// Delta Flight Search API fetcher using Scrappey.com
const Scrappey = require('scrappey-wrapper');
const fs = require('fs');

// Initialize Scrappey with your API key
const scrappey = new Scrappey('CPLgrNtC9kgMlgvBpMLydXJU3wIYVhD9bvxKn0ZO8SRWPNJvpgu4Ezhwki1U');

// Default Delta GraphQL query and variables
const deltaGraphQLPayload = {
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

async function fetchDeltaFlightData(fromAirport = "MCO", toAirport = "BCN", departureDate = "2025-08-21", pageNum = 1) {
    try {
        console.log(`🛫 Fetching Delta flight data: ${fromAirport} → ${toAirport} on ${departureDate}...`);
        
        // Create session with residential proxy (US) - important for Delta
        const session = await scrappey.createSession({
            proxy: {
                country: 'US'
            }
        });
        
        console.log('✅ Scrappey session created successfully:', session.session);
        
        // Step 1: First visit Delta.com to establish session and get cookies
        console.log('🔄 Step 1: Visiting Delta.com to establish session...');
        const initialVisit = await scrappey.get({
            url: 'https://www.delta.com/',
            session: session.session,
            customHeaders: {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Ch-Ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
            }
        });
        
        console.log('✅ Initial visit successful, cookies established');
        
        // Step 2: Wait a bit to simulate human behavior
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Step 3: Update payload with user parameters
        const payload = {
            ...deltaGraphQLPayload,
            variables: {
                ...deltaGraphQLPayload.variables,
                offerSearchCriteria: {
                    ...deltaGraphQLPayload.variables.offerSearchCriteria,
                    offersCriteria: {
                        ...deltaGraphQLPayload.variables.offerSearchCriteria.offersCriteria,
                        resultsPageNum: pageNum
                    },
                    flightRequestCriteria: {
                        ...deltaGraphQLPayload.variables.offerSearchCriteria.flightRequestCriteria,
                        searchOriginDestination: [{
                            departureLocalTs: `${departureDate}T00:00:00`,
                            destinations: [{
                                airportCode: toAirport,
                                airportRadiusMileCnt: { unitOfMeasure: "MI", unitOfMeasureCnt: 100 }
                            }],
                            origins: [{
                                airportCode: fromAirport,
                                airportRadiusMileCnt: { unitOfMeasure: "MI", unitOfMeasureCnt: 100 }
                            }]
                        }]
                    }
                }
            }
        };
        
        // Step 4: Generate transaction ID (required by Delta)
        const transactionId = `${generateUUID()}_${Date.now()}`;
        
        console.log('🔄 Step 2: Making GraphQL request to Delta API...');
        
        // Step 5: Use Scrappey's sendRequest method for POST to Delta API
        const response = await scrappey.sendRequest({
            cmd: 'request.post',
            endpoint: 'request.post',
            url: 'https://offer-api-prd.delta.com/prd/rm-offer-gql',
            session: session.session,
            customHeaders: {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9",
                "Airline": "DL",
                "Applicationid": "DC",
                "Authorization": "GUEST",
                "Channelid": "DCOM",
                "Content-Type": "application/json",
                "Origin": "https://www.delta.com",
                "Priority": "u=1, i",
                "Referer": "https://www.delta.com/",
                "Sec-Ch-Ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Transactionid": transactionId,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                "X-App-Type": "shop-mach"
            },
            requestBody: JSON.stringify(payload)
        });
        
        console.log('✅ Delta GraphQL request successful');
        console.log('📊 Full response structure:', JSON.stringify(response, null, 2));
        
        // Debug the response structure
        if (response.solution) {
            console.log('📊 Solution status:', response.solution.status);
            console.log('📊 Solution responseUrl:', response.solution.responseUrl);
            console.log('📊 Solution headers:', response.solution.headers);
        }
        
        // Get the response data
        let responseData = response.solution?.response;
        if (!responseData) {
            console.log('⚠️ No response data found');
            console.log('📋 Available response keys:', Object.keys(response));
            if (response.solution) {
                console.log('📋 Solution keys:', Object.keys(response.solution));
            }
            throw new Error('No response data received from Delta API');
        }

        console.log('📊 Response data type:', typeof responseData);
        console.log('📄 Response data preview:', String(responseData).substring(0, 200) + '...');
        
        // Parse JSON response
        let jsonData;
        try {
            if (typeof responseData === 'string') {
                // Check if response is wrapped in HTML
                if (responseData.includes('<div id="resultContainer">')) {
                    console.log('🔧 Extracting JSON from HTML wrapper...');
                    
                    // Look for the JSON inside the resultContainer div
                    let match = responseData.match(/<div id="resultContainer"><div>(\{.*?\})<\/div>/s);
                    if (match && match[1]) {
                        console.log('✅ Found JSON in HTML wrapper:', match[1].substring(0, 100) + '...');
                        jsonData = JSON.parse(match[1]);
                    } else {
                        // Try broader match for nested content
                        match = responseData.match(/<div id="resultContainer">.*?(\{.*?\}).*?<\/div>/s);
                        if (match && match[1]) {
                            console.log('✅ Found JSON with broader match:', match[1].substring(0, 100) + '...');
                            jsonData = JSON.parse(match[1]);
                        } else {
                            // Try to find any JSON-like structure containing "data"
                            match = responseData.match(/(\{[^{}]*"data"[^{}]*\{.*?\}.*?\})/s);
                            if (match && match[1]) {
                                console.log('✅ Found JSON pattern:', match[1].substring(0, 100) + '...');
                                jsonData = JSON.parse(match[1]);
                            } else {
                                throw new Error('Could not extract JSON from HTML wrapper');
                            }
                        }
                    }
                } else if (responseData.trim().startsWith('{') || responseData.trim().startsWith('[')) {
                    // Try to parse as JSON directly
                    jsonData = JSON.parse(responseData);
                } else {
                    throw new Error('Response is not JSON format and has no HTML wrapper');
                }
            } else {
                // Already parsed object
                jsonData = responseData;
            }
        } catch (parseError) {
            console.log('❌ JSON Parse Error:', parseError.message);
            console.log('📄 Raw response preview:', String(responseData).substring(0, 500));
            
            // Dump raw response for debugging
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const rawFilename = `delta_raw_response_error_${timestamp}.txt`;
            fs.writeFileSync(rawFilename, String(responseData));
            console.log(`💾 Raw response saved to: ${rawFilename}`);
            
            throw new Error(`Failed to parse JSON response: ${parseError.message}`);
        }
        
        // Generate timestamp for filename
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `delta_flights_${fromAirport}_${toAirport}_${departureDate}_page${pageNum}_${timestamp}.json`;
        
        // Save the JSON response
        fs.writeFileSync(filename, JSON.stringify(jsonData, null, 2));
        console.log(`💾 Delta flight data saved to: ${filename}`);
        
        // Analyze the response
        analyzeDeltaFlightResponse(jsonData, fromAirport, toAirport, departureDate);
        
        // Also save as latest.json for easy access
        fs.writeFileSync(`delta_flights_latest.json`, JSON.stringify(jsonData, null, 2));
        console.log(`💾 Also saved as: delta_flights_latest.json`);
        
        // Destroy session to clean up
        await scrappey.destroySession(session.session);
        console.log('🧹 Session cleaned up');
        
        return jsonData;
        
    } catch (error) {
        console.error('❌ Error fetching Delta flight data:', error.message);
        throw error;
    }
}

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function analyzeDeltaFlightResponse(jsonData, fromAirport, toAirport, departureDate) {
    try {
        console.log('\n📊 Analyzing Delta flight response...');
        
        if (jsonData.data && jsonData.data.gqlSearchOffers) {
            const searchOffers = jsonData.data.gqlSearchOffers;
            
            console.log(`🛫 Flight Search: ${fromAirport} → ${toAirport} on ${departureDate}`);
            console.log(`🆔 Offer Response ID: ${searchOffers.offerResponseId || 'N/A'}`);
            
            if (searchOffers.gqlOffersSets && searchOffers.gqlOffersSets.length > 0) {
                console.log(`\n✈️ Found ${searchOffers.gqlOffersSets.length} offer sets:`);
                
                searchOffers.gqlOffersSets.forEach((offerSet, index) => {
                    console.log(`\n  📍 Offer Set ${index + 1}:`);
                    console.log(`     Origin: ${offerSet.originAirportCode || 'N/A'}`);
                    
                    if (offerSet.offers && offerSet.offers.length > 0) {
                        console.log(`     💰 ${offerSet.offers.length} offers available:`);
                        
                        offerSet.offers.forEach((offer, offerIndex) => {
                            const pricing = offer.offerPricing?.totalAmt?.currencyEquivalentPrice;
                            const miles = offer.offerPricing?.totalAmt?.milesEquivalentPrice;
                            const properties = offer.additionalOfferProperties;
                            
                            console.log(`       ${offerIndex + 1}. Price: ${pricing?.formattedCurrencyAmt || 'N/A'}`);
                            if (miles?.mileCnt) {
                                console.log(`          Miles: ${miles.mileCnt.toLocaleString()}`);
                            }
                            console.log(`          Sold Out: ${offer.soldOut ? 'Yes' : 'No'}`);
                            if (properties) {
                                console.log(`          Lowest Fare: ${properties.lowestFare ? 'Yes' : 'No'}`);
                                console.log(`          Offered: ${properties.offered ? 'Yes' : 'No'}`);
                                console.log(`          Discount Available: ${properties.discountAvailable ? 'Yes' : 'No'}`);
                            }
                        });
                    } else {
                        console.log(`     ❌ No offers found in this set`);
                    }
                });
            } else {
                console.log('❌ No offer sets found');
            }
            
            if (searchOffers.offerDataList && searchOffers.offerDataList.length > 0) {
                const offerData = searchOffers.offerDataList[0];
                if (offerData.responseProperties?.tripTypeText) {
                    console.log(`\n🎫 Trip Type: ${offerData.responseProperties.tripTypeText}`);
                }
                if (offerData.pricingOptions?.length > 0) {
                    const currency = offerData.pricingOptions[0]?.pricingOptionDetail?.currencyCode;
                    if (currency) {
                        console.log(`💱 Currency: ${currency}`);
                    }
                }
            }
        } else if (jsonData.errors) {
            console.log('❌ GraphQL errors found:');
            jsonData.errors.forEach((error, index) => {
                console.log(`  ${index + 1}. ${error.message}`);
            });
        } else {
            console.log('⚠️ Unexpected response structure');
            console.log('📋 Available keys:', Object.keys(jsonData));
        }
        
        console.log(`\n🎉 Successfully analyzed Delta flight response!`);
        
    } catch (error) {
        console.log('⚠️ Error analyzing response:', error.message);
    }
}

// Function to fetch multiple pages of results
async function fetchMultiplePages(fromAirport = "MCO", toAirport = "BCN", departureDate = "2025-08-21", maxPages = 5) {
    console.log(`🔄 Fetching multiple pages of Delta flight data (up to ${maxPages} pages)...`);
    
    const allResults = [];
    
    for (let page = 1; page <= maxPages; page++) {
        try {
            console.log(`\n⏳ Processing page ${page}/${maxPages}...`);
            const result = await fetchDeltaFlightData(fromAirport, toAirport, departureDate, page);
            allResults.push(result);
            
            // Check if there are more results
            if (result.data?.gqlSearchOffers?.gqlOffersSets?.length === 0) {
                console.log(`✅ No more results found on page ${page}, stopping.`);
                break;
            }
            
            // Wait between requests to be respectful
            if (page < maxPages) {
                await new Promise(resolve => setTimeout(resolve, 3000));
            }
            
        } catch (error) {
            console.error(`❌ Failed to fetch page ${page}:`, error.message);
            break;
        }
    }
    
    // Save combined results
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const combinedFilename = `delta_flights_combined_${fromAirport}_${toAirport}_${departureDate}_${timestamp}.json`;
    
    const combinedData = {
        searchCriteria: { fromAirport, toAirport, departureDate },
        totalPages: allResults.length,
        fetchedAt: new Date().toISOString(),
        results: allResults
    };
    
    fs.writeFileSync(combinedFilename, JSON.stringify(combinedData, null, 2));
    console.log(`\n💾 Combined results saved to: ${combinedFilename}`);
    
    return combinedData;
}

// Main execution
async function main() {
    const args = process.argv.slice(2);
    
    // Parse command line arguments
    const fromArg = args.find(arg => arg.startsWith('--from='));
    const toArg = args.find(arg => arg.startsWith('--to='));
    const dateArg = args.find(arg => arg.startsWith('--date='));
    const pageArg = args.find(arg => arg.startsWith('--page='));
    const maxPagesArg = args.find(arg => arg.startsWith('--max-pages='));
    
    const fromAirport = fromArg ? fromArg.split('=')[1] : 'MCO';
    const toAirport = toArg ? toArg.split('=')[1] : 'BCN';
    const departureDate = dateArg ? dateArg.split('=')[1] : '2025-08-21';
    const page = pageArg ? parseInt(pageArg.split('=')[1]) : 1;
    const maxPages = maxPagesArg ? parseInt(maxPagesArg.split('=')[1]) : 5;
    
    if (args.includes('--multi-page') || args.includes('-m')) {
        // Fetch multiple pages
        await fetchMultiplePages(fromAirport, toAirport, departureDate, maxPages);
    } else {
        // Single page fetch
        await fetchDeltaFlightData(fromAirport, toAirport, departureDate, page);
    }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Gracefully shutting down...');
    process.exit(0);
});

// Run the script
if (require.main === module) {
    main().catch(error => {
        console.error('💥 Fatal error:', error);
        process.exit(1);
    });
}

module.exports = { fetchDeltaFlightData, fetchMultiplePages, analyzeDeltaFlightResponse };
