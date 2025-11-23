#!/usr/bin/env python3
"""
Nuclear Data Import Script
Command-line tool for importing nuclear physics data from various sources
"""

import argparse
import sys
from batch_data_import import BatchDataImporter

def main():
    parser = argparse.ArgumentParser(
        description="Import nuclear physics data from various sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import from Google Scholar
  python import_nuclear_data.py --source google_scholar --query "nuclear fusion" --max-results 100
  
  # Import from MIT OpenCourseWare
  python import_nuclear_data.py --source mit_ocw --course-url "https://ocw.mit.edu/courses/22-01/"
  
  # Import from IAEA NUCLEUS
  python import_nuclear_data.py --source iaea --nuclide "U-235"
  
  # Import from file
  python import_nuclear_data.py --source file --file-path "data.txt"
  
  # Import all cutting-edge domains
  python import_nuclear_data.py --source cutting-edge
  
  # Import all fundamental physics
  python import_nuclear_data.py --source fundamental
  
  # Full import (all sources)
  python import_nuclear_data.py --source all
        """
    )
    
    parser.add_argument(
        '--source',
        type=str,
        required=True,
        choices=['google_scholar', 'mit_ocw', 'researchgate', 'nature', 'iaea', 'file', 
                 'cutting-edge', 'fundamental', 'predefined', 'all'],
        help='Data source to import from'
    )
    
    parser.add_argument(
        '--query',
        type=str,
        help='Search query (for Google Scholar, Nature)'
    )
    
    parser.add_argument(
        '--max-results',
        type=int,
        default=50,
        help='Maximum number of results to import (default: 50)'
    )
    
    parser.add_argument(
        '--course-url',
        type=str,
        help='MIT OCW course URL'
    )
    
    parser.add_argument(
        '--nuclide',
        type=str,
        help='Nuclide identifier (e.g., U-235) for IAEA import'
    )
    
    parser.add_argument(
        '--file-path',
        type=str,
        help='Path to file for file import'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='data_sources.json',
        help='Path to configuration file (default: data_sources.json)'
    )
    
    args = parser.parse_args()
    
    # Initialize importer
    importer = BatchDataImporter(config_file=args.config)
    data_importer = importer.importer
    
    print("=" * 60)
    print("Nuclear Physics Data Import Tool")
    print("=" * 60)
    print(f"Source: {args.source}")
    print()
    
    imported_count = 0
    
    try:
        if args.source == 'google_scholar':
            if not args.query:
                print("Error: --query is required for Google Scholar import")
                sys.exit(1)
            print(f"Importing from Google Scholar: {args.query}")
            papers = data_importer.import_from_google_scholar(args.query, args.max_results)
            importer.knowledge_manager.batch_add_knowledge(papers)
            imported_count = len(papers)
            
        elif args.source == 'mit_ocw':
            if not args.course_url:
                print("Error: --course-url is required for MIT OCW import")
                sys.exit(1)
            print(f"Importing from MIT OpenCourseWare: {args.course_url}")
            materials = data_importer.import_from_mit_ocw([args.course_url])
            importer.knowledge_manager.batch_add_knowledge(materials)
            imported_count = len(materials)
            
        elif args.source == 'nature':
            if not args.query:
                print("Error: --query is required for Nature import")
                sys.exit(1)
            print(f"Importing from Nature: {args.query}")
            papers = data_importer.import_from_nature(args.query, args.max_results)
            importer.knowledge_manager.batch_add_knowledge(papers)
            imported_count = len(papers)
            
        elif args.source == 'iaea':
            if not args.nuclide:
                print("Error: --nuclide is required for IAEA import")
                sys.exit(1)
            print(f"Importing from IAEA NUCLEUS/NDS: {args.nuclide}")
            data = data_importer.import_from_iaea_nucleus({
                'nuclide': args.nuclide,
                'data_type': 'decay'
            })
            importer.knowledge_manager.batch_add_knowledge(data)
            imported_count = len(data)
            
        elif args.source == 'file':
            if not args.file_path:
                print("Error: --file-path is required for file import")
                sys.exit(1)
            print(f"Importing from file: {args.file_path}")
            data = data_importer.import_from_file(args.file_path)
            importer.knowledge_manager.batch_add_knowledge(data)
            imported_count = len(data)
            
        elif args.source == 'cutting-edge':
            print("Importing cutting-edge domains...")
            stats = importer.import_cutting_edge_domains()
            imported_count = stats.get('total', 0)
            
        elif args.source == 'fundamental':
            print("Importing fundamental nuclear physics...")
            stats = importer.import_fundamental_nuclear_physics()
            imported_count = stats.get('total', 0)
            
        elif args.source == 'predefined':
            print("Importing from predefined sources...")
            stats = importer.import_from_predefined_sources()
            imported_count = stats.get('total', 0)
            
        elif args.source == 'all':
            print("Importing from all sources (full import)...")
            stats = importer.import_all()
            imported_count = stats.get('grand_total', 0)
        
        print()
        print("=" * 60)
        print(f"Import Complete!")
        print(f"Total items imported: {imported_count}")
        print("=" * 60)
        
        # Show knowledge base summary
        kb_summary = importer.knowledge_manager.get_knowledge_summary()
        print(f"\nKnowledge Base Statistics:")
        print(f"  Total Entities: {kb_summary['total_entities']}")
        print(f"  Total Facts: {kb_summary['total_facts']}")
        print(f"  Total Topics: {kb_summary['total_topics']}")
        print(f"  Documents Indexed: {kb_summary['total_documents_indexed']}")
        
    except KeyboardInterrupt:
        print("\n\nImport interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during import: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

