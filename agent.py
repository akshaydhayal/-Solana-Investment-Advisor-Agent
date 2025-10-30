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
# Knowledge Graph Integration (Simplified for hosted environment)

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

# ===== Knowledge Graph Classes (Simplified for Hosted Environment) =====

class SolanaKnowledgeBase:
    """Simplified knowledge base for Solana investment analysis"""
    
    def __init__(self):
        # Asset information
        self.assets = {
            "SOL": {"name": "Solana", "category": "native_token", "risk": "medium", "description": "Solana native token, high performance blockchain"},
            "USDC": {"name": "USD Coin", "category": "stablecoin", "risk": "low", "description": "USD Coin, stablecoin for trading and DeFi"},
            "USDT": {"name": "Tether", "category": "stablecoin", "risk": "low", "description": "Tether, stablecoin for trading and DeFi"},
            "RAY": {"name": "Raydium", "category": "defi_token", "risk": "medium", "description": "Raydium token, DEX and AMM protocol"},
            "BONK": {"name": "BONK", "category": "memecoin", "risk": "high", "description": "BONK memecoin, high volatility, speculative"},
            "JUP": {"name": "Jupiter", "category": "defi_token", "risk": "medium", "description": "Jupiter token, DEX aggregator"},
            "ORCA": {"name": "Orca", "category": "defi_token", "risk": "medium", "description": "Orca token, user-friendly DEX"},
            "MNGO": {"name": "Mango", "category": "defi_token", "risk": "medium", "description": "Mango token, lending protocol"}
        }
        
        # Staking strategies
        self.staking_strategies = {
            "small": "Under $1000, stake 50-70% with Solana Foundation for stability",
            "medium": "$1000-$10000, diversify staking across validators",
            "large": "Over $10000, use liquid staking and DeFi strategies"
        }
        
        # Investment allocations
        self.allocations = {
            "conservative": "70% SOL staking, 20% stablecoins, 10% DeFi",
            "balanced": "50% SOL staking, 30% DeFi tokens, 20% stablecoins",
            "aggressive": "30% SOL staking, 50% DeFi tokens, 20% memecoins"
        }
        
        # Market conditions
        self.market_strategies = {
            "bull_market": "Focus on growth tokens, reduce stablecoin allocation",
            "bear_market": "Increase stablecoin allocation, focus on staking",
            "sideways": "DCA strategies, yield farming, balanced allocation"
        }
        
        print("✅ Solana Knowledge Base initialized with comprehensive investment data")
    
    def get_asset_info(self, symbol: str) -> str:
        """Get asset information"""
        asset = self.assets.get(symbol.upper(), {})
        return asset.get("description", f"Unknown asset: {symbol}")
    
    def get_risk_level(self, symbol: str) -> str:
        """Get risk level for asset"""
        asset = self.assets.get(symbol.upper(), {})
        return asset.get("risk", "unknown")
    
    def get_staking_recommendation(self, portfolio_value: float) -> str:
        """Get staking recommendation based on portfolio size"""
        if portfolio_value < 1000:
            return self.staking_strategies["small"]
        elif portfolio_value < 10000:
            return self.staking_strategies["medium"]
        else:
            return self.staking_strategies["large"]
    
    def get_allocation_strategy(self, risk_tolerance: str) -> str:
        """Get allocation strategy based on risk tolerance"""
        return self.allocations.get(risk_tolerance, self.allocations["balanced"])
    
    def get_market_strategy(self, market_trend: str) -> str:
        """Get market-based strategy"""
        return self.market_strategies.get(market_trend, self.market_strategies["sideways"])

class KnowledgeProcessor:
    """Processes investment queries using simplified knowledge base"""
    
    def __init__(self):
        self.knowledge = SolanaKnowledgeBase()
    
    def analyze_portfolio(self, wallet_data: dict, zerion_data: dict = None, market_data: dict = None):
        """Analyze portfolio using knowledge base"""
        
        try:
            # Prepare portfolio data for analysis
            portfolio_data = {
                "portfolio_value": 0,
                "assets": [],
                "risk_tolerance": "balanced"
            }
            
            # Extract portfolio value
            if zerion_data and "error" not in zerion_data:
                portfolio_value = zerion_data.get("total_value_usd", 0)
                portfolio_data["portfolio_value"] = portfolio_value
                
                # Determine risk tolerance based on portfolio size
                if portfolio_value < 1000:
                    portfolio_data["risk_tolerance"] = "conservative"
                elif portfolio_value > 10000:
                    portfolio_data["risk_tolerance"] = "aggressive"
            
            # Extract assets from wallet data
            token_accounts = wallet_data.get("token_accounts", [])
            for token_account in token_accounts:
                try:
                    parsed_data = token_account.get("account", {}).get("data", {}).get("parsed", {})
                    info = parsed_data.get("info", {})
                    token_amount = info.get("tokenAmount", {})
                    
                    mint = info.get("mint", "")
                    amount = float(token_amount.get("uiAmount", 0))
                    
                    if amount > 0:
                        symbol = self._identify_token_symbol(mint)
                        portfolio_data["assets"].append({
                            "symbol": symbol,
                            "mint": mint,
                            "amount": amount
                        })
                except:
                    continue
            
            # Add SOL if present
            sol_balance = wallet_data.get("sol_balance", 0)
            if sol_balance > 0:
                portfolio_data["assets"].append({
                    "symbol": "SOL",
                    "mint": "11111111111111111111111111111111",
                    "amount": sol_balance
                })
            
            # Prepare market data
            market_context = {
                "market_trend": market_data.get("market_trend", "neutral") if market_data else "neutral",
                "price_change_7d": market_data.get("price_change_7d", 0) if market_data else 0
            }
            
            # Get insights from knowledge base
            insights = self._get_investment_insights(portfolio_data, market_context)
            
            return {
                "insights": insights,
                "portfolio_analysis": portfolio_data,
                "recommendations": self._generate_knowledge_recommendations(portfolio_data, market_context)
            }
            
        except Exception as e:
            print(f"Error in knowledge portfolio analysis: {str(e)}")
            return {
                "insights": ["Knowledge base analysis failed"],
                "portfolio_analysis": {},
                "recommendations": []
            }
    
    def _identify_token_symbol(self, mint: str) -> str:
        """Identify token symbol from mint address"""
        token_map = {
            "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
            "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT",
            "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": "BONK",
            "So11111111111111111111111111111111111111112": "SOL",
            "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R": "RAY",
            "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN": "JUP",
            "orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE": "ORCA",
            "MangoCzJ36AjZyKwVj3VnYU4GOnOGMVzVhR7c3SBF9Qi": "MNGO"
        }
        return token_map.get(mint, mint[:8] + "...")
    
    def _get_investment_insights(self, portfolio_data: dict, market_data: dict):
        """Get comprehensive investment insights using knowledge base"""
        insights = []
        
        try:
            # Analyze each asset in portfolio
            for asset in portfolio_data.get("assets", []):
                asset_name = asset.get("symbol", "").upper()
                
                # Get asset information
                asset_info = self.knowledge.get_asset_info(asset_name)
                if asset_info:
                    insights.append(f"Asset {asset_name}: {asset_info}")
                
                # Get risk assessment
                risk_level = self.knowledge.get_risk_level(asset_name)
                if risk_level != "unknown":
                    insights.append(f"Risk level for {asset_name}: {risk_level}")
            
            # Get staking recommendations
            staking_rec = self.knowledge.get_staking_recommendation(portfolio_data.get("portfolio_value", 0))
            if staking_rec:
                insights.append(f"Staking strategy: {staking_rec}")
            
            # Get DeFi strategies
            defi_strategy = self.knowledge.get_allocation_strategy(portfolio_data.get("risk_tolerance", "balanced"))
            if defi_strategy:
                insights.append(f"DeFi allocation: {defi_strategy}")
            
            # Get market-based strategies
            market_strategy = self.knowledge.get_market_strategy(market_data.get("market_trend", "neutral"))
            if market_strategy:
                insights.append(f"Market strategy: {market_strategy}")
            
            return insights
            
        except Exception as e:
            print(f"Error getting investment insights: {str(e)}")
            return ["Knowledge base analysis temporarily unavailable"]
    
    def _generate_knowledge_recommendations(self, portfolio_data: dict, market_context: dict):
        """Generate recommendations based on knowledge base"""
        recommendations = []
        
        try:
            # Get staking recommendations
            staking_rec = self.knowledge.get_staking_recommendation(portfolio_data.get("portfolio_value", 0))
            if staking_rec:
                recommendations.append({
                    "type": "staking",
                    "priority": "high",
                    "action": "Optimize Staking Strategy",
                    "description": staking_rec,
                    "reasoning": "Based on your portfolio size and knowledge base analysis"
                })
            
            # Get DeFi strategies
            defi_strategy = self.knowledge.get_allocation_strategy(portfolio_data.get("risk_tolerance", "balanced"))
            if defi_strategy:
                recommendations.append({
                    "type": "defi",
                    "priority": "medium",
                    "action": "DeFi Allocation Strategy",
                    "description": defi_strategy,
                    "reasoning": "Knowledge base suggests optimal DeFi allocation"
                })
            
            # Get market-based strategies
            market_strategy = self.knowledge.get_market_strategy(market_context.get("market_trend", "neutral"))
            if market_strategy:
                recommendations.append({
                    "type": "market_timing",
                    "priority": "medium",
                    "action": "Market-Based Strategy",
                    "description": market_strategy,
                    "reasoning": "Current market conditions suggest this approach"
                })
            
            return recommendations
            
        except Exception as e:
            print(f"Error generating knowledge recommendations: {str(e)}")
            return []

class SolanaWalletAnalyzer:
    """Analyzes Solana wallet data and provides investment recommendations"""
    
    def __init__(self):
        self.asi_api_key = ASI_ONE_API_KEY
        self.zerion_api_key = ZERION_API_KEY
        self.rpc_urls = SOLANA_RPC_URLS
        self.knowledge_processor = KnowledgeProcessor()
    
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

    async def get_knowledge_recommendations(self, portfolio_data: Dict[str, Any], zerion_data: Dict[str, Any] = None) -> List[str]:
        """Get investment recommendations from knowledge base"""
        try:
            # Get market data for better analysis
            market_data = await self.get_market_data()
            
            # Use knowledge processor for intelligent analysis
            knowledge_analysis = self.knowledge_processor.analyze_portfolio(portfolio_data, zerion_data, market_data)
            
            # Extract insights and recommendations
            insights = knowledge_analysis.get("insights", [])
            knowledge_recommendations = knowledge_analysis.get("recommendations", [])
            
            # Convert knowledge recommendations to string format
            recommendations = []
            
            # Add knowledge insights
            for insight in insights[:3]:  # Limit to 3 insights
                recommendations.append(f"🧠 Knowledge Insight: {insight}")
            
            # Add knowledge recommendations
            for rec in knowledge_recommendations[:3]:  # Limit to 3 recommendations
                if isinstance(rec, dict):
                    recommendations.append(f"🎯 {rec.get('action', 'Recommendation')}: {rec.get('description', 'No description')}")
                else:
                    recommendations.append(f"🎯 Knowledge Recommendation: {rec}")
            
            # Fallback to basic recommendations if knowledge base fails
            if not recommendations:
                sol_balance = portfolio_data.get("sol_balance", 0)
                token_count = len(portfolio_data.get("token_accounts", []))
                
                if sol_balance > 0:
                    recommendations.append(f"Consider staking your {sol_balance:.2f} SOL for 6-8% APY using knowledge base insights.")
                
                if token_count < 3:
                    recommendations.append("Diversify your portfolio with more tokens based on risk analysis.")
                
                recommendations.append("Use knowledge base for advanced DeFi strategy optimization.")
            
            return recommendations[:5]  # Limit to 5 recommendations
                    
        except Exception as e:
            print(f"Knowledge recommendations failed: {str(e)}")
            # Provide basic fallback recommendations on error
            sol_balance = portfolio_data.get("sol_balance", 0)
            return [f"Knowledge analysis error. Consider staking your {sol_balance:.2f} SOL for 6-8% APY."]
    
    async def generate_recommendations(self, wallet_address: str) -> List[Dict[str, Any]]:
        """Generate comprehensive investment recommendations"""
        recommendations = []
        
        # Get wallet data
        wallet_data = await self.get_wallet_balance(wallet_address)
        if "error" in wallet_data:
            return [{"type": "error", "message": wallet_data["error"]}]
        
        # Get Zerion portfolio data
        zerion_data = await self.get_zerion_portfolio(wallet_address)
        
        # Get knowledge recommendations with Zerion data
        knowledge_recs = await self.get_knowledge_recommendations(wallet_data, zerion_data)
        
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
        
        # Add knowledge recommendations
        for rec in knowledge_recs:
            if not rec.startswith("ASI API key") and not rec.startswith("Failed"):
                recommendations.append({
                    "type": "knowledge_advice",
                    "priority": "medium",
                    "action": "Follow Knowledge guidance",
                    "description": rec,
                    "reasoning": "AI-powered recommendation from knowledge base analysis"
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

def _format_wallet_stats(wallet_data: Dict[str, Any], zerion_data: Dict[str, Any] = None, zerion_positions: List[Dict[str, Any]] = None, knowledge_insights: List[str] = None) -> str:
    """Format wallet statistics for display"""
    sol_balance = wallet_data.get("sol_balance", 0)
    token_accounts = wallet_data.get("token_accounts", [])
    source = wallet_data.get("source", wallet_data.get("rpc_used", "Unknown"))
    
    formatted = "## 📊 Wallet Statistics\n\n"
    
    # Basic blockchain data
    formatted += f"**SOL Balance:** {sol_balance:.4f} SOL\n"
    formatted += f"**Token Holdings:** {len(token_accounts)} tokens\n\n"
    
    # Knowledge Base Insights
    if knowledge_insights and len(knowledge_insights) > 0:
        formatted += "### 🧠 Knowledge Base Analysis\n\n"
        for insight in knowledge_insights[:3]:  # Show top 3 insights
            formatted += f"• {insight}\n"
        formatted += "\n"
    
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
                    
                    # Get wallet data, Zerion portfolio, and Zerion positions for statistics
                    wallet_data = await analyzer.get_wallet_balance(wallet_address)
                    zerion_data = await analyzer.get_zerion_portfolio(wallet_address)
                    zerion_positions = await analyzer.get_zerion_positions(wallet_address)
                    
                    # Get knowledge base insights
                    knowledge_analysis = analyzer.knowledge_processor.analyze_portfolio(wallet_data, zerion_data, await analyzer.get_market_data())
                    knowledge_insights = knowledge_analysis.get("insights", [])
                    
                    # Get recommendations
                    recommendations = await analyzer.generate_recommendations(wallet_address)
                    
                    # Debug logging
                    ctx.logger.info(f"Zerion positions fetched: {len(zerion_positions) if zerion_positions else 0} positions")
                    ctx.logger.info(f"Knowledge insights generated: {len(knowledge_insights)} insights")
                    if zerion_positions and len(zerion_positions) > 0:
                        ctx.logger.info(f"First position: {zerion_positions[0].get('symbol', 'Unknown')} - ${zerion_positions[0].get('value_usd', 0)}")
                    else:
                        ctx.logger.warning("Zerion positions is empty or None - will fallback to basic token data")
                    
                    if recommendations and not any(rec.get("type") == "error" for rec in recommendations):
                        response_text = f"**Wallet Analysis Complete!**\n\n"
                        response_text += f"**Wallet:** `{wallet_address[:8]}...{wallet_address[-8:]}`\n\n"
                        
                        if "error" not in wallet_data:
                            response_text += _format_wallet_stats(wallet_data, zerion_data, zerion_positions, knowledge_insights)
                        
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
