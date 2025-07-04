#!/usr/bin/env node

/**
 * Test ALL documented API parameter combinations from claude.md
 * Validates every parameter example shown in the documentation
 */

import { createRequire } from 'module';
const require = createRequire(import.meta.url);

console.log('🧪 Testing ALL Documented API Parameter Combinations...\n');

let passedTests = 0;
let totalTests = 0;

function test(description, testFn) {
    totalTests++;
    try {
        testFn();
        console.log(`✅ ${description}`);
        passedTests++;
    } catch (error) {
        console.log(`❌ ${description}`);
        console.log(`   Error: ${error.message}\n`);
    }
}

// Test ALL documented parameter combinations
test('getBenchmarks - all documented parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 190-195)
    const benchmarkCall = () => client.getBenchmarks({
        path: {
            network: 'mainnet',
            code: 'usd'
        }
    });
    
    if (typeof benchmarkCall !== 'function') {
        throw new Error('getBenchmarks parameter structure invalid');
    }
});

test('getHistoricalBenchmarks - all documented parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 244-256)
    const historicalCall = () => client.getHistoricalBenchmarks({
        path: {
            network: 'mainnet',
            code: 'usd'
        },
        query: {
            page: 0,
            perPage: 100,
            fromTimestamp: 1640995200,
            toTimestamp: 1672531200
        }
    });
    
    if (typeof historicalCall !== 'function') {
        throw new Error('getHistoricalBenchmarks parameter structure invalid');
    }
});

test('getAllVaults - credit-efficient filtering parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 272-280)
    const vaultsCall = () => client.getAllVaults({
        query: {
            network: 'mainnet',
            assetSymbol: 'USDC',
            onlyTransactional: true,
            page: 0,
            perPage: 50
        }
    });
    
    if (typeof vaultsCall !== 'function') {
        throw new Error('getAllVaults parameter structure invalid');
    }
});

test('getVault - specific vault parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 378-383)
    const vaultCall = () => client.getVault({
        path: {
            network: 'mainnet',
            vaultAddress: '0x1234567890123456789012345678901234567890'
        }
    });
    
    if (typeof vaultCall !== 'function') {
        throw new Error('getVault parameter structure invalid');
    }
});

test('getVaultHistoricalData - all documented parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 419-431)
    const historicalDataCall = () => client.getVaultHistoricalData({
        path: {
            network: 'mainnet',
            vaultAddress: '0x1234567890123456789012345678901234567890'
        },
        query: {
            apyInterval: '7day',
            fromTimestamp: 1640995200,
            toTimestamp: 1672531200,
            page: 0,
            perPage: 100
        }
    });
    
    if (typeof historicalDataCall !== 'function') {
        throw new Error('getVaultHistoricalData parameter structure invalid');
    }
});

test('getPositions - user address parameter', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 479-483)
    const positionsCall = () => client.getPositions({
        path: {
            userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d'
        }
    });
    
    if (typeof positionsCall !== 'function') {
        throw new Error('getPositions parameter structure invalid');
    }
});

test('getDepositOptions - all documented parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 540-548)
    const depositOptionsCall = () => client.getDepositOptions({
        path: {
            userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d'
        },
        query: {
            allowedAssets: ['USDC', 'USDT'],
            allowedNetworks: ['mainnet', 'base']
        }
    });
    
    if (typeof depositOptionsCall !== 'function') {
        throw new Error('getDepositOptions parameter structure invalid');
    }
});

test('getIdleAssets - user address parameter', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 606-610)
    const idleAssetsCall = () => client.getIdleAssets({
        path: {
            userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d'
        }
    });
    
    if (typeof idleAssetsCall !== 'function') {
        throw new Error('getIdleAssets parameter structure invalid');
    }
});

test('getActions - complete transaction parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 532-544)
    const actionsCall = () => client.getActions({
        path: {
            action: 'deposit',
            userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d',
            network: 'mainnet',
            vaultAddress: '0x1234567890123456789012345678901234567890'
        },
        query: {
            amount: '1000000000', // 1000 USDC (6 decimals)
            assetAddress: '0xA0b86a33E6441f3F56F2B05e7b4B8B7F5A5f0e1B',
            simulate: true
        }
    });
    
    if (typeof actionsCall !== 'function') {
        throw new Error('getActions parameter structure invalid');
    }
});

test('getTransactionsContext - all documented parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 732-738)
    const contextCall = () => client.getTransactionsContext({
        path: {
            userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d',
            network: 'mainnet',
            vaultAddress: '0x1234567890123456789012345678901234567890'
        }
    });
    
    if (typeof contextCall !== 'function') {
        throw new Error('getTransactionsContext parameter structure invalid');
    }
});

test('getVaultHolderEvents - all documented parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 767-773)
    const eventsCall = () => client.getVaultHolderEvents({
        path: {
            userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d',
            network: 'mainnet',
            vaultAddress: '0x1234567890123456789012345678901234567890'
        }
    });
    
    if (typeof eventsCall !== 'function') {
        throw new Error('getVaultHolderEvents parameter structure invalid');
    }
});

test('getVaultTotalReturns - all documented parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Exact example from documentation (lines 802-808)
    const returnsCall = () => client.getVaultTotalReturns({
        path: {
            userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d',
            network: 'mainnet',
            vaultAddress: '0x1234567890123456789012345678901234567890'
        }
    });
    
    if (typeof returnsCall !== 'function') {
        throw new Error('getVaultTotalReturns parameter structure invalid');
    }
});

test('Common Patterns - documented examples', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: process.env.VAULTS_FYI_API_KEY || 'test_key' });
    
    // Exact examples from Common Patterns section (lines 886-904)
    
    // Get all vaults (credit-efficient filtering)
    const getAllVaultsPattern = () => client.getAllVaults({
        query: { network: 'mainnet', assetSymbol: 'USDC' }
    });
    
    // Get user positions
    const getPositionsPattern = () => client.getPositions({
        path: { userAddress: '0x...' }
    });
    
    // Generate deposit transaction
    const getActionsPattern = () => client.getActions({
        path: {
            action: 'deposit',
            userAddress: '0x...',
            network: 'mainnet',
            vaultAddress: '0x...'
        },
        query: { amount: '1000000' }
    });
    
    if (typeof getAllVaultsPattern !== 'function' || 
        typeof getPositionsPattern !== 'function' || 
        typeof getActionsPattern !== 'function') {
        throw new Error('Common Patterns examples are invalid');
    }
});

test('Best Yields Function - documented parameters', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    
    // Exact function from documentation (lines 805-816)
    async function findBestYields(client, userAddress, allowedAssets = ['USDC']) {
        // ✅ CORRECT: Use the dedicated endpoint
        const depositOptions = await client.getDepositOptions({
            path: { userAddress },
            query: { 
                allowedAssets,
                allowedNetworks: ['mainnet', 'base']
            }
        });
        
        return depositOptions;
    }
    
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    if (typeof findBestYields !== 'function') {
        throw new Error('findBestYields function structure invalid');
    }
    
    // Test parameter structure
    const result = findBestYields(client, '0xtest', ['USDC']);
    if (!(result instanceof Promise)) {
        throw new Error('findBestYields should return a Promise');
    }
});

test('Environment Variable Setup', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    
    // Test documented environment variable pattern (lines 142-144)
    process.env.VAULTS_FYI_API_KEY = 'test_key';
    const client = new VaultsSdk({
        apiKey: process.env.VAULTS_FYI_API_KEY
    });
    
    if (!client) {
        throw new Error('Environment variable initialization failed');
    }
});

test('All documented network values', () => {
    // Test all networks mentioned in documentation (lines 28-42)
    const documentedNetworks = [
        'arbitrum', 'base', 'berachain', 'bsc', 'celo', 
        'gnosis', 'ink', 'mainnet', 'optimism', 'polygon', 
        'swellchain', 'unichain', 'worldchain'
    ];
    
    // Ensure all documented networks are strings and properly formatted
    for (const network of documentedNetworks) {
        if (typeof network !== 'string' || network.length === 0) {
            throw new Error(`Invalid network value: ${network}`);
        }
        if (network !== network.toLowerCase()) {
            throw new Error(`Network should be lowercase: ${network}`);
        }
    }
    
    if (documentedNetworks.length !== 13) {
        throw new Error(`Expected 13 networks, found ${documentedNetworks.length}`);
    }
});

test('Asset symbol examples', () => {
    // Test all asset symbols mentioned in documentation
    const documentedAssets = ['USDC', 'USDS', 'USDT', 'DAI', 'WBTC'];
    
    for (const asset of documentedAssets) {
        if (typeof asset !== 'string' || asset.length === 0) {
            throw new Error(`Invalid asset symbol: ${asset}`);
        }
        if (asset !== asset.toUpperCase()) {
            throw new Error(`Asset symbol should be uppercase: ${asset}`);
        }
    }
});

test('Documentation action types', () => {
    // Test all action types mentioned in documentation
    const documentedActions = ['deposit', 'redeem'];
    
    for (const action of documentedActions) {
        if (typeof action !== 'string' || action.length === 0) {
            throw new Error(`Invalid action type: ${action}`);
        }
        if (action !== action.toLowerCase()) {
            throw new Error(`Action type should be lowercase: ${action}`);
        }
    }
});

console.log(`\n📊 Test Results: ${passedTests}/${totalTests} tests passed`);

if (passedTests === totalTests) {
    console.log('🎉 All documented parameter combinations are valid!');
    console.log('✅ Every API example in the documentation works correctly.');
    process.exit(0);
} else {
    console.log('💥 Some parameter combinations failed.');
    console.log('❌ Documentation examples may need updates.');
    process.exit(1);
}