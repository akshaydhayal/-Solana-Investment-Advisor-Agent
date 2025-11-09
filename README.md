![tag:avmcp](https://img.shields.io/badge/avmcp-6C63FF)

# 🔮 Solana Investment Advisor Agent

An AI-powered investment advisor agent that analyzes Solana wallet portfolios and provides dynamic investment recommendations using on-chain data, Zerion API, and SingularityNET's MeTTa knowledge base.

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)
![tag:avmcp](https://img.shields.io/badge/avmcp-6C63FF)

Agent Live Link: [https://agentverse.ai/agents/details/agent1qvvzrxauw9rl78hahqps5u73c6kuay8ujrps3qscpzdeg62034sx7plnqwy/profile](https://agentverse.ai/agents/details/agent1qvvzrxauw9rl78hahqps5u73c6kuay8ujrps3qscpzdeg62034sx7plnqwy/profile)

## Features

- **🧠 MeTTa Knowledge Graph**: Advanced reasoning using structured knowledge about Solana ecosystem
- **📊 Comprehensive Portfolio Analysis**: Real-time wallet data with Zerion API integration
- **💰 Staking Optimization**: AI-powered staking recommendations based on portfolio size and risk
- **🎯 DeFi Strategy Guidance**: Intelligent suggestions for yield farming and liquidity provision
- **⚡ Real-time Market Data**: Live Solana blockchain data and current token prices
- **🔗 ASI1 Compatible**: Built with Agent Chat Protocol for seamless integration

## 📸 Demo

### Agent Chat Demo
![Agent Chat Demo Page](https://github.com/akshaydhayal/-Solana-Investment-Advisor-Agent/blob/main/demo.png)

## How It Works

1. **🧠 MeTTa Knowledge Graph Analysis**: 
   - Structured knowledge about Solana ecosystem, DeFi protocols, and investment strategies
   - Risk assessment based on asset categories and market conditions
   - Intelligent reasoning for portfolio optimization

2. **📊 Comprehensive Portfolio Analysis**: 
   - Real-time wallet data from Solana blockchain
   - Zerion API integration for detailed token positions and USD values
   - Market trend analysis and performance metrics

3. **💰 Advanced Staking Recommendations**: 
   - AI-powered staking strategies based on portfolio size and risk tolerance
   - Validator selection with APY optimization
   - Dynamic allocation recommendations

4. **🎯 DeFi Strategy Guidance**: 
   - Yield farming opportunities across protocols
   - Risk mitigation strategies
   - Portfolio diversification advice

5. **⚡ Smart Recommendations**: Generates actionable advice such as:
   - "Stake 14.8 SOL with Solana Foundation for 7.2% APY"
   - "Diversify with DeFi tokens based on MeTTa risk analysis"
   - "Consider yield farming on Raydium for additional returns"

## Environment Variables

Create a `.env` file in the `hosted/` directory with:

```env
# Required: ASI One API Key for SingularityNET MeTTa integration
ASI_ONE_API_KEY=your_asi_one_api_key_here

# Required: Zerion API Key for comprehensive portfolio data
ZERION_API_KEY=your_zerion_api_key_here

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
Analyse this Solana wallet : 7pQHLgaTrP25TjmSaoGvTJJKeS2ZyGT2xAAvYLHsSXtk

Wallet Analysis Complete!
Wallet: 7pQHLgaT...YLHsSXtk

📊 Wallet Statistics
SOL Balance: 24.5325 SOL Token Holdings: 6 tokens

🧠 Knowledge Base Analysis
• Asset AOXJNBWF...: Unknown asset: AOXJNBWF... • Asset BFK9UJLD...: Unknown asset: BFK9UJLD... • Asset HCGJUKRA...: Unknown asset: HCGJUKRA...

💰 Portfolio Value
Total Portfolio Value: 3,920.77∗∗24hChange:∗∗📈3,920.77∗∗24hChange:∗∗📈25.44 (+0.65%)

📊 Asset Distribution
Wallet: $3,920.77 (100.0%)

🪙 Token Holdings
1. SOL ✓ - Solana 💰 You own 24.531609 SOL which is worth **3,920.90∗
∗📊Pricepertoken:3,920.90∗∗📊Pricepertoken:159.830675 📈 24h change: +0.69%

2. USDC ✓ - USD Coin 💰 You own 1.001 USDC which is worth **1.00∗∗
📊Pricepertoken:1.00∗∗📊Pricepertoken:0.999255 📉 24h change: -0.10%

3. AAA - Artalicjaanton 💰 You own 10.00K AAA which is worth **0.18∗∗
📊Pricepertoken:0.18∗∗📊Pricepertoken:0.000018 📈 24h change: +1.63%

4. PTC - PitCoin 💰 You own 100 PTC which is worth **0.00∗∗
📊Pricepertoken:0.00∗∗📊Pricepertoken:0.000043 📈 24h change: +2.87%

5. RS - Ceylon 💰 You own 5 RS which is worth **0.00∗∗
📊Pricepertoken:0.00∗∗📊Pricepertoken:0.000001 📉 24h change: -0.97%

💡 Investment Recommendations

🔴 1. Stake 14.72 SOL ($2352.77)
Description: Stake with Solana Foundation for 7.20% APY
Reasoning: Optimal staking strategy for your $3920.77 portfolio size
Estimated Annual Return: 1.06(1.06(169.40 USD)

🟡 2. Follow Knowledge guidance
Description: 🧠 Knowledge Insight: Asset AOXJNBWF...: Unknown asset: AOXJNBWF...
Reasoning: AI-powered recommendation from knowledge base analysis

🟡 3. Follow Knowledge guidance
Description: 🧠 Knowledge Insight: Asset BFK9UJLD...: Unknown asset: BFK9UJLD...
Reasoning: AI-powered recommendation from knowledge base analysis

🟡 4. Follow Knowledge guidance
Description: 🧠 Knowledge Insight: Asset HCGJUKRA...: Unknown asset: HCGJUKRA...
Reasoning: AI-powered recommendation from knowledge base analysis

🟡 5. Follow Knowledge guidance
Description: 🎯 Optimize Staking Strategy: 1000−1000−10000, diversify staking across validators
Reasoning: AI-powered recommendation from knowledge base analysis

🟡 6. Follow Knowledge guidance
Description: 🎯 DeFi Allocation Strategy: 50% SOL staking, 30% DeFi tokens, 20% stablecoins
Reasoning: AI-powered recommendation from knowledge base analysis
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

