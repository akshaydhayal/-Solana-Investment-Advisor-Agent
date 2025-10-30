"""
MeTTa Query Processor for Solana Investment Advisor
Handles complex queries and reasoning using the MeTTa knowledge graph
"""

from metta import MeTTa
from knowledge import initialize_solana_knowledge_graph, query_solana_knowledge, get_investment_insights

class MeTTAProcessor:
    """Processes investment queries using MeTTa knowledge graph"""
    
    def __init__(self):
        self.metta = MeTTa()
        initialize_solana_knowledge_graph(self.metta)
    
    def analyze_portfolio(self, wallet_data: dict, zerion_data: dict = None, market_data: dict = None):
        """Analyze portfolio using MeTTa knowledge graph"""
        
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
                        # Try to identify token symbol
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
            
            # Get insights from knowledge graph
            insights = get_investment_insights(self.metta, portfolio_data, market_context)
            
            return {
                "insights": insights,
                "portfolio_analysis": portfolio_data,
                "recommendations": self._generate_metta_recommendations(portfolio_data, market_context)
            }
            
        except Exception as e:
            print(f"Error in MeTTa portfolio analysis: {str(e)}")
            return {
                "insights": ["Knowledge graph analysis failed"],
                "portfolio_analysis": {},
                "recommendations": []
            }
    
    def _identify_token_symbol(self, mint: str) -> str:
        """Identify token symbol from mint address"""
        
        # Common Solana token mints
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
    
    def _generate_metta_recommendations(self, portfolio_data: dict, market_context: dict):
        """Generate recommendations based on MeTTa knowledge graph"""
        
        recommendations = []
        
        try:
            # Get staking recommendations
            staking_recs = query_solana_knowledge(self.metta, "staking_recommendations", context=portfolio_data)
            if staking_recs:
                recommendations.append({
                    "type": "staking",
                    "priority": "high",
                    "action": "Optimize Staking Strategy",
                    "description": staking_recs[0],
                    "reasoning": "Based on your portfolio size and MeTTa knowledge graph analysis"
                })
            
            # Get DeFi strategies
            defi_strategies = query_solana_knowledge(self.metta, "defi_strategies", context=portfolio_data)
            if defi_strategies:
                recommendations.append({
                    "type": "defi",
                    "priority": "medium",
                    "action": "DeFi Allocation Strategy",
                    "description": defi_strategies[0],
                    "reasoning": "MeTTa knowledge graph suggests optimal DeFi allocation"
                })
            
            # Get market-based strategies
            market_strategies = query_solana_knowledge(self.metta, "market_conditions", context=market_context)
            if market_strategies:
                recommendations.append({
                    "type": "market_timing",
                    "priority": "medium",
                    "action": "Market-Based Strategy",
                    "description": market_strategies[0],
                    "reasoning": "Current market conditions suggest this approach"
                })
            
            # Get yield strategies
            yield_strategies = query_solana_knowledge(self.metta, "yield_strategies")
            if yield_strategies:
                recommendations.append({
                    "type": "yield_farming",
                    "priority": "medium",
                    "action": "Yield Optimization",
                    "description": yield_strategies[0],
                    "reasoning": "MeTTa knowledge graph identifies yield opportunities"
                })
            
            # Risk management recommendations
            risk_mitigation = query_solana_knowledge(self.metta, "risk_mitigation", context={"risk_type": "high_volatility"})
            if risk_mitigation:
                recommendations.append({
                    "type": "risk_management",
                    "priority": "high",
                    "action": "Risk Mitigation",
                    "description": risk_mitigation[0],
                    "reasoning": "MeTTa knowledge graph recommends risk management strategies"
                })
            
            return recommendations
            
        except Exception as e:
            print(f"Error generating MeTTa recommendations: {str(e)}")
            return []
    
    def query_asset_knowledge(self, asset_symbol: str):
        """Query specific asset knowledge"""
        
        try:
            asset_info = query_solana_knowledge(self.metta, "asset_info", asset_symbol.upper())
            risk_level = query_solana_knowledge(self.metta, "risk_assessment", asset_symbol.upper())
            
            return {
                "asset_info": asset_info[0] if asset_info else "No information available",
                "risk_level": risk_level[0] if risk_level else "Unknown"
            }
            
        except Exception as e:
            print(f"Error querying asset knowledge: {str(e)}")
            return {"asset_info": "Query failed", "risk_level": "Unknown"}
    
    def get_protocol_recommendations(self, protocol_type: str = "dex"):
        """Get protocol recommendations based on type"""
        
        try:
            query_str = f'!(match &self (protocol_type $protocol {protocol_type}) $protocol)'
            results = self.metta.run(query_str)
            
            protocols = []
            for protocol in results:
                if isinstance(protocol, str):
                    protocol_info = query_solana_knowledge(self.metta, "protocol_info", protocol)
                    protocols.append({
                        "name": protocol,
                        "info": protocol_info[0] if protocol_info else "No description available"
                    })
            
            return protocols
            
        except Exception as e:
            print(f"Error getting protocol recommendations: {str(e)}")
            return []
    
    def analyze_risk_factors(self, portfolio_assets: list):
        """Analyze risk factors for portfolio assets"""
        
        risk_analysis = []
        
        try:
            for asset in portfolio_assets:
                symbol = asset.get("symbol", "").upper()
                risk_level = query_solana_knowledge(self.metta, "risk_assessment", symbol)
                risk_factors = query_solana_knowledge(self.metta, "risk_factor", symbol)
                
                if risk_level or risk_factors:
                    risk_analysis.append({
                        "asset": symbol,
                        "risk_level": risk_level[0] if risk_level else "Unknown",
                        "risk_factors": risk_factors if risk_factors else []
                    })
            
            return risk_analysis
            
        except Exception as e:
            print(f"Error analyzing risk factors: {str(e)}")
            return []


