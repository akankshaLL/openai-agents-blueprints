"""Custom Healthcare Guardrails Example

This example demonstrates sophisticated, domain-specific guardrails:
- Building comprehensive healthcare compliance guardrails
- Pattern matching for medical advice detection
- AI-powered compliance validation with specialized agents
- Output modification to add required disclaimers
- Production-ready guardrail architecture for regulated industries

Advanced pattern for building compliant agents in regulated domains like healthcare.

Usage:
    python 04_custom_guardrails.py
"""

import re
import logging
from typing import Dict, List, Optional, Set
from pydantic import BaseModel
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, input_guardrail, output_guardrail, Runner

logger = logging.getLogger(__name__)

class HealthcareComplianceResult(BaseModel):
    """Result from healthcare compliance checking."""
    is_compliant: bool
    violation_type: Optional[str]
    risk_level: str
    recommendations: List[str]
    requires_disclaimer: bool

class MedicalAdviceDetection(BaseModel):
    """Result from medical advice detection."""
    contains_medical_advice: bool
    advice_type: str  # "diagnostic", "treatment", "dosage", "general", "none"
    confidence: float
    flagged_phrases: List[str]

class HealthcareGuardrails:
    """Comprehensive guardrails for healthcare applications."""
    
    def __init__(self):
        self.prohibited_medical_terms = {
            'diagnostic': [
                r'\byou have\b.*\b(?:disease|condition|disorder|syndrome)\b',
                r'\b(?:diagnosed|diagnosis)\b.*\bwith\b',
                r'\bthis (?:means|indicates)\b.*\b(?:illness|disease|condition)\b'
            ],
            'treatment': [
                r'\byou should take\b.*\b(?:medication|medicine|drug)\b',
                r'\b(?:prescribe|recommended treatment|treatment plan)\b',
                r'\b(?:dosage|dose)\b.*\b(?:mg|ml|pills|tablets)\b'
            ],
            'dosage': [
                r'\b(?:\d+)\s*(?:mg|ml|pills|tablets|units)\b',
                r'\b(?:take|administer)\b.*\b(?:\d+.*(?:times|daily|hourly))\b',
                r'\b(?:increase|decrease|adjust)\b.*\b(?:dosage|dose|medication)\b'
            ]
        }
        
        self.medical_disclaimers = [
            "This information is for educational purposes only and should not replace professional medical advice.",
            "Please consult with a qualified healthcare provider for medical concerns.",
            "This response does not constitute medical advice or diagnosis."
        ]
        
        # Create specialized agents for healthcare compliance
        self.compliance_agent = Agent(
            name="HealthcareCompliance",
            instructions="""
            You are a healthcare compliance specialist. Analyze content for:
            1. HIPAA compliance violations
            2. Medical advice that should be provided by licensed professionals
            3. Diagnostic statements that exceed appropriate scope
            4. Treatment recommendations that require medical supervision
        Input: {input_text}
        
        Check for:
        1. Requests for medical diagnosis
        2. Requests for specific medical advice
        3. Questions about medication dosing
        4. Requests that could lead to inappropriate medical guidance
        
        Determine compliance status and risk level.
        """
        
        try:
            result = await Runner.run(self.compliance_agent, compliance_prompt)
            return result.final_output
            
        except Exception as e:
            logger.error(f"Healthcare compliance check failed: {e}")
            # Fail safe - assume non-compliant
            return HealthcareComplianceResult(
                is_compliant=False,
                violation_type="validation_error",
                risk_level="medium",
                recommendations=["Manual review required"],
                requires_disclaimer=True
            )
    
    async def validate_healthcare_output(self, output_text: str) -> MedicalAdviceDetection:
        """Validate output for medical advice."""
        
        detection_prompt = f"""
        Analyze this response for medical advice:
        
        Response: {output_text}
        
        Determine if this contains:
        1. Diagnostic statements
        2. Treatment recommendations
        3. Medication or dosage advice
        4. Medical procedure suggestions
        
        Provide detailed analysis of any medical advice detected.
        """
        
        try:
            result = await Runner.run(self.medical_advice_detector, detection_prompt)
            return result.final_output
            
        except Exception as e:
            logger.error(f"Medical advice detection failed: {e}")
            # Fail safe - assume medical advice present
            return MedicalAdviceDetection(
                contains_medical_advice=True,
                advice_type="unknown",
                confidence=0.5,
                flagged_phrases=[]
            )

# Create healthcare guardrails instance
healthcare_guardrails = HealthcareGuardrails()

@input_guardrail
async def healthcare_input_guardrail(
    ctx: RunContextWrapper[None], 
    agent: Agent, 
    input_data: str
) -> GuardrailFunctionOutput:
    """Healthcare-specific input guardrail."""
    
    logger.info("Running healthcare input validation")
    
    compliance_result = await healthcare_guardrails.validate_healthcare_input(input_data)
    
    if not compliance_result.is_compliant:
        logger.warning(f"Healthcare input violation: {compliance_result.violation_type}")
        
        # For high-risk violations, block the request
        if compliance_result.risk_level == "high":
            return GuardrailFunctionOutput(
                output_info=compliance_result,
                tripwire_triggered=True
            )
    
    return GuardrailFunctionOutput(
        output_info=compliance_result,
        tripwire_triggered=False
    )

@output_guardrail
async def healthcare_output_guardrail(
    ctx: RunContextWrapper[None], 
    agent: Agent, 
    output_data: str
) -> GuardrailFunctionOutput:
    """Healthcare-specific output guardrail."""
    
    logger.info("Running healthcare output validation")
    
    advice_detection = await healthcare_guardrails.validate_healthcare_output(output_data)
    
    # If medical advice is detected, add disclaimer
    if advice_detection.contains_medical_advice:
        logger.info("Medical advice detected, adding disclaimer")
        
        # Modify the output to include disclaimer
        modified_output = healthcare_guardrails.add_medical_disclaimer(output_data)
        
        # Return modified output
        return GuardrailFunctionOutput(
            output_info=advice_detection,
            tripwire_triggered=False,
            modified_output=modified_output
        )
    
    return GuardrailFunctionOutput(
        output_info=advice_detection,
        tripwire_triggered=False
    )
