"""
Batch Data Import Tool for Nuclear Physics Knowledge Base
Imports data from multiple sources for cutting-edge domains and fundamental nuclear physics
"""

import json
import os
from typing import List, Dict
from data_importer import DataImporter
from knowledge_manager import KnowledgeManager

class BatchDataImporter:
    def __init__(self, config_file: str = "data_sources.json"):
        """Initialize batch importer with configuration"""
        self.importer = DataImporter()
        self.knowledge_manager = KnowledgeManager()
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        # Default configuration
        return {
            "google_scholar_queries": [
                "nuclear fusion reactor design",
                "nuclear medicine imaging",
                "nuclear waste transmutation",
                "quantum computing nuclear physics"
            ],
            "mit_ocw_courses": [],
            "nature_keywords": ["nuclear physics", "fusion energy", "nuclear medicine"],
            "iaea_nuclides": ["U-235", "Pu-239", "Th-232"],
            "import_schedule": "weekly"
        }
    
    def import_cutting_edge_domains(self) -> Dict:
        """
        Import data for cutting-edge nuclear physics domains
        
        Returns:
            Dictionary with import statistics
        """
        print("=" * 60)
        print("Importing Cutting-Edge Nuclear Physics Data")
        print("=" * 60)
        
        all_imported = []
        stats = {
            "nuclear_fusion": 0,
            "nuclear_medicine": 0,
            "waste_management": 0,
            "quantum_computing": 0,
            "total": 0
        }
        
        # 1. Nuclear Fusion
        print("\n[1/4] Importing Nuclear Fusion data...")
        fusion_queries = [
            "ITER tokamak fusion reactor",
            "inertial confinement fusion",
            "magnetic confinement fusion",
            "plasma physics nuclear fusion"
        ]
        for query in fusion_queries:
            try:
                papers = self.importer.import_from_google_scholar(query, max_results=20)
                fusion_papers = [p for p in papers if "fusion" in p.get("content", "").lower()]
                all_imported.extend(fusion_papers)
                stats["nuclear_fusion"] += len(fusion_papers)
                print(f"  Imported {len(fusion_papers)} papers for: {query}")
            except Exception as e:
                print(f"  Error importing fusion data: {e}")
        
        # 2. Nuclear Medicine
        print("\n[2/4] Importing Nuclear Medicine data...")
        medicine_queries = [
            "PET SPECT nuclear medicine imaging",
            "radiotherapy nuclear medicine",
            "radioisotope medical applications"
        ]
        for query in medicine_queries:
            try:
                papers = self.importer.import_from_google_scholar(query, max_results=20)
                medicine_papers = [p for p in papers if any(kw in p.get("content", "").lower() 
                                                           for kw in ["PET", "SPECT", "radiotherapy", "medical"])]
                all_imported.extend(medicine_papers)
                stats["nuclear_medicine"] += len(medicine_papers)
                print(f"  Imported {len(medicine_papers)} papers for: {query}")
            except Exception as e:
                print(f"  Error importing medicine data: {e}")
        
        # 3. Waste Management
        print("\n[3/4] Importing Nuclear Waste Management data...")
        waste_queries = [
            "nuclear waste transmutation",
            "nuclear waste reprocessing",
            "geological disposal nuclear waste"
        ]
        for query in waste_queries:
            try:
                papers = self.importer.import_from_google_scholar(query, max_results=20)
                waste_papers = [p for p in papers if "waste" in p.get("content", "").lower()]
                all_imported.extend(waste_papers)
                stats["waste_management"] += len(waste_papers)
                print(f"  Imported {len(waste_papers)} papers for: {query}")
            except Exception as e:
                print(f"  Error importing waste management data: {e}")
        
        # 4. Quantum Computing
        print("\n[4/4] Importing Quantum Computing in Nuclear Physics data...")
        quantum_queries = [
            "quantum computing nuclear physics simulation",
            "quantum algorithm nuclear physics",
            "quantum simulation nuclear reactions"
        ]
        for query in quantum_queries:
            try:
                papers = self.importer.import_from_google_scholar(query, max_results=20)
                quantum_papers = [p for p in papers if "quantum" in p.get("content", "").lower()]
                all_imported.extend(quantum_papers)
                stats["quantum_computing"] += len(quantum_papers)
                print(f"  Imported {len(quantum_papers)} papers for: {query}")
            except Exception as e:
                print(f"  Error importing quantum computing data: {e}")
        
        # Import to knowledge base
        print(f"\nImporting {len(all_imported)} items to knowledge base...")
        self.knowledge_manager.batch_add_knowledge(all_imported)
        
        stats["total"] = len(all_imported)
        print(f"\n✓ Cutting-edge domains import complete!")
        print(f"  Total items imported: {stats['total']}")
        print(f"  - Nuclear Fusion: {stats['nuclear_fusion']}")
        print(f"  - Nuclear Medicine: {stats['nuclear_medicine']}")
        print(f"  - Waste Management: {stats['waste_management']}")
        print(f"  - Quantum Computing: {stats['quantum_computing']}")
        
        return stats
    
    def import_fundamental_nuclear_physics(self) -> Dict:
        """
        Import fundamental nuclear physics data
        
        Returns:
            Dictionary with import statistics
        """
        print("=" * 60)
        print("Importing Fundamental Nuclear Physics Data")
        print("=" * 60)
        
        all_imported = []
        stats = {
            "nuclear_structure": 0,
            "nuclear_reactions": 0,
            "neutron_physics": 0,
            "decay_processes": 0,
            "nuclear_data": 0,
            "total": 0
        }
        
        # 1. Nuclear Structure
        print("\n[1/5] Importing Nuclear Structure data...")
        structure_queries = [
            "nuclear shell model",
            "nuclear structure theory",
            "magic numbers nuclear physics"
        ]
        for query in structure_queries:
            try:
                papers = self.importer.import_from_google_scholar(query, max_results=15)
                all_imported.extend(papers)
                stats["nuclear_structure"] += len(papers)
                print(f"  Imported {len(papers)} papers for: {query}")
            except Exception as e:
                print(f"  Error importing structure data: {e}")
        
        # 2. Nuclear Reactions
        print("\n[2/5] Importing Nuclear Reactions data...")
        reaction_queries = [
            "nuclear reaction mechanisms",
            "neutron capture reactions",
            "fission fusion reactions"
        ]
        for query in reaction_queries:
            try:
                papers = self.importer.import_from_google_scholar(query, max_results=15)
                all_imported.extend(papers)
                stats["nuclear_reactions"] += len(papers)
                print(f"  Imported {len(papers)} papers for: {query}")
            except Exception as e:
                print(f"  Error importing reaction data: {e}")
        
        # 3. Neutron Physics
        print("\n[3/5] Importing Neutron Physics data...")
        neutron_queries = [
            "neutron transport theory",
            "neutron cross sections",
            "neutron moderation"
        ]
        for query in neutron_queries:
            try:
                papers = self.importer.import_from_google_scholar(query, max_results=15)
                all_imported.extend(papers)
                stats["neutron_physics"] += len(papers)
                print(f"  Imported {len(papers)} papers for: {query}")
            except Exception as e:
                print(f"  Error importing neutron physics data: {e}")
        
        # 4. Decay Processes
        print("\n[4/5] Importing Decay Processes data...")
        decay_queries = [
            "alpha beta gamma decay",
            "nuclear decay chains",
            "radioactive decay theory"
        ]
        for query in decay_queries:
            try:
                papers = self.importer.import_from_google_scholar(query, max_results=15)
                all_imported.extend(papers)
                stats["decay_processes"] += len(papers)
                print(f"  Imported {len(papers)} papers for: {query}")
            except Exception as e:
                print(f"  Error importing decay data: {e}")
        
        # 5. Nuclear Data from IAEA
        print("\n[5/5] Importing Nuclear Data from IAEA NUCLEUS/NDS...")
        nuclides = self.config.get("iaea_nuclides", ["U-235", "Pu-239", "Th-232"])
        for nuclide in nuclides:
            try:
                data = self.importer.import_from_iaea_nucleus({
                    "nuclide": nuclide,
                    "data_type": "decay"
                })
                all_imported.extend(data)
                stats["nuclear_data"] += len(data)
                print(f"  Imported data for: {nuclide}")
            except Exception as e:
                print(f"  Error importing IAEA data for {nuclide}: {e}")
        
        # Import to knowledge base
        print(f"\nImporting {len(all_imported)} items to knowledge base...")
        self.knowledge_manager.batch_add_knowledge(all_imported)
        
        stats["total"] = len(all_imported)
        print(f"\n✓ Fundamental nuclear physics import complete!")
        print(f"  Total items imported: {stats['total']}")
        print(f"  - Nuclear Structure: {stats['nuclear_structure']}")
        print(f"  - Nuclear Reactions: {stats['nuclear_reactions']}")
        print(f"  - Neutron Physics: {stats['neutron_physics']}")
        print(f"  - Decay Processes: {stats['decay_processes']}")
        print(f"  - Nuclear Data: {stats['nuclear_data']}")
        
        return stats
    
    def import_from_predefined_sources(self) -> Dict:
        """Import from predefined sources in configuration"""
        print("=" * 60)
        print("Importing from Predefined Sources")
        print("=" * 60)
        
        all_imported = []
        stats = {"total": 0}
        
        # Google Scholar queries
        queries = self.config.get("google_scholar_queries", [])
        if queries:
            print(f"\nImporting from Google Scholar ({len(queries)} queries)...")
            for query in queries:
                try:
                    papers = self.importer.import_from_google_scholar(query, max_results=30)
                    all_imported.extend(papers)
                    print(f"  Imported {len(papers)} papers for: {query}")
                except Exception as e:
                    print(f"  Error importing: {e}")
        
        # MIT OCW courses
        courses = self.config.get("mit_ocw_courses", [])
        if courses:
            print(f"\nImporting from MIT OpenCourseWare ({len(courses)} courses)...")
            for course_url in courses:
                try:
                    materials = self.importer.import_from_mit_ocw([course_url])
                    all_imported.extend(materials)
                    print(f"  Imported materials from: {course_url}")
                except Exception as e:
                    print(f"  Error importing: {e}")
        
        # Nature keywords
        nature_keywords = self.config.get("nature_keywords", [])
        if nature_keywords:
            print(f"\nImporting from Nature ({len(nature_keywords)} keywords)...")
            for keyword in nature_keywords:
                try:
                    papers = self.importer.import_from_nature(keyword, max_results=20)
                    all_imported.extend(papers)
                    print(f"  Imported {len(papers)} papers for: {keyword}")
                except Exception as e:
                    print(f"  Error importing: {e}")
        
        # Import to knowledge base
        if all_imported:
            print(f"\nImporting {len(all_imported)} items to knowledge base...")
            self.knowledge_manager.batch_add_knowledge(all_imported)
        
        stats["total"] = len(all_imported)
        print(f"\n✓ Predefined sources import complete!")
        print(f"  Total items imported: {stats['total']}")
        
        return stats
    
    def import_all(self) -> Dict:
        """Import all data from all sources"""
        print("=" * 60)
        print("FULL DATA IMPORT - All Sources")
        print("=" * 60)
        
        total_stats = {
            "cutting_edge": {},
            "fundamental": {},
            "predefined": {},
            "grand_total": 0
        }
        
        # Import cutting-edge domains
        total_stats["cutting_edge"] = self.import_cutting_edge_domains()
        
        # Import fundamental physics
        total_stats["fundamental"] = self.import_fundamental_nuclear_physics()
        
        # Import from predefined sources
        total_stats["predefined"] = self.import_from_predefined_sources()
        
        # Calculate grand total
        total_stats["grand_total"] = (
            total_stats["cutting_edge"].get("total", 0) +
            total_stats["fundamental"].get("total", 0) +
            total_stats["predefined"].get("total", 0)
        )
        
        print("\n" + "=" * 60)
        print("IMPORT SUMMARY")
        print("=" * 60)
        print(f"Cutting-Edge Domains: {total_stats['cutting_edge'].get('total', 0)} items")
        print(f"Fundamental Physics: {total_stats['fundamental'].get('total', 0)} items")
        print(f"Predefined Sources: {total_stats['predefined'].get('total', 0)} items")
        print(f"GRAND TOTAL: {total_stats['grand_total']} items")
        print("=" * 60)
        
        # Optimize knowledge base
        print("\nOptimizing knowledge base...")
        self.knowledge_manager.optimize_vector_index()
        
        # Get final statistics
        kb_summary = self.knowledge_manager.get_knowledge_summary()
        print(f"\nKnowledge Base Statistics:")
        print(f"  Total Entities: {kb_summary['total_entities']}")
        print(f"  Total Facts: {kb_summary['total_facts']}")
        print(f"  Total Topics: {kb_summary['total_topics']}")
        print(f"  Documents Indexed: {kb_summary['total_documents_indexed']}")
        
        return total_stats

if __name__ == "__main__":
    importer = BatchDataImporter()
    
    # Run full import
    print("\nStarting full data import...")
    stats = importer.import_all()
    
    print("\n✓ Import complete!")

