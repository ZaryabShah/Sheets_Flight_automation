// GraphQL API fetcher for Stake.com provider data
const Scrappey = require('scrappey-wrapper');
const fs = require('fs');

// Initialize Scrappey with your API key
const scrappey = new Scrappey('kUo6cgMMLdDHy3r1zMTiX5TqUME9IHVcPalRfRlKK8qk94Mq8Rd7rctXIARY');

// GraphQL query and variables
const graphqlPayload = {
    query: `query SlugKuratorGroup($slug: String!, $limit: Int!, $offset: Int!, $showGames: Boolean = true, $sort: GameKuratorGroupGameSortEnum = popular, $showProviders: Boolean = false, $filterIds: [String!], $isActivePlayersFeatureFlagOn: Boolean = false, $language: LanguageEnum = en) {
  slugKuratorGroup(slug: $slug) {
    ...GameKuratorGroup
    gameCount(filterIds: $filterIds, language: $language)
    groupGamesList(
      limit: $limit
      offset: $offset
      sort: $sort
      filterIds: $filterIds
      language: $language
    ) @include(if: $showGames) {
      ...GameKuratorGroupGame
      game {
        playerCount @include(if: $isActivePlayersFeatureFlagOn)
      }
    }
    filtersProvider: filters(type: provider) @include(if: $showProviders) {
      count
      group {
        id
        translation
        gameCount
      }
    }
  }
}

fragment GameKuratorGroup on GameKuratorGroup {
  id
  slug
  translation
  icon
  type
}

fragment GameKuratorGroupGame on GameKuratorGroupGame {
  id
  game {
    ...GameCardKuratorGame
  }
}

fragment GameCardKuratorGame on GameKuratorGame {
  id
  name
  slug
  thumbnailUrl
  thumbnailBlurHash
  isBlocked
  isWidgetEnabled
  groupGames {
    group {
      translation
      type
      id
      slug
    }
  }
}`,
    variables: {
        slug: "pragmatic-play",
        sort: "userCount",
        filterIds: null,
        limit: 39,
        isActivePlayersFeatureFlagOn: true,
        offset: 39
    }
};

async function fetchProviderDataGraphQL(providerSlug = "pragmatic-play", limit = 39, offset = 0) {
    try {
        console.log(`🚀 Fetching ${providerSlug} data via GraphQL API...`);
        
        // Create session with residential proxy (US)
        const session = await scrappey.createSession({
            proxy: {
                country: 'US'
            }
        });
        
        console.log('✅ Session created successfully:', session.session);
        
        // Update variables with user input
        const payload = {
            ...graphqlPayload,
            variables: {
                ...graphqlPayload.variables,
                slug: providerSlug,
                limit: limit,
                offset: offset
            }
        };
        
        // Make POST request to GraphQL API
        const response = await scrappey.post({
            url: 'https://stake.com/_api/graphql',
            session: session.session,
            postData: JSON.stringify(payload),
            customHeaders: {
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Origin': 'https://stake.com',
                'Referer': `https://stake.com/casino/group/${providerSlug}`,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
                'x-language': 'en',
                'x-operation-name': 'SlugKuratorGroup',
                'x-operation-type': 'query'
            }
        });
        
        console.log('✅ GraphQL request successful');
        console.log('📊 Response status:', response.status);
        
        // Check the actual response structure and log for debugging
        console.log('📋 Full response structure:', Object.keys(response));
        console.log('📄 Raw response preview:', JSON.stringify(response).substring(0, 500) + '...');
        
        let responseData;
        if (response.solution && response.solution.response) {
            responseData = response.solution.response;
        } else if (response.response) {
            responseData = response.response;
        } else if (response.data) {
            responseData = response.data;
        } else if (response.content) {
            responseData = response.content;
        } else {
            console.log('❌ Could not find response data in any expected field');
            console.log('📋 Available keys:', Object.keys(response));
            throw new Error('Could not find response data');
        }
        
        console.log('📊 Response data type:', typeof responseData);
        console.log('📄 Response data preview:', String(responseData).substring(0, 200) + '...');
        
        // Parse JSON response with error handling
        let jsonData;
        try {
            if (typeof responseData === 'string') {
                // Check if response is wrapped in HTML
                if (responseData.includes('<div id="resultContainer">')) {
                    console.log('🔧 Extracting JSON from HTML wrapper...');
                    
                    // Try multiple extraction patterns
                    let jsonString = null;
                    
                    // Pattern 1: Look for JSON between div tags (more flexible)
                    let match = responseData.match(/<div id="resultContainer"><div>({.*?})<\/div>/s);
                    if (match && match[1]) {
                        jsonString = match[1];
                    } else {
                        // Pattern 2: Look for any JSON object in the response
                        match = responseData.match(/({.*})/s);
                        if (match && match[1]) {
                            jsonString = match[1];
                        } else {
                            // Pattern 3: Extract everything between the first { and last }
                            const firstBrace = responseData.indexOf('{');
                            const lastBrace = responseData.lastIndexOf('}');
                            if (firstBrace !== -1 && lastBrace !== -1 && firstBrace < lastBrace) {
                                jsonString = responseData.substring(firstBrace, lastBrace + 1);
                            }
                        }
                    }
                    
                    if (jsonString) {
                        console.log('✅ Successfully extracted JSON from HTML');
                        console.log('📄 JSON preview:', jsonString.substring(0, 200) + '...');
                        jsonData = JSON.parse(jsonString);
                    } else {
                        console.log('❌ Could not extract JSON from HTML wrapper');
                        console.log('💾 Dumping full raw response to file...');
                        
                        // Generate timestamp for filename
                        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
                        const rawFilename = `stake_raw_response_${timestamp}.txt`;
                        
                        // Save the raw response
                        fs.writeFileSync(rawFilename, responseData);
                        console.log(`💾 Raw response saved to: ${rawFilename}`);
                        
                        throw new Error('Could not extract JSON from HTML wrapper');
                    }
                } else if (responseData.trim().startsWith('{') || responseData.trim().startsWith('[')) {
                    // Direct JSON response
                    jsonData = JSON.parse(responseData);
                } else {
                    console.log('❌ Response is not JSON format');
                    console.log('� Dumping full raw response to file...');
                    
                    // Generate timestamp for filename
                    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
                    const rawFilename = `stake_raw_response_${timestamp}.txt`;
                    
                    // Save the raw response
                    fs.writeFileSync(rawFilename, responseData);
                    console.log(`💾 Raw response saved to: ${rawFilename}`);
                    console.log('�📄 Raw response preview:', responseData.substring(0, 1000));
                    
                    throw new Error('Response is not valid JSON');
                }
            } else {
                jsonData = responseData;
            }
        } catch (parseError) {
            console.log('❌ JSON Parse Error:', parseError.message);
            
            // Always dump the raw response when there's a parse error
            console.log('� Dumping full raw response to file due to parse error...');
            
            // Generate timestamp for filename
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const rawFilename = `stake_raw_response_error_${timestamp}.txt`;
            
            // Save the raw response
            fs.writeFileSync(rawFilename, String(responseData));
            console.log(`💾 Raw response saved to: ${rawFilename}`);
            console.log('�📄 Raw response data preview:', String(responseData).substring(0, 1000));
            
            throw new Error(`Failed to parse JSON response: ${parseError.message}`);
        }
        
        console.log('📏 Response data keys:', Object.keys(jsonData));
        
        // Generate timestamp for filename
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `stake_${providerSlug}_graphql_${timestamp}.json`;
        
        // Save the JSON response
        fs.writeFileSync(filename, JSON.stringify(jsonData, null, 2));
        console.log(`💾 GraphQL response saved to: ${filename}`);
        
        // Analyze the GraphQL response
        analyzeGraphQLResponse(jsonData, providerSlug);
        
        // Also save as latest.json for easy access
        fs.writeFileSync(`stake_${providerSlug}_latest.json`, JSON.stringify(jsonData, null, 2));
        console.log(`💾 Also saved as: stake_${providerSlug}_latest.json`);
        
        // Destroy session to clean up
        await scrappey.destroySession(session.session);
        console.log('🧹 Session cleaned up');
        
        return jsonData;
        
    } catch (error) {
        console.error('❌ Error fetching GraphQL data:', error.message);
        throw error;
    }
}

function analyzeGraphQLResponse(jsonData, providerSlug) {
    try {
        console.log('\n📊 Analyzing GraphQL response...');
        
        if (jsonData.data && jsonData.data.slugKuratorGroup) {
            const group = jsonData.data.slugKuratorGroup;
            
            console.log(`🏢 Provider: ${group.translation || group.slug}`);
            console.log(`🎮 Total games: ${group.gameCount || 'Unknown'}`);
            console.log(`🆔 Group ID: ${group.id}`);
            console.log(`🔗 Slug: ${group.slug}`);
            console.log(`📂 Type: ${group.type}`);
            
            if (group.groupGamesList && group.groupGamesList.length > 0) {
                console.log(`\n🎯 Found ${group.groupGamesList.length} games in this batch:`);
                
                group.groupGamesList.forEach((gameItem, index) => {
                    const game = gameItem.game;
                    console.log(`  ${index + 1}. ${game.name} (${game.slug})`);
                    if (game.playerCount !== undefined) {
                        console.log(`     👥 Players: ${game.playerCount}`);
                    }
                });
            }
            
            if (group.filtersProvider && group.filtersProvider.group) {
                console.log(`\n🏭 Available providers: ${group.filtersProvider.group.length}`);
                group.filtersProvider.group.forEach((provider, index) => {
                    console.log(`  ${index + 1}. ${provider.translation} (${provider.gameCount} games)`);
                });
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
        
        console.log(`\n🎉 Successfully analyzed ${providerSlug} GraphQL response!`);
        
    } catch (error) {
        console.log('⚠️ Error analyzing response:', error.message);
    }
}

// Function to fetch all providers
async function fetchAllProviders() {
    const commonProviders = [
        'pragmatic-play',
        'evolution',
        'netent',
        'play-n-go',
        'microgaming',
        'big-time-gaming',
        'yggdrasil',
        'red-tiger',
        'push-gaming',
        'hacksaw-gaming'
    ];
    
    console.log('🚀 Fetching data for all major providers...');
    
    for (const provider of commonProviders) {
        try {
            console.log(`\n⏳ Processing ${provider}...`);
            await fetchProviderDataGraphQL(provider, 50, 0);
            
            // Wait a bit between requests to be respectful
            await new Promise(resolve => setTimeout(resolve, 2000));
            
        } catch (error) {
            console.error(`❌ Failed to fetch ${provider}:`, error.message);
            continue;
        }
    }
    
    console.log('\n🎉 Finished fetching all providers!');
}

// Function for continuous monitoring
async function continuousMonitoring(providerSlug, intervalMinutes = 30) {
    console.log(`🔄 Starting continuous monitoring for ${providerSlug} every ${intervalMinutes} minutes...`);
    
    // Fetch immediately on start
    await fetchProviderDataGraphQL(providerSlug);
    
    // Set up interval for continuous fetching
    setInterval(async () => {
        console.log(`\n⏰ Scheduled fetch for ${providerSlug} starting...`);
        try {
            await fetchProviderDataGraphQL(providerSlug);
        } catch (error) {
            console.error('❌ Scheduled fetch failed:', error.message);
        }
    }, intervalMinutes * 60 * 1000);
}

// Main execution
async function main() {
    const args = process.argv.slice(2);
    
    // Parse command line arguments
    const providerArg = args.find(arg => arg.startsWith('--provider='));
    const limitArg = args.find(arg => arg.startsWith('--limit='));
    const offsetArg = args.find(arg => arg.startsWith('--offset='));
    const intervalArg = args.find(arg => arg.startsWith('--interval='));
    
    const provider = providerArg ? providerArg.split('=')[1] : 'pragmatic-play';
    const limit = limitArg ? parseInt(limitArg.split('=')[1]) : 39;
    const offset = offsetArg ? parseInt(offsetArg.split('=')[1]) : 0;
    const interval = intervalArg ? parseInt(intervalArg.split('=')[1]) : 30;
    
    if (args.includes('--all')) {
        // Fetch all providers
        await fetchAllProviders();
    } else if (args.includes('--continuous') || args.includes('-c')) {
        // Continuous monitoring
        await continuousMonitoring(provider, interval);
    } else {
        // Single fetch
        await fetchProviderDataGraphQL(provider, limit, offset);
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

module.exports = { fetchProviderDataGraphQL, fetchAllProviders, continuousMonitoring };
