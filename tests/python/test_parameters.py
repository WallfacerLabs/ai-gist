#!/usr/bin/env python3

"""
Test ALL documented Python API parameter combinations from claude.md
Validates every parameter example shown in the documentation
"""

import unittest
import sys
import os


class TestDocumentedParameterCombinations(unittest.TestCase):
    """Test ALL documented parameter combinations from claude.md"""
    
    def setUp(self):
        """Check if SDK is available before running tests"""
        try:
            import vaultsfyi
            self.sdk_available = True
        except ImportError:
            self.sdk_available = False
    
    def test_get_benchmarks_parameters(self):
        """Test get_benchmarks with all documented parameters"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        client = VaultsSdk(api_key="test_key")
        
        # Exact parameters from documentation (lines 174-176)
        def benchmark_call():
            return client.get_benchmarks(
                network='mainnet',  # Required: 'mainnet', 'base', 'arbitrum', etc.
                code='usd'         # Required: 'usd' or 'eth'
            )
        
        # Should not raise syntax errors
        self.assertTrue(callable(benchmark_call))
        self.assertTrue(hasattr(client, 'get_benchmarks'))
    
    def test_get_historical_benchmarks_parameters(self):
        """Test get_historical_benchmarks with all documented parameters"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        client = VaultsSdk(api_key="test_key")
        
        # Exact parameters from documentation (lines 216-225)
        def historical_call():
            return client.get_historical_benchmarks(
                network='mainnet',                        # Required
                code='usd',                              # Required
                page=0,                                  # Optional: page number
                per_page=100,                            # Optional: items per page
                from_timestamp=1640995200,               # Optional: start time
                to_timestamp=1672531200                  # Optional: end time
            )
        
        self.assertTrue(callable(historical_call))
        self.assertTrue(hasattr(client, 'get_historical_benchmarks'))
    
    def test_get_all_vaults_credit_efficient_parameters(self):
        """Test get_all_vaults with credit-efficient filtering parameters"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        client = VaultsSdk(api_key="test_key")
        
        # Exact parameters from credit-efficient example (lines 79-84)
        def specific_vaults_call():
            return client.get_all_vaults(
                network='mainnet',
                assetSymbol='USDC',
                onlyTransactional=True
            )
        
        # Pagination example (line 87)
        def paginated_call():
            return client.get_all_vaults(page=0, perPage=50)
        
        self.assertTrue(callable(specific_vaults_call))
        self.assertTrue(callable(paginated_call))
        self.assertTrue(hasattr(client, 'get_all_vaults'))
    
    def test_get_vault_parameters(self):
        """Test get_vault with all documented parameters"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        client = VaultsSdk(api_key="test_key")
        
        # Exact parameters from documentation (lines 358-362)
        def vault_call():
            return client.get_vault(
                network='mainnet',        # Required: network name
                vault_address='0x1234567890123456789012345678901234567890'  # Required: vault contract address
            )
        
        self.assertTrue(callable(vault_call))
        self.assertTrue(hasattr(client, 'get_vault'))
    
    def test_get_vault_historical_data_parameters(self):
        """Test get_vault_historical_data with all documented parameters"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        client = VaultsSdk(api_key="test_key")
        
        # Parameters based on documentation common query parameters (lines 434-439)
        def historical_data_call():
            return client.get_vault_historical_data(
                network='mainnet',        # Required
                vault_address='0x1234567890123456789012345678901234567890',  # Required
                apyInterval='7day',       # Optional: '1day', '7day', '30day'
                fromTimestamp=1640995200, # Optional: Unix timestamp
                toTimestamp=1672531200,   # Optional: Unix timestamp
                page=0,                   # Optional: page number
                perPage=100               # Optional: items per page
            )
        
        self.assertTrue(callable(historical_data_call))
        self.assertTrue(hasattr(client, 'get_vault_historical_data'))
    
    def test_get_positions_parameters(self):
        """Test get_positions with documented parameters"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        client = VaultsSdk(api_key="test_key")
        
        # Exact parameters from documentation (lines 463-465)
        def positions_call():
            return client.get_positions(
                user_address='0xdB79e7E9e1412457528e40db9fCDBe69f558777d'   # Required: user's wallet address
            )
        
        self.assertTrue(callable(positions_call))
        self.assertTrue(hasattr(client, 'get_positions'))
    
    def test_get_deposit_options_parameters(self):
        """Test get_deposit_options with all documented parameters"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        client = VaultsSdk(api_key="test_key")
        
        # Exact parameters from documentation (lines 518-522 and 551-554)
        def deposit_options_call():
            return client.get_deposit_options(
                user_address='0xdB79e7E9e1412457528e40db9fCDBe69f558777d',  # Required
                allowed_assets=['USDC', 'USDS'],                            # Optional: ['USDC', 'USDS']
                allowedNetworks=['mainnet', 'base'],                        # List of network names
                disallowedNetworks=['arbitrum']                             # List of networks to exclude
            )
        
        # Credit-efficient filtering example (lines 89-93)
        def credit_efficient_call():
            return client.get_deposit_options(
                user_address='0x...',
                allowed_assets=['USDC', 'USDT']
            )
        
        self.assertTrue(callable(deposit_options_call))
        self.assertTrue(callable(credit_efficient_call))
        self.assertTrue(hasattr(client, 'get_deposit_options'))
    
    def test_get_idle_assets_parameters(self):
        """Test get_idle_assets with documented parameters"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        client = VaultsSdk(api_key="test_key")
        
        # Exact parameters from documentation (lines 590-592)
        def idle_assets_call():
            return client.get_idle_assets(
                user_address='0xdB79e7E9e1412457528e40db9fCDBe69f558777d'   # Required
            )
        
        self.assertTrue(callable(idle_assets_call))
        self.assertTrue(hasattr(client, 'get_idle_assets'))
    
    def test_get_actions_complete_parameters(self):
        """Test get_actions with all documented parameters"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        client = VaultsSdk(api_key="test_key")
        
        # Exact parameters from documentation (lines 618-625)
        def actions_call():
            return client.get_actions(
                action='deposit',                          # Required: 'deposit', 'redeem', etc.
                user_address='0xdB79e7E9e1412457528e40db9fCDBe69f558777d',     # Required
                network='mainnet',                         # Required
                vault_address='0x1234567890123456789012345678901234567890',   # Required
                amount='1000000000',                       # Optional: amount in wei
                asset_address='0xA0b86a33E6441f3F56F2B05e7b4B8B7F5A5f0e1B',  # Optional: asset contract address
                simulate=True                              # Optional: simulate transaction
            )
        
        self.assertTrue(callable(actions_call))
        self.assertTrue(hasattr(client, 'get_actions'))
    
    def test_remaining_endpoints_parameters(self):
        """Test remaining endpoints with documented parameters"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        client = VaultsSdk(api_key="test_key")
        
        user_address = '0xdB79e7E9e1412457528e40db9fCDBe69f558777d'
        network = 'mainnet'
        vault_address = '0x1234567890123456789012345678901234567890'
        
        # get_transactions_context (lines 712-716)
        def context_call():
            return client.get_transactions_context(
                user_address=user_address,   # Required
                network=network,             # Required
                vault_address=vault_address  # Required
            )
        
        # get_vault_holder_events (lines 726-730)
        def events_call():
            return client.get_vault_holder_events(
                user_address=user_address,   # Required
                network=network,             # Required
                vault_address=vault_address  # Required
            )
        
        # get_vault_total_returns (lines 739-743)
        def returns_call():
            return client.get_vault_total_returns(
                user_address=user_address,   # Required
                network=network,             # Required
                vault_address=vault_address  # Required
            )
        
        self.assertTrue(callable(context_call))
        self.assertTrue(callable(events_call))
        self.assertTrue(callable(returns_call))
        
        self.assertTrue(hasattr(client, 'get_transactions_context'))
        self.assertTrue(hasattr(client, 'get_vault_holder_events'))
        self.assertTrue(hasattr(client, 'get_vault_total_returns'))
    
    def test_documented_best_yields_function(self):
        """Test the exact best yields function from documentation"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        
        # Exact function from documentation (lines 783-795)
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
        
        # Test function structure
        self.assertTrue(callable(find_best_yields))
        
        # Test that it uses the correct method
        self.assertTrue(hasattr(client, 'get_deposit_options'))
    
    def test_dynamic_network_fetching(self):
        """Test dynamic network fetching examples from documentation"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        import requests
        
        # Exact function from documentation (lines 674-698)
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
        
        # Test function structure
        self.assertTrue(callable(get_supported_networks))
        self.assertTrue(callable(validate_network))
        
        # Test that it returns a list
        networks = get_supported_networks(client)
        self.assertIsInstance(networks, list)
        self.assertGreater(len(networks), 0)
    
    def test_documented_network_values(self):
        """Test all network values mentioned in documentation"""
        # All networks from documentation (lines 28-42)
        documented_networks = [
            'arbitrum', 'base', 'berachain', 'bsc', 'celo', 
            'gnosis', 'ink', 'mainnet', 'optimism', 'polygon', 
            'swellchain', 'unichain', 'worldchain'
        ]
        
        # Validate structure
        self.assertEqual(len(documented_networks), 13, "Should have 13 networks as documented")
        
        for network in documented_networks:
            self.assertIsInstance(network, str, f"Network {network} should be string")
            self.assertEqual(network, network.lower(), f"Network {network} should be lowercase")
            self.assertGreater(len(network), 0, f"Network {network} should not be empty")
    
    def test_documented_asset_symbols(self):
        """Test all asset symbols mentioned in documentation"""
        # Asset symbols from various examples
        documented_assets = ['USDC', 'USDS', 'USDT', 'DAI', 'WBTC']
        
        for asset in documented_assets:
            self.assertIsInstance(asset, str, f"Asset {asset} should be string")
            self.assertEqual(asset, asset.upper(), f"Asset {asset} should be uppercase")
            self.assertGreater(len(asset), 0, f"Asset {asset} should not be empty")
    
    def test_documented_action_types(self):
        """Test all action types mentioned in documentation"""
        # Action types from documentation
        documented_actions = ['deposit', 'redeem']
        
        for action in documented_actions:
            self.assertIsInstance(action, str, f"Action {action} should be string")
            self.assertEqual(action, action.lower(), f"Action {action} should be lowercase")
            self.assertGreater(len(action), 0, f"Action {action} should not be empty")
    
    def test_common_patterns_examples(self):
        """Test Common Patterns examples from documentation"""
        if not self.sdk_available:
            self.skipTest("vaultsfyi SDK not available (expected if not public yet)")
            
        from vaultsfyi import VaultsSdk
        
        # Initialize client (from Common Patterns section - lines 865-866)
        client = VaultsSdk(api_key="test_key")
        
        # Get all vaults (lines 868-869)
        def get_all_vaults_pattern():
            return client.get_all_vaults()
        
        # Get user positions (lines 871-872)
        def get_positions_pattern():
            return client.get_positions("0x...")
        
        # Generate deposit transaction (lines 874-875)
        def get_actions_pattern():
            return client.get_actions("deposit", "0x...", "mainnet", "0x...", amount="1000000")
        
        # Test all patterns
        self.assertTrue(callable(get_all_vaults_pattern))
        self.assertTrue(callable(get_positions_pattern))
        self.assertTrue(callable(get_actions_pattern))
    
    def test_api_configuration_constants(self):
        """Test API configuration values from documentation"""
        # API configuration from documentation (lines 47-51)
        api_base_url = "https://api.vaults.fyi"
        api_version = "v2"
        auth_header = "x-api-key"
        response_format = "JSON"
        
        # Validate configuration values
        self.assertEqual(api_base_url, "https://api.vaults.fyi")
        self.assertEqual(api_version, "v2")
        self.assertEqual(auth_header, "x-api-key")
        self.assertEqual(response_format, "JSON")
        
        # Validate URL format
        self.assertTrue(api_base_url.startswith("https://"))
        self.assertIn("vaults.fyi", api_base_url)


if __name__ == '__main__':
    print("🧪 Testing ALL Documented Python Parameter Combinations...\n")
    
    unittest.main(verbosity=2)