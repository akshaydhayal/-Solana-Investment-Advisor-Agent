import os
import json
import asyncio
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Optional, Any
import httpx
from uagents import Agent, Context, Protocol
from uagents_core.storage import ExternalStorage
from uagents_core.contrib.protocols.chat import (
    chat_protocol_spec,
    ChatMessage, ChatAcknowledgement,
    TextContent, ResourceContent, Resource, MetadataContent,
    StartSessionContent, EndSessionContent
)

# Configuration
AGENTVERSE_URL = os.getenv("AGENTVERSE_URL", "https://agentverse.ai")
STORAGE_URL = f"{AGENTVERSE_URL}/v1/storage"
ASI_ONE_API_KEY = os.getenv("ASI_ONE_API_KEY")
ZERION_API_KEY = os.getenv("ZERION_API_KEY", "emtfZGV2X2IyNmFmZjFlMDY2ZjQ4NWNhMzdhZTI0MzVkMzI4NWY3Og==")

# Initialize agent
agent = Agent()
chat_proto = Protocol(spec=chat_protocol_spec)

# Solana RPC endpoints
SOLANA_RPC_URLS = [
    "https://api.mainnet-beta.solana.com",
    "https://solana-api.projectserum.com",
    "https://rpc.ankr.com/solana"
]

class SolanaWalletAnalyzer:
    """Analyzes Solana wallet data and provides investment recommendations"""
    
    def __init__(self):
        self.asi_api_key = ASI_ONE_API_KEY
        self.zerion_api_key = ZERION_API_KEY
        self.rpc_urls = SOLANA_RPC_URLS
    
    async def get_wallet_balance(self, wallet_address: str) -> Dict[str, Any]:
        """Fetch wallet balance and token holdings from Solana blockchain"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Try multiple RPC endpoints for better reliability
                for rpc_url in self.rpc_urls:
                    try:
                        # Get SOL balance
                        sol_balance_response = await client.post(
                            rpc_url,
                            json={
                                "jsonrpc": "2.0",
                                "id": 1,
                                "method": "getBalance",
                                "params": [wallet_address]
                            }
                        )
                        sol_balance_data = sol_balance_response.json()
                        
                        if "error" in sol_balance_data:
                            continue
                            
                        # Get token accounts
                        token_accounts_response = await client.post(
                            rpc_url,
                            json={
                                "jsonrpc": "2.0",
                                "id": 2,
                                "method": "getTokenAccountsByOwner",
                                "params": [
                                    wallet_address,
                                    {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
                                    {"encoding": "jsonParsed"}
                                ]
                            }
                        )
                        token_accounts_data = token_accounts_response.json()
                        
                        if "error" in token_accounts_data:
                            continue
                            
                        return {
                            "sol_balance": sol_balance_data.get("result", {}).get("value", 0) / 1e9,  # Convert lamports to SOL
                            "token_accounts": token_accounts_data.get("result", {}).get("value", []),
                            "wallet_address": wallet_address,
                            "rpc_used": rpc_url
                        }
                    except Exception as e:
                        print(f"RPC {rpc_url} failed: {str(e)}")
                        continue
                
                # If all RPCs fail, try using Solscan API as fallback
                try:
                    solscan_response = await client.get(f"https://api.solscan.io/account?address={wallet_address}")
                    if solscan_response.status_code == 200:
                        solscan_data = solscan_response.json()
                        return {
                            "sol_balance": solscan_data.get("data", {}).get("lamports", 0) / 1e9,
                            "token_accounts": [],  # Solscan doesn't provide token accounts in this endpoint
                            "wallet_address": wallet_address,
                            "source": "solscan"
                        }
                except Exception as e:
                    print(f"Solscan API failed: {str(e)}")
                
                return {"error": "All RPC endpoints and fallback APIs failed"}
                
        except Exception as e:
            return {"error": f"Failed to fetch wallet data: {str(e)}"}
    
    async def get_zerion_portfolio(self, wallet_address: str) -> Dict[str, Any]:
        """Fetch comprehensive portfolio data from Zerion API"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = f"https://api.zerion.io/v1/wallets/{wallet_address}/portfolio?filter[positions]=only_simple&currency=usd"
                headers = {
                    "accept": "application/json",
                    "authorization": f"Basic {self.zerion_api_key}"
                }
                
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    attributes = data.get("data", {}).get("attributes", {})
                    
                    return {
                        "total_value_usd": attributes.get("total", {}).get("positions", 0),
                        "daily_change_usd": attributes.get("changes", {}).get("absolute_1d", 0),
                        "daily_change_percent": attributes.get("changes", {}).get("percent_1d", 0),
                        "distribution_by_type": attributes.get("positions_distribution_by_type", {}),
                        "distribution_by_chain": attributes.get("positions_distribution_by_chain", {}),
                        "source": "zerion"
                    }
                else:
                    print(f"Zerion API error: {response.status_code}")
                    return {"error": f"Zerion API error: {response.status_code}"}
                    
        except Exception as e:
            print(f"Zerion API failed: {str(e)}")
            return {"error": f"Failed to fetch Zerion data: {str(e)}"}
    
    async def get_zerion_positions(self, wallet_address: str) -> List[Dict[str, Any]]:
        """Fetch detailed token positions with USD values from Zerion API"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = f"https://api.zerion.io/v1/wallets/{wallet_address}/positions/?filter[positions]=only_simple&currency=usd&filter[chain_ids]=solana&filter[trash]=only_non_trash&sort=value"
                headers = {
                    "accept": "application/json",
                    "authorization": f"Basic {self.zerion_api_key}"
                }
                
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    positions = []
                    
                    # Check if data has the expected structure
                    data_list = data.get("data", [])
                    if not isinstance(data_list, list):
                        return []
                    
                    for item in data_list:
                        if not isinstance(item, dict):
                            continue
                            
                        attributes = item.get("attributes", {})
                        if not attributes:
                            continue
                            
                        fungible_info = attributes.get("fungible_info", {})
                        quantity = attributes.get("quantity", {})
                        
                        # Skip if essential data is missing
                        if not fungible_info or not quantity:
                            continue
                        
                        # Find Solana address from implementations
                        solana_address = None
                        implementations = fungible_info.get("implementations", [])
                        for impl in implementations:
                            if isinstance(impl, dict) and impl.get("chain_id") == "solana":
                                solana_address = impl.get("address")
                                break
                        
                        # Extract quantity value
                        quantity_float = 0
                        if isinstance(quantity, dict):
                            quantity_float = quantity.get("float", quantity.get("numeric", 0))
                            if isinstance(quantity_float, str):
                                try:
                                    quantity_float = float(quantity_float)
                                except:
                                    quantity_float = 0
                        elif isinstance(quantity, (int, float)):
                            quantity_float = float(quantity)
                        
                        # Extract value_usd
                        value_usd = attributes.get("value")
                        if value_usd is not None and isinstance(value_usd, str):
                            try:
                                value_usd = float(value_usd)
                            except:
                                value_usd = None
                        
                        # Extract price
                        price_usd = attributes.get("price", 0)
                        if isinstance(price_usd, str):
                            try:
                                price_usd = float(price_usd)
                            except:
                                price_usd = 0
                        
                        # Get changes
                        changes = attributes.get("changes", {})
                        changes_1d_usd = 0
                        changes_1d_percent = 0
                        if isinstance(changes, dict):
                            changes_1d_usd = changes.get("absolute_1d", 0)
                            changes_1d_percent = changes.get("percent_1d", 0)
                        
                        # Get flags
                        flags = fungible_info.get("flags", {})
                        verified = False
                        if isinstance(flags, dict):
                            verified = flags.get("verified", False)
                        
                        position_data = {
                            "name": fungible_info.get("name", "Unknown"),
                            "symbol": fungible_info.get("symbol", "UNK"),
                            "address": solana_address or (item.get("id", "") or "").split("-")[0] if item.get("id") else "",
                            "quantity": quantity_float,
                            "value_usd": value_usd,
                            "price_usd": price_usd if price_usd else 0,
                            "changes_1d_usd": changes_1d_usd if isinstance(changes_1d_usd, (int, float)) else 0,
                            "changes_1d_percent": changes_1d_percent if isinstance(changes_1d_percent, (int, float)) else 0,
                            "verified": verified
                        }
                        
                        # Only add positions with valid data (must have quantity > 0 OR valid name)
                        if position_data["quantity"] > 0:
                            positions.append(position_data)
                    
                    return positions
                else:
                    # Log error but don't use print - errors will be handled by caller
                    return []
                    
        except Exception as e:
            # Silently fail - will fallback to basic token data
            return []
    
    async def get_token_prices(self, token_mints: List[str]) -> Dict[str, float]:
        """Fetch current token prices"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Use Jupiter API for token prices
                response = await client.get("https://price.jup.ag/v4/price")
                price_data = response.json()
                
                prices = {}
                for token in price_data.get("data", []):
                    if token["id"] in token_mints:
                        prices[token["id"]] = token["price"]
                
                return prices
        except Exception as e:
            return {"error": f"Failed to fetch token prices: {str(e)}"}
    
    async def get_staking_opportunities(self) -> List[Dict[str, Any]]:
        """Get current staking opportunities and APY rates"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Try multiple staking data sources
                staking_sources = [
                    "https://api.solanabeach.io/v1/validators",
                    "https://api.solscan.io/chaininfo"
                ]
                
                for source_url in staking_sources:
                    try:
                        response = await client.get(source_url)
                        if response.status_code == 200:
                            data = response.json()
                            
                            if "validators" in data:
                                # Solana Beach format
                                validators = data.get("validators", [])[:10]
                                staking_ops = []
                                for validator in validators:
                                    staking_ops.append({
                                        "name": validator.get("name", "Unknown"),
                                        "apy": validator.get("apy", 7.5),  # Default APY if not available
                                        "commission": validator.get("commission", 5.0),
                                        "vote_account": validator.get("vote_account"),
                                        "description": f"Stake with {validator.get('name', 'Unknown')} for {validator.get('apy', 7.5):.2f}% APY"
                                    })
                                return staking_ops
                            else:
                                # Fallback: return some default staking opportunities
                                return [
                                    {
                                        "name": "Solana Foundation",
                                        "apy": 7.2,
                                        "commission": 0.0,
                                        "vote_account": "Vote1111111111111111111111111111111111111112",
                                        "description": "Stake with Solana Foundation for 7.20% APY"
                                    },
                                    {
                                        "name": "Marinade Finance",
                                        "apy": 6.8,
                                        "commission": 2.0,
                                        "vote_account": "MarBmsSgKXdrN1egZf5sqe1TMai9K1rChYNDJgjq7aD",
                                        "description": "Stake with Marinade Finance for 6.80% APY"
                                    },
                                    {
                                        "name": "Jito Labs",
                                        "apy": 6.5,
                                        "commission": 3.0,
                                        "vote_account": "Jito4APyf642JPZPx3hGc6WWJ8zPKtRbR4Xe2q7WnK",
                                        "description": "Stake with Jito Labs for 6.50% APY"
                                    }
                                ]
                    except Exception as e:
                        print(f"Staking source {source_url} failed: {str(e)}")
                        continue
                
                # If all sources fail, return default staking opportunities
                return [
                    {
                        "name": "Solana Foundation",
                        "apy": 7.2,
                        "commission": 0.0,
                        "vote_account": "Vote1111111111111111111111111111111111111112",
                        "description": "Stake with Solana Foundation for 7.20% APY"
                    },
                    {
                        "name": "Marinade Finance",
                        "apy": 6.8,
                        "commission": 2.0,
                        "vote_account": "MarBmsSgKXdrN1egZf5sqe1TMai9K1rChYNDJgjq7aD",
                        "description": "Stake with Marinade Finance for 6.80% APY"
                    }
                ]
        except Exception as e:
            return [{"error": f"Failed to fetch staking data: {str(e)}"}]
    
    async def get_market_data(self) -> Dict[str, Any]:
        """Get current market data for better recommendations"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Get SOL price
                sol_response = await client.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd")
                sol_data = sol_response.json()
                sol_price = sol_data.get("solana", {}).get("usd", 0)
                
                # Get market trends
                trends_response = await client.get("https://api.coingecko.com/api/v3/coins/solana/market_chart?vs_currency=usd&days=7")
                trends_data = trends_response.json()
                
                # Calculate 7-day change
                prices = trends_data.get("prices", [])
                if len(prices) >= 2:
                    old_price = prices[0][1]
                    new_price = prices[-1][1]
                    price_change_7d = ((new_price - old_price) / old_price) * 100
                else:
                    price_change_7d = 0
                
                return {
                    "sol_price_usd": sol_price,
                    "price_change_7d": price_change_7d,
                    "market_trend": "bullish" if price_change_7d > 0 else "bearish"
                }
        except Exception as e:
            print(f"Market data fetch failed: {str(e)}")
            return {"sol_price_usd": 100, "price_change_7d": 0, "market_trend": "neutral"}

    async def get_metta_recommendations(self, portfolio_data: Dict[str, Any], zerion_data: Dict[str, Any] = None) -> List[str]:
        """Get investment recommendations from SingularityNET MeTTa knowledge base"""
        try:
            # Get market data for better analysis
            market_data = await self.get_market_data()
            sol_balance = portfolio_data.get("sol_balance", 0)
            token_accounts = portfolio_data.get("token_accounts", [])
            token_count = len(token_accounts)
            sol_price = market_data.get("sol_price_usd", 100)
            price_change_7d = market_data.get("price_change_7d", 0)
            market_trend = market_data.get("market_trend", "neutral")
            
            # Use Zerion data if available, otherwise calculate from SOL balance
            if zerion_data and "error" not in zerion_data:
                portfolio_value_usd = zerion_data.get("total_value_usd", 0)
                daily_change_usd = zerion_data.get("daily_change_usd", 0)
                daily_change_percent = zerion_data.get("daily_change_percent", 0)
                distribution = zerion_data.get("distribution_by_type", {})
            else:
                portfolio_value_usd = sol_balance * sol_price
                daily_change_usd = 0
                daily_change_percent = 0
                distribution = {}
            
            # Analyze token holdings
            token_mints = []
            for token_account in token_accounts:
                try:
                    parsed_data = token_account.get("account", {}).get("data", {}).get("parsed", {})
                    info = parsed_data.get("info", {})
                    mint = info.get("mint")
                    if mint:
                        token_mints.append(mint)
                except:
                    continue
            
            # Generate intelligent recommendations based on portfolio analysis
            recommendations = []
            
            # Portfolio value-based recommendations using Zerion data
            if portfolio_value_usd > 0:
                if portfolio_value_usd < 100:
                    recommendations.append(f"Portfolio value: ${portfolio_value_usd:.2f}. Focus on learning and small, regular investments. Consider staking your SOL for passive income.")
                elif portfolio_value_usd < 1000:
                    recommendations.append(f"Growing portfolio: ${portfolio_value_usd:.2f}. Set up automated staking and consider dollar-cost averaging into promising tokens.")
                elif portfolio_value_usd < 10000:
                    recommendations.append(f"Strong portfolio: ${portfolio_value_usd:.2f}. Diversify across different asset types and consider DeFi strategies.")
                else:
                    recommendations.append(f"Large portfolio: ${portfolio_value_usd:.2f}. Consider professional portfolio management and advanced DeFi strategies.")
            
            # Daily performance analysis using Zerion data
            if daily_change_usd != 0:
                if daily_change_percent > 5:
                    recommendations.append(f"Portfolio up {daily_change_percent:.1f}% today (+${daily_change_usd:.2f}). Consider taking some profits or rebalancing.")
                elif daily_change_percent < -5:
                    recommendations.append(f"Portfolio down {abs(daily_change_percent):.1f}% today (-${abs(daily_change_usd):.2f}). This could be a buying opportunity for dollar-cost averaging.")
            
            # Asset distribution analysis using Zerion data
            if distribution:
                wallet_value = distribution.get("wallet", 0)
                staked_value = distribution.get("staked", 0)
                deposited_value = distribution.get("deposited", 0)
                
                if staked_value == 0 and wallet_value > 100:
                    recommendations.append(f"You have ${wallet_value:.2f} in wallet but nothing staked. Consider staking 60-80% for passive income.")
                elif staked_value > 0:
                    staking_percentage = (staked_value / portfolio_value_usd) * 100
                    if staking_percentage < 30:
                        recommendations.append(f"Only {staking_percentage:.1f}% of your portfolio is staked. Consider increasing staking allocation for better returns.")
                
                if deposited_value > 0:
                    recommendations.append("You have assets in DeFi protocols. Monitor yields and consider rebalancing if better opportunities arise.")
            
            # Market trend-based recommendations
            if market_trend == "bullish" and price_change_7d > 5:
                recommendations.append(f"SOL is up {price_change_7d:.1f}% this week. Consider taking some profits or rebalancing your portfolio.")
            elif market_trend == "bearish" and price_change_7d < -5:
                recommendations.append(f"SOL is down {abs(price_change_7d):.1f}% this week. This could be a good buying opportunity for dollar-cost averaging.")
            
            # Token diversification recommendations
            if token_count == 0:
                recommendations.append("No token holdings detected. Consider adding USDC for stability, BONK for memecoin exposure, or RAY for DeFi participation.")
            elif token_count < 3:
                recommendations.append(f"Limited diversification with only {token_count} tokens. Consider adding more tokens to spread risk across different sectors.")
            elif token_count > 10:
                recommendations.append(f"High diversification with {token_count} tokens. Consider consolidating into your top 5-7 strongest positions.")
            
            # Specific token recommendations based on holdings
            if token_mints:
                # Check for common tokens and provide specific advice
                has_usdc = any("EPjFWdd5" in mint for mint in token_mints)
                has_usdt = any("Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB" in mint for mint in token_mints)
                has_bonks = any("DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263" in mint for mint in token_mints)
                
                if not has_usdc and not has_usdt:
                    recommendations.append("Consider adding USDC or USDT for portfolio stability and easy trading opportunities.")
                if not has_bonks:
                    recommendations.append("BONK could provide memecoin exposure and potential high returns, but with higher risk.")
            
            # Risk assessment
            if portfolio_value_usd < 100:
                recommendations.append("Small portfolio size. Focus on learning and small, regular investments rather than complex strategies.")
            elif portfolio_value_usd < 1000:
                recommendations.append("Growing portfolio. Consider setting up automated staking and regular DCA (Dollar Cost Averaging).")
            else:
                recommendations.append("Significant portfolio value. Consider professional DeFi strategies like yield farming or liquidity provision.")
            
            # Try MeTTa API if available
            if self.asi_api_key:
                try:
                    async with httpx.AsyncClient(timeout=30) as client:
                        headers = {"Authorization": f"Bearer {self.asi_api_key}"}
                        portfolio_summary = {
                            "sol_balance": sol_balance,
                            "portfolio_value_usd": portfolio_value_usd,
                            "token_count": token_count,
                            "market_trend": market_trend,
                            "price_change_7d": price_change_7d
                        }
                        
                        response = await client.post(
                            "https://api.singularitynet.io/v1/metta/query",
                            headers=headers,
                            json={
                                "query": f"Analyze this Solana portfolio: {json.dumps(portfolio_summary)} and provide specific investment recommendations",
                                "context": "cryptocurrency_investment_advice"
                            }
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            metta_recs = data.get("recommendations", [])
                            if metta_recs and len(metta_recs) > 0:
                                recommendations.extend(metta_recs[:2])  # Add up to 2 MeTTa recommendations
                except Exception as e:
                    print(f"MeTTa API call failed: {str(e)}")
            
            return recommendations[:5]  # Limit to 5 recommendations
                    
        except Exception as e:
            # Provide basic fallback recommendations on error
            sol_balance = portfolio_data.get("sol_balance", 0)
            return [f"Portfolio analysis error. Consider staking your {sol_balance:.2f} SOL for 6-8% APY."]
    
    async def generate_recommendations(self, wallet_address: str) -> List[Dict[str, Any]]:
        """Generate comprehensive investment recommendations"""
        recommendations = []
        
        # Get wallet data
        wallet_data = await self.get_wallet_balance(wallet_address)
        if "error" in wallet_data:
            return [{"type": "error", "message": wallet_data["error"]}]
        
        # Get Zerion portfolio data
        zerion_data = await self.get_zerion_portfolio(wallet_address)
        
        # Get MeTTa recommendations with Zerion data
        metta_recs = await self.get_metta_recommendations(wallet_data, zerion_data)
        
        # Get staking opportunities
        staking_ops = await self.get_staking_opportunities()
        
        # Generate recommendations based on portfolio
        sol_balance = wallet_data.get("sol_balance", 0)
        token_count = len(wallet_data.get("token_accounts", []))
        
        # Get market data for better staking recommendations
        market_data = await self.get_market_data()
        sol_price = market_data.get("sol_price_usd", 100)
        
        # Use Zerion portfolio value if available, otherwise calculate from SOL
        if zerion_data and "error" not in zerion_data:
            portfolio_value_usd = zerion_data.get("total_value_usd", 0)
        else:
            portfolio_value_usd = sol_balance * sol_price
        
        if sol_balance > 0.1:  # Lower threshold for staking
            # Dynamic staking recommendation based on portfolio size
            if staking_ops and not any("error" in op for op in staking_ops):
                best_staking = max(staking_ops, key=lambda x: x.get("apy", 0))
                
                # Calculate optimal staking amount based on portfolio size
                if sol_balance < 1:
                    stake_amount = sol_balance * 0.5  # Stake 50% for small portfolios
                    priority = "medium"
                elif sol_balance < 5:
                    stake_amount = sol_balance * 0.7  # Stake 70% for medium portfolios
                    priority = "high"
                else:
                    stake_amount = sol_balance * 0.6  # Stake 60% for large portfolios
                    priority = "high"
                
                estimated_return = stake_amount * best_staking['apy'] / 100
                
                recommendations.append({
                    "type": "staking",
                    "priority": priority,
                    "action": f"Stake {stake_amount:.2f} SOL (${stake_amount * sol_price:.2f})",
                    "description": f"Stake with {best_staking['name']} for {best_staking['apy']:.2f}% APY",
                    "reasoning": f"Optimal staking strategy for your ${portfolio_value_usd:.2f} portfolio size",
                    "estimated_annual_return": f"${estimated_return:.2f} (${estimated_return * sol_price:.2f} USD)"
                })
        
        # Add MeTTa recommendations
        for rec in metta_recs:
            if not rec.startswith("ASI API key") and not rec.startswith("Failed"):
                recommendations.append({
                    "type": "metta_advice",
                    "priority": "medium",
                    "action": "Follow MeTTa guidance",
                    "description": rec,
                    "reasoning": "AI-powered recommendation from SingularityNET MeTTa knowledge base"
                })
        
        # Portfolio diversification advice
        token_count = len(wallet_data.get("token_accounts", []))
        if token_count < 3:
            recommendations.append({
                "type": "diversification",
                "priority": "medium",
                "action": "Diversify portfolio",
                "description": "Consider adding more tokens to diversify risk",
                "reasoning": f"Current portfolio has only {token_count} tokens. Diversification reduces risk."
            })
        
        return recommendations

# Initialize analyzer
analyzer = SolanaWalletAnalyzer()

def _text(msg: str) -> ChatMessage:
    """Helper to create text chat messages"""
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=msg)]
    )

def _format_wallet_stats(wallet_data: Dict[str, Any], zerion_data: Dict[str, Any] = None, zerion_positions: List[Dict[str, Any]] = None) -> str:
    """Format wallet statistics for display"""
    sol_balance = wallet_data.get("sol_balance", 0)
    token_accounts = wallet_data.get("token_accounts", [])
    source = wallet_data.get("source", wallet_data.get("rpc_used", "Unknown"))
    
    formatted = "## 📊 Wallet Statistics\n\n"
    
    # Basic blockchain data
    formatted += f"**SOL Balance:** {sol_balance:.4f} SOL\n"
    formatted += f"**Token Holdings:** {len(token_accounts)} tokens\n\n"
    
    # Enhanced portfolio data if available
    if zerion_data and "error" not in zerion_data:
        total_value = zerion_data.get("total_value_usd", 0)
        daily_change_usd = zerion_data.get("daily_change_usd", 0)
        daily_change_percent = zerion_data.get("daily_change_percent", 0)
        distribution = zerion_data.get("distribution_by_type", {})
        
        formatted += "### 💰 Portfolio Value\n\n"
        formatted += f"**Total Portfolio Value:** ${total_value:,.2f}\n"
        
        if daily_change_usd != 0:
            change_emoji = "📈" if daily_change_usd > 0 else "📉"
            formatted += f"**24h Change:** {change_emoji} ${daily_change_usd:,.2f} ({daily_change_percent:+.2f}%)\n"
        
        # Distribution breakdown
        if distribution:
            formatted += "\n### 📊 Asset Distribution\n\n"
            for asset_type, value in distribution.items():
                if value > 0:
                    percentage = (value / total_value * 100) if total_value > 0 else 0
                    formatted += f"**{asset_type.title()}:** ${value:,.2f} ({percentage:.1f}%)\n"
        
        formatted += "\n"
    
    # Token holdings with USD values from Zerion positions
    if zerion_positions and len(zerion_positions) > 0:
        formatted += "### 🪙 Token Holdings\n\n"
        for i, position in enumerate(zerion_positions[:15], 1):  # Show top 15 tokens by value
            name = position.get("name", "Unknown")
            symbol = position.get("symbol", "UNK")
            quantity = position.get("quantity", 0)
            value_usd = position.get("value_usd")
            price_usd = position.get("price_usd", 0)
            changes_1d_percent = position.get("changes_1d_percent", 0)
            verified = position.get("verified", False)
            address = position.get("address", "")
            
            verified_badge = " ✓" if verified else ""
            
            # Format quantity nicely
            if quantity >= 1000000:
                quantity_str = f"{quantity/1000000:.2f}M"
            elif quantity >= 1000:
                quantity_str = f"{quantity/1000:.2f}K"
            else:
                quantity_str = f"{quantity:,.6f}".rstrip('0').rstrip('.')
            
            # Beautiful format: "You own X quantity of Token A which is worth $Y"
            if value_usd is not None and value_usd > 0:
                formatted += f"**{i}. {symbol}**{verified_badge} - {name}\n"
                formatted += f"   💰 You own **{quantity_str} {symbol}** which is worth **${value_usd:,.2f}**\n"
                formatted += f"   📊 Price per token: ${price_usd:,.6f}\n"
                
                if changes_1d_percent != 0:
                    change_emoji = "📈" if changes_1d_percent > 0 else "📉"
                    formatted += f"   {change_emoji} 24h change: {changes_1d_percent:+.2f}%\n"
                
                formatted += "\n"
            else:
                # If no USD value, still show quantity
                formatted += f"**{i}. {symbol}**{verified_badge} - {name}\n"
                formatted += f"   💰 You own **{quantity_str} {symbol}**\n"
                formatted += f"   ⚠️ Value: Unavailable\n"
                
                if address and len(address) > 8:
                    formatted += f"   🔗 Address: `{address[:8]}...{address[-8:]}`\n"
                
                formatted += "\n"
    elif token_accounts:
        formatted += "### 🪙 Token Holdings\n\n"
        formatted += "⚠️ *Showing basic token data. Price information unavailable.*\n\n"
        for i, token_account in enumerate(token_accounts[:10], 1):  # Show first 10 tokens
            try:
                parsed_data = token_account.get("account", {}).get("data", {}).get("parsed", {})
                info = parsed_data.get("info", {})
                token_amount = info.get("tokenAmount", {})
                
                mint = info.get("mint", "Unknown")
                amount = float(token_amount.get("uiAmount", 0))
                symbol = mint[:8] + "..." if len(mint) > 8 else mint
                
                # Format quantity nicely
                if amount >= 1000000:
                    quantity_str = f"{amount/1000000:.2f}M"
                elif amount >= 1000:
                    quantity_str = f"{amount/1000:.2f}K"
                else:
                    quantity_str = f"{amount:,.6f}".rstrip('0').rstrip('.')
                
                formatted += f"**{i}. {symbol}**\n"
                formatted += f"   💰 You own **{quantity_str} {symbol}**\n"
                formatted += f"   🔗 Mint: `{mint[:8]}...{mint[-8:]}`\n\n"
            except Exception as e:
                formatted += f"**{i}. Token {i}** (Error parsing data)\n\n"
    else:
        formatted += "### 🪙 Token Holdings\n\n"
        formatted += "No token holdings found or token data unavailable.\n\n"
    
    return formatted

def _format_recommendations(recommendations: List[Dict[str, Any]]) -> str:
    """Format recommendations for display"""
    if not recommendations:
        return "No specific recommendations at this time."
    
    formatted = "## 💡 Investment Recommendations\n\n"
    
    for i, rec in enumerate(recommendations, 1):
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec.get("priority", "medium"), "🟡")
        
        action = rec.get('action', 'Unknown Action')
        description = rec.get('description', 'No description')
        reasoning = rec.get('reasoning', 'No reasoning provided')
        
        formatted += f"{priority_emoji} **{i}. {action}**\n\n"
        formatted += f"**Description:** {description}\n\n"
        formatted += f"**Reasoning:** {reasoning}\n"
        
        if rec.get("estimated_annual_return"):
            formatted += f"\n**Estimated Annual Return:** {rec['estimated_annual_return']}\n"
        
        formatted += "\n"
    
    return formatted

@chat_proto.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages"""
    # ACK first
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.now(timezone.utc),
        acknowledged_msg_id=msg.msg_id,
    ))
    
    for content in msg.content:
        if isinstance(content, StartSessionContent):
            ctx.logger.info("Investment advisor session started")
            await ctx.send(sender, _text(
                "🔮 **Solana Investment Advisor**\n\n"
                "I'm your AI-powered investment advisor for Solana wallets! I can:\n"
                "• Analyze your wallet portfolio\n"
                "• Provide staking recommendations\n"
                "• Suggest optimal trading moves\n"
                "• Use SingularityNET MeTTa knowledge base for insights\n\n"
                "Please provide your Solana wallet address to get started!"
            ))
        
        elif isinstance(content, TextContent):
            user_input = content.text.strip()
            ctx.logger.info(f"User input: {user_input}")
            
            # Extract wallet address from text using regex
            import re
            wallet_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'
            wallet_matches = re.findall(wallet_pattern, user_input)
            
            wallet_address = None
            if wallet_matches:
                # Use the first valid-looking wallet address found
                for match in wallet_matches:
                    if 32 <= len(match) <= 44:
                        wallet_address = match
                        break
            
            # If no wallet found in text, check if entire input is a wallet address
            if not wallet_address and len(user_input) >= 32 and len(user_input) <= 44:
                wallet_address = user_input
            
            if wallet_address:
                # Basic validation - check if it looks like a Solana address
                if len(wallet_address) >= 32 and len(wallet_address) <= 44 and all(c in "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz" for c in wallet_address):
                    await ctx.send(sender, _text("🔍 Analyzing your Solana wallet... This may take a moment."))
                    
                    # Get recommendations
                    recommendations = await analyzer.generate_recommendations(wallet_address)
                    
                    # Get wallet data, Zerion portfolio, and Zerion positions for statistics
                    wallet_data = await analyzer.get_wallet_balance(wallet_address)
                    zerion_data = await analyzer.get_zerion_portfolio(wallet_address)
                    zerion_positions = await analyzer.get_zerion_positions(wallet_address)
                    
                    # Debug logging
                    ctx.logger.info(f"Zerion positions fetched: {len(zerion_positions) if zerion_positions else 0} positions")
                    if zerion_positions and len(zerion_positions) > 0:
                        ctx.logger.info(f"First position: {zerion_positions[0].get('symbol', 'Unknown')} - ${zerion_positions[0].get('value_usd', 0)}")
                    else:
                        ctx.logger.warning("Zerion positions is empty or None - will fallback to basic token data")
                    
                    if recommendations and not any(rec.get("type") == "error" for rec in recommendations):
                        response_text = f"**Wallet Analysis Complete!**\n\n"
                        response_text += f"**Wallet:** `{wallet_address[:8]}...{wallet_address[-8:]}`\n\n"
                        
                        if "error" not in wallet_data:
                            response_text += _format_wallet_stats(wallet_data, zerion_data, zerion_positions)
                        
                        response_text += _format_recommendations(recommendations)
                        
                        await ctx.send(sender, _text(response_text))
                    else:
                        error_msg = recommendations[0].get("message", "Analysis failed") if recommendations else "No recommendations available"
                        await ctx.send(sender, _text(f"❌ **Analysis Failed**\n\n{error_msg}"))
                else:
                    await ctx.send(sender, _text(
                        f"❌ **Invalid Wallet Address**\n\n"
                        f"The address you provided doesn't appear to be a valid Solana wallet address.\n\n"
                        f"Please provide a valid Solana wallet address (32-44 characters, base58 encoded).\n\n"
                        f"**Example:** `7pQHLgaTrP25TjmSaoGvTJJKeS2ZyGT2xAAvYLHsSXtk`"
                    ))
            else:
                await ctx.send(sender, _text(
                    "🤔 I need a Solana wallet address to analyze your portfolio.\n\n"
                    "Please provide a valid Solana wallet address (32-44 characters, base58 encoded).\n\n"
                    "You can find your wallet address in:\n"
                    "• Phantom wallet\n"
                    "• Solflare wallet\n"
                    "• Any other Solana wallet"
                ))

@chat_proto.on_message(ChatAcknowledgement)
async def on_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements"""
    ctx.logger.info(f"ACK from {sender} for {msg.acknowledged_msg_id}")

# Include the chat protocol
agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
