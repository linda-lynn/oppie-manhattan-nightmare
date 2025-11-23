"""
Multi-Source Data Importer for Nuclear Physics Knowledge Base
Supports: IAEA NUCLEUS/NDS, Google Scholar, MIT OpenCourseWare, Research Gate, Nature, and local files
"""

import requests
import json
import re
import os
from typing import Dict, List, Optional
from datetime import datetime
import time
from urllib.parse import quote

class DataImporter:
    def __init__(self):
        """Initialize data importer with API endpoints and configuration"""
        # IAEA NUCLEUS/NDS API endpoints
        self.iaea_nds_url = "https://nds.iaea.org/relnsd/v1/data"
        self.iaea_livechart_url = "https://www-nds.iaea.org/relnsd/v0/data"
        
        # Google Scholar (using scholarly library or SerpAPI)
        self.google_scholar_base = "https://scholar.google.com"
        
        # MIT OpenCourseWare base URL
        self.mit_ocw_base = "https://ocw.mit.edu"
        
        # Research Gate base URL
        self.researchgate_base = "https://www.researchgate.net"
        
        # Nature API (requires API key)
        self.nature_api_base = "https://api.nature.com"
        
        # New Scientist base URL
        self.new_scientist_base = "https://www.newscientist.com"
        
        # Request headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/html, */*'
        }
        
        # Rate limiting
        self.request_delay = 1.0  # seconds between requests
        
    def import_from_iaea_nucleus(self, query_params: Dict) -> List[Dict]:
        """
        Import nuclear data from IAEA NUCLEUS/NDS API
        
        Args:
            query_params: Dictionary with query parameters
                - nuclide: str (e.g., "U235")
                - data_type: str (e.g., "decay", "levels", "mass")
                - format: str (default: "json")
        
        Returns:
            List of imported data dictionaries
        """
        imported_data = []
        
        try:
            # Build query URL
            nuclide = query_params.get('nuclide', '')
            data_type = query_params.get('data_type', 'decay')
            
            # Example: Get decay data for a nuclide
            if nuclide:
                # Format: Z-A (e.g., 92-235 for U-235)
                if '-' in nuclide:
                    parts = nuclide.split('-')
                    element = parts[0]
                    mass = parts[1]
                else:
                    # Try to parse (e.g., "U235" -> Z=92, A=235)
                    match = re.match(r'([A-Za-z]+)(\d+)', nuclide)
                    if match:
                        element = match.group(1)
                        mass = match.group(2)
                    else:
                        return imported_data
                
                # Get atomic number
                element_to_Z = {
                    'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
                    'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
                    'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Fe': 26, 'Cu': 29,
                    'Zn': 30, 'Cd': 48, 'Gd': 64, 'Xe': 54, 'Pb': 82, 'Th': 90, 'U': 92,
                    'Pu': 94, 'Am': 95
                }
                
                Z = element_to_Z.get(element.capitalize())
                if not Z:
                    return imported_data
                
                A = int(mass)
                
                # Construct API URL
                url = f"{self.iaea_nds_url}/decay?Z={Z}&A={A}"
                
                time.sleep(self.request_delay)
                response = requests.get(url, headers=self.headers, timeout=30)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        imported_data.append({
                            "source": "iaea",
                            "nuclide": f"{element}-{A}",
                            "atomic_number": Z,
                            "mass_number": A,
                            "data_type": data_type,
                            "content": json.dumps(data),
                            "formulas": self.extract_formulas(str(data)),
                            "nuclides": [f"{element}-{A}"],
                            "concepts": ["decay", "nuclear_data"],
                            "publication_date": datetime.now().isoformat(),
                            "url": url,
                            "keywords": ["IAEA", "NUCLEUS", "NDS", "nuclear_data"],
                            "domain": "nuclear_data"
                        })
                    except json.JSONDecodeError:
                        # Try CSV format
                        csv_data = response.text
                        imported_data.append({
                            "source": "iaea",
                            "nuclide": f"{element}-{A}",
                            "atomic_number": Z,
                            "mass_number": A,
                            "data_type": data_type,
                            "content": csv_data,
                            "formulas": [],
                            "nuclides": [f"{element}-{A}"],
                            "concepts": ["decay", "nuclear_data"],
                            "publication_date": datetime.now().isoformat(),
                            "url": url,
                            "keywords": ["IAEA", "NUCLEUS", "NDS", "nuclear_data"],
                            "domain": "nuclear_data"
                        })
                        
        except Exception as e:
            print(f"Error importing from IAEA NUCLEUS: {e}")
        
        return imported_data
    
    def import_from_google_scholar(self, query: str, max_results: int = 100) -> List[Dict]:
        """
        Import papers from Google Scholar
        
        Args:
            query: Search query string
            max_results: Maximum number of results to import
        
        Returns:
            List of imported paper dictionaries
        """
        imported_data = []
        
        try:
            # Try using scholarly library if available
            try:
                from scholarly import scholarly
                
                search_query = scholarly.search_pubs(query)
                count = 0
                
                for pub in search_query:
                    if count >= max_results:
                        break
                    
                    try:
                        # Fill in publication details
                        filled_pub = scholarly.fill(pub)
                        
                        title = filled_pub.get('bib', {}).get('title', '')
                        authors = filled_pub.get('bib', {}).get('author', [])
                        abstract = filled_pub.get('bib', {}).get('abstract', '')
                        year = filled_pub.get('bib', {}).get('pub_year', '')
                        url = filled_pub.get('pub_url', '')
                        
                        # Extract content
                        content = f"{title}\n\nAbstract: {abstract}"
                        
                        imported_data.append(self.normalize_data({
                            "source": "google_scholar",
                            "title": title,
                            "authors": authors if isinstance(authors, list) else [authors],
                            "abstract": abstract,
                            "content": content,
                            "formulas": self.extract_formulas(content),
                            "nuclides": self.extract_nuclides(content),
                            "concepts": self.extract_concepts(content),
                            "publication_date": f"{year}-01-01" if year else datetime.now().isoformat(),
                            "url": url,
                            "keywords": query.split(),
                            "domain": self._classify_domain(content)
                        }))
                        
                        count += 1
                        time.sleep(self.request_delay)
                        
                    except Exception as e:
                        print(f"Error processing Google Scholar result: {e}")
                        continue
                        
            except ImportError:
                # Fallback: Use web scraping (simplified)
                print("scholarly library not available. Install with: pip install scholarly")
                # Could implement web scraping here if needed
                pass
                
        except Exception as e:
            print(f"Error importing from Google Scholar: {e}")
        
        return imported_data
    
    def import_from_mit_ocw(self, course_urls: List[str]) -> List[Dict]:
        """
        Import course materials from MIT OpenCourseWare
        
        Args:
            course_urls: List of MIT OCW course URLs
        
        Returns:
            List of imported course material dictionaries
        """
        imported_data = []
        
        try:
            from bs4 import BeautifulSoup
            
            for url in course_urls:
                try:
                    time.sleep(self.request_delay)
                    response = requests.get(url, headers=self.headers, timeout=30)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract course information
                        title = soup.find('title')
                        title_text = title.text if title else "MIT OCW Course"
                        
                        # Extract main content
                        content_divs = soup.find_all(['div', 'p'], class_=lambda x: x and ('content' in x.lower() or 'lecture' in x.lower()))
                        content = '\n'.join([div.get_text() for div in content_divs[:10]])  # First 10 content blocks
                        
                        if not content:
                            # Fallback: get all text
                            content = soup.get_text()[:5000]  # Limit to 5000 chars
                        
                        imported_data.append(self.normalize_data({
                            "source": "mit_ocw",
                            "title": title_text,
                            "authors": ["MIT OpenCourseWare"],
                            "abstract": content[:500] + "..." if len(content) > 500 else content,
                            "content": content,
                            "formulas": self.extract_formulas(content),
                            "nuclides": self.extract_nuclides(content),
                            "concepts": self.extract_concepts(content),
                            "publication_date": datetime.now().isoformat(),
                            "url": url,
                            "keywords": ["MIT", "OpenCourseWare", "nuclear_physics"],
                            "domain": self._classify_domain(content)
                        }))
                        
                except Exception as e:
                    print(f"Error importing MIT OCW course {url}: {e}")
                    continue
                    
        except ImportError:
            print("beautifulsoup4 not available. Install with: pip install beautifulsoup4")
        except Exception as e:
            print(f"Error importing from MIT OpenCourseWare: {e}")
        
        return imported_data
    
    def import_from_researchgate(self, paper_ids: List[str]) -> List[Dict]:
        """
        Import papers from Research Gate
        
        Args:
            paper_ids: List of Research Gate paper IDs or URLs
        
        Returns:
            List of imported paper dictionaries
        """
        imported_data = []
        
        try:
            from bs4 import BeautifulSoup
            
            for paper_id in paper_ids:
                try:
                    # Construct URL if needed
                    if not paper_id.startswith('http'):
                        url = f"{self.researchgate_base}/publication/{paper_id}"
                    else:
                        url = paper_id
                    
                    time.sleep(self.request_delay * 2)  # Longer delay for Research Gate
                    response = requests.get(url, headers=self.headers, timeout=30)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract paper information
                        title_elem = soup.find('h1', class_=lambda x: x and 'title' in x.lower())
                        title = title_elem.text.strip() if title_elem else "Research Gate Paper"
                        
                        # Extract abstract
                        abstract_elem = soup.find('div', class_=lambda x: x and 'abstract' in x.lower())
                        abstract = abstract_elem.get_text() if abstract_elem else ""
                        
                        # Extract full content
                        content_elem = soup.find('div', class_=lambda x: x and 'content' in x.lower())
                        content = content_elem.get_text() if content_elem else abstract
                        
                        imported_data.append(self.normalize_data({
                            "source": "researchgate",
                            "title": title,
                            "authors": [],  # Would need more parsing
                            "abstract": abstract,
                            "content": content,
                            "formulas": self.extract_formulas(content),
                            "nuclides": self.extract_nuclides(content),
                            "concepts": self.extract_concepts(content),
                            "publication_date": datetime.now().isoformat(),
                            "url": url,
                            "keywords": ["ResearchGate"],
                            "domain": self._classify_domain(content)
                        }))
                        
                except Exception as e:
                    print(f"Error importing Research Gate paper {paper_id}: {e}")
                    continue
                    
        except ImportError:
            print("beautifulsoup4 not available. Install with: pip install beautifulsoup4")
        except Exception as e:
            print(f"Error importing from Research Gate: {e}")
        
        return imported_data
    
    def import_from_nature(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Import papers from Nature journals
        
        Args:
            query: Search query string
            max_results: Maximum number of results
        
        Returns:
            List of imported paper dictionaries
        """
        imported_data = []
        
        try:
            # Nature API requires API key, so we'll use web scraping as fallback
            search_url = f"https://www.nature.com/search?q={quote(query)}"
            
            time.sleep(self.request_delay)
            response = requests.get(search_url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find article links
                article_links = soup.find_all('a', href=re.compile(r'/articles/'))
                count = 0
                
                for link in article_links[:max_results]:
                    if count >= max_results:
                        break
                    
                    try:
                        article_url = link.get('href')
                        if not article_url.startswith('http'):
                            article_url = f"https://www.nature.com{article_url}"
                        
                        time.sleep(self.request_delay)
                        article_response = requests.get(article_url, headers=self.headers, timeout=30)
                        
                        if article_response.status_code == 200:
                            article_soup = BeautifulSoup(article_response.content, 'html.parser')
                            
                            title = article_soup.find('h1')
                            title_text = title.text.strip() if title else "Nature Article"
                            
                            abstract = article_soup.find('div', class_=lambda x: x and 'abstract' in str(x).lower())
                            abstract_text = abstract.get_text() if abstract else ""
                            
                            content = abstract_text  # Simplified - could extract full text
                            
                            imported_data.append(self.normalize_data({
                                "source": "nature",
                                "title": title_text,
                                "authors": [],
                                "abstract": abstract_text,
                                "content": content,
                                "formulas": self.extract_formulas(content),
                                "nuclides": self.extract_nuclides(content),
                                "concepts": self.extract_concepts(content),
                                "publication_date": datetime.now().isoformat(),
                                "url": article_url,
                                "keywords": query.split() + ["Nature"],
                                "domain": self._classify_domain(content)
                            }))
                            
                            count += 1
                            
                    except Exception as e:
                        print(f"Error processing Nature article: {e}")
                        continue
                        
        except ImportError:
            print("beautifulsoup4 not available. Install with: pip install beautifulsoup4")
        except Exception as e:
            print(f"Error importing from Nature: {e}")
        
        return imported_data
    
    def import_from_new_scientist(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Import articles from New Scientist
        
        Args:
            query: Search query string
            max_results: Maximum number of results
        
        Returns:
            List of imported article dictionaries
        """
        imported_data = []
        
        try:
            from bs4 import BeautifulSoup
            
            # New Scientist search URL
            search_url = f"https://www.newscientist.com/search/?q={quote(query)}"
            
            time.sleep(self.request_delay)
            response = requests.get(search_url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find article links (New Scientist uses different structure)
                article_links = soup.find_all('a', href=re.compile(r'/article/'))
                count = 0
                
                for link in article_links[:max_results]:
                    if count >= max_results:
                        break
                    
                    try:
                        article_url = link.get('href')
                        if not article_url.startswith('http'):
                            article_url = f"https://www.newscientist.com{article_url}"
                        
                        time.sleep(self.request_delay)
                        article_response = requests.get(article_url, headers=self.headers, timeout=30)
                        
                        if article_response.status_code == 200:
                            article_soup = BeautifulSoup(article_response.content, 'html.parser')
                            
                            # Extract title
                            title_elem = article_soup.find('h1') or article_soup.find('title')
                            title_text = title_elem.text.strip() if title_elem else "New Scientist Article"
                            
                            # Extract content
                            content_elem = article_soup.find('div', class_=lambda x: x and ('content' in str(x).lower() or 'article' in str(x).lower()))
                            content = content_elem.get_text() if content_elem else ""
                            
                            # Extract abstract/summary (first paragraph)
                            abstract_elem = article_soup.find('p', class_=lambda x: x and 'summary' in str(x).lower())
                            abstract_text = abstract_elem.get_text() if abstract_elem else (content[:500] + "..." if len(content) > 500 else content)
                            
                            imported_data.append(self.normalize_data({
                                "source": "new_scientist",
                                "title": title_text,
                                "authors": [],
                                "abstract": abstract_text,
                                "content": content,
                                "formulas": self.extract_formulas(content),
                                "nuclides": self.extract_nuclides(content),
                                "concepts": self.extract_concepts(content),
                                "publication_date": datetime.now().isoformat(),
                                "url": article_url,
                                "keywords": query.split() + ["New Scientist"],
                                "domain": self._classify_domain(content)
                            }))
                            
                            count += 1
                            
                    except Exception as e:
                        print(f"Error processing New Scientist article: {e}")
                        continue
                        
        except ImportError:
            print("beautifulsoup4 not available. Install with: pip install beautifulsoup4")
        except Exception as e:
            print(f"Error importing from New Scientist: {e}")
        
        return imported_data
    
    def import_from_matlab_code(self, file_path: str) -> List[Dict]:
        """
        Import quantum physics calculations from MATLAB code files
        
        Args:
            file_path: Path to MATLAB .m file
        
        Returns:
            List of imported calculation dictionaries
        """
        imported_data = []
        
        try:
            if not os.path.exists(file_path):
                print(f"MATLAB file not found: {file_path}")
                return imported_data
            
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # Extract comments (documentation) and code
            comments = []
            formulas = []
            
            # Extract MATLAB comments (lines starting with %)
            for line in code_content.split('\n'):
                if line.strip().startswith('%'):
                    comments.append(line.strip()[1:].strip())
            
            # Extract formulas from code (look for mathematical expressions)
            formula_patterns = [
                r'[A-Za-z_][A-Za-z0-9_]*\s*=\s*[^;]+',  # Variable assignments
                r'exp\([^)]+\)',  # Exponential functions
                r'sqrt\([^)]+\)',  # Square roots
                r'[A-Za-z_][A-Za-z0-9_]*\s*\([^)]+\)',  # Function calls
            ]
            
            for pattern in formula_patterns:
                matches = re.findall(pattern, code_content)
                formulas.extend(matches)
            
            # Combine comments and code
            content = '\n'.join(comments) + '\n\n' + code_content
            
            filename = os.path.basename(file_path)
            title = os.path.splitext(filename)[0]
            
            imported_data.append(self.normalize_data({
                "source": "matlab",
                "title": f"MATLAB Code: {title}",
                "authors": [],
                "abstract": '\n'.join(comments[:3]) if comments else "MATLAB quantum physics calculation",
                "content": content,
                "formulas": formulas + self.extract_formulas(content),
                "nuclides": self.extract_nuclides(content),
                "concepts": self.extract_concepts(content) + ["quantum_computing", "quantum_mechanics"],
                "publication_date": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                "url": f"file://{file_path}",
                "keywords": ["MATLAB", "quantum", "calculation"] + filename.split('_'),
                "domain": "quantum_computing" if "quantum" in content.lower() else "general_nuclear_physics"
            }))
            
        except Exception as e:
            print(f"Error importing MATLAB code from {file_path}: {e}")
        
        return imported_data
    
    def import_from_file(self, file_path: str, format: str = "auto") -> List[Dict]:
        """
        Import data from local file
        
        Args:
            file_path: Path to the file
            format: File format (txt, csv, json, pdf, or "auto" for detection)
        
        Returns:
            List of imported data dictionaries
        """
        imported_data = []
        
        try:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return imported_data
            
            # Auto-detect format
            if format == "auto":
                ext = os.path.splitext(file_path)[1].lower()
                format = ext[1:] if ext else "txt"
            
            # Read file based on format
            content = ""
            if format == "txt":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif format == "json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    content = json.dumps(data, indent=2)
            elif format == "csv":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif format == "pdf":
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        content = '\n'.join([page.extract_text() for page in pdf_reader.pages])
                except ImportError:
                    print("PyPDF2 not available. Install with: pip install PyPDF2")
                    return imported_data
            else:
                print(f"Unsupported format: {format}")
                return imported_data
            
            # Extract metadata from filename
            filename = os.path.basename(file_path)
            title = os.path.splitext(filename)[0]
            
            imported_data.append(self.normalize_data({
                "source": "file",
                "title": title,
                "authors": [],
                "abstract": content[:500] + "..." if len(content) > 500 else content,
                "content": content,
                "formulas": self.extract_formulas(content),
                "nuclides": self.extract_nuclides(content),
                "concepts": self.extract_concepts(content),
                "publication_date": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                "url": f"file://{file_path}",
                "keywords": filename.split('_'),
                "domain": self._classify_domain(content)
            }))
            
        except Exception as e:
            print(f"Error importing from file {file_path}: {e}")
        
        return imported_data
    
    def extract_formulas(self, text: str) -> List[str]:
        """Extract mathematical formulas and physics equations from text"""
        formulas = []
        
        # Pattern for common nuclear physics formulas
        patterns = [
            r'E\s*=\s*mc[²2]',  # E=mc²
            r'k_eff\s*=\s*[^=]+',  # k_eff formulas
            r'σ\s*=\s*[^=]+',  # Cross sections
            r'λ\s*=\s*[^=]+',  # Decay constants
            r'[A-Z][a-z]?\d*\s*→\s*[A-Z][a-z]?\d*',  # Decay chains
            r'[A-Z][a-z]?\d*\s*\+\s*[A-Z][a-z]?\d*\s*→',  # Nuclear reactions
            r'η\s*=\s*[^=]+',  # Eta (neutron reproduction)
            r'ε\s*=\s*[^=]+',  # Epsilon (fast fission factor)
            r'p\s*=\s*[^=]+',  # Resonance escape probability
            r'f\s*=\s*[^=]+',  # Thermal utilization
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            formulas.extend(matches)
        
        # Remove duplicates
        return list(set(formulas))
    
    def extract_nuclides(self, text: str) -> List[str]:
        """Extract nuclide information from text"""
        nuclides = []
        
        # Pattern: Element-Mass (e.g., U-235, Pu-239)
        pattern = r'\b([A-Z][a-z]?)[-\s]*(\d+)\b'
        matches = re.findall(pattern, text)
        
        for element, mass in matches:
            nuclide = f"{element}-{mass}"
            if nuclide not in nuclides:
                nuclides.append(nuclide)
        
        return nuclides
    
    def extract_concepts(self, text: str) -> List[str]:
        """Extract nuclear physics concepts from text"""
        concepts = []
        text_lower = text.lower()
        
        concept_keywords = {
            "critical_mass": ["critical mass", "criticality"],
            "cross_section": ["cross section", "neutron cross section"],
            "binding_energy": ["binding energy", "mass defect"],
            "fission": ["fission", "fissile", "fissionable"],
            "fusion": ["fusion", "tokamak", "ITER", "inertial confinement"],
            "decay": ["decay", "alpha decay", "beta decay", "gamma decay"],
            "reactor_physics": ["reactor", "neutron multiplication", "k_eff"],
            "nuclear_medicine": ["PET", "SPECT", "radiotherapy", "nuclear medicine"],
            "waste_management": ["transmutation", "nuclear waste", "reprocessing"],
            "quantum_computing": ["quantum computing", "quantum simulation", "quantum algorithm"],
            "quantum_mechanics": ["schrödinger", "wave function", "quantum mechanics", "uncertainty principle", "quantum state"],
            "quantum_field_theory": ["quantum field theory", "QCD", "feynman diagram", "lagrangian", "quantum chromodynamics"],
            "quantum_entanglement": ["entanglement", "bell state", "quantum correlation", "EPR"]
        }
        
        for concept, keywords in concept_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                concepts.append(concept)
        
        return concepts
    
    def _classify_domain(self, content: str) -> str:
        """Classify content into domain categories"""
        content_lower = content.lower()
        
        domain_keywords = {
            "nuclear_fusion": ["fusion", "tokamak", "ITER", "plasma", "inertial confinement"],
            "nuclear_medicine": ["PET", "SPECT", "radiotherapy", "medical imaging", "radioisotope"],
            "waste_management": ["transmutation", "nuclear waste", "reprocessing", "repository"],
            "quantum_computing": ["quantum", "qubit", "quantum algorithm", "quantum simulation"],
            "quantum_mechanics": ["schrödinger", "wave function", "quantum mechanics", "uncertainty principle", "quantum state", "hamiltonian"],
            "quantum_field_theory": ["quantum field theory", "QCD", "feynman diagram", "lagrangian", "quantum chromodynamics", "gauge theory"],
            "reactor_physics": ["reactor", "neutron transport", "criticality", "fuel cycle"],
            "nuclear_structure": ["shell model", "nuclear structure", "magic numbers", "nuclear model"],
            "nuclear_data": ["cross section", "decay data", "nuclear data", "evaluation"]
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return domain
        
        return "general_nuclear_physics"
    
    def normalize_data(self, data: Dict) -> Dict:
        """Normalize imported data to standard format"""
        normalized = {
            "source": data.get("source", "unknown"),
            "title": data.get("title", ""),
            "authors": data.get("authors", []),
            "abstract": data.get("abstract", ""),
            "content": data.get("content", ""),
            "formulas": data.get("formulas", []),
            "nuclides": data.get("nuclides", []),
            "concepts": data.get("concepts", []),
            "publication_date": data.get("publication_date", datetime.now().isoformat()),
            "url": data.get("url", ""),
            "keywords": data.get("keywords", []),
            "domain": data.get("domain", "general_nuclear_physics"),
            "imported_at": datetime.now().isoformat()
        }
        
        # Ensure lists are lists
        for key in ["authors", "formulas", "nuclides", "concepts", "keywords"]:
            if not isinstance(normalized[key], list):
                normalized[key] = [normalized[key]] if normalized[key] else []
        
        return normalized
    
    def parse_paper_content(self, content: str) -> Dict:
        """Parse paper content to extract structured information"""
        return {
            "abstract": self._extract_abstract(content),
            "methods": self._extract_methods(content),
            "results": self._extract_results(content),
            "formulas": self.extract_formulas(content),
            "nuclides": self.extract_nuclides(content),
            "concepts": self.extract_concepts(content)
        }
    
    def _extract_abstract(self, content: str) -> str:
        """Extract abstract section from content"""
        # Look for abstract markers
        abstract_patterns = [
            r'Abstract[:\s]+(.*?)(?=\n\n|\n[A-Z]|$)',
            r'ABSTRACT[:\s]+(.*?)(?=\n\n|\n[A-Z]|$)',
            r'Summary[:\s]+(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        for pattern in abstract_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:1000]  # Limit length
        
        # Fallback: first paragraph
        paragraphs = content.split('\n\n')
        return paragraphs[0][:500] if paragraphs else ""
    
    def _extract_methods(self, content: str) -> str:
        """Extract methods section from content"""
        methods_patterns = [
            r'Method[s]?[:\s]+(.*?)(?=\n\nResults|\n\nConclusion|$)',
            r'Experimental[:\s]+(.*?)(?=\n\nResults|\n\nConclusion|$)'
        ]
        
        for pattern in methods_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:2000]
        
        return ""
    
    def _extract_results(self, content: str) -> str:
        """Extract results section from content"""
        results_patterns = [
            r'Result[s]?[:\s]+(.*?)(?=\n\nDiscussion|\n\nConclusion|$)',
            r'Finding[s]?[:\s]+(.*?)(?=\n\nDiscussion|\n\nConclusion|$)'
        ]
        
        for pattern in results_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:2000]
        
        return ""

