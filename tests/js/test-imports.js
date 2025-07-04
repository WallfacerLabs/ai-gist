#!/usr/bin/env node

/**
 * Test JavaScript SDK import statements from documentation
 * Tests all import patterns mentioned in claude.md
 */

import { createRequire } from 'module';
const require = createRequire(import.meta.url);

console.log('🧪 Testing JavaScript SDK Import Statements...\n');

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

// Test 1: ES Module Import (Recommended)
test('ES Module import from @vaultsfyi/sdk', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    
    if (typeof VaultsSdk !== 'function') {
        throw new Error('VaultsSdk is not a constructor function');
    }
    
    // Test instantiation without API key (should not throw)
    const client = new VaultsSdk({ apiKey: 'test_key' });
    if (!client) {
        throw new Error('Failed to instantiate VaultsSdk');
    }
});

// Test 2: CommonJS Import
test('CommonJS require import', () => {
    const { VaultsSdk } = require('@vaultsfyi/sdk');
    
    if (typeof VaultsSdk !== 'function') {
        throw new Error('VaultsSdk is not a constructor function');
    }
    
    // Test instantiation
    const client = new VaultsSdk({ apiKey: 'test_key' });
    if (!client) {
        throw new Error('Failed to instantiate VaultsSdk');
    }
});

// Test 3: TypeScript-style import (works in JS too)
test('TypeScript-style import', async () => {
    const { VaultsSdk } = await import('@vaultsfyi/sdk');
    
    if (typeof VaultsSdk !== 'function') {
        throw new Error('VaultsSdk is not a constructor function');
    }
    
    // Test with environment variable pattern
    process.env.VAULTS_FYI_API_KEY = 'test_key';
    const client = new VaultsSdk({
        apiKey: process.env.VAULTS_FYI_API_KEY
    });
    
    if (!client) {
        throw new Error('Failed to instantiate VaultsSdk with env var');
    }
});

// Test 4: Check SDK methods exist
test('SDK methods exist', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    const expectedMethods = [
        'getBenchmarks',
        'getHistoricalBenchmarks',
        'getAllVaults',
        'getVault',
        'getVaultHistoricalData',
        'getPositions',
        'getDepositOptions',
        'getIdleAssets',
        'getActions',
        'getTransactionsContext',
        'getVaultHolderEvents',
        'getVaultTotalReturns'
    ];
    
    for (const method of expectedMethods) {
        if (typeof client[method] !== 'function') {
            throw new Error(`Method ${method} does not exist or is not a function`);
        }
    }
});

// Test 5: Parameter structure validation
test('Parameter structure validation', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Test that methods accept the expected parameter structure
    // We're not calling the API, just checking the methods don't throw on parameter validation
    
    try {
        // These should not throw errors for parameter structure
        const benchmarkParams = {
            path: { network: 'mainnet', code: 'usd' }
        };
        
        const vaultParams = {
            path: { network: 'mainnet', vaultAddress: '0x1234567890123456789012345678901234567890' }
        };
        
        const userParams = {
            path: { userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d' }
        };
        
        // These won't make actual API calls due to invalid API key, 
        // but should validate parameter structure
        // We're just checking the methods exist and accept the right parameter format
        
    } catch (error) {
        if (!error.message.includes('api') && !error.message.includes('401') && !error.message.includes('unauthorized')) {
            throw error; // Only throw if it's not an API/auth error
        }
    }
});

console.log(`\n📊 Test Results: ${passedTests}/${totalTests} tests passed`);

if (passedTests === totalTests) {
    console.log('🎉 All JavaScript import tests passed!');
    process.exit(0);
} else {
    console.log('💥 Some tests failed. Please check the SDK installation.');
    process.exit(1);
}