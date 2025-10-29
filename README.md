![tag:avmcp](https://img.shields.io/badge/avmcp-6C63FF)

# 🔮 Solana Investment Advisor Agent

An AI-powered investment advisor agent that analyzes Solana wallet portfolios and provides dynamic investment recommendations using on-chain data and SingularityNET's MeTTa knowledge base.

## Features

- **Wallet Analysis**: Fetches and analyzes Solana wallet balances and token holdings
- **Staking Recommendations**: Suggests optimal staking opportunities with APY calculations
- **AI-Powered Insights**: Leverages SingularityNET MeTTa knowledge base for investment advice
- **Real-time Data**: Uses live Solana blockchain data and current token prices
- **ASI1 Compatible**: Built with Agent Chat Protocol for seamless integration

## How It Works

1. **Portfolio Analysis**: The agent fetches your Solana wallet data including:
   - SOL balance
   - Token holdings and quantities
   - Current market values

2. **Staking Opportunities**: Identifies high-yield staking validators with:
   - Current APY rates
   - Validator reputation
   - Commission rates

3. **MeTTa Integration**: Queries SingularityNET's MeTTa knowledge base for:
   - Market trend analysis
   - Investment strategies
   - Risk assessment

4. **Smart Recommendations**: Generates actionable advice such as:
   - "Stake 5 SOL with Validator X for 7.2% APY"
   - "Diversify portfolio - add more tokens"
   - "Consider swapping USDC to SOL based on market conditions"

## Environment Variables

Create a `.env` file in the `hosted/` directory with:

```env
# Required: ASI One API Key for SingularityNET MeTTa integration
ASI_ONE_API_KEY=your_asi_one_api_key_here

# Optional: Agentverse URL (defaults to https://agentverse.ai)
AGENTVERSE_URL=https://agentverse.ai
```

## Usage

1. **Start the Agent**: The agent runs on Agentverse hosted environment
2. **Connect via Chat**: Use the Agentverse Chat UI to interact
3. **Provide Wallet Address**: Send your Solana wallet address
4. **Get Recommendations**: Receive personalized investment advice

### Example Interaction

```
User: 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM

Agent: 🔍 Analyzing your Solana wallet... This may take a moment.

Agent: ## 💡 Investment Recommendations

### 🔴 1. Stake 8.0 SOL
**Description:** Stake with Solana Beach Validator for 7.2% APY
**Reasoning:** High APY staking opportunity with reputable validator
**Estimated Annual Return:** $0.58

### 🟡 2. Follow MeTTa guidance
**Description:** Current market conditions favor SOL accumulation
**Reasoning:** AI-powered recommendation from SingularityNET MeTTa knowledge base

### 🟡 3. Diversify portfolio
**Description:** Consider adding more tokens to diversify risk
**Reasoning:** Current portfolio has only 2 tokens. Diversification reduces risk.
```

## Supported Operations

- ✅ Solana wallet balance analysis
- ✅ Token portfolio evaluation
- ✅ Staking opportunity identification
- ✅ MeTTa knowledge base integration
- ✅ Real-time price fetching
- ✅ Investment recommendation generation

## Limitations

- **Solana Only**: Currently supports Solana blockchain only
- **Read-Only**: Agent provides recommendations but doesn't execute trades
- **API Dependencies**: Requires ASI One API key for MeTTa integration
- **Network Dependent**: Performance depends on Solana RPC availability

## Technical Details

- **Protocol**: Agent Chat Protocol (ASI1 compatible)
- **Runtime**: Agentverse Hosted
- **Dependencies**: uAgents v0.22.9, httpx, base58
- **Data Sources**: Solana RPC, Jupiter API, Solana Beach API, SingularityNET MeTTa

## Security

- **No Private Keys**: Agent never requests or stores private keys
- **Read-Only Access**: Only analyzes public wallet data
- **Secure Communication**: Uses Agent Chat Protocol for encrypted messaging

## Testing

1. Deploy the agent to Agentverse
2. Connect via Agentverse Chat UI
3. Send a valid Solana wallet address
4. Verify recommendations are generated
5. Test with different wallet types and balances

## Support

For issues or questions:
- Check the Agentverse logs for error messages
- Verify your ASI One API key is valid
- Ensure the wallet address is a valid Solana address
- Check network connectivity to Solana RPC endpoints
