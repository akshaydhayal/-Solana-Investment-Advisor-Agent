"""
MeTTa Knowledge Graph for Solana Investment Advisor
Contains structured knowledge about Solana blockchain, DeFi protocols, staking, and investment strategies
"""

from metta import MeTTa, E, S, ValueAtom

def initialize_solana_knowledge_graph(metta: MeTTa):
    """Initialize the MeTTa knowledge graph with Solana-specific investment knowledge"""
    
    # ===== SOLANA ECOSYSTEM KNOWLEDGE =====
    
    # Solana Core Assets
    metta.space().add_atom(E(S("asset"), S("SOL"), ValueAtom("Solana native token, high performance blockchain")))
    metta.space().add_atom(E(S("asset"), S("USDC"), ValueAtom("USD Coin, stablecoin for trading and DeFi")))
    metta.space().add_atom(E(S("asset"), S("USDT"), ValueAtom("Tether, stablecoin for trading and DeFi")))
    metta.space().add_atom(E(S("asset"), S("RAY"), ValueAtom("Raydium token, DEX and AMM protocol")))
    metta.space().add_atom(E(S("asset"), S("BONK"), ValueAtom("BONK memecoin, high volatility, speculative")))
    metta.space().add_atom(E(S("asset"), S("JUP"), ValueAtom("Jupiter token, DEX aggregator")))
    metta.space().add_atom(E(S("asset"), S("ORCA"), ValueAtom("Orca token, user-friendly DEX")))
    metta.space().add_atom(E(S("asset"), S("MNGO"), ValueAtom("Mango token, lending protocol")))
    
    # Asset Categories
    metta.space().add_atom(E(S("category"), S("SOL"), S("native_token")))
    metta.space().add_atom(E(S("category"), S("USDC"), S("stablecoin")))
    metta.space().add_atom(E(S("category"), S("USDT"), S("stablecoin")))
    metta.space().add_atom(E(S("category"), S("RAY"), S("defi_token")))
    metta.space().add_atom(E(S("category"), S("BONK"), S("memecoin")))
    metta.space().add_atom(E(S("category"), S("JUP"), S("defi_token")))
    metta.space().add_atom(E(S("category"), S("ORCA"), S("defi_token")))
    metta.space().add_atom(E(S("category"), S("MNGO"), S("defi_token")))
    
    # Risk Levels
    metta.space().add_atom(E(S("risk_level"), S("SOL"), S("medium")))
    metta.space().add_atom(E(S("risk_level"), S("USDC"), S("low")))
    metta.space().add_atom(E(S("risk_level"), S("USDT"), S("low")))
    metta.space().add_atom(E(S("risk_level"), S("RAY"), S("medium")))
    metta.space().add_atom(E(S("risk_level"), S("BONK"), S("high")))
    metta.space().add_atom(E(S("risk_level"), S("JUP"), S("medium")))
    metta.space().add_atom(E(S("risk_level"), S("ORCA"), S("medium")))
    metta.space().add_atom(E(S("risk_level"), S("MNGO"), S("medium")))
    
    # ===== STAKING KNOWLEDGE =====
    
    # Staking Validators and APY
    metta.space().add_atom(E(S("validator"), S("Solana Foundation"), ValueAtom("Official validator, 7.2% APY, 0% commission")))
    metta.space().add_atom(E(S("validator"), S("Marinade Finance"), ValueAtom("Liquid staking, 6.8% APY, 2% commission")))
    metta.space().add_atom(E(S("validator"), S("Jito Labs"), ValueAtom("MEV protection, 6.5% APY, 3% commission")))
    metta.space().add_atom(E(S("validator"), S("P2P Validator"), ValueAtom("Professional validator, 6.9% APY, 5% commission")))
    metta.space().add_atom(E(S("validator"), S("Everstake"), ValueAtom("Reliable validator, 6.7% APY, 4% commission")))
    
    # Staking Strategies
    metta.space().add_atom(E(S("staking_strategy"), S("conservative"), ValueAtom("Stake 60-80% with Solana Foundation for stability")))
    metta.space().add_atom(E(S("staking_strategy"), S("balanced"), ValueAtom("Mix of Foundation and liquid staking protocols")))
    metta.space().add_atom(E(S("staking_strategy"), S("aggressive"), ValueAtom("Use liquid staking for higher yields and DeFi integration")))
    
    # Staking Recommendations by Portfolio Size
    metta.space().add_atom(E(S("portfolio_size"), S("small"), ValueAtom("Under $1000, stake 50-70% with Foundation")))
    metta.space().add_atom(E(S("portfolio_size"), S("medium"), ValueAtom("$1000-$10000, diversify staking across validators")))
    metta.space().add_atom(E(S("portfolio_size"), S("large"), ValueAtom("Over $10000, use liquid staking and DeFi strategies")))
    
    # ===== DEFI PROTOCOLS =====
    
    # DEX Protocols
    metta.space().add_atom(E(S("protocol"), S("Raydium"), ValueAtom("AMM DEX, high liquidity, farming rewards")))
    metta.space().add_atom(E(S("protocol"), S("Orca"), ValueAtom("User-friendly DEX, concentrated liquidity")))
    metta.space().add_atom(E(S("protocol"), S("Jupiter"), ValueAtom("DEX aggregator, best price routing")))
    metta.space().add_atom(E(S("protocol"), S("Serum"), ValueAtom("Order book DEX, professional trading")))
    
    # Lending Protocols
    metta.space().add_atom(E(S("protocol"), S("Mango Markets"), ValueAtom("Lending and borrowing, leveraged trading")))
    metta.space().add_atom(E(S("protocol"), S("Solend"), ValueAtom("Lending protocol, supply and borrow assets")))
    metta.space().add_atom(E(S("protocol"), S("Kamino Finance"), ValueAtom("Leveraged yield farming, automated strategies")))
    
    # Yield Farming
    metta.space().add_atom(E(S("yield_farming"), S("Raydium"), ValueAtom("LP tokens, 5-15% APY, impermanent loss risk")))
    metta.space().add_atom(E(S("yield_farming"), S("Orca"), ValueAtom("Concentrated liquidity, 3-12% APY")))
    metta.space().add_atom(E(S("yield_farming"), S("Mango"), ValueAtom("Lending rewards, 2-8% APY, lower risk")))
    
    # ===== INVESTMENT STRATEGIES =====
    
    # Portfolio Allocation Strategies
    metta.space().add_atom(E(S("allocation"), S("conservative"), ValueAtom("70% SOL staking, 20% stablecoins, 10% DeFi")))
    metta.space().add_atom(E(S("allocation"), S("balanced"), ValueAtom("50% SOL staking, 30% DeFi tokens, 20% stablecoins")))
    metta.space().add_atom(E(S("allocation"), S("aggressive"), ValueAtom("30% SOL staking, 50% DeFi tokens, 20% memecoins")))
    
    # Market Conditions
    metta.space().add_atom(E(S("market_condition"), S("bull_market"), ValueAtom("Focus on growth tokens, reduce stablecoin allocation")))
    metta.space().add_atom(E(S("market_condition"), S("bear_market"), ValueAtom("Increase stablecoin allocation, focus on staking")))
    metta.space().add_atom(E(S("market_condition"), S("sideways"), ValueAtom("DCA strategies, yield farming, balanced allocation")))
    
    # ===== RISK FACTORS =====
    
    # Risk Assessment
    metta.space().add_atom(E(S("risk_factor"), S("memecoin"), S("high_volatility")))
    metta.space().add_atom(E(S("risk_factor"), S("defi_token"), S("smart_contract_risk")))
    metta.space().add_atom(E(S("risk_factor"), S("stablecoin"), S("depeg_risk")))
    metta.space().add_atom(E(S("risk_factor"), S("staking"), S("slashing_risk")))
    metta.space().add_atom(E(S("risk_factor"), S("yield_farming"), S("impermanent_loss")))
    
    # Risk Mitigation
    metta.space().add_atom(E(S("risk_mitigation"), S("high_volatility"), ValueAtom("Diversify, set stop losses, small position sizes")))
    metta.space().add_atom(E(S("risk_mitigation"), S("smart_contract_risk"), ValueAtom("Use audited protocols, start with small amounts")))
    metta.space().add_atom(E(S("risk_mitigation"), S("depeg_risk"), ValueAtom("Diversify across multiple stablecoins")))
    metta.space().add_atom(E(S("risk_mitigation"), S("slashing_risk"), ValueAtom("Choose reputable validators, monitor performance")))
    metta.space().add_atom(E(S("risk_mitigation"), S("impermanent_loss"), ValueAtom("Use stable pairs, monitor ratios")))
    
    # ===== MARKET INDICATORS =====
    
    # Technical Indicators
    metta.space().add_atom(E(S("indicator"), S("rsi_oversold"), ValueAtom("RSI < 30, potential buying opportunity")))
    metta.space().add_atom(E(S("indicator"), S("rsi_overbought"), ValueAtom("RSI > 70, consider taking profits")))
    metta.space().add_atom(E(S("indicator"), S("volume_spike"), ValueAtom("High volume indicates strong interest")))
    metta.space().add_atom(E(S("indicator"), S("support_level"), ValueAtom("Price near support, potential bounce")))
    metta.space().add_atom(E(S("indicator"), S("resistance_level"), ValueAtom("Price near resistance, potential pullback")))
    
    # Market Sentiment
    metta.space().add_atom(E(S("sentiment"), S("fear"), ValueAtom("Market fear, potential buying opportunity")))
    metta.space().add_atom(E(S("sentiment"), S("greed"), ValueAtom("Market greed, consider taking profits")))
    metta.space().add_atom(E(S("sentiment"), S("neutral"), ValueAtom("Market neutral, DCA strategies recommended")))
    
    # ===== INVESTMENT RULES =====
    
    # Portfolio Rules
    metta.space().add_atom(E(S("rule"), S("diversification"), ValueAtom("Never put more than 20% in any single asset")))
    metta.space().add_atom(E(S("rule"), S("risk_management"), ValueAtom("Only invest what you can afford to lose")))
    metta.space().add_atom(E(S("rule"), S("dca"), ValueAtom("Dollar cost average to reduce timing risk")))
    metta.space().add_atom(E(S("rule"), S("rebalancing"), ValueAtom("Rebalance portfolio monthly or quarterly")))
    
    # Staking Rules
    metta.space().add_atom(E(S("staking_rule"), S("minimum_stake"), ValueAtom("Minimum 0.1 SOL to stake effectively")))
    metta.space().add_atom(E(S("staking_rule"), S("validator_diversity"), ValueAtom("Stake with multiple validators to reduce risk")))
    metta.space().add_atom(E(S("staking_rule"), S("commission_check"), ValueAtom("Check validator commission rates regularly")))
    
    # ===== DEFI STRATEGIES =====
    
    # Yield Strategies
    metta.space().add_atom(E(S("yield_strategy"), S("lending"), ValueAtom("Supply assets to lending protocols for interest")))
    metta.space().add_atom(E(S("yield_strategy"), S("liquidity_provision"), ValueAtom("Provide liquidity to DEX pools for trading fees")))
    metta.space().add_atom(E(S("yield_strategy"), S("leveraged_staking"), ValueAtom("Use liquid staking tokens for additional yield")))
    
    # Arbitrage Opportunities
    metta.space().add_atom(E(S("arbitrage"), S("dex_price_diff"), ValueAtom("Price differences between DEXs create arbitrage")))
    metta.space().add_atom(E(S("arbitrage"), S("cross_chain"), ValueAtom("Price differences between chains")))
    
    # ===== MARKET TIMING =====
    
    # Entry Strategies
    metta.space().add_atom(E(S("entry_strategy"), S("dip_buying"), ValueAtom("Buy during market dips for better entry")))
    metta.space().add_atom(E(S("entry_strategy"), S("breakout"), ValueAtom("Buy on breakout above resistance")))
    metta.space().add_atom(E(S("entry_strategy"), S("support_bounce"), ValueAtom("Buy when price bounces off support")))
    
    # Exit Strategies
    metta.space().add_atom(E(S("exit_strategy"), S("profit_taking"), ValueAtom("Take profits at predetermined levels")))
    metta.space().add_atom(E(S("exit_strategy"), S("stop_loss"), ValueAtom("Set stop losses to limit downside")))
    metta.space().add_atom(E(S("exit_strategy"), S("trailing_stop"), ValueAtom("Use trailing stops to lock in profits")))
    
    # ===== PROTOCOL RELATIONSHIPS =====
    
    # Protocol Dependencies
    metta.space().add_atom(E(S("depends_on"), S("Raydium"), S("Serum")))
    metta.space().add_atom(E(S("depends_on"), S("Jupiter"), S("Raydium")))
    metta.space().add_atom(E(S("depends_on"), S("Orca"), S("Whirlpools")))
    
    # Protocol Categories
    metta.space().add_atom(E(S("protocol_type"), S("Raydium"), S("dex")))
    metta.space().add_atom(E(S("protocol_type"), S("Orca"), S("dex")))
    metta.space().add_atom(E(S("protocol_type"), S("Jupiter"), S("aggregator")))
    metta.space().add_atom(E(S("protocol_type"), S("Mango"), S("lending")))
    metta.space().add_atom(E(S("protocol_type"), S("Solend"), S("lending")))
    
    # ===== ADVANCED STRATEGIES =====
    
    # Leverage Strategies
    metta.space().add_atom(E(S("leverage_strategy"), S("long_leverage"), ValueAtom("Borrow against staked SOL for additional positions")))
    metta.space().add_atom(E(S("leverage_strategy"), S("short_leverage"), ValueAtom("Short overvalued assets using borrowed funds")))
    
    # Options and Derivatives
    metta.space().add_atom(E(S("derivative"), S("options"), ValueAtom("Options for hedging and speculation")))
    metta.space().add_atom(E(S("derivative"), S("futures"), ValueAtom("Futures for leveraged exposure")))
    
    # Cross-chain Strategies
    metta.space().add_atom(E(S("cross_chain"), S("bridge_arbitrage"), ValueAtom("Arbitrage between Solana and other chains")))
    metta.space().add_atom(E(S("cross_chain"), S("multi_chain_yield"), ValueAtom("Yield farming across multiple chains")))
    
    print("✅ Solana Knowledge Graph initialized with comprehensive investment data")

def query_solana_knowledge(metta: MeTTa, query_type: str, asset: str = None, context: dict = None):
    """Query the Solana knowledge graph for investment insights"""
    
    try:
        if query_type == "asset_info":
            # Get asset information
            query_str = f'!(match &self (asset {asset} $info) $info)'
            results = metta.run(query_str)
            return results
            
        elif query_type == "risk_assessment":
            # Get risk level for asset
            query_str = f'!(match &self (risk_level {asset} $risk) $risk)'
            results = metta.run(query_str)
            return results
            
        elif query_type == "staking_recommendations":
            # Get staking recommendations based on portfolio size
            portfolio_value = context.get("portfolio_value", 0) if context else 0
            if portfolio_value < 1000:
                size = "small"
            elif portfolio_value < 10000:
                size = "medium"
            else:
                size = "large"
            
            query_str = f'!(match &self (portfolio_size {size} $strategy) $strategy)'
            results = metta.run(query_str)
            return results
            
        elif query_type == "defi_strategies":
            # Get DeFi strategies based on risk tolerance
            risk_tolerance = context.get("risk_tolerance", "balanced") if context else "balanced"
            query_str = f'!(match &self (allocation {risk_tolerance} $strategy) $strategy)'
            results = metta.run(query_str)
            return results
            
        elif query_type == "market_conditions":
            # Get strategies based on market conditions
            market_trend = context.get("market_trend", "neutral") if context else "neutral"
            query_str = f'!(match &self (market_condition {market_trend} $strategy) $strategy)'
            results = metta.run(query_str)
            return results
            
        elif query_type == "risk_mitigation":
            # Get risk mitigation strategies
            risk_type = context.get("risk_type", "high_volatility") if context else "high_volatility"
            query_str = f'!(match &self (risk_mitigation {risk_type} $strategy) $strategy)'
            results = metta.run(query_str)
            return results
            
        elif query_type == "yield_strategies":
            # Get yield farming strategies
            query_str = '!(match &self (yield_strategy $protocol $strategy) $strategy)'
            results = metta.run(query_str)
            return results
            
        elif query_type == "protocol_info":
            # Get protocol information
            query_str = f'!(match &self (protocol {asset} $info) $info)'
            results = metta.run(query_str)
            return results
            
        else:
            return []
            
    except Exception as e:
        print(f"Error querying MeTTa knowledge graph: {str(e)}")
        return []

def get_investment_insights(metta: MeTTa, portfolio_data: dict, market_data: dict):
    """Get comprehensive investment insights using MeTTa knowledge graph"""
    
    insights = []
    
    try:
        # Analyze each asset in portfolio
        for asset in portfolio_data.get("assets", []):
            asset_name = asset.get("symbol", "").upper()
            
            # Get asset information
            asset_info = query_solana_knowledge(metta, "asset_info", asset_name)
            if asset_info:
                insights.append(f"Asset {asset_name}: {asset_info[0]}")
            
            # Get risk assessment
            risk_level = query_solana_knowledge(metta, "risk_assessment", asset_name)
            if risk_level:
                insights.append(f"Risk level for {asset_name}: {risk_level[0]}")
        
        # Get staking recommendations
        staking_recs = query_solana_knowledge(metta, "staking_recommendations", context=portfolio_data)
        if staking_recs:
            insights.append(f"Staking strategy: {staking_recs[0]}")
        
        # Get DeFi strategies
        defi_strategies = query_solana_knowledge(metta, "defi_strategies", context=portfolio_data)
        if defi_strategies:
            insights.append(f"DeFi allocation: {defi_strategies[0]}")
        
        # Get market-based strategies
        market_strategies = query_solana_knowledge(metta, "market_conditions", context=market_data)
        if market_strategies:
            insights.append(f"Market strategy: {market_strategies[0]}")
        
        # Get yield strategies
        yield_strategies = query_solana_knowledge(metta, "yield_strategies")
        if yield_strategies:
            insights.append(f"Yield opportunities: {yield_strategies[0]}")
        
        return insights
        
    except Exception as e:
        print(f"Error getting investment insights: {str(e)}")
        return ["Knowledge graph analysis temporarily unavailable"]


