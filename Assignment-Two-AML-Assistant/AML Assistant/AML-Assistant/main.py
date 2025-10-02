# main.py
#!/usr/bin/env python3
"""
Ultimate AML Assistant - Enterprise Anti-Money Laundering System
"""

import asyncio
import logging
import sys
from decimal import Decimal
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('aml_assistant.log')
    ]
)

logger = logging.getLogger(__name__)

async def demo_ultimate_assistant():
    """Demonstrate the ultimate AML assistant capabilities"""
    from src.core.aml_assistant import aml_assistant
    
    print("🚀 ULTIMATE AML ASSISTANT DEMO")
    print("=" * 60)
    
    # Show system status
    status = aml_assistant.get_system_status()
    print(f"🤖 AI Provider: {status['ai_engine']['primary_provider']}")
    print(f"🏦 Bank System: {status['bank_integration']['system_type']}")
    print(f"🎯 Simulation Mode: {status['bank_integration']['simulation_mode']}")
    print(f"📊 Alerts Processed: {status['alerts_processed']}")
    print("=" * 60)
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Normal Business Transaction",
            "transaction": {
                "transaction_id": "DEMO_NORMAL_001",
                "customer_id": "CUST002",  # Low risk customer
                "amount": Decimal('2500.00'),
                "type": "wire_transfer",
                "currency": "USD",
                "counterparty": "Regular Supplier",
                "channel": "online",
                "description": "Monthly service payment"
            }
        },
        {
            "name": "High-Risk Cash Deposit", 
            "transaction": {
                "transaction_id": "DEMO_HIGH_RISK_001",
                "customer_id": "CUST003",  # High risk customer
                "amount": Decimal('15000.00'),
                "type": "cash_deposit", 
                "currency": "USD",
                "counterparty": "Unknown",
                "channel": "branch",
                "description": "Large cash deposit"
            }
        },
        {
            "name": "Potential Structuring",
            "transaction": {
                "transaction_id": "DEMO_STRUCT_001", 
                "customer_id": "CUST001",  # Medium risk customer
                "amount": Decimal('9500.00'),
                "type": "cash_deposit",
                "currency": "USD",
                "counterparty": "Multiple Sources",
                "channel": "branch", 
                "description": "Business cash deposit"
            }
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n�� Analyzing: {scenario['name']}")
        print("-" * 40)
        
        result = await aml_assistant.analyze_transaction(scenario['transaction'])
        
        print(f"   Amount: ${scenario['transaction']['amount']}")
        print(f"   Type: {scenario['transaction']['type']}")
        print(f"   Customer: {scenario['transaction']['customer_id']}")
        print(f"   ➡️  Risk Level: {result['risk_assessment']['risk_level'].upper()}")
        print(f"   📈 Risk Score: {result['risk_assessment']['risk_score']}/100")
        print(f"   🤖 AI Provider: {result['risk_assessment']['ai_provider']}")
        print(f"   🎯 Confidence: {result['risk_assessment']['confidence']:.2f}")
        print(f"   🏦 Bank System: {result['system_info']['bank_system']}")
        
        if result['detected_patterns']:
            print(f"   🚨 Patterns: {', '.join(result['detected_patterns'])}")
        
        if result['risk_assessment']['primary_factors']:
            print(f"   📋 Factors: {', '.join(result['risk_assessment']['primary_factors'][:2])}")
    
    print("\n" + "=" * 60)
    print("✅ Ultimate AML Assistant Demo Completed!")
    print("💡 The system automatically:")
    print("   - Detects available AI providers")
    print("   - Connects to bank systems (or uses simulation)")
    print("   - Uses intelligent fallback mechanisms") 
    print("   - Learns and adapts over time")
    print("=" * 60)

async def main():
    """Main application entry point"""
    try:
        await demo_ultimate_assistant()
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
