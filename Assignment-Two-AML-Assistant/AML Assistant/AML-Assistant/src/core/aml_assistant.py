# src/core/aml_assistant.py
import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime
from decimal import Decimal
from enum import Enum

from ..ai.intelligent_engine import IntelligentAIEngine
from ..integration.bank_system import BankIntegrationManager
from ..core.core_config import config_manager

logger = logging.getLogger(__name__)

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    SEVERE = "severe"

class AlertType(str, Enum):
    STRUCTURING = "structuring"
    LAYERING = "layering"
    PEP = "pep"
    SANCTIONS = "sanctions"
    BEHAVIORAL = "behavioral"
    GEOGRAPHIC = "geographic"

class UltimateAMLAssistant:
    """Ultimate AML Assistant with AI, auto-detection, and learning"""
    
    def __init__(self):
        self.ai_engine = IntelligentAIEngine()
        self.bank_integration = BankIntegrationManager()
        self.alert_counter = 0
        
        logger.info("Ultimate AML Assistant initialized")
    
    async def analyze_transaction(self, transaction_data: Dict) -> Dict[str, Any]:
        """Complete transaction analysis with AI and bank integration"""
        
        # Step 1: Get context from bank system
        bank_context = await self.bank_integration.process_transaction(transaction_data)
        
        # Step 2: AI-powered risk analysis
        ai_analysis = await self.ai_engine.analyze_transaction(
            transaction_data, 
            bank_context['customer_profile']
        )
        
        # Step 3: Generate comprehensive result
        result = self._generate_comprehensive_result(
            transaction_data, bank_context, ai_analysis
        )
        
        # Step 4: Submit alert if high risk
        if result['risk_assessment']['risk_level'] in [RiskLevel.HIGH, RiskLevel.SEVERE]:
            await self._submit_alert(result)
        
        logger.info(f"Transaction {transaction_data.get('transaction_id')} analyzed - Risk: {result['risk_assessment']['risk_level']}")
        
        return result
    
    def _generate_comprehensive_result(self, transaction_data: Dict, 
                                    bank_context: Dict, ai_analysis: Dict) -> Dict[str, Any]:
        """Generate comprehensive analysis result"""
        
        return {
            'transaction_id': transaction_data.get('transaction_id'),
            'timestamp': datetime.now().isoformat(),
            'risk_assessment': {
                'risk_level': ai_analysis.get('risk_level', RiskLevel.MEDIUM),
                'risk_score': ai_analysis.get('risk_score', 50),
                'primary_factors': ai_analysis.get('risk_factors', []),
                'confidence': ai_analysis.get('confidence', 0.5),
                'ai_provider': ai_analysis.get('ai_provider', 'local')
            },
            'detected_patterns': ai_analysis.get('detected_patterns', []),
            'recommended_actions': ai_analysis.get('recommended_actions', []),
            'system_info': {
                'bank_system': bank_context.get('system_type', 'simulation'),
                'simulation_mode': bank_context.get('simulation_mode', True),
                'analysis_method': ai_analysis.get('analysis_method', 'local_intelligence')
            },
            'context': {
                'customer_risk_tier': bank_context['customer_profile'].get('risk_tier', 'unknown'),
                'transaction_count': len(bank_context.get('recent_transactions', [])),
                'customer_since_days': bank_context['customer_profile'].get('account_age_days', 0)
            }
        }
    
    async def _submit_alert(self, analysis_result: Dict):
        """Submit alert to bank system"""
        self.alert_counter += 1
        alert_data = {
            'alert_id': f"ALERT_{self.alert_counter:06d}",
            'transaction_id': analysis_result['transaction_id'],
            'risk_level': analysis_result['risk_assessment']['risk_level'],
            'risk_score': analysis_result['risk_assessment']['risk_score'],
            'detected_patterns': analysis_result['detected_patterns'],
            'reasoning': f"High risk transaction detected: {analysis_result['risk_assessment']['primary_factors']}",
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            success = await self.bank_integration.system.submit_alert(alert_data)
            if success:
                logger.info(f"Alert {alert_data['alert_id']} submitted successfully")
            else:
                logger.warning(f"Failed to submit alert {alert_data['alert_id']}")
        except Exception as e:
            logger.error(f"Error submitting alert: {e}")
    
    async def provide_feedback(self, transaction_id: str, correct_assessment: Dict):
        """Provide feedback for learning and improvement"""
        await self.ai_engine.learn_from_feedback(transaction_id, correct_assessment)
        logger.info(f"Feedback received for transaction {transaction_id}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and capabilities"""
        return {
            'ai_engine': {
                'primary_provider': self.ai_engine.config['provider'],
                'available_providers': list(self.ai_engine.available_providers.keys()),
                'learning_enabled': config_manager.config['ai']['enable_learning']
            },
            'bank_integration': {
                'system_type': type(self.bank_integration.system).__name__,
                'simulation_mode': isinstance(self.bank_integration.system, 
                                           self.bank_integration.system.__class__.__bases__[0]),
                'health_status': True  # Simplified
            },
            'alerts_processed': self.alert_counter,
            'config': config_manager.config
        }

# Global assistant instance
aml_assistant = UltimateAMLAssistant()
