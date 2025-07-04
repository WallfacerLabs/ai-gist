#!/usr/bin/env node

/**
 * Main test runner for JavaScript tests
 * Runs all JavaScript tests to verify documentation examples
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('🚀 Running JavaScript Tests for vaults.fyi Documentation\n');

const tests = [
    { name: 'Import Tests', file: 'test-imports.js' },
    { name: 'Example Tests', file: 'test-examples.js' },
    { name: 'Parameter Coverage Tests', file: 'test-parameters.js' }
];

let passedTests = 0;
let totalTests = tests.length;

function runTest(testFile) {
    return new Promise((resolve) => {
        console.log(`\n🏃 Running ${testFile}...`);
        
        const testProcess = spawn('node', [join(__dirname, testFile)], {
            stdio: 'inherit'
        });
        
        testProcess.on('close', (code) => {
            if (code === 0) {
                passedTests++;
                console.log(`✅ ${testFile} passed\n`);
            } else {
                console.log(`❌ ${testFile} failed\n`);
            }
            resolve(code);
        });
        
        testProcess.on('error', (error) => {
            console.log(`❌ Error running ${testFile}: ${error.message}\n`);
            resolve(1);
        });
    });
}

async function runAllTests() {
    console.log('📋 Test Plan:');
    tests.forEach((test, index) => {
        console.log(`   ${index + 1}. ${test.name} (${test.file})`);
    });
    console.log('');
    
    for (const test of tests) {
        await runTest(test.file);
    }
    
    console.log('='.repeat(60));
    console.log(`📊 Final Results: ${passedTests}/${totalTests} test suites passed`);
    
    if (passedTests === totalTests) {
        console.log('🎉 All JavaScript tests passed!');
        console.log('✅ All documentation examples are working correctly.');
        process.exit(0);
    } else {
        console.log('💥 Some tests failed.');
        console.log('❌ Documentation examples may need to be updated.');
        process.exit(1);
    }
}

// Check if @vaultsfyi/sdk is installed
try {
    await import('@vaultsfyi/sdk');
    console.log('✅ @vaultsfyi/sdk is available');
} catch (error) {
    console.log('❌ @vaultsfyi/sdk is not installed.');
    console.log('   Please run: npm install @vaultsfyi/sdk');
    console.log('   Or run: npm install (to install from package.json)');
    process.exit(1);
}

runAllTests();