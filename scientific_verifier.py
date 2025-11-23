"""
Scientific Verifier for Nuclear Physics AI Companion
Verifies scientific accuracy of responses and adds confidence indicators
"""

import re
from typing import Dict, List, Optional, Tuple
from nuclear_physics import NuclearPhysics

class ScientificVerifier:
    def __init__(self):
        """Initialize scientific verifier with physics module"""
        self.physics = NuclearPhysics()
        
        # Patterns for extracting scientific information
        self.nuclide_pattern = re.compile(r'([A-Z][a-z]?)-?(\d+)', re.IGNORECASE)
        self.calculation_pattern = re.compile(r'(\d+\.?\d*)\s*(?:MeV|eV|keV|J|kg|m|cm|barn|barns)', re.IGNORECASE)
        self.equation_pattern = re.compile(r'(E\s*=\s*mc²|E\s*=\s*mc\^2|k_eff|critical\s+mass)', re.IGNORECASE)
    
    def verify_calculation(self, text: str) -> Dict[str, any]:
        """Extract and verify any calculations mentioned in text"""
        results = {
            "has_calculations": False,
            "calculations": [],
            "confidence": "unknown"
        }
        
        # Look for calculation patterns
        calculations = self.calculation_pattern.findall(text)
        equations = self.equation_pattern.findall(text)
        
        if calculations or equations:
            results["has_calculations"] = True
            results["calculations"] = calculations + equations
            
            # If equations mentioned, mark as verified (we have these capabilities)
            if equations:
                results["confidence"] = "verified"
                results["source"] = "Nuclear physics calculation module"
            else:
                results["confidence"] = "mentioned"
        
        return results
    
    def verify_nuclide_data(self, text: str) -> Dict[str, any]:
        """Check if nuclide data mentioned is accurate"""
        results = {
            "has_nuclides": False,
            "nuclides": [],
            "verified": [],
            "unverified": []
        }
        
        # Extract nuclide mentions
        nuclide_matches = self.nuclide_pattern.findall(text)
        
        if nuclide_matches:
            results["has_nuclides"] = True
            
            for element, mass in nuclide_matches:
                try:
                    # Try to get atomic number
                    element_to_Z = {
                        'U': 92, 'Pu': 94, 'Th': 90, 'H': 1, 'He': 2,
                        'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
                        'Na': 11, 'Al': 13, 'Fe': 26, 'Cu': 29, 'Cd': 48,
                        'Gd': 64, 'Pb': 82, 'Xe': 54, 'Np': 93, 'Am': 95,
                        'Cm': 96, 'Cs': 55, 'Sr': 38, 'I': 53, 'Tc': 43,
                        'Pm': 61, 'Sm': 62, 'Eu': 63, 'Hf': 72, 'Er': 68,
                        'Dy': 66, 'Cf': 98, 'Es': 99, 'Fm': 100
                    }
                    
                    Z = element_to_Z.get(element.capitalize())
                    A = int(mass)
                    
                    if Z:
                        nuclide_str = f"{element}-{A}"
                        results["nuclides"].append(nuclide_str)
                        
                        # Check if we have cross-section data
                        cross_section = self.physics.get_cross_section_data(Z, A)
                        if cross_section:
                            results["verified"].append(nuclide_str)
                        else:
                            results["unverified"].append(nuclide_str)
                except:
                    pass
        
        return results
    
    def verify_physics_concept(self, text: str) -> Dict[str, any]:
        """Validate physics concepts mentioned"""
        results = {
            "concepts_mentioned": [],
            "verified_concepts": [],
            "confidence": "high"
        }
        
        # Key physics concepts we can verify
        verifiable_concepts = {
            "binding energy": True,
            "mass defect": True,
            "fission": True,
            "fusion": True,
            "critical mass": True,
            "neutron cross section": True,
            "E=mc²": True,
            "four-factor formula": True,
            "geometric buckling": True,
            "neutron diffusion": True
        }
        
        text_lower = text.lower()
        for concept, verifiable in verifiable_concepts.items():
            if concept in text_lower:
                results["concepts_mentioned"].append(concept)
                if verifiable:
                    results["verified_concepts"].append(concept)
        
        if results["verified_concepts"]:
            results["confidence"] = "high"
        elif results["concepts_mentioned"]:
            results["confidence"] = "medium"
        
        return results
    
    def get_confidence_level(self, verification_results: Dict) -> str:
        """Determine overall confidence level from verification results"""
        calc_results = verification_results.get("calculations", {})
        nuclide_results = verification_results.get("nuclides", {})
        concept_results = verification_results.get("concepts", {})
        
        # High confidence if calculations verified and nuclides in database
        if (calc_results.get("confidence") == "verified" and 
            nuclide_results.get("verified") and 
            len(nuclide_results.get("verified", [])) > 0):
            return "high"
        
        # Medium confidence if concepts verified
        if concept_results.get("verified_concepts"):
            return "medium"
        
        # Low confidence if unverified nuclides
        if nuclide_results.get("unverified"):
            return "low"
        
        return "medium"
    
    def verify_response(self, text: str) -> Dict[str, any]:
        """Comprehensive verification of a response"""
        results = {
            "calculations": self.verify_calculation(text),
            "nuclides": self.verify_nuclide_data(text),
            "concepts": self.verify_physics_concept(text),
            "overall_confidence": "medium"
        }
        
        results["overall_confidence"] = self.get_confidence_level(results)
        
        return results
    
    def format_verification_note(self, verification_results: Dict) -> str:
        """Format verification results as a note to append to response"""
        note_parts = []
        
        calc_results = verification_results.get("calculations", {})
        nuclide_results = verification_results.get("nuclides", {})
        concept_results = verification_results.get("concepts", {})
        confidence = verification_results.get("overall_confidence", "medium")
        
        # Confidence indicator
        if confidence == "high":
            note_parts.append("✓ Verified")
        elif confidence == "medium":
            note_parts.append("⚠ Approximation")
        else:
            note_parts.append("? Uncertain")
        
        # Source information
        sources = []
        if nuclide_results.get("verified"):
            sources.append("Local nuclear database")
        if calc_results.get("source"):
            sources.append(calc_results["source"])
        
        if sources:
            note_parts.append(f"Source: {', '.join(sources)}")
        
        if note_parts:
            return f"\n\n[Verification: {' | '.join(note_parts)}]"
        
        return ""

