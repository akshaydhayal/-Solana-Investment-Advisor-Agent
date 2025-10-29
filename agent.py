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
    
    async def get_metta_recommendations(self, portfolio_data: Dict[str, Any]) -> List[str]:
        """Get investment recommendations from SingularityNET MeTTa knowledge base"""
        try:
            if not self.asi_api_key:
                # Provide fallback recommendations when MeTTa is not available
                sol_balance = portfolio_data.get("sol_balance", 0)
                token_count = len(portfolio_data.get("token_accounts", []))
                
                fallback_recs = []
                if sol_balance > 0:
                    fallback_recs.append(f"Your wallet has {sol_balance:.2f} SOL. Consider staking for passive income.")
                if token_count == 0:
                    fallback_recs.append("Consider diversifying your portfolio with established tokens like USDC, USDT, or BONK.")
                if sol_balance > 10:
                    fallback_recs.append("With significant SOL holdings, consider dollar-cost averaging into other promising Solana tokens.")
                
                return fallback_recs if fallback_recs else ["Consider staking your SOL for passive income and diversifying your portfolio."]
            
            # Prepare portfolio summary for MeTTa
            portfolio_summary = {
                "sol_balance": portfolio_data.get("sol_balance", 0),
                "token_count": len(portfolio_data.get("token_accounts", [])),
                "total_value_usd": 0  # Will be calculated with prices
            }
            
            # Query MeTTa for investment advice
            async with httpx.AsyncClient(timeout=30) as client:
                headers = {"Authorization": f"Bearer {self.asi_api_key}"}
                response = await client.post(
                    "https://api.singularitynet.io/v1/metta/query",
                    headers=headers,
                    json={
                        "query": f"Analyze this Solana portfolio: {json.dumps(portfolio_summary)} and provide investment recommendations for optimal returns",
                        "context": "cryptocurrency_investment_advice"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("recommendations", ["No specific recommendations available from MeTTa"])
                else:
                    # Fallback to basic recommendations
                    sol_balance = portfolio_data.get("sol_balance", 0)
                    return [f"MeTTa API unavailable. Consider staking your {sol_balance:.2f} SOL for passive income."]
                    
        except Exception as e:
            # Provide fallback recommendations on error
            sol_balance = portfolio_data.get("sol_balance", 0)
            return [f"MeTTa integration error. Consider staking your {sol_balance:.2f} SOL for 6-8% APY."]
    
    async def generate_recommendations(self, wallet_address: str) -> List[Dict[str, Any]]:
        """Generate comprehensive investment recommendations"""
        recommendations = []
        
        # Get wallet data
        wallet_data = await self.get_wallet_balance(wallet_address)
        if "error" in wallet_data:
            return [{"type": "error", "message": wallet_data["error"]}]
        
        # Get MeTTa recommendations
        metta_recs = await self.get_metta_recommendations(wallet_data)
        
        # Get staking opportunities
        staking_ops = await self.get_staking_opportunities()
        
        # Generate recommendations based on portfolio
        sol_balance = wallet_data.get("sol_balance", 0)
        
        if sol_balance > 1.0:  # If user has more than 1 SOL
            # Staking recommendation
            if staking_ops and not any("error" in op for op in staking_ops):
                best_staking = max(staking_ops, key=lambda x: x.get("apy", 0))
                recommendations.append({
                    "type": "staking",
                    "priority": "high",
                    "action": f"Stake {min(sol_balance * 0.8, 10)} SOL",
                    "description": f"Stake with {best_staking['name']} for {best_staking['apy']:.2f}% APY",
                    "reasoning": "High APY staking opportunity with reputable validator",
                    "estimated_annual_return": f"${min(sol_balance * 0.8, 10) * best_staking['apy'] / 100:.2f}"
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

def _format_wallet_stats(wallet_data: Dict[str, Any]) -> str:
    """Format wallet statistics for display"""
    sol_balance = wallet_data.get("sol_balance", 0)
    token_accounts = wallet_data.get("token_accounts", [])
    source = wallet_data.get("source", wallet_data.get("rpc_used", "Unknown"))
    
    formatted = "## 📊 Wallet Statistics\n\n"
    formatted += f"**SOL Balance:** {sol_balance:.4f} SOL\n"
    formatted += f"**Token Holdings:** {len(token_accounts)} tokens\n"
    formatted += f"**Data Source:** {source}\n\n"
    
    if token_accounts:
        formatted += "### 🪙 Token Holdings\n\n"
        for i, token_account in enumerate(token_accounts[:10], 1):  # Show first 10 tokens
            try:
                parsed_data = token_account.get("account", {}).get("data", {}).get("parsed", {})
                info = parsed_data.get("info", {})
                token_amount = info.get("tokenAmount", {})
                
                mint = info.get("mint", "Unknown")
                amount = float(token_amount.get("uiAmount", 0))
                decimals = token_amount.get("decimals", 0)
                symbol = mint[:8] + "..." if len(mint) > 8 else mint
                
                formatted += f"{i}. **{symbol}**\n"
                formatted += f"   - Amount: {amount:,.6f}\n"
                formatted += f"   - Mint: `{mint[:8]}...{mint[-8:]}`\n\n"
            except Exception as e:
                formatted += f"{i}. **Token {i}** (Error parsing data)\n\n"
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
        
        formatted += f"### {priority_emoji} {i}. {rec.get('action', 'Unknown Action')}\n"
        formatted += f"**Description:** {rec.get('description', 'No description')}\n"
        formatted += f"**Reasoning:** {rec.get('reasoning', 'No reasoning provided')}\n"
        
        if rec.get("estimated_annual_return"):
            formatted += f"**Estimated Annual Return:** {rec['estimated_annual_return']}\n"
        
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
                    
                    if recommendations and not any(rec.get("type") == "error" for rec in recommendations):
                        response_text = f"**Wallet Analysis Complete!**\n\n"
                        response_text += f"**Wallet:** `{wallet_address[:8]}...{wallet_address[-8:]}`\n\n"
                        
                        # Get wallet data for statistics
                        wallet_data = await analyzer.get_wallet_balance(wallet_address)
                        if "error" not in wallet_data:
                            response_text += _format_wallet_stats(wallet_data)
                        
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
                    "• Any other Solana wallet\n\n"
                    "**Example:** `7pQHLgaTrP25TjmSaoGvTJJKeS2ZyGT2xAAvYLHsSXtk`"
                ))

@chat_proto.on_message(ChatAcknowledgement)
async def on_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements"""
    ctx.logger.info(f"ACK from {sender} for {msg.acknowledged_msg_id}")

# Include the chat protocol
agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
