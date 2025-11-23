"""
Import MATLAB Files into Knowledge Base
Batch import MATLAB .m files for quantum physics and nuclear physics calculations
"""

import os
import sys
import glob
from knowledge_manager import KnowledgeManager
from data_importer import DataImporter

def import_matlab_directory(directory_path: str, knowledge_manager: KnowledgeManager, 
                            data_importer: DataImporter):
    """Import all MATLAB .m files from a directory"""
    
    print("=" * 60)
    print("Importing MATLAB Files from Directory")
    print("=" * 60)
    print(f"Directory: {directory_path}\n")
    
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found!")
        return
    
    # Find all .m files
    matlab_files = glob.glob(os.path.join(directory_path, "**/*.m"), recursive=True)
    matlab_files += glob.glob(os.path.join(directory_path, "*.m"), recursive=False)
    
    if not matlab_files:
        print(f"No MATLAB .m files found in '{directory_path}'")
        print("\nExample: Create a MATLAB file like:")
        print("""
% quantum_schrodinger_solver.m
% Solves the time-independent Schrödinger equation
% for a particle in a potential well

function [E, psi] = quantum_schrodinger_solver(V, x, m)
    % Parameters:
    % V: potential energy function
    % x: position vector
    % m: particle mass
    
    % Hamiltonian: H = -hbar^2/(2m) * d^2/dx^2 + V(x)
    hbar = 1.0545718e-34;  % Reduced Planck constant
    
    % Solve eigenvalue problem: H*psi = E*psi
    % ... (implementation)
end
        """)
        return
    
    print(f"Found {len(matlab_files)} MATLAB file(s)\n")
    
    imported_count = 0
    failed_count = 0
    
    for matlab_file in matlab_files:
        try:
            print(f"Importing: {os.path.basename(matlab_file)}")
            
            # Import MATLAB file
            imported_data = data_importer.import_from_matlab_code(matlab_file)
            
            if imported_data:
                for item in imported_data:
                    # Add to knowledge base
                    knowledge_manager.add_knowledge(item)
                    
                    # Add to vector index
                    doc_id = f"matlab_{os.path.basename(matlab_file)}_{imported_count}"
                    text = item.get("content", "")
                    if text:
                        knowledge_manager.add_to_vector_index(doc_id, text)
                    
                    imported_count += 1
                    print(f"  ✓ Successfully imported")
            else:
                print(f"  ✗ No data extracted")
                failed_count += 1
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed_count += 1
    
    # Save knowledge base
    print("\n" + "=" * 60)
    print("Saving knowledge base...")
    knowledge_manager._save_knowledge_base()
    knowledge_manager._save_vector_index()
    print("✓ Knowledge base saved")
    
    # Print summary
    print("\n" + "=" * 60)
    print("Import Summary:")
    print("=" * 60)
    print(f"Total files found: {len(matlab_files)}")
    print(f"Successfully imported: {imported_count}")
    print(f"Failed: {failed_count}")
    print("=" * 60)


def import_single_matlab_file(file_path: str, knowledge_manager: KnowledgeManager,
                              data_importer: DataImporter):
    """Import a single MATLAB file"""
    
    print("=" * 60)
    print("Importing Single MATLAB File")
    print("=" * 60)
    print(f"File: {file_path}\n")
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found!")
        return
    
    if not file_path.endswith('.m'):
        print(f"Warning: File '{file_path}' is not a MATLAB .m file")
    
    try:
        # Import MATLAB file
        imported_data = data_importer.import_from_matlab_code(file_path)
        
        if imported_data:
            for item in imported_data:
                print(f"\nExtracted:")
                print(f"  Title: {item.get('title', 'N/A')}")
                print(f"  Formulas found: {len(item.get('formulas', []))}")
                print(f"  Concepts: {', '.join(item.get('concepts', [])[:5])}")
                
                # Add to knowledge base
                knowledge_manager.add_knowledge(item)
                
                # Add to vector index
                doc_id = f"matlab_{os.path.basename(file_path)}"
                text = item.get("content", "")
                if text:
                    knowledge_manager.add_to_vector_index(doc_id, text)
            
            # Save knowledge base
            print("\nSaving knowledge base...")
            knowledge_manager._save_knowledge_base()
            knowledge_manager._save_vector_index()
            print("✓ Successfully imported and saved!")
        else:
            print("No data extracted from MATLAB file")
            
    except Exception as e:
        print(f"Error importing MATLAB file: {e}")


def create_example_matlab_file():
    """Create an example MATLAB file for testing"""
    
    example_code = """% quantum_schrodinger_solver.m
% Solves the time-independent Schrödinger equation
% for a particle in a potential well
% 
% Equation: H*psi = E*psi
% Where H = -hbar^2/(2m) * d^2/dx^2 + V(x)
%
% This implements the quantum mechanical wave function solution

function [E, psi] = quantum_schrodinger_solver(V, x, m)
    % Parameters:
    %   V: potential energy function V(x)
    %   x: position vector
    %   m: particle mass
    
    % Physical constants
    hbar = 1.0545718e-34;  % Reduced Planck constant (J·s)
    
    % Hamiltonian operator: H = -hbar^2/(2m) * d^2/dx^2 + V(x)
    % Discretize the second derivative
    dx = x(2) - x(1);
    N = length(x);
    
    % Kinetic energy operator (finite difference)
    T = -hbar^2/(2*m) * (diag(ones(N-1,1),1) - 2*eye(N) + diag(ones(N-1,1),-1)) / dx^2;
    
    % Potential energy operator (diagonal)
    V_matrix = diag(V);
    
    % Total Hamiltonian
    H = T + V_matrix;
    
    % Solve eigenvalue problem: H*psi = E*psi
    [psi, E] = eig(H);
    E = diag(E);
    
    % Normalize wave functions
    for i = 1:length(E)
        psi(:,i) = psi(:,i) / sqrt(trapz(x, abs(psi(:,i)).^2));
    end
end

% Example usage:
% x = linspace(-10, 10, 1000);
% V = 0.5 * x.^2;  % Harmonic oscillator potential
% m = 9.109e-31;   % Electron mass
% [E, psi] = quantum_schrodinger_solver(V, x, m);
"""
    
    example_file = "example_quantum_schrodinger.m"
    with open(example_file, 'w', encoding='utf-8') as f:
        f.write(example_code)
    
    print(f"Created example MATLAB file: {example_file}")
    print("You can now import it using:")
    print(f"  python3 import_matlab_files.py --file {example_file}")
    return example_file


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import MATLAB files into knowledge base')
    parser.add_argument('--file', '-f', type=str, help='Import a single MATLAB .m file')
    parser.add_argument('--directory', '-d', type=str, help='Import all .m files from a directory')
    parser.add_argument('--create-example', action='store_true', help='Create an example MATLAB file')
    
    args = parser.parse_args()
    
    # Initialize components
    knowledge_manager = KnowledgeManager()
    data_importer = DataImporter()
    
    if args.create_example:
        create_example_matlab_file()
    elif args.file:
        import_single_matlab_file(args.file, knowledge_manager, data_importer)
    elif args.directory:
        import_matlab_directory(args.directory, knowledge_manager, data_importer)
    else:
        print("MATLAB File Importer")
        print("=" * 60)
        print("\nUsage:")
        print("  Import single file:")
        print("    python3 import_matlab_files.py --file path/to/file.m")
        print("\n  Import directory:")
        print("    python3 import_matlab_files.py --directory path/to/matlab/code/")
        print("\n  Create example file:")
        print("    python3 import_matlab_files.py --create-example")
        print("\n" + "=" * 60)
        
        # Check if there are any .m files in current directory
        current_dir_m_files = glob.glob("*.m")
        if current_dir_m_files:
            print(f"\nFound {len(current_dir_m_files)} MATLAB file(s) in current directory:")
            for f in current_dir_m_files:
                print(f"  - {f}")
            print("\nImport them with:")
            print(f"  python3 import_matlab_files.py --directory .")


if __name__ == "__main__":
    main()

