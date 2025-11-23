"""
Import Mathematical Data into Knowledge Base
Imports comprehensive mathematical formulas, derivations, and calculations
"""

import json
import os
import sys
from knowledge_manager import KnowledgeManager
from mathematical_data_generator import MathematicalDataGenerator
from data_importer import DataImporter

def import_mathematical_data(knowledge_manager: KnowledgeManager):
    """Import all mathematical data into knowledge base"""
    
    print("=" * 60)
    print("Importing Mathematical Data into Knowledge Base")
    print("=" * 60)
    
    # Generate mathematical formulas
    print("\n1. Generating mathematical formulas...")
    generator = MathematicalDataGenerator()
    mathematical_data = generator.generate_all_mathematical_data()
    
    print(f"   Generated {len(mathematical_data)} mathematical formulas")
    
    # Import into knowledge base
    print("\n2. Importing into knowledge base...")
    imported_count = 0
    
    for item in mathematical_data:
        try:
            # Extract entities
            entities = knowledge_manager.extract_entities(item["content"])
            
            # Add to knowledge base
            knowledge_item = {
                "content": item["content"],
                "source": item["source"],
                "title": item["title"],
                "formulas": item.get("formulas", []),
                "nuclides": entities.get("nuclides", []),
                "concepts": entities.get("concepts", []),
                "keywords": item.get("keywords", []),
                "domain": item.get("domain", "general"),
                "category": item.get("category", ""),
                "publication_date": item.get("publication_date", ""),
                "imported_at": item.get("imported_at", "")
            }
            
            knowledge_manager.add_knowledge(knowledge_item)
            imported_count += 1
            
            if imported_count % 10 == 0:
                print(f"   Imported {imported_count}/{len(mathematical_data)} formulas...")
                
        except Exception as e:
            print(f"   Error importing item '{item.get('title', 'unknown')}': {e}")
            continue
    
    print(f"\n✓ Successfully imported {imported_count} mathematical formulas")
    
    # Add to vector index for semantic search
    print("\n3. Building semantic search index...")
    for idx, item in enumerate(mathematical_data):
        doc_id = f"math_formula_{idx}_{item.get('category', 'unknown')}"
        text = item.get("content", "")
        if text:
            knowledge_manager.add_to_vector_index(doc_id, text)
    print("   ✓ Vector index updated")
    
    # Save knowledge base
    print("\n4. Saving knowledge base...")
    knowledge_manager._save_knowledge_base()
    knowledge_manager._save_vector_index()
    print("   ✓ Knowledge base saved")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("Import Statistics:")
    print("=" * 60)
    
    categories = {}
    domains = {}
    
    for item in mathematical_data:
        cat = item.get("category", "unknown")
        dom = item.get("domain", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
        domains[dom] = domains.get(dom, 0) + 1
    
    print("\nCategories:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    print("\nDomains:")
    for dom, count in sorted(domains.items()):
        print(f"  {dom}: {count}")
    
    print("\n" + "=" * 60)
    print("Mathematical data import completed!")
    print("=" * 60)


def import_from_external_sources(knowledge_manager: KnowledgeManager, data_importer: DataImporter):
    """Import mathematical data from external sources"""
    
    print("\n" + "=" * 60)
    print("Importing Mathematical Data from External Sources")
    print("=" * 60)
    
    # Import from Research Gate (quantum physics papers)
    print("\n1. Importing from Research Gate...")
    quantum_queries = [
        "quantum mechanics nuclear physics",
        "quantum field theory nuclear",
        "schrödinger equation nuclear structure"
    ]
    
    for query in quantum_queries:
        print(f"   Searching: {query}")
        # Note: This would require actual Research Gate paper IDs
        # For now, we'll skip actual API calls and just show the structure
        pass
    
    # Import from Nature (mathematical physics)
    print("\n2. Importing from Nature...")
    nature_queries = [
        "quantum mechanics formulas",
        "nuclear physics mathematics",
        "quantum field theory calculations"
    ]
    
    for query in nature_queries:
        print(f"   Searching: {query}")
        try:
            results = data_importer.import_from_nature(query, max_results=10)
            print(f"   Found {len(results)} articles")
            
            for item in results:
                knowledge_manager.add_knowledge(item)
        except Exception as e:
            print(f"   Error: {e}")
    
    # Import from New Scientist
    print("\n3. Importing from New Scientist...")
    new_scientist_queries = [
        "quantum mechanics",
        "nuclear physics mathematics"
    ]
    
    for query in new_scientist_queries:
        print(f"   Searching: {query}")
        try:
            results = data_importer.import_from_new_scientist(query, max_results=10)
            print(f"   Found {len(results)} articles")
            
            for item in results:
                knowledge_manager.add_knowledge(item)
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n✓ External source import completed")


def main():
    """Main function"""
    print("Mathematical Data Import Script")
    print("=" * 60)
    
    # Initialize components
    knowledge_manager = KnowledgeManager()
    data_importer = DataImporter()
    
    # Import generated mathematical data
    import_mathematical_data(knowledge_manager)
    
    # Optionally import from external sources (commented out to avoid API calls)
    # import_from_external_sources(knowledge_manager, data_importer)
    
    print("\n" + "=" * 60)
    print("All mathematical data has been imported!")
    print("=" * 60)
    print("\nThe knowledge base now contains comprehensive mathematical formulas,")
    print("derivations, and calculations for nuclear physics and quantum mechanics.")


if __name__ == "__main__":
    main()

