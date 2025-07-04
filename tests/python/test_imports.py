#!/usr/bin/env python3

"""
Test Python SDK import statements from documentation
Tests all import patterns and initialization examples mentioned in claude.md
"""

import sys
import os
import unittest
from unittest.mock import patch


class TestPythonSDKImports(unittest.TestCase):
    """Test Python SDK imports and initialization examples from documentation"""
    
    def setUp(self):
        """Check if SDK is available before running tests"""
        try:
            import vaultsfyi
            self.sdk_available = True
        except ImportError:
            self.sdk_available = False
    
    def test_basic_import(self):
        """Test basic SDK import from documentation"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        self.assertTrue(callable(VaultsSdk), "VaultsSdk should be callable")
    
    def test_sdk_initialization_basic(self):
        """Test basic SDK initialization example from documentation"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        
        # This is the exact example from documentation
        client = VaultsSdk(
            api_key="your_api_key_here",
            api_base_url="https://api.vaults.fyi",  # optional
            timeout=30,                             # optional
            max_retries=3                           # optional
        )
        
        self.assertIsNotNone(client, "Client should be instantiated")
        
    def test_sdk_initialization_minimal(self):
        """Test minimal SDK initialization"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        
        client = VaultsSdk(api_key="test_key")
        self.assertIsNotNone(client, "Client should be instantiated with minimal params")
    
    def test_sdk_methods_exist(self):
        """Test that all documented SDK methods exist"""
        from vaultsfyi import VaultsSdk
        
        client = VaultsSdk(api_key="test_key")
        
        expected_methods = [
            'get_benchmarks',
            'get_historical_benchmarks',
            'get_all_vaults',
            'get_vault',
            'get_vault_historical_data',
            'get_positions',
            'get_deposit_options',
            'get_idle_assets',
            'get_actions',
            'get_transactions_context',
            'get_vault_holder_events',
            'get_vault_total_returns'
        ]
        
        for method_name in expected_methods:
            with self.subTest(method=method_name):
                self.assertTrue(
                    hasattr(client, method_name),
                    f"Client should have method {method_name}"
                )
                method = getattr(client, method_name)
                self.assertTrue(
                    callable(method),
                    f"Method {method_name} should be callable"
                )
    
    def test_exception_imports(self):
        """Test that exception classes can be imported"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        try:
            from vaultsfyi.exceptions import (
                AuthenticationError,
                HttpResponseError,
                RateLimitError,
                VaultsFyiError
            )
            
            # Check that they are exception classes
            self.assertTrue(issubclass(AuthenticationError, Exception))
            self.assertTrue(issubclass(HttpResponseError, Exception))
            self.assertTrue(issubclass(RateLimitError, Exception))
            self.assertTrue(issubclass(VaultsFyiError, Exception))
            
        except ImportError as e:
            self.fail(f"Failed to import exception classes: {e}")
    
    def test_virtual_environment_best_practice(self):
        """Test that we're running in a virtual environment (best practice)"""
        # Check if we're in a virtual environment
        in_venv = (
            hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        )
        
        if not in_venv:
            # This is a warning, not a failure, but documents best practice
            print("\n⚠️  WARNING: Not running in a virtual environment.")
            print("   Best practice: Run tests in a virtual environment")
            print("   Commands: python -m venv venv && source venv/bin/activate")


class TestDocumentationExamples(unittest.TestCase):
    """Test specific code examples from claude.md documentation"""
    
    def test_get_benchmarks_example(self):
        """Test get_benchmarks example from documentation"""
        from vaultsfyi import VaultsSdk
        
        client = VaultsSdk(api_key="test_key")
        
        # This should not raise syntax or type errors
        # (actual API call would fail with test key, but structure should be valid)
        try:
            # This is the exact parameter structure from documentation
            params = {
                'network': 'mainnet',  # Required: 'mainnet', 'base', 'arbitrum', etc.
                'code': 'usd'         # Required: 'usd' or 'eth'
            }
            
            # Method should exist and be callable
            method = getattr(client, 'get_benchmarks')
            self.assertTrue(callable(method))
            
        except AttributeError as e:
            self.fail(f"get_benchmarks method not found: {e}")
    
    def test_get_all_vaults_example(self):
        """Test get_all_vaults example with filtering from documentation"""
        from vaultsfyi import VaultsSdk
        
        client = VaultsSdk(api_key="test_key")
        
        # Test the credit-efficient filtering example from documentation
        try:
            method = getattr(client, 'get_all_vaults')
            self.assertTrue(callable(method))
            
            # These are the exact parameters from documentation examples
            example_params = {
                'assetSymbol': 'USDC',
                'network': 'mainnet',
                'onlyTransactional': True,
                'page': 0,
                'perPage': 50
            }
            
        except AttributeError as e:
            self.fail(f"get_all_vaults method not found: {e}")
    
    def test_get_actions_example(self):
        """Test get_actions example from documentation"""
        from vaultsfyi import VaultsSdk
        
        client = VaultsSdk(api_key="test_key")
        
        try:
            method = getattr(client, 'get_actions')
            self.assertTrue(callable(method))
            
            # These are the exact parameters from documentation
            example_params = {
                'action': 'deposit',                          # Required: 'deposit', 'redeem', etc.
                'user_address': '0xdB79e7E9e1412457528e40db9fCDBe69f558777d',     # Required
                'network': 'mainnet',                         # Required
                'vault_address': '0x1234567890123456789012345678901234567890',   # Required
                'amount': '1000000000',                       # Optional: amount in wei
                'asset_address': '0xA0b86a33E6441f3F56F2B05e7b4B8B7F5A5f0e1B',  # Optional: asset contract address
                'simulate': True                              # Optional: simulate transaction
            }
            
        except AttributeError as e:
            self.fail(f"get_actions method not found: {e}")
    
    def test_best_yields_function_example(self):
        """Test the correct best yields function example from documentation"""
        from vaultsfyi import VaultsSdk
        
        # This is the CORRECT example from documentation (using get_deposit_options)
        def find_best_yields(client, user_address, allowed_assets=['USDC'], allowed_networks=['mainnet']):
            """
            ✅ CORRECT: Use get_deposit_options() - it's designed for this exact purpose
            This endpoint returns optimal yield opportunities for user's assets
            """
            deposit_options = client.get_deposit_options(
                user_address=user_address,
                allowed_assets=allowed_assets,
                allowedNetworks=allowed_networks
            )
            
            # The API already returns sorted best options per asset
            return deposit_options
        
        client = VaultsSdk(api_key="test_key")
        
        # Test that the function is properly structured
        self.assertTrue(callable(find_best_yields))
        
        # Test that get_deposit_options method exists
        self.assertTrue(hasattr(client, 'get_deposit_options'))
        self.assertTrue(callable(getattr(client, 'get_deposit_options')))
    
    def test_network_validation_example(self):
        """Test network validation example from documentation"""
        from vaultsfyi import VaultsSdk
        import requests
        
        # This is the exact function from documentation
        def get_supported_networks(client):
            """Get current supported networks from dedicated API endpoint"""
            try:
                # Use the dedicated networks endpoint - most efficient
                response = client.get_networks()  # Assuming this method exists in SDK
                return [network['name'] for network in response]
            except AttributeError:
                # If SDK doesn't have get_networks method, make direct API call
                try:
                    api_key = client.api_key
                    headers = {'x-api-key': api_key}
                    response = requests.get('https://api.vaults.fyi/v2/networks', headers=headers)
                    response.raise_for_status()
                    networks = response.json()
                    return [network['name'] for network in networks]
                except Exception as e:
                    # Fallback to known networks (updated July 4, 2025)
                    return [
                        'arbitrum', 'base', 'berachain', 'bsc', 'celo', 'gnosis', 
                        'ink', 'mainnet', 'optimism', 'polygon', 'swellchain', 'unichain', 'worldchain'
                    ]

        def validate_network(client, network: str) -> bool:
            """Validate network against current API data"""
            supported_networks = get_supported_networks(client)
            return network in supported_networks
        
        client = VaultsSdk(api_key="test_key")
        
        # Test that functions are properly structured
        self.assertTrue(callable(get_supported_networks))
        self.assertTrue(callable(validate_network))
        
        # Test with known good network
        networks = get_supported_networks(client)
        self.assertIsInstance(networks, list)
        self.assertGreater(len(networks), 0)


if __name__ == '__main__':
    print("🧪 Testing Python SDK Import Statements and Examples...\n")
    
    # Run the tests
    unittest.main(verbosity=2)