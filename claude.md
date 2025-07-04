# Vaults.fyi API Development Guide for AI Agents

This guide provides comprehensive instructions for AI agents working with the vaults.fyi API and SDKs. It covers the complete API structure, exact parameter specifications, and response schemas to prevent hallucination of non-existent endpoints or fields.

## Project Overview

Vaults.fyi is a DeFi infrastructure platform that provides standardized access to over 500 DeFi vaults across 50+ protocols and 10+ blockchain networks. The platform normalizes complex DeFi data into consistent, comparable formats for lending, staking, and yield farming opportunities.

### Key Capabilities
- **Market Data**: Real-time and historical APY, TVL, and performance metrics
- **Transactional Support**: Generate executable transaction payloads for deposits/withdrawals
- **Portfolio Tracking**: Monitor user positions across multiple protocols and networks
- **Benchmark Rates**: Standardized interest rate benchmarks across DeFi protocols
- **Risk Assessment**: Normalized risk scores and reputation metrics

### Supported Networks

**IMPORTANT: Network coverage expands frequently. Always check current networks via API rather than relying on this static list.**

Get current networks dynamically:
```python
# ✅ CORRECT: Use dedicated networks endpoint
networks = client.get_networks()  # Most efficient approach
# OR direct API call if SDK method doesn't exist:
# GET https://api.vaults.fyi/v2/networks
```

**Current Networks (as of July 4, 2025):**
- **Arbitrum** (chainId: 42161, CAIP: eip155:42161)
- **Base** (chainId: 8453, CAIP: eip155:8453)
- **Berachain** (chainId: 80094, CAIP: eip155:80094)
- **BSC** (chainId: 56, CAIP: eip155:56)
- **Celo** (chainId: 42220, CAIP: eip155:42220)
- **Gnosis** (chainId: 100, CAIP: eip155:100)
- **Ink** (chainId: 57073, CAIP: eip155:57073)
- **Mainnet** (chainId: 1, CAIP: eip155:1)
- **Optimism** (chainId: 10, CAIP: eip155:10)
- **Polygon** (chainId: 137, CAIP: eip155:137)
- **Swellchain** (chainId: 1923, CAIP: eip155:1923)
- **Unichain** (chainId: 130, CAIP: eip155:130)
- **Worldchain** (chainId: 480, CAIP: eip155:480)

**Total: 13 networks (as of July 4, 2025). This list may be outdated. Always verify against live API data.**

## API Architecture

### Base Configuration
- **API Base URL**: `https://api.vaults.fyi`
- **API Version**: v2
- **Authentication**: API key via `x-api-key` header
- **Rate Limits**: 10 requests/minute (basic), higher limits for PRO tier
- **Response Format**: JSON

### 🚨 CRITICAL: CREDIT-BASED API SYSTEM 🚨

**THE VAULTS.FYI API IS CREDIT-BASED. EVERY REQUEST CONSUMES CREDITS.**

**ALWAYS FILTER DATA AT THE API LEVEL, NEVER IN MEMORY AFTER FETCHING**

❌ **WRONG - Wastes Credits:**
```python
# DON'T DO THIS - Fetches all data then filters in memory
all_vaults = client.get_all_vaults()
usdc_vaults = [v for v in all_vaults['data'] if v['asset']['symbol'] == 'USDC']
```

✅ **CORRECT - Filters at API Level:**
```python
# DO THIS - Only fetches what you need
usdc_vaults = client.get_all_vaults(assetSymbol='USDC')
```

**MANDATORY FILTERING PRACTICES:**
1. **Always use query parameters** to filter data at the API level
2. **Never fetch all data** then filter in memory - this wastes credits
3. **Use pagination wisely** - only fetch pages you actually need
4. **Be specific with filters** - combine multiple filters when possible
5. **Cache results** when appropriate to avoid repeated API calls

**Examples of Credit-Efficient Filtering:**
```python
# ✅ Filter by network AND asset symbol
specific_vaults = client.get_all_vaults(
    network='mainnet',
    assetSymbol='USDC',
    onlyTransactional=True
)

# ✅ Use pagination efficiently
first_page = client.get_all_vaults(page=0, perPage=50)

# ✅ Filter deposit options by allowed assets
deposit_options = client.get_deposit_options(
    user_address='0x...',
    allowed_assets=['USDC', 'USDT']
)
```

### SDK Installation and Setup

#### Python SDK

**IMPORTANT: Always use virtual environments for Python projects**

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the SDK
pip install vaultsfyi
```

```python
from vaultsfyi import VaultsSdk

client = VaultsSdk(
    api_key="your_api_key_here",
    api_base_url="https://api.vaults.fyi",  # optional
    timeout=30,                             # optional
    max_retries=3                           # optional
)
```

#### JavaScript SDK

**Installation and Setup**

```bash
# Install the SDK
npm install @vaultsfyi/sdk

# Set up environment variable
export VAULTS_FYI_API_KEY="your_api_key_here"
```

**ES Module Import (Recommended)**
```javascript
import pkg from '@vaultsfyi/sdk';
const { VaultsSdk } = pkg;

const client = new VaultsSdk({
    apiKey: process.env.VAULTS_FYI_API_KEY
});
```

**CommonJS Import**
```javascript
const { VaultsSdk } = require('@vaultsfyi/sdk');

const client = new VaultsSdk({
    apiKey: process.env.VAULTS_FYI_API_KEY
});
```

**TypeScript Usage**
```typescript
import { VaultsSdk } from '@vaultsfyi/sdk';

const client = new VaultsSdk({
    apiKey: process.env.VAULTS_FYI_API_KEY!
});
```

## Complete API Endpoint Reference

### 1. Benchmarks - `get_benchmarks()`

**Purpose**: Get current benchmark APY rates for a network and currency code.

**Python Parameters**:
```python
get_benchmarks(
    network: str,     # Required: 'mainnet', 'base', 'arbitrum', etc.
    code: str         # Required: 'usd' or 'eth'
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getBenchmarks({
  path: {
    network: string,    // Required: 'mainnet', 'base', 'arbitrum', etc.
    code: string        // Required: 'usd' or 'eth'
  }
})

// Example usage
const benchmarks = await client.getBenchmarks({
  path: {
    network: 'mainnet',
    code: 'usd'
  }
});
```

**Response Structure**:
```json
{
  "apy": {
    "_1day": 0.05,
    "_7day": 0.051,
    "_30day": 0.052
  },
  "timestamp": 1640995200
}
```

### 2. Historical Benchmarks - `get_historical_benchmarks()`

**Purpose**: Get historical benchmark APY data with time-series information.

**Python Parameters**:
```python
get_historical_benchmarks(
    network: str,                        # Required
    code: str,                          # Required
    page: Optional[int] = None,         # Optional: page number
    per_page: Optional[int] = None,     # Optional: items per page
    from_timestamp: Optional[int] = None, # Optional: start time
    to_timestamp: Optional[int] = None,   # Optional: end time
    **kwargs
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getHistoricalBenchmarks({
  path: {
    network: string,    // Required
    code: string        // Required
  },
  query?: {
    page?: number,              // Optional: page number
    perPage?: number,           // Optional: items per page
    fromTimestamp?: number,     // Optional: start time (Unix timestamp)
    toTimestamp?: number        // Optional: end time (Unix timestamp)
  }
})

// Example usage
const historicalData = await client.getHistoricalBenchmarks({
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
```

**Response Structure**:
```json
{
  "data": [
    {
      "apy": {
        "_1day": 0.05,
        "_7day": 0.051,
        "_30day": 0.052
      },
      "timestamp": 1640995200
    }
  ],
  "pagination": {
    "page": 0,
    "perPage": 100,
    "total": 150
  }
}
```

### 3. All Vaults - `get_all_vaults()`

**Purpose**: Retrieve all available vaults with filtering and pagination.

**Python Parameters**:
```python
get_all_vaults(**kwargs) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getAllVaults({
  query?: {
    page?: number,              // Page number (starting from 0)
    perPage?: number,           // Number of items per page
    network?: string,           // Network filter ('mainnet', 'base', etc.)
    assetSymbol?: string,       // Asset symbol filter ('USDC', 'USDS', etc.)
    onlyTransactional?: boolean, // Only vaults supporting transactions
    onlyAppFeatured?: boolean   // Only featured vaults
  }
})

// Example usage - Credit-efficient filtering
const vaults = await client.getAllVaults({
  query: {
    network: 'mainnet',
    assetSymbol: 'USDC',
    onlyTransactional: true,
    page: 0,
    perPage: 50
  }
});
```

**🚨 CREDIT WARNING: Always use filters to reduce API response size and save credits! 🚨**

**Response Structure**:
```json
{
  "data": [
    {
      "address": "0x1234567890123456789012345678901234567890",
      "name": "Vault Name",
      "network": {
        "name": "mainnet",
        "chainId": 1,
        "networkCaip": "eip155:1"
      },
      "protocol": {
        "name": "Protocol Name"
      },
      "asset": {
        "address": "0x...",
        "symbol": "USDC",
        "name": "USD Coin",
        "decimals": 6,
        "assetPriceInUsd": "1.0"
      },
      "apy": {
        "total": 0.0525
      },
      "isTransactional": true,
      "isAppFeatured": true
    }
  ],
  "pagination": {
    "hasNext": true,
    "page": 0,
    "perPage": 100
  }
}
```

### 4. Specific Vault - `get_vault()`

**Purpose**: Get detailed information about a specific vault.

**Python Parameters**:
```python
get_vault(
    network: str,        # Required: network name
    vault_address: str,  # Required: vault contract address
    **kwargs
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getVault({
  path: {
    network: string,        // Required: network name
    vaultAddress: string    // Required: vault contract address
  },
  query?: { [key: string]: any }
})

// Example usage
const vault = await client.getVault({
  path: {
    network: 'mainnet',
    vaultAddress: '0x1234567890123456789012345678901234567890'
  }
});
```

**Response Structure**: Same as individual vault object in `get_all_vaults()` response.

### 5. Vault Historical Data - `get_vault_historical_data()`

**Purpose**: Get historical performance data for a specific vault.

**Python Parameters**:
```python
get_vault_historical_data(
    network: str,        # Required
    vault_address: str,  # Required
    **kwargs
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getVaultHistoricalData({
  path: {
    network: string,        // Required
    vaultAddress: string    // Required
  },
  query?: {
    apyInterval?: string,   // Optional: '1day', '7day', '30day'
    fromTimestamp?: number, // Optional: Unix timestamp
    toTimestamp?: number,   // Optional: Unix timestamp
    page?: number,          // Optional: page number
    perPage?: number        // Optional: items per page
  }
})

// Example usage
const historicalData = await client.getVaultHistoricalData({
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
```

**Common Query Parameters**:
- `apyInterval`: '1day', '7day', '30day'
- `fromTimestamp`: Unix timestamp
- `toTimestamp`: Unix timestamp
- `page`: Page number
- `perPage`: Items per page

**Response Structure**:
```json
{
  "data": [
    {
      "timestamp": 1640995200,
      "apy": {
        "total": 0.052
      }
    }
  ],
  "itemsOnPage": 100,
  "nextPage": 1
}
```

### 6. User Positions - `get_positions()`

**Purpose**: Get all active positions for a user across all supported protocols.

**Python Parameters**:
```python
get_positions(
    user_address: str,   # Required: user's wallet address
    **kwargs
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getPositions({
  path: {
    userAddress: string   // Required: user's wallet address
  }
})

// Example usage
const positions = await client.getPositions({
  path: {
    userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d'
  }
});
```

**Response Structure**:
```json
{
  "data": [
    {
      "network": {
        "name": "mainnet",
        "chainId": 1
      },
      "protocol": {
        "name": "Protocol Name"
      },
      "name": "Vault Name",
      "asset": {
        "symbol": "USDC",
        "balanceUsd": "1000.50",
        "balanceNative": "1000500000"
      },
      "apy": {
        "total": 0.0525
      }
    }
  ]
}
```

### 7. Deposit Options - `get_deposit_options()`

**Purpose**: Get optimal deposit opportunities for a user's assets.

**Python Parameters**:
```python
get_deposit_options(
    user_address: str,                    # Required
    allowed_assets: Optional[List[str]] = None,  # Optional: ['USDC', 'USDS']
    **kwargs
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getDepositOptions({
  path: {
    userAddress: string                   // Required
  },
  query?: {
    allowedAssets?: string[],             // Optional: ['USDC', 'USDS']
    allowedNetworks?: string[],           // Optional: list of network names
    disallowedNetworks?: string[]         // Optional: networks to exclude
  }
})

// Example usage
const depositOptions = await client.getDepositOptions({
  path: {
    userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d'
  },
  query: {
    allowedAssets: ['USDC', 'USDT'],
    allowedNetworks: ['mainnet', 'base']
  }
});
```

**Query Parameters**:
- `allowedAssets`: List of asset symbols like `['USDC', 'USDS']`
- `allowedNetworks`: List of network names
- `disallowedNetworks`: List of networks to exclude

**Response Structure**:
```json
{
  "userBalances": [
    {
      "asset": {
        "symbol": "USDC",
        "balanceUsd": "1000.00"
      },
      "depositOptions": [
        {
          "name": "Vault Name",
          "network": {
            "name": "mainnet"
          },
          "protocol": {
            "name": "Protocol Name"
          },
          "apy": {
            "total": 0.0525
          }
        }
      ]
    }
  ]
}
```

### 8. Idle Assets - `get_idle_assets()`

**Purpose**: Get user's idle (non-earning) assets across all networks.

**Python Parameters**:
```python
get_idle_assets(
    user_address: str,   # Required
    **kwargs
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getIdleAssets({
  path: {
    userAddress: string   // Required
  }
})

// Example usage
const idleAssets = await client.getIdleAssets({
  path: {
    userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d'
  }
});
```

**Response Structure**:
```json
{
  "data": [
    {
      "symbol": "USDC",
      "balanceNative": "1000000000",
      "balanceUsd": "1000.00",
      "network": {
        "name": "mainnet"
      }
    }
  ]
}
```

### 9. Transaction Actions - `get_actions()`

**Purpose**: Generate executable transaction payloads for vault interactions.

**Python Parameters**:
```python
get_actions(
    action: str,                          # Required: 'deposit', 'redeem', etc.
    user_address: str,                    # Required
    network: str,                         # Required
    vault_address: str,                   # Required
    amount: Optional[str] = None,         # Optional: amount in wei
    asset_address: Optional[str] = None,  # Optional: asset contract address
    simulate: bool = False,               # Optional: simulate transaction
    **kwargs
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getActions({
  path: {
    action: string,        // Required: 'deposit', 'redeem', etc.
    userAddress: string,   // Required: user's wallet address
    network: string,       // Required: network name
    vaultAddress: string   // Required: vault contract address
  },
  query?: {
    amount?: string,       // Optional: amount in wei
    assetAddress?: string, // Optional: asset contract address
    simulate?: boolean     // Optional: simulate transaction
  }
})

// Example usage
const actions = await client.getActions({
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
```

**Response Structure**:
```json
{
  "actions": [
    {
      "name": "Approve USDC",
      "tx": {
        "to": "0x1234567890123456789012345678901234567890",
        "data": "0x095ea7b3...",
        "value": "0",
        "gasLimit": "50000"
      }
    },
    {
      "name": "Deposit into Vault",
      "tx": {
        "to": "0x0987654321098765432109876543210987654321",
        "data": "0xb6b55f25...",
        "value": "0",
        "gasLimit": "200000"
      }
    }
  ]
}
```

### 10. Transaction Context - `get_transactions_context()`

**Purpose**: Get contextual information for transaction preparation.

**Python Parameters**:
```python
get_transactions_context(
    user_address: str,   # Required
    network: str,        # Required
    vault_address: str,  # Required
    **kwargs
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getTransactionsContext({
  path: {
    userAddress: string,    // Required
    network: string,        // Required
    vaultAddress: string    // Required
  }
})

// Example usage
const context = await client.getTransactionsContext({
  path: {
    userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d',
    network: 'mainnet',
    vaultAddress: '0x1234567890123456789012345678901234567890'
  }
});
```

### 11. Vault Holder Events - `get_vault_holder_events()`

**Purpose**: Get historical events for a user's interactions with a specific vault.

**Python Parameters**:
```python
get_vault_holder_events(
    user_address: str,   # Required
    network: str,        # Required
    vault_address: str,  # Required
    **kwargs
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getVaultHolderEvents({
  path: {
    userAddress: string,    // Required
    network: string,        // Required
    vaultAddress: string    // Required
  }
})

// Example usage
const events = await client.getVaultHolderEvents({
  path: {
    userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d',
    network: 'mainnet',
    vaultAddress: '0x1234567890123456789012345678901234567890'
  }
});
```

### 12. Vault Total Returns - `get_vault_total_returns()`

**Purpose**: Calculate total returns for a user's position in a specific vault.

**Python Parameters**:
```python
get_vault_total_returns(
    user_address: str,   # Required
    network: str,        # Required
    vault_address: str,  # Required
    **kwargs
) -> Dict[str, Any]
```

**JavaScript Parameters**:
```javascript
// Method signature
client.getVaultTotalReturns({
  path: {
    userAddress: string,    // Required
    network: string,        // Required
    vaultAddress: string    // Required
  }
})

// Example usage
const returns = await client.getVaultTotalReturns({
  path: {
    userAddress: '0xdB79e7E9e1412457528e40db9fCDBe69f558777d',
    network: 'mainnet',
    vaultAddress: '0x1234567890123456789012345678901234567890'
  }
});
```

## Error Handling

### Common Error Responses
```json
{
  "error": "Error Type",
  "message": "Error description",
  "code": "ERROR_CODE"
}
```

### HTTP Status Codes
- `200 OK`: Successful request
- `400 Bad Request`: Invalid parameters or malformed request
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Credits exhausted or insufficient permissions
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Python SDK Error Classes
```python
from vaultsfyi.exceptions import (
    AuthenticationError,
    HttpResponseError,
    RateLimitError,
    VaultsSdkError
)
```

### JavaScript SDK Error Classes
```typescript
import { HttpResponseError } from 'vaultsfyi';
```

## Best Practices

### 1. Python Virtual Environment Management

**CRITICAL: Always use virtual environments for Python projects to avoid dependency conflicts**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install vaultsfyi

# Create requirements.txt for reproducibility
pip freeze > requirements.txt

# Deactivate when done
deactivate
```

### 2. Rate Limit Management
```python
import time
from vaultsfyi.exceptions import RateLimitError

try:
    response = client.get_all_vaults()
except RateLimitError:
    time.sleep(60)  # Wait before retrying
    response = client.get_all_vaults()
```

### 3. Project Structure with Virtual Environment

```bash
# Recommended project structure
my-vaults-project/
├── venv/                 # Virtual environment (never commit to git)
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
├── requirements.txt      # Dependencies list
├── .gitignore           # Include venv/ in .gitignore
└── README.md

# .gitignore should contain:
venv/
*.pyc
__pycache__/
.env
```

### 4. Pagination Pattern
```python
def get_all_vaults_paginated(client):
    page = 0
    all_vaults = []
    
    while True:
        response = client.get_all_vaults(page=page, perPage=100)
        all_vaults.extend(response['data'])
        
        if not response['pagination'].get('hasNext', False):
            break
        page += 1
    
    return all_vaults
```

### 5. Error Handling Pattern
```python
def safe_api_call(client, method, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return getattr(client, method)(*args, **kwargs)
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
        except HttpResponseError as e:
            print(f"HTTP Error: {e.status_code} - {e.message}")
            raise
```

### 6. Network Validation

**IMPORTANT: Network list changes frequently. Always validate against live API data.**

```python
def get_supported_networks(client):
    """Get current supported networks from dedicated API endpoint"""
    try:
        # Use the dedicated networks endpoint - most efficient
        response = client.get_networks()  # Assuming this method exists in SDK
        return [network['name'] for network in response]
    except AttributeError:
        # If SDK doesn't have get_networks method, make direct API call
        try:
            import requests
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
```

## Common Use Cases

### 1. Find Best Yield Opportunities

**🚨 CREDIT-EFFICIENT APPROACH: Use the dedicated deposit options endpoint**

```python
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

# ❌ WRONG - Don't do this (wastes credits):
# def find_best_yields_wrong(client, asset_symbol='USDC', min_apy=0.03):
#     vaults = client.get_all_vaults(assetSymbol=asset_symbol)  # Fetches ALL vaults
#     return [v for v in vaults['data'] if v['apy']['total'] >= min_apy]  # Filters in memory
```

**JavaScript Example:**
```javascript
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
```

### 2. Portfolio Analysis
```python
def analyze_portfolio(client, user_address):
    positions = client.get_positions(user_address)
    idle_assets = client.get_idle_assets(user_address)
    
    total_earning = sum(
        float(pos['asset']['balanceUsd']) for pos in positions['data']
    )
    total_idle = sum(
        float(asset['balanceUsd']) for asset in idle_assets['data']
    )
    
    return {
        'total_earning': total_earning,
        'total_idle': total_idle,
        'efficiency': total_earning / (total_earning + total_idle)
    }
```

### 3. Transaction Preparation
```python
def prepare_deposit(client, user_address, network, vault_address, amount):
    actions = client.get_actions(
        action='deposit',
        user_address=user_address,
        network=network,
        vault_address=vault_address,
        amount=amount,
        simulate=True
    )
    
    return actions['actions']
```

## SDK Development Notes

### Python SDK
- **Repository**: https://github.com/WallfacerLabs/python-sdk
- **Package**: `vaultsfyi` on PyPI
- **Implementation**: Uses `requests` library with retry logic and proper error handling
- **Structure**: Modular design with separate client, exceptions, and utilities modules

### JavaScript SDK
- **Package**: `@vaultsfyi/sdk` on npm
- **Implementation**: Uses native `fetch` API with TypeScript support
- **Features**: OpenAPI-generated types for complete type safety
- **Requirements**: Node.js 16+ with ES modules support

### Key Implementation Details
- Both SDKs use the same API endpoints and response structures
- Both implement proper error handling and rate limiting
- Consistent method naming and parameter handling across languages

## Quick Reference

### Essential Commands
```bash
# Python SDK (always use virtual environment)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install vaultsfyi

# JavaScript SDK
npm install @vaultsfyi/sdk
```

### Common Patterns

**Python**
```python
# Initialize client
client = VaultsSdk(api_key="your_key")

# Get all vaults
vaults = client.get_all_vaults()

# Get user positions
positions = client.get_positions("0x...")

# Generate deposit transaction
actions = client.get_actions("deposit", "0x...", "mainnet", "0x...", amount="1000000")
```

**JavaScript**
```javascript
// Initialize client
import pkg from '@vaultsfyi/sdk';
const { VaultsSdk } = pkg;
const client = new VaultsSdk({ apiKey: process.env.VAULTS_FYI_API_KEY });

// Get all vaults (credit-efficient filtering)
const vaults = await client.getAllVaults({
  query: { network: 'mainnet', assetSymbol: 'USDC' }
});

// Get user positions
const positions = await client.getPositions({
  path: { userAddress: '0x...' }
});

// Generate deposit transaction
const actions = await client.getActions({
  path: {
    action: 'deposit',
    userAddress: '0x...',
    network: 'mainnet',
    vaultAddress: '0x...'
  },
  query: { amount: '1000000' }
});
```

This guide provides exact parameter specifications and response structures based on the actual SDK implementations to ensure accuracy and prevent API hallucinations.