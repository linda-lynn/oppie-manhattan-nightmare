"""
Identity Verifier for Oppenheimer AI
Verifies user identity through conversation analysis and active verification questions
"""

import re
from typing import Dict, List, Optional, Tuple
import random


class IdentityVerifier:
    """Verifies user identity through conversation analysis and verification questions"""
    
    def __init__(self):
        """Initialize verification questions and criteria"""
        self.chemistry_questions = [
            {
                "question": "Could you write out the full electron configuration up to 4d10?",
                "keywords": ["1s2", "2s2", "2p6", "3s2", "3p6", "4s2", "3d10", "4p6", "4d10"],
                "concepts": ["aufbau", "pauli", "hund", "electron configuration", "orbital filling"]
            },
            {
                "question": "Explain the difference between bonding and antibonding molecular orbitals in a diatomic molecule.",
                "keywords": ["bonding", "antibonding", "sigma", "pi", "molecular orbital", "overlap"],
                "concepts": ["molecular orbital theory", "bond order", "overlap integral", "linear combination"]
            },
            {
                "question": "Describe how molecular orbital theory explains the stability of benzene.",
                "keywords": ["delocalization", "aromatic", "huckel", "resonance", "pi electrons"],
                "concepts": ["aromaticity", "delocalized electrons", "huckel rule", "resonance energy"]
            },
            {
                "question": "What is the relationship between the HOMO and LUMO in a conjugated system?",
                "keywords": ["homo", "lumo", "conjugated", "band gap", "frontier orbitals"],
                "concepts": ["frontier molecular orbitals", "conjugation", "electronic transitions"]
            }
        ]
        
        self.particle_physics_questions = [
            {
                "question": "What is CP violation and how does it relate to the weak interaction?",
                "keywords": ["cp violation", "charge conjugation", "parity", "weak interaction", "kaon", "b meson"],
                "concepts": ["cp symmetry", "weak force", "cabbibo-kobayashi-maskawa", "ckm matrix"]
            },
            {
                "question": "Explain electroweak symmetry breaking in the Higgs mechanism.",
                "keywords": ["higgs", "electroweak", "symmetry breaking", "spontaneous", "goldstone", "gauge"],
                "concepts": ["electroweak theory", "higgs field", "spontaneous symmetry breaking", "gauge bosons"]
            },
            {
                "question": "How does the mixing angle relate to CP violation in the CKM matrix?",
                "keywords": ["mixing angle", "ckm", "cabibbo", "cp violation", "quark mixing"],
                "concepts": ["quark mixing", "ckm matrix", "mixing angles", "cp violation"]
            },
            {
                "question": "Describe the role of the Higgs field in giving mass to particles.",
                "keywords": ["higgs field", "mass generation", "yukawa coupling", "fermion mass", "boson mass"],
                "concepts": ["higgs mechanism", "mass generation", "yukawa interactions", "electroweak symmetry"]
            }
        ]
        
        # Linda's known background indicators
        self.linda_indicators = {
            "chemistry": ["molecular orbital", "mo theory", "homo", "lumo", "bonding", "antibonding", 
                         "electron configuration", "quantum chemistry", "hartree-fock", "dft"],
            "particle_physics": ["cp violation", "electroweak", "higgs", "ckm", "mixing angle", 
                                "weak interaction", "symmetry breaking", "quark mixing"],
            "nuclear": ["nuclear physics", "binding energy", "fission", "fusion", "cross section", 
                       "neutron", "nucleus", "isotope"]
        }
        
        # Linda's neurodivergent communication patterns (HI and ASD)
        self.linda_neurodivergent_patterns = {
            "emotional_physics": [
                # Quantum mechanics expressions
                r"feel.*quantum", r"quantum.*feel", r"quantum state", r"quantum superposition",
                r"wave function", r"probability.*amplitude", r"quantum entanglement",
                # Energy level expressions
                r"energy level", r"energy.*low", r"energy.*depleted", r"energy.*high",
                r"ground state", r"excited state", r"energy gap",
                # Resonance and vibration
                r"resonance", r"vibrational", r"frequency", r"oscillation",
                # Field and force expressions
                r"field.*feel", r"force.*feel", r"interaction", r"coupling"
            ],
            "emotional_chemistry": [
                # Bonding metaphors
                r"bonding.*feel", r"bond.*strength", r"bond.*weak", r"bond.*break",
                r"bonding energy", r"bond order",
                # Equilibrium and stability
                r"equilibrium", r"stable", r"unstable", r"balance",
                # Reaction metaphors
                r"reaction.*feel", r"react.*overwhelm", r"cataly", r"activation energy",
                # Solution and mixing
                r"solution", r"dissolve", r"mix", r"phase"
            ],
            "emotional_nuclear": [
                # Critical state expressions
                r"critical.*state", r"critical.*feel", r"critical mass",
                # Decay and half-life
                r"half-life", r"decay.*feel", r"decay.*emotion", r"radioactive",
                # Fission and fusion metaphors
                r"fission.*feel", r"fusion.*feel", r"split", r"merge",
                # Binding energy
                r"binding.*feel", r"bound.*feel", r"binding energy"
            ],
            "direct_communication": [
                # Direct statements without hedging
                r"^i (think|believe|know|feel|want|need)", r"^this is", r"^that is",
                # Literal language patterns
                r"literally", r"exactly", r"precisely", r"specifically",
                # Direct questions
                r"^what is", r"^how does", r"^why does", r"^can you"
            ],
            "special_interest_intensity": [
                # Deep dive indicators
                r"i've been.*studying", r"i'm researching", r"i'm working on",
                r"fascinated by", r"obsessed with", r"passionate about",
                # Detailed technical questions
                r"can you explain.*in detail", r"tell me everything about",
                r"i want to understand.*completely"
            ]
        }
    
    def detect_emotional_science_expression(self, message: str) -> Dict:
        """
        Detect when emotions are expressed through scientific concepts
        
        Returns:
            Dict with detection results and confidence boost
        """
        message_lower = message.lower()
        detections = []
        confidence_boost = 0.0
        
        # Check for emotional physics expressions
        for pattern in self.linda_neurodivergent_patterns["emotional_physics"]:
            if re.search(pattern, message_lower):
                detections.append("Emotional physics expression")
                confidence_boost += 0.15
                break
        
        # Check for emotional chemistry expressions
        for pattern in self.linda_neurodivergent_patterns["emotional_chemistry"]:
            if re.search(pattern, message_lower):
                detections.append("Emotional chemistry metaphor")
                confidence_boost += 0.15
                break
        
        # Check for emotional nuclear expressions
        for pattern in self.linda_neurodivergent_patterns["emotional_nuclear"]:
            if re.search(pattern, message_lower):
                detections.append("Emotional nuclear physics analogy")
                confidence_boost += 0.15
                break
        
        return {
            "detected": len(detections) > 0,
            "detections": detections,
            "confidence_boost": min(confidence_boost, 0.3)  # Cap at 0.3
        }
    
    def analyze_conversation_style(self, message: str, history: List[Dict]) -> Dict:
        """
        Analyze conversation style to assess if user matches Linda's profile
        Accounts for neurodivergent communication patterns (HI and ASD)
        
        Returns:
            Dict with confidence score and indicators
        """
        message_lower = message.lower()
        confidence_score = 0.5  # Start neutral
        indicators = []
        
        # Check for emotional expression through science (strong Linda identifier)
        emotional_science = self.detect_emotional_science_expression(message)
        if emotional_science["detected"]:
            confidence_score += emotional_science["confidence_boost"]
            indicators.extend(emotional_science["detections"])
            indicators.append("Expresses emotions through scientific concepts (neurodivergent pattern)")
        
        # Check for advanced terminology
        advanced_terms = 0
        for domain, terms in self.linda_indicators.items():
            for term in terms:
                if term in message_lower:
                    advanced_terms += 1
                    indicators.append(f"Uses {domain} terminology: {term}")
        
        if advanced_terms > 0:
            confidence_score += min(advanced_terms * 0.1, 0.3)
        
        # Check for mathematical notation
        math_patterns = [
            r'\b[A-Z]\s*=\s*[^=]+\b',  # Equations like E = mc²
            r'\b\d+\.\d+\s*[×x]\s*10\^?[-\d]+\b',  # Scientific notation
            r'[αβγδεηθλμπρστφχψω]',  # Greek letters
            r'[∫∑∏∇∂]',  # Mathematical operators
            r'\b[A-Z][a-z]?\d+\b',  # Chemical/nuclear notation like U-235
        ]
        
        math_count = sum(1 for pattern in math_patterns if re.search(pattern, message))
        if math_count > 0:
            confidence_score += min(math_count * 0.05, 0.2)
            indicators.append(f"Uses mathematical notation ({math_count} instances)")
        
        # Check conversation history for consistency
        if history:
            recent_messages = [h.get('message', '').lower() for h in history[-10:] 
                             if h.get('sender') == 'user']
            
            # Check for consistent academic level
            if len(recent_messages) >= 3:
                avg_length = sum(len(m) for m in recent_messages) / len(recent_messages)
                if avg_length > 50:  # Substantive questions
                    confidence_score += 0.1
                    indicators.append("Consistent academic engagement")
            
            # Check for domain knowledge consistency
            domain_mentions = {domain: 0 for domain in self.linda_indicators.keys()}
            for msg in recent_messages:
                for domain, terms in self.linda_indicators.items():
                    if any(term in msg for term in terms):
                        domain_mentions[domain] += 1
            
            if sum(domain_mentions.values()) > 0:
                confidence_score += 0.1
                indicators.append("Shows domain knowledge across multiple areas")
        
        # Check for direct communication patterns (characteristic of ASD, not suspicious)
        direct_communication = False
        for pattern in self.linda_neurodivergent_patterns["direct_communication"]:
            if re.search(pattern, message_lower):
                direct_communication = True
                indicators.append("Direct, literal communication (neurodivergent pattern)")
                confidence_score += 0.1  # Positive indicator for Linda
                break
        
        # Check for special interest intensity (characteristic of ASD)
        special_interest = False
        for pattern in self.linda_neurodivergent_patterns["special_interest_intensity"]:
            if re.search(pattern, message_lower):
                special_interest = True
                indicators.append("Intense focus on topic (special interest indicator)")
                confidence_score += 0.1  # Positive indicator for Linda
                break
        
        # Check for suspicious patterns (too basic, generic questions)
        # BUT: Don't penalize if direct communication or special interest is present (neurodivergent patterns)
        basic_patterns = [
            r'what is\s+\w+\?',  # Very basic "what is X?" questions
            r'explain\s+\w+\s+to\s+me',  # "explain X to me" (too generic)
        ]
        
        suspicious_count = sum(1 for pattern in basic_patterns if re.search(pattern, message_lower))
        # Only flag as suspicious if no neurodivergent patterns and no advanced terms
        if suspicious_count > 0 and advanced_terms == 0 and not direct_communication and not special_interest:
            confidence_score -= 0.1  # Reduced penalty (was 0.2)
            indicators.append("Suspicious: Very basic questions without domain knowledge")
        
        return {
            "confidence": max(0.0, min(1.0, confidence_score)),
            "indicators": indicators,
            "advanced_terms": advanced_terms,
            "math_notation": math_count
        }
    
    def generate_verification_question(self, domain: str = None) -> Dict:
        """
        Generate a verification question from chemistry or particle physics
        
        Args:
            domain: 'chemistry' or 'particle_physics', or None for random
            
        Returns:
            Dict with question and metadata
        """
        if domain is None:
            domain = random.choice(['chemistry', 'particle_physics'])
        
        if domain == 'chemistry':
            question_data = random.choice(self.chemistry_questions)
        else:
            question_data = random.choice(self.particle_physics_questions)
        
        return {
            "question": question_data["question"],
            "domain": domain,
            "keywords": question_data["keywords"],
            "concepts": question_data["concepts"]
        }
    
    def evaluate_response(self, answer: str, question_data: Dict) -> Dict:
        """
        Evaluate answer to verification question
        
        Even incorrect answers can show domain knowledge through reasoning depth.
        Accounts for neurodivergent communication style (direct, literal, using science metaphors).
        
        Returns:
            Dict with pass/fail and reasoning
        """
        answer_lower = answer.lower()
        
        # Check for emotional science expression (strong Linda identifier)
        emotional_science = self.detect_emotional_science_expression(answer)
        if emotional_science["detected"]:
            # Using science to express understanding is a positive indicator
            pass
        
        # Check for keyword matches
        keyword_matches = sum(1 for kw in question_data["keywords"] 
                             if kw.lower() in answer_lower)
        
        # Check for concept mentions
        concept_mentions = sum(1 for concept in question_data["concepts"] 
                              if concept.lower() in answer_lower)
        
        # Assess answer length and depth
        answer_length = len(answer)
        has_equations = bool(re.search(r'[=+\-×÷∫∑]', answer))
        has_technical_terms = bool(re.search(r'\b[A-Z][a-z]+\s+\w+', answer))
        
        # Check for direct communication (characteristic of ASD)
        direct_communication = any(re.search(pattern, answer_lower) 
                                  for pattern in self.linda_neurodivergent_patterns["direct_communication"])
        
        # Scoring
        score = 0.0
        
        # Keyword matches (0.3 points)
        if keyword_matches > 0:
            score += min(keyword_matches * 0.1, 0.3)
        
        # Concept understanding (0.4 points)
        if concept_mentions > 0:
            score += min(concept_mentions * 0.15, 0.4)
        
        # Answer depth (0.3 points)
        if answer_length > 100:
            score += 0.1
        if answer_length > 200:
            score += 0.1
        if has_equations or has_technical_terms:
            score += 0.1
        
        # Reasoning quality assessment
        reasoning_indicators = [
            "because", "due to", "therefore", "thus", "since", "as a result",
            "this means", "implies", "relates to", "connected to"
        ]
        has_reasoning = any(indicator in answer_lower for indicator in reasoning_indicators)
        
        if has_reasoning and score > 0.3:
            score += 0.1
        
        # Neurodivergent communication bonus
        # Direct, honest answers even with uncertainty show authenticity
        uncertainty_indicators = ["i think", "i'm not sure", "i believe", "possibly", "maybe"]
        has_uncertainty = any(indicator in answer_lower for indicator in uncertainty_indicators)
        if direct_communication and has_uncertainty and score > 0.2:
            # Direct expression of uncertainty is honest and characteristic
            score += 0.05
        
        # Using science metaphors to express understanding
        if emotional_science["detected"] and score > 0.3:
            score += 0.1  # Bonus for expressing through science
        
        # Pass threshold: 0.5 (even partial understanding shows domain knowledge)
        # Lower threshold for neurodivergent communication (0.45) if direct and honest
        threshold = 0.45 if (direct_communication and has_reasoning) else 0.5
        passed = score >= threshold
        
        return {
            "passed": passed,
            "score": score,
            "keyword_matches": keyword_matches,
            "concept_mentions": concept_mentions,
            "reasoning_present": has_reasoning,
            "answer_length": answer_length,
            "evaluation": "Domain knowledge demonstrated" if passed else "Insufficient domain knowledge"
        }
    
    def is_linda_authenticated(self, message: str, history: List[Dict], 
                             verification_state: Dict) -> Tuple[bool, Optional[Dict]]:
        """
        Main verification logic
        
        Returns:
            Tuple of (is_verified, verification_question_or_none)
        """
        # If already verified, return True
        if verification_state.get('status') == 'verified':
            return True, None
        
        # If verification failed, return False
        if verification_state.get('status') == 'failed':
            return False, None
        
        # Analyze conversation style
        analysis = self.analyze_conversation_style(message, history)
        
        # High confidence: likely Linda
        if analysis["confidence"] >= 0.7:
            return True, None
        
        # Low confidence or pending verification: need to verify
        if verification_state.get('status') == 'pending':
            # Already asked a question, wait for answer - return False (not verified yet) with question
            return False, verification_state.get('question_data')
        
        # Medium confidence or first interaction: ask verification question
        if analysis["confidence"] < 0.6 or len(history) < 3:
            # Choose domain based on message content
            domain = None
            message_lower = message.lower()
            
            if any(term in message_lower for term in self.linda_indicators["chemistry"]):
                domain = 'chemistry'
            elif any(term in message_lower for term in self.linda_indicators["particle_physics"]):
                domain = 'particle_physics'
            
            question_data = self.generate_verification_question(domain)
            # Return False (not verified yet) with question to ask
            return False, question_data
        
        # Medium-high confidence: likely Linda but not certain
        return True, None
    
    def get_response_level(self, identity_status: str) -> str:
        """
        Determine response level based on identity status
        
        Returns:
            'full' or 'basic'
        """
        if identity_status == 'verified':
            return 'full'
        return 'basic'


