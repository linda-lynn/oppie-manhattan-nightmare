"""
Personality Enhancer for J. Robert Oppenheimer AI Companion
Enhances responses with historical context, philosophical reflections, and authentic speech patterns
"""

import json
import os
import random
import re
from typing import Dict, List, Optional

class PersonalityEnhancer:
    def __init__(self, personality_file: str = "oppenheimer_personality.json"):
        """Initialize personality enhancer with personality database"""
        self.personality_data = self._load_personality_data(personality_file)
    
    def _load_personality_data(self, filepath: str) -> Dict:
        """Load personality data from JSON file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load personality data: {e}")
        
        # Return empty structure if file not found
        return {
            "historical_quotes": [],
            "personality_traits": {},
            "speech_patterns": {},
            "historical_references": {},
            "philosophical_reflections": [],
            "companion_qualities": {}
        }
    
    def add_historical_context(self, text: str, topic: Optional[str] = None) -> str:
        """Add relevant historical references to the response with increased frequency"""
        if not self.personality_data.get("historical_references"):
            return text
        
        refs = self.personality_data["historical_references"]
        
        # Check if text mentions nuclear physics concepts (increased to 40-50% chance)
        if any(concept in text.lower() for concept in ["nuclear", "fission", "critical", "reactor", "atomic", "isotope"]):
            if random.random() < 0.45:  # Increased from 30% to 45%
                locations = refs.get("locations", [])
                if locations:
                    location = random.choice(locations)
                    if "los alamos" not in text.lower() and location.lower() not in text.lower():
                        text += f"\n\nThis brings to mind our work at {location} during those crucial years."
        
        # Check if text mentions theoretical physics (increased to 35-40% chance)
        if any(concept in text.lower() for concept in ["quantum", "theory", "equation", "principle", "mathematical", "theoretical", "schrödinger", "hamiltonian"]):
            if random.random() < 0.38:  # Increased from 25% to 38%
                colleagues = refs.get("colleagues", [])
                if colleagues:
                    colleague = random.choice(colleagues)
                    if colleague.lower() not in text.lower():
                        text += f"\n\n{colleague} and I often discussed similar questions during our time together. The theoretical framework we developed then remains foundational to this day."
        
        return text
    
    def add_philosophical_reflection(self, text: str, context: Optional[str] = None) -> str:
        """Add contemplative philosophical elements when appropriate with increased frequency"""
        reflections = self.personality_data.get("philosophical_reflections", [])
        
        if not reflections:
            return text
        
        # Expanded list of philosophical topics
        philosophical_topics = [
            "responsibility", "ethics", "consequence", "implication", "future", "impact",
            "weapon", "destruction", "peace", "humanity", "scientist", "knowledge", "power",
            "discovery", "research", "understanding", "truth", "reality", "nature", "universe",
            "existence", "meaning", "purpose", "wisdom", "understanding"
        ]
        
        if any(topic in text.lower() for topic in philosophical_topics):
            if random.random() < 0.45:  # Increased from 35% to 45% chance
                reflection = random.choice(reflections)
                text += f"\n\n{reflection}"
        
        # Also add philosophical reflection for longer responses (to enhance depth)
        if len(text) > 500 and random.random() < 0.25:  # 25% chance for longer responses
            reflection = random.choice(reflections)
            if reflection not in text:
                text += f"\n\n{reflection}"
        
        return text
    
    def add_moral_reflection(self, text: str, context: Optional[str] = None) -> str:
        """Add moral reflection when discussing weapons, destruction, or scientific responsibility"""
        moral_reflections = self.personality_data.get("moral_reflections", [])
        
        if not moral_reflections:
            return text
        
        # Trigger words for moral reflection
        moral_topics = [
            "weapon", "bomb", "destruction", "war", "kill", "death", "atomic bomb",
            "nuclear weapon", "mass destruction", "responsibility", "ethics", "moral",
            "consequence", "impact", "humanity", "scientist responsibility"
        ]
        
        if any(topic in text.lower() for topic in moral_topics):
            if random.random() < 0.4:  # 40% chance for moral topics
                reflection = random.choice(moral_reflections)
                text += f"\n\n{reflection}"
        
        return text
    
    def add_historical_context_moral(self, text: str, context: Optional[str] = None) -> str:
        """Add historical context with moral implications"""
        historical_events = self.personality_data.get("historical_moral_events", [])
        
        if not historical_events:
            return text
        
        # Check for topics that might trigger historical moral context
        historical_topics = [
            "trinity", "test", "hiroshima", "nagasaki", "manhattan", "atomic bomb",
            "nuclear weapon", "first test", "first explosion"
        ]
        
        if any(topic in text.lower() for topic in historical_topics):
            if random.random() < 0.3:  # 30% chance
                event = random.choice(historical_events)
                event_name = event.get("event", "")
                reflection = event.get("reflection", "")
                if reflection:
                    text += f"\n\nThis brings to mind {event_name}. {reflection}"
        
        return text
    
    def apply_speech_patterns(self, text: str) -> str:
        """Enhance text to match Oppenheimer's speech patterns with increased frequency"""
        patterns = self.personality_data.get("speech_patterns", {})
        common_phrases = patterns.get("common_phrases", [])
        mathematical_phrases = patterns.get("mathematical_phrases", [])
        
        # Increased frequency for stronger personality (30-40% chance)
        if random.random() < 0.35 and common_phrases:
            # Add a thoughtful phrase at the beginning
            phrase = random.choice(common_phrases)
            if not any(text.startswith(p) for p in common_phrases):
                text = f"{phrase} {text}"
        
        # Add mathematical phrases when discussing physics/math (40% chance)
        if mathematical_phrases and any(keyword in text.lower() for keyword in 
            ["equation", "formula", "calculate", "derive", "mathematical", "theoretical", 
             "quantum", "nuclear", "binding", "cross section", "scattering", "decay"]):
            if random.random() < 0.4:
                math_phrase = random.choice(mathematical_phrases)
                # Insert after first sentence if text is long enough
                sentences = text.split('. ')
                if len(sentences) > 1:
                    sentences.insert(1, math_phrase)
                    text = '. '.join(sentences)
                else:
                    text = f"{math_phrase} {text}"
        
        return text
    
    def add_companion_touch(self, text: str, conversation_context: Optional[Dict] = None) -> str:
        """Add companion-like warmth and personal connection with increased frequency"""
        qualities = self.personality_data.get("companion_qualities", {})
        
        # Increased frequency for encouragement (35-40% chance)
        if random.random() < 0.38:  # Increased from 25% to 38%
            encouragements = qualities.get("encouragement", [])
            if encouragements:
                encouragement = random.choice(encouragements)
                # Add at end (removed length restriction for more frequent encouragement)
                text += f"\n\n{encouragement}"
        
        # Reference past conversations if context provided (increased frequency)
        if conversation_context and random.random() < 0.35:  # Increased from 30% to 35%
            connections = qualities.get("connection", [])
            if connections:
                connection_phrase = random.choice(connections)
                # Add connection phrase to show continuity
                text = f"{connection_phrase} {text}"
        
        return text
    
    def enhance_response(self, text: str, context: Optional[Dict] = None) -> str:
        """Apply all personality enhancements to a response with increased intensity"""
        # Apply in order: speech patterns, historical context, philosophical reflection, 
        # moral reflection, historical moral context, companion touch
        enhanced = self.apply_speech_patterns(text)
        enhanced = self.add_historical_context(enhanced, context.get("topic") if context else None)
        enhanced = self.add_philosophical_reflection(enhanced, context.get("context") if context else None)
        enhanced = self.add_moral_reflection(enhanced, context.get("context") if context else None)
        enhanced = self.add_historical_context_moral(enhanced, context.get("context") if context else None)
        enhanced = self.add_companion_touch(enhanced, context.get("conversation") if context else None)
        
        # Ensure response length is adequate (add more depth if too short)
        if len(enhanced) < 300 and context:
            # Add additional context or reflection for short responses
            topic = context.get("topic", "")
            if topic:
                # Add a thoughtful expansion
                patterns = self.personality_data.get("speech_patterns", {})
                mathematical_phrases = patterns.get("mathematical_phrases", [])
                if mathematical_phrases and any(kw in topic.lower() for kw in 
                    ["calculate", "derive", "equation", "formula", "theoretical"]):
                    math_phrase = random.choice(mathematical_phrases)
                    enhanced += f"\n\n{math_phrase} This requires careful mathematical treatment, and I encourage you to work through the derivations yourself to deepen your understanding."
        
        return enhanced
    
    def get_thinking_phrase(self) -> str:
        """Get a random thinking phrase for the thinking process display"""
        patterns = self.personality_data.get("speech_patterns", {})
        thinking_indicators = patterns.get("thinking_indicators", [])
        
        if thinking_indicators:
            return random.choice(thinking_indicators)
        return "Let me consider this carefully..."

