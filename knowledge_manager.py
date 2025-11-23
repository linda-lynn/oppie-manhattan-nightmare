"""
Knowledge Management System for Long-term Learning
Designed for 6-year graduate research use

Features:
- Knowledge extraction from conversations
- Semantic search using TF-IDF
- Knowledge base management
- Entity-relationship extraction
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple
from collections import Counter
import math
from datetime import datetime

class KnowledgeManager:
    def __init__(self, knowledge_base_file: str = "knowledge_base.json", 
                 vector_index_file: str = "vector_index.json"):
        self.knowledge_base_file = knowledge_base_file
        self.vector_index_file = vector_index_file
        
        # Load existing knowledge
        self.knowledge_base = self._load_knowledge_base()
        self.vector_index = self._load_vector_index()
        
        # Extractable patterns
        self.nuclide_pattern = r'\b([A-Z][a-z]?)-?(\d+)\b'
        self.formula_pattern = r'([A-Z][a-z]?\d*|E|m|c²|c\^2|k_eff|η|ε|p|f)'
        self.physical_constant_pattern = r'(\d+\.?\d*)\s*(MeV|keV|eV|J|kg|m|u|barn|barns)'
        
        # Cutting-edge domain keywords
        self.cutting_edge_keywords = {
            "nuclear_fusion": ["fusion reactor", "tokamak", "ITER", "plasma", "inertial confinement", "magnetic confinement"],
            "nuclear_medicine": ["PET scan", "SPECT", "radiotherapy", "nuclear medicine", "medical imaging", "radioisotope"],
            "waste_management": ["transmutation", "nuclear waste", "reprocessing", "repository", "geological disposal"],
            "quantum_computing": ["quantum computing", "quantum simulation", "quantum algorithm", "qubit", "quantum computer"],
            "reactor_physics": ["reactor design", "neutron transport", "fuel cycle", "safety analysis"],
            "nuclear_structure": ["shell model", "nuclear structure", "magic numbers", "nuclear model", "ab initio"]
        }
        
    def _load_knowledge_base(self) -> Dict:
        """Load knowledge base from file"""
        try:
            if os.path.exists(self.knowledge_base_file):
                with open(self.knowledge_base_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data if isinstance(data, dict) else {}
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
        return {
            "entities": {},  # Nuclides, concepts, formulas
            "relationships": [],  # Entity relationships
            "facts": [],  # Extracted facts
            "calculations": [],  # Stored calculation results
            "topics": {},  # Topic clusters
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def _load_vector_index(self) -> Dict:
        """Load vector index for semantic search"""
        try:
            if os.path.exists(self.vector_index_file):
                with open(self.vector_index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading vector index: {e}")
        return {
            "documents": [],
            "term_frequencies": {},
            "document_frequencies": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_knowledge_base(self):
        """Save knowledge base to file"""
        try:
            self.knowledge_base["last_updated"] = datetime.now().isoformat()
            with open(self.knowledge_base_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving knowledge base: {e}")
    
    def _save_vector_index(self):
        """Save vector index to file"""
        try:
            self.vector_index["last_updated"] = datetime.now().isoformat()
            with open(self.vector_index_file, 'w', encoding='utf-8') as f:
                json.dump(self.vector_index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving vector index: {e}")
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text: nuclides, formulas, concepts"""
        entities = {
            "nuclides": [],
            "formulas": [],
            "concepts": [],
            "values": []
        }
        
        # Extract nuclides (e.g., U-235, Pu239, B-10)
        nuclide_matches = re.findall(self.nuclide_pattern, text)
        for element, mass in nuclide_matches:
            nuclide = f"{element}-{mass}"
            if nuclide not in entities["nuclides"]:
                entities["nuclides"].append(nuclide)
        
        # Extract formulas (E=mc², k_eff, etc.)
        if "E=mc²" in text or "E=mc^2" in text:
            entities["formulas"].append("E=mc²")
        if "k_eff" in text or "k-eff" in text:
            entities["formulas"].append("k_eff")
        if "four-factor" in text.lower() or "η" in text or "epsilon" in text.lower():
            entities["formulas"].append("four_factor_formula")
        
        # Extract key concepts
        concepts = [
            "critical mass", "cross section", "binding energy", "fission",
            "fusion", "neutron capture", "alpha decay", "beta decay",
            "shell model", "liquid drop model", "mass defect", "Q value"
        ]
        for concept in concepts:
            if concept.lower() in text.lower():
                entities["concepts"].append(concept)
        
        # Extract numerical values with units
        value_matches = re.findall(self.physical_constant_pattern, text)
        for value, unit in value_matches:
            entities["values"].append(f"{value} {unit}")
        
        return entities
    
    def extract_knowledge(self, conversation_text: str, context: str = "") -> Dict:
        """Extract structured knowledge from conversation"""
        entities = self.extract_entities(conversation_text)
        
        knowledge = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "entities": entities,
            "summary": self._summarize_text(conversation_text),
            "topics": self._identify_topics(conversation_text)
        }
        
        return knowledge
    
    def _summarize_text(self, text: str, max_length: int = 200) -> str:
        """Create a summary of the text"""
        # Simple summarization: take first few sentences
        sentences = re.split(r'[.!?]\s+', text)
        summary = '. '.join(sentences[:3])
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        return summary
    
    def _identify_topics(self, text: str) -> List[str]:
        """Identify topics in the text"""
        topics = []
        text_lower = text.lower()
        
        topic_keywords = {
            "critical_mass": ["critical mass", "critical point", "criticality"],
            "cross_sections": ["cross section", "neutron cross section", "absorption", "scattering"],
            "binding_energy": ["binding energy", "mass defect", "E=mc²"],
            "fission": ["fission", "fissile", "fissionable"],
            "fusion": ["fusion", "fusion reaction"],
            "decay": ["decay", "alpha decay", "beta decay", "half-life"],
            "reactor_physics": ["reactor", "neutron multiplication", "k_eff", "four-factor"],
            "nuclear_structure": ["shell model", "nuclear structure", "magic numbers"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def add_knowledge(self, knowledge: Dict):
        """Add extracted knowledge to knowledge base"""
        # Update entities
        for entity_type, entity_list in knowledge.get("entities", {}).items():
            if entity_type not in self.knowledge_base["entities"]:
                self.knowledge_base["entities"][entity_type] = {}
            
            for entity in entity_list:
                if entity not in self.knowledge_base["entities"][entity_type]:
                    self.knowledge_base["entities"][entity_type][entity] = {
                        "first_seen": knowledge.get("timestamp"),
                        "mentions": 0,
                        "contexts": []
                    }
                
                self.knowledge_base["entities"][entity_type][entity]["mentions"] += 1
                self.knowledge_base["entities"][entity_type][entity]["contexts"].append(
                    knowledge.get("summary", "")
                )
        
        # Add to facts
        self.knowledge_base["facts"].append(knowledge)
        
        # Update topics
        for topic in knowledge.get("topics", []):
            if topic not in self.knowledge_base["topics"]:
                self.knowledge_base["topics"][topic] = []
            self.knowledge_base["topics"][topic].append(knowledge.get("timestamp"))
        
        # Keep only last 1000 facts to manage size
        if len(self.knowledge_base["facts"]) > 1000:
            self.knowledge_base["facts"] = self.knowledge_base["facts"][-1000:]
        
        self._save_knowledge_base()
    
    def add_to_vector_index(self, document_id: str, text: str):
        """Add document to vector index for semantic search"""
        # Simple tokenization
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Update term frequencies
        doc_term_freq = Counter(words)
        for word, count in doc_term_freq.items():
            if word not in self.vector_index["term_frequencies"]:
                self.vector_index["term_frequencies"][word] = {}
            self.vector_index["term_frequencies"][word][document_id] = count
            
            # Update document frequencies
            if word not in self.vector_index["document_frequencies"]:
                self.vector_index["document_frequencies"][word] = 0
            if document_id not in self.vector_index.get("term_frequencies", {}).get(word, {}):
                self.vector_index["document_frequencies"][word] += 1
        
        # Add document
        self.vector_index["documents"].append({
            "id": document_id,
            "text": text[:500],  # Store first 500 chars
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 500 documents
        if len(self.vector_index["documents"]) > 500:
            self.vector_index["documents"] = self.vector_index["documents"][-500:]
        
        self._save_vector_index()
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Semantic search using TF-IDF similarity"""
        query_words = re.findall(r'\b\w+\b', query.lower())
        
        if not query_words:
            return []
        
        scores = {}
        total_docs = len(self.vector_index["documents"])
        
        # Calculate TF-IDF scores
        for doc in self.vector_index["documents"]:
            doc_id = doc["id"]
            doc_words = re.findall(r'\b\w+\b', doc["text"].lower())
            doc_term_freq = Counter(doc_words)
            
            score = 0.0
            for word in query_words:
                # Term Frequency (TF)
                tf = doc_term_freq.get(word, 0) / len(doc_words) if doc_words else 0
                
                # Inverse Document Frequency (IDF)
                df = self.vector_index["document_frequencies"].get(word, 0)
                idf = math.log(total_docs / (df + 1)) if total_docs > 0 else 0
                
                # TF-IDF score
                score += tf * idf
            
            if score > 0:
                scores[doc_id] = {
                    "score": score,
                    "text": doc["text"],
                    "timestamp": doc.get("timestamp", "")
                }
        
        # Sort by score and return top K
        sorted_results = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
        return [{"id": doc_id, **info} for doc_id, info in sorted_results[:top_k]]
    
    def search_knowledge_base(self, query: str) -> Dict:
        """Search knowledge base for relevant information"""
        results = {
            "entities": [],
            "facts": [],
            "topics": [],
            "related_conversations": []
        }
        
        query_lower = query.lower()
        
        # Search entities
        for entity_type, entities in self.knowledge_base.get("entities", {}).items():
            for entity, info in entities.items():
                if query_lower in entity.lower() or query_lower in str(info.get("contexts", [])).lower():
                    results["entities"].append({
                        "type": entity_type,
                        "name": entity,
                        "mentions": info.get("mentions", 0),
                        "first_seen": info.get("first_seen", ""),
                        "sample_context": info.get("contexts", [])[-1] if info.get("contexts") else ""
                    })
        
        # Search facts
        for fact in self.knowledge_base.get("facts", [])[-100:]:  # Last 100 facts
            if query_lower in fact.get("summary", "").lower() or any(
                query_lower in str(topic).lower() for topic in fact.get("topics", [])
            ):
                results["facts"].append(fact)
        
        # Semantic search in vector index
        semantic_results = self.semantic_search(query, top_k=3)
        results["related_conversations"] = semantic_results
        
        return results
    
    def get_knowledge_summary(self) -> Dict:
        """Get summary statistics of knowledge base"""
        return {
            "total_entities": sum(
                len(entities) for entities in self.knowledge_base.get("entities", {}).values()
            ),
            "total_facts": len(self.knowledge_base.get("facts", [])),
            "total_topics": len(self.knowledge_base.get("topics", {})),
            "total_documents_indexed": len(self.vector_index.get("documents", [])),
            "most_mentioned_entities": self._get_most_mentioned(),
            "active_topics": self._get_active_topics(),
            "created": self.knowledge_base.get("created", ""),
            "last_updated": self.knowledge_base.get("last_updated", "")
        }
    
    def _get_most_mentioned(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get most mentioned entities"""
        all_entities = []
        for entity_type, entities in self.knowledge_base.get("entities", {}).items():
            for entity, info in entities.items():
                all_entities.append((f"{entity} ({entity_type})", info.get("mentions", 0)))
        
        return sorted(all_entities, key=lambda x: x[1], reverse=True)[:top_n]
    
    def _get_active_topics(self) -> List[str]:
        """Get most active topics"""
        topics = self.knowledge_base.get("topics", {})
        topic_counts = {topic: len(timestamps) for topic, timestamps in topics.items()}
        return sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def batch_add_knowledge(self, knowledge_list: List[Dict], batch_size: int = 100):
        """
        Batch add knowledge to knowledge base with performance optimization
        
        Args:
            knowledge_list: List of knowledge dictionaries to add
            batch_size: Number of items to process before saving
        """
        total = len(knowledge_list)
        print(f"Batch importing {total} knowledge items...")
        
        for i, knowledge in enumerate(knowledge_list):
            # Extract knowledge from imported data format
            if "content" in knowledge:
                # This is imported data, extract knowledge from it
                extracted = self.extract_knowledge(
                    knowledge.get("content", ""),
                    context=f"Imported from {knowledge.get('source', 'unknown')}"
                )
                # Merge with imported metadata
                extracted["source"] = knowledge.get("source", "unknown")
                extracted["title"] = knowledge.get("title", "")
                extracted["url"] = knowledge.get("url", "")
                extracted["domain"] = knowledge.get("domain", "general_nuclear_physics")
                extracted["formulas"] = knowledge.get("formulas", [])
                extracted["nuclides"] = knowledge.get("nuclides", [])
                extracted["concepts"] = knowledge.get("concepts", [])
                knowledge = extracted
            
            # Add to knowledge base
            self.add_knowledge(knowledge)
            
            # Add to vector index
            doc_id = f"imported_{knowledge.get('timestamp', datetime.now().isoformat())}_{i}"
            content = knowledge.get("content", knowledge.get("summary", ""))
            if content:
                self.add_to_vector_index(doc_id, content)
            
            # Save periodically to avoid data loss
            if (i + 1) % batch_size == 0:
                print(f"Processed {i + 1}/{total} items...")
                self._save_knowledge_base()
                self._save_vector_index()
        
        # Final save
        self._save_knowledge_base()
        self._save_vector_index()
        print(f"Batch import complete: {total} items imported")
    
    def enhance_entity_extraction(self):
        """Enhance entity extraction with more patterns"""
        # Add more nuclide patterns
        self.nuclide_pattern = r'\b([A-Z][a-z]?)[-\s]*(\d+)\b'
        
        # Add more formula patterns
        self.formula_patterns = [
            r'E\s*=\s*mc[²2]',
            r'k_eff\s*=\s*[^=]+',
            r'σ\s*=\s*[^=]+',
            r'λ\s*=\s*[^=]+',
            r'η\s*=\s*[^=]+',
            r'ε\s*=\s*[^=]+',
            r'p\s*=\s*[^=]+',
            r'f\s*=\s*[^=]+',
            r'[A-Z][a-z]?\d*\s*→\s*[A-Z][a-z]?\d*',  # Decay chains
            r'[A-Z][a-z]?\d*\s*\+\s*[A-Z][a-z]?\d*\s*→',  # Reactions
        ]
        
        # Add cutting-edge domain keywords
        self.cutting_edge_keywords = {
            "nuclear_fusion": ["fusion reactor", "tokamak", "ITER", "plasma", "inertial confinement", "magnetic confinement"],
            "nuclear_medicine": ["PET scan", "SPECT", "radiotherapy", "nuclear medicine", "medical imaging", "radioisotope"],
            "waste_management": ["transmutation", "nuclear waste", "reprocessing", "repository", "geological disposal"],
            "quantum_computing": ["quantum computing", "quantum simulation", "quantum algorithm", "qubit", "quantum computer"],
            "reactor_physics": ["reactor design", "neutron transport", "fuel cycle", "safety analysis"],
            "nuclear_structure": ["shell model", "nuclear structure", "magic numbers", "nuclear model", "ab initio"]
        }
    
    def add_domain_classification(self, knowledge: Dict) -> str:
        """Classify knowledge into domain categories"""
        content = (knowledge.get("content", "") + " " + knowledge.get("summary", "")).lower()
        
        for domain, keywords in self.cutting_edge_keywords.items():
            if any(keyword.lower() in content for keyword in keywords):
                return domain
        
        return "general_nuclear_physics"
    
    def add_citation_tracking(self, knowledge: Dict):
        """Track data sources and citations"""
        if "citations" not in self.knowledge_base:
            self.knowledge_base["citations"] = {}
        
        source = knowledge.get("source", "unknown")
        url = knowledge.get("url", "")
        title = knowledge.get("title", "")
        
        citation_key = f"{source}_{hash(url + title) % 10000}"
        
        if citation_key not in self.knowledge_base["citations"]:
            self.knowledge_base["citations"][citation_key] = {
                "source": source,
                "url": url,
                "title": title,
                "first_cited": knowledge.get("timestamp", datetime.now().isoformat()),
                "citation_count": 0
            }
        
        self.knowledge_base["citations"][citation_key]["citation_count"] += 1
    
    def optimize_vector_index(self):
        """Optimize vector index for large-scale data"""
        # Increase document limit for large-scale imports
        max_documents = 10000  # Increased from 500
        
        if len(self.vector_index["documents"]) > max_documents:
            # Keep most recent documents
            self.vector_index["documents"] = self.vector_index["documents"][-max_documents:]
            
            # Clean up term frequencies for removed documents
            removed_ids = set()
            # This is simplified - in production, track removed IDs
            
            # Rebuild document frequencies
            doc_ids = {doc["id"] for doc in self.vector_index["documents"]}
            for word in list(self.vector_index["term_frequencies"].keys()):
                self.vector_index["term_frequencies"][word] = {
                    doc_id: count for doc_id, count in self.vector_index["term_frequencies"][word].items()
                    if doc_id in doc_ids
                }
                
                # Update document frequency
                self.vector_index["document_frequencies"][word] = len(
                    self.vector_index["term_frequencies"][word]
                )
        
        self._save_vector_index()
    
    def build_semantic_graph(self) -> Dict:
        """Build entity relationship graph for complex semantic search"""
        graph = {
            "nodes": [],
            "edges": []
        }
        
        # Create nodes from entities
        for entity_type, entities in self.knowledge_base.get("entities", {}).items():
            for entity, info in entities.items():
                graph["nodes"].append({
                    "id": entity,
                    "type": entity_type,
                    "mentions": info.get("mentions", 0)
                })
        
        # Create edges from facts (entities mentioned together)
        for fact in self.knowledge_base.get("facts", []):
            entities_in_fact = []
            for entity_type, entity_list in fact.get("entities", {}).items():
                entities_in_fact.extend(entity_list)
            
            # Create edges between entities mentioned together
            for i, entity1 in enumerate(entities_in_fact):
                for entity2 in entities_in_fact[i+1:]:
                    graph["edges"].append({
                        "source": entity1,
                        "target": entity2,
                        "weight": 1  # Could be weighted by co-occurrence frequency
                    })
        
        return graph




