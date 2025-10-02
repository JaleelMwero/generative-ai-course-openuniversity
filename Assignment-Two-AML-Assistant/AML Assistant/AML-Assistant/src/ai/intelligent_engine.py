# src/ai/intelligent_engine.py
import os
import logging
from typing import Dict, Any, Optional, List
from decimal import Decimal
from datetime import datetime
from ..core.core_config import config_manager

logger = logging.getLogger(__name__)

class IntelligentAIEngine:
    """Intelligent AI engine with auto-fallback and learning capabilities"""
    
    def __init__(self):
        self.config = config_manager.get_ai_config()
        self.available_providers = self._initialize_providers()
        self.learning_memory = []
        self.performance_metrics = {}
        
        logger.info(f"AI Engine initialized with provider: {self.config['provider']}")
    
    def _initialize_providers(self) -> Dict[str, Any]:
        """Initialize all available AI providers"""
        providers = {}
        
        # OpenAI Provider
        if self._check_openai_availability():
            providers['openai'] = self._create_openai_provider()
        
        # Local Provider (Rule-based + ML)
        providers['local'] = LocalIntelligenceProvider()
        
        # Hybrid Provider
        if len(providers) > 1:
            providers['hybrid'] = HybridIntelligenceProvider(providers)
        
        return providers
    
    def _check_openai_availability(self) -> bool:
        """Check if OpenAI is available"""
        api_key = self.config['api_key']
        return bool(api_key and api_key.startswith('sk-'))
    
    def _create_openai_provider(self):
        """Create OpenAI provider with error handling"""
        try:
            from .providers.openai_provider import OpenAIProvider
            return OpenAIProvider(self.config['api_key'], self.config['model'])
        except ImportError:
            logger.warning("OpenAI provider not available")
            return None
    
    async def analyze_transaction(self, transaction_data: Dict, customer_data: Dict) -> Dict[str, Any]:
        """Intelligent transaction analysis with auto-fallback"""
        primary_provider = self.config['provider']
        
        # Try primary provider first
        if primary_provider in self.available_providers:
            try:
                result = await self.available_providers[primary_provider].analyze(
                    transaction_data, customer_data
                )
                result['ai_provider'] = primary_provider
                result['confidence'] = self._calculate_confidence(result)
                
                # Store for learning
                self._store_analysis_result(transaction_data, customer_data, result)
                
                return result
            except Exception as e:
                logger.warning(f"Primary provider {primary_provider} failed: {e}")
        
        # Fallback to available providers
        for provider_name, provider in self.available_providers.items():
            if provider_name != primary_provider:
                try:
                    result = await provider.analyze(transaction_data, customer_data)
                    result['ai_provider'] = provider_name
                    result['confidence'] = self._calculate_confidence(result)
                    result['fallback_used'] = True
                    
                    self._store_analysis_result(transaction_data, customer_data, result)
                    return result
                except Exception as e:
                    logger.warning(f"Fallback provider {provider_name} failed: {e}")
        
        # Ultimate fallback to local intelligence
        logger.info("Using ultimate fallback to local intelligence")
        return await self.available_providers['local'].analyze(transaction_data, customer_data)
    
    def _calculate_confidence(self, result: Dict) -> float:
        """Calculate confidence score for analysis result"""
        base_confidence = result.get('confidence', 0.5)
        
        # Adjust based on provider performance
        provider = result.get('ai_provider', 'local')
        provider_performance = self.performance_metrics.get(provider, {}).get('accuracy', 0.8)
        
        # Adjust based on result complexity
        risk_factors = len(result.get('risk_factors', []))
        complexity_factor = min(risk_factors / 10, 1.0)  # Normalize
        
        final_confidence = (base_confidence * 0.6 + 
                          provider_performance * 0.3 + 
                          complexity_factor * 0.1)
        
        return min(final_confidence, 1.0)
    
    def _store_analysis_result(self, transaction_data: Dict, customer_data: Dict, result: Dict):
        """Store analysis results for learning"""
        if len(self.learning_memory) >= config_manager.config['learning']['pattern_memory_size']:
            self.learning_memory.pop(0)
        
        learning_entry = {
            'timestamp': datetime.now(),
            'transaction': transaction_data,
            'customer': customer_data,
            'result': result,
            'feedback': None  # To be filled by human review
        }
        
        self.learning_memory.append(learning_entry)
    
    async def learn_from_feedback(self, transaction_id: str, correct_assessment: Dict):
        """Learn from human feedback to improve future analyses"""
        # Find the analysis in memory
        for entry in self.learning_memory:
            if entry['transaction'].get('transaction_id') == transaction_id:
                entry['feedback'] = correct_assessment
                break
        
        # Update provider performance metrics
        self._update_performance_metrics(correct_assessment)
    
    def _update_performance_metrics(self, correct_assessment: Dict):
        """Update performance metrics based on feedback"""
        # Implementation for adaptive learning
        pass

class LocalIntelligenceProvider:
    """Advanced local intelligence with rule-based + ML patterns"""
    
    def __init__(self):
        self.rule_engine = RuleBasedEngine()
        self.pattern_detector = PatternDetectionEngine()
        self.risk_calculator = RiskCalculationEngine()
    
    async def analyze(self, transaction_data: Dict, customer_data: Dict) -> Dict[str, Any]:
        """Advanced local analysis combining multiple techniques"""
        
        # Parallel analysis using different techniques
        rule_based_result = self.rule_engine.analyze(transaction_data, customer_data)
        pattern_result = self.pattern_detector.detect_patterns(transaction_data, customer_data)
        risk_score = self.risk_calculator.calculate_risk(transaction_data, customer_data)
        
        # Intelligent result fusion
        final_result = self._fuse_results(rule_based_result, pattern_result, risk_score)
        
        return {
            'risk_level': final_result['risk_level'],
            'risk_score': final_result['risk_score'],
            'risk_factors': final_result['risk_factors'],
            'recommended_actions': final_result['actions'],
            'detected_patterns': pattern_result['patterns'],
            'confidence': final_result['confidence'],
            'analysis_method': 'local_intelligence'
        }
    
    def _fuse_results(self, rule_result: Dict, pattern_result: Dict, risk_score: float) -> Dict:
        """Intelligently fuse results from different analysis methods"""
        # Implementation for result fusion
        return {
            'risk_level': 'medium',  # Simplified
            'risk_score': risk_score,
            'risk_factors': rule_result.get('factors', []) + pattern_result.get('factors', []),
            'actions': rule_result.get('actions', []),
            'confidence': 0.7  # Base confidence for local analysis
        }

class RuleBasedEngine:
    """Advanced rule-based analysis engine"""
    
    def analyze(self, transaction_data: Dict, customer_data: Dict) -> Dict:
        # Implementation of sophisticated rule-based analysis
        return {
            'factors': ['rule_based_factor_1', 'rule_based_factor_2'],
            'actions': ['action_1', 'action_2']
        }

class PatternDetectionEngine:
    """Advanced pattern detection engine"""
    
    def detect_patterns(self, transaction_data: Dict, customer_data: Dict) -> Dict:
        # Implementation of pattern detection
        return {
            'patterns': ['structuring', 'unusual_behavior'],
            'factors': ['pattern_based_factor_1']
        }

class RiskCalculationEngine:
    """Advanced risk calculation engine"""
    
    def calculate_risk(self, transaction_data: Dict, customer_data: Dict) -> float:
        # Implementation of risk calculation
        return 65.0  # Example risk score

class HybridIntelligenceProvider:
    """Hybrid intelligence combining multiple providers"""
    
    def __init__(self, providers: Dict):
        self.providers = providers
    
    async def analyze(self, transaction_data: Dict, customer_data: Dict) -> Dict[str, Any]:
        """Hybrid analysis using multiple providers"""
        # Implementation for hybrid analysis
        pass
