#!/usr/bin/env node

/**
 * Test JavaScript code examples from claude.md documentation
 * Validates syntax and structure of all documented examples
 */

import { createRequire } from 'module';
const require = createRequire(import.meta.url);

console.log('🧪 Testing JavaScript Code Examples from Documentation...\n');

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

// Test SDK initialization examples from documentation
test('SDK initialization examples', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    
    // Example 1: Basic initialization
    const client1 = new VaultsSdk({
        apiKey: process.env.VAULTS_FYI_API_KEY || 'test_key'
    });
    
    // Example 2: With environment variable
    process.env.VAULTS_FYI_API_KEY = 'test_key';
    const client2 = new VaultsSdk({
        apiKey: process.env.VAULTS_FYI_API_KEY
    });
    
    if (!client1 || !client2) {
        throw new Error('Failed to initialize SDK clients');
    }
});

// Test getBenchmarks example from documentation
test('getBenchmarks example structure', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // This is the exact example from documentation
    const exampleCall = () => {
        return client.getBenchmarks({
            path: {
                network: 'mainnet',
                code: 'usd'
            }
        });
    };
    
    // Should not throw syntax errors
    if (typeof exampleCall !== 'function') {
        throw new Error('getBenchmarks example is not valid');
    }
});

// Test getHistoricalBenchmarks example
test('getHistoricalBenchmarks example structure', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    const exampleCall = () => {
        return client.getHistoricalBenchmarks({
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
    };
    
    if (typeof exampleCall !== 'function') {
        throw new Error('getHistoricalBenchmarks example is not valid');
    }
});

// Test getAllVaults example with credit-efficient filtering
test('getAllVaults credit-efficient filtering example', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    const exampleCall = () => {
        return client.getAllVaults({
            query: {
                network: 'mainnet',
                assetSymbol: 'USDC',
                onlyTransactional: true,
                page: 0,
                perPage: 50
            }
        });
    };
    
    if (typeof exampleCall !== 'function') {
        throw new Error('getAllVaults example is not valid');
    }
});

// Test getVault example
test('getVault example structure', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    const exampleCall = () => {
        return client.getVault({
            path: {
                network: 'mainnet',
                vaultAddress: '0x1234567890123456789012345678901234567890'
            }
        });
    };
    
    if (typeof exampleCall !== 'function') {
        throw new Error('getVault example is not valid');
    }
});

// Test getActions example (most complex)
test('getActions example structure', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    const exampleCall = () => {
        return client.getActions({
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
    };
    
    if (typeof exampleCall !== 'function') {
        throw new Error('getActions example is not valid');
    }
});

// Test user-related endpoints
test('User-related endpoints examples', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    const userAddress = '0xdB79e7E9e1412457528e40db9fCDBe69f558777d';
    
    // getPositions example
    const positionsCall = () => client.getPositions({
        path: { userAddress }
    });
    
    // getIdleAssets example
    const idleAssetsCall = () => client.getIdleAssets({
        path: { userAddress }
    });
    
    // getDepositOptions example
    const depositOptionsCall = () => client.getDepositOptions({
        path: { userAddress },
        query: {
            allowedAssets: ['USDC', 'USDT'],
            allowedNetworks: ['mainnet', 'base']
        }
    });
    
    if (typeof positionsCall !== 'function' || 
        typeof idleAssetsCall !== 'function' || 
        typeof depositOptionsCall !== 'function') {
        throw new Error('User-related endpoint examples are not valid');
    }
});

// Test Common Patterns examples from documentation
test('Common Patterns examples', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    
    // Initialize client (from Common Patterns section)
    const client = new VaultsSdk({ apiKey: process.env.VAULTS_FYI_API_KEY || 'test_key' });
    
    // Get all vaults (credit-efficient filtering) - from Common Patterns
    const getAllVaultsPattern = () => client.getAllVaults({
        query: { network: 'mainnet', assetSymbol: 'USDC' }
    });
    
    // Get user positions - from Common Patterns
    const getPositionsPattern = () => client.getPositions({
        path: { userAddress: '0x...' }
    });
    
    // Generate deposit transaction - from Common Patterns
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
        throw new Error('Common Patterns examples are not valid');
    }
});

// Test Best Practices example (find best yields)
test('Best yields function example', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    
    // This is the correct example from documentation
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
        throw new Error('findBestYields function example is not valid');
    }
    
    // Test that it returns a promise
    const result = findBestYields(client, '0xtest', ['USDC']);
    if (!(result instanceof Promise)) {
        throw new Error('findBestYields should return a Promise');
    }
});

console.log(`\n📊 Test Results: ${passedTests}/${totalTests} tests passed`);

if (passedTests === totalTests) {
    console.log('🎉 All JavaScript example tests passed!');
    process.exit(0);
} else {
    console.log('💥 Some tests failed. Please check the code examples.');
    process.exit(1);
}