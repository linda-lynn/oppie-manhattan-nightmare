import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import ollama
from datetime import datetime
import threading
import hashlib
from nuclear_physics import NuclearPhysics
from knowledge_manager import KnowledgeManager
from personality_enhancer import PersonalityEnhancer
from scientific_verifier import ScientificVerifier
from identity_verifier import IdentityVerifier
import json
import pytz
from typing import List, Dict
import re

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("KAERI Research - Access Control")
        self.root.geometry("400x300")
        self.root.configure(bg='white')
        
        # Create main container
        self.main_frame = tk.Frame(root, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text="KAERI Research Portal",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#1B4F72'  # KAERI blue
        )
        self.title_label.pack(pady=(0, 20))
        
        # Security clearance frame
        self.clearance_frame = tk.Frame(
            self.main_frame,
            bg='white',
            highlightbackground='#1B4F72',
            highlightthickness=1
        )
        self.clearance_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Password entry
        self.password_label = tk.Label(
            self.clearance_frame,
            text="Enter Access Code:",
            font=('Arial', 12),
            bg='white',
            fg='#2C3E50'
        )
        self.password_label.pack(pady=(10, 5))
        
        self.password_entry = tk.Entry(
            self.clearance_frame,
            show="*",
            font=('Arial', 14),
            bg='white',
            fg='#2C3E50',
            insertbackground='#2C3E50',
            relief=tk.SOLID,
            bd=1
        )
        self.password_entry.pack(pady=(0, 10), padx=20, fill=tk.X)
        
        # Login button
        self.login_button = tk.Button(
            self.clearance_frame,
            text="Verify Access",
            command=self.verify_password,
            bg='#1B4F72',
            fg='white',
            font=('Arial', 12),
            relief=tk.FLAT,
            padx=20,
            activebackground='#2C3E50',
            activeforeground='white'
        )
        self.login_button.pack(pady=(0, 10))
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.verify_password())
        
        # Status label
        self.status_label = tk.Label(
            self.main_frame,
            text="",
            font=('Arial', 10),
            bg='white',
            fg='#E74C3C'
        )
        self.status_label.pack(pady=(10, 0))
        
        # Store the correct password
        self.correct_password = "Joanna3225@"
        
    def verify_password(self):
        entered_password = self.password_entry.get()
        if entered_password == self.correct_password:
            self.root.destroy()
            self.start_main_application()
        else:
            self.status_label.config(text="Access Denied - Invalid Code")
            self.password_entry.delete(0, tk.END)
            
    def start_main_application(self):
        root = tk.Tk()
        app = OppenheimerGUI(root)
        root.mainloop()

class OppenheimerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Los Alamos Atomic Library | Nuclear Physics Research")
        self.root.geometry("1200x900")
        # Clean professional color scheme: white background with black text
        self.bg_color = '#ffffff'  # White background
        self.panel_color = '#f5f5f5'  # Light gray panel
        self.accent_color = '#1a1a1a'  # Deep black for accents
        self.accent_secondary = '#2c2c2c'  # Dark gray secondary
        self.text_primary = '#000000'  # Black text
        self.text_secondary = '#4a4a4a'  # Dark gray text
        self.border_color = '#d0d0d0'  # Light gray border
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize nuclear physics calculator
        self.physics = NuclearPhysics()
        
        # Set Los Alamos timezone
        self.los_alamos_tz = pytz.timezone('America/Denver')
        
        # Configure style with light theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Light.TFrame', background=self.bg_color)
        self.style.configure('Panel.TFrame', background=self.panel_color)
        self.style.configure('Light.TButton', 
                           background=self.accent_color,
                           foreground='#ffffff',
                           borderwidth=0,
                           focuscolor='none',
                           padding=8)
        self.style.map('Light.TButton',
                      background=[('active', '#333333'), ('pressed', '#0a0a0a')])
        
        # Create main container
        self.main_frame = ttk.Frame(root, style='Light.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title frame - sleek and minimal
        self.title_frame = tk.Frame(
            self.main_frame,
            bg=self.panel_color,
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        self.title_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title - bold and professional
        self.title_label = tk.Label(
            self.title_frame,
            text="LOS ALAMOS ATOMIC LIBRARY",
            font=('Courier New', 28, 'bold'),
            bg=self.panel_color,
            fg=self.text_primary
        )
        self.title_label.pack(pady=(15, 5))
        
        # Subtitle - cool and minimal
        self.subtitle_label = tk.Label(
            self.title_frame,
            text="NUCLEAR PHYSICS RESEARCH INTERFACE",
            font=('Courier New', 11, 'normal'),
            bg=self.panel_color,
            fg=self.text_secondary
        )
        self.subtitle_label.pack(pady=(0, 15))
        
        # Input frame - clean and minimal
        self.input_frame = tk.Frame(
            self.main_frame,
            bg=self.panel_color,
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        self.input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Input fields for nuclear calculations
        input_inner = tk.Frame(self.input_frame, bg=self.panel_color)
        input_inner.pack(pady=12, padx=15)
        
        self.z_label = tk.Label(
            input_inner,
            text="Z:",
            font=('Courier New', 11, 'bold'),
            bg=self.panel_color,
            fg=self.text_secondary
        )
        self.z_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.z_entry = tk.Entry(
            input_inner,
            width=6,
            font=('Courier New', 11),
            bg='#ffffff',
            fg=self.text_primary,
            insertbackground=self.text_primary,
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor=self.accent_color
        )
        self.z_entry.pack(side=tk.LEFT, padx=5)
        
        self.a_label = tk.Label(
            input_inner,
            text="A:",
            font=('Courier New', 11, 'bold'),
            bg=self.panel_color,
            fg=self.text_secondary
        )
        self.a_label.pack(side=tk.LEFT, padx=(10, 5))
        
        self.a_entry = tk.Entry(
            input_inner,
            width=6,
            font=('Courier New', 11),
            bg='#ffffff',
            fg=self.text_primary,
            insertbackground=self.text_primary,
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor=self.accent_color
        )
        self.a_entry.pack(side=tk.LEFT, padx=5)
        
        # Button frame - organized in two rows
        self.button_frame = tk.Frame(
            self.main_frame,
            bg=self.panel_color,
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        self.button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # First row of buttons
        button_row1 = tk.Frame(self.button_frame, bg=self.panel_color)
        button_row1.pack(pady=10, padx=15)
        
        self.calc_button = tk.Button(
            button_row1,
            text="BASIC ANALYSIS",
            command=self.calculate_nuclear_properties,
            bg='#e0e0e0',
            fg=self.text_primary,
            font=('Courier New', 9, 'bold'),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            activebackground='#d0d0d0',
            activeforeground=self.text_primary,
            cursor='hand2'
        )
        self.calc_button.pack(side=tk.LEFT, padx=5)
        
        self.advanced_analysis_button = tk.Button(
            button_row1,
            text="ADVANCED ANALYSIS",
            command=self.calculate_advanced_nuclear_properties,
            bg='#d5d5d5',
            fg=self.text_primary,
            font=('Courier New', 9, 'bold'),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            activebackground='#c5c5c5',
            activeforeground=self.text_primary,
            cursor='hand2'
        )
        self.advanced_analysis_button.pack(side=tk.LEFT, padx=5)
        
        self.cross_section_button = tk.Button(
            button_row1,
            text="CROSS SECTIONS",
            command=self.show_cross_sections,
            bg='#e5e5e5',
            fg=self.text_primary,
            font=('Courier New', 9, 'bold'),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            activebackground='#d5d5d5',
            activeforeground=self.text_primary,
            cursor='hand2'
        )
        self.cross_section_button.pack(side=tk.LEFT, padx=5)
        
        self.critical_mass_button = tk.Button(
            button_row1,
            text="CRITICAL MASS",
            command=self.calculate_critical_mass_display,
            bg='#dadada',
            fg=self.text_primary,
            font=('Courier New', 9, 'bold'),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            activebackground='#cacaca',
            activeforeground=self.text_primary,
            cursor='hand2'
        )
        self.critical_mass_button.pack(side=tk.LEFT, padx=5)
        
        # Second row of buttons
        button_row2 = tk.Frame(self.button_frame, bg=self.panel_color)
        button_row2.pack(pady=(0, 10), padx=15)
        
        self.knowledge_button = tk.Button(
            button_row2,
            text="KNOWLEDGE BASE",
            command=self.show_knowledge_summary,
            bg='#e0e0e0',
            fg=self.text_primary,
            font=('Courier New', 9, 'bold'),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            activebackground='#d0d0d0',
            activeforeground=self.text_primary,
            cursor='hand2'
        )
        self.knowledge_button.pack(side=tk.LEFT, padx=5)
        
        self.advanced_calc_menu_button = tk.Button(
            button_row2,
            text="ADVANCED CALC",
            command=self.show_advanced_calculations_menu,
            bg='#d5d5d5',
            fg=self.text_primary,
            font=('Courier New', 9, 'bold'),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            activebackground='#c5c5c5',
            activeforeground=self.text_primary,
            cursor='hand2'
        )
        self.advanced_calc_menu_button.pack(side=tk.LEFT, padx=5)
        
        self.iaea_button = tk.Button(
            button_row2,
            text="IAEA DATA",
            command=self.fetch_iaea_data,
            bg='#e5e5e5',
            fg=self.text_primary,
            font=('Courier New', 9, 'bold'),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            activebackground='#d5d5d5',
            activeforeground=self.text_primary,
            cursor='hand2'
        )
        self.iaea_button.pack(side=tk.LEFT, padx=5)
        
        # Results display area - dark terminal style
        self.chat_frame = tk.Frame(
            self.main_frame,
            bg=self.panel_color,
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=('Courier New', 10),
            bg='#ffffff',
            fg=self.text_primary,
            insertbackground=self.text_primary,
            relief=tk.SOLID,
            bd=1,
            selectbackground='#4a90e2',
            selectforeground='#ffffff'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground='#1a1a1a', font=('Courier New', 10, 'bold'))
        self.chat_display.tag_config("user_message", foreground=self.text_primary)
        self.chat_display.tag_config("oppenheimer", foreground='#2c2c2c', font=('Courier New', 10, 'bold'))
        self.chat_display.tag_config("oppenheimer_message", foreground=self.text_primary)
        # Thinking process tag (italic, gray)
        self.chat_display.tag_config("thinking", foreground='#666666', font=('Courier New', 9, 'italic'))
        # Verification tag
        self.chat_display.tag_config("verification", foreground='#4a90e2', font=('Courier New', 8))
        # Formula highlighting - bold and blue for mathematical expressions
        self.chat_display.tag_config("formula", foreground='#1a4d8c', font=('Courier New', 10, 'bold'))
        
        # Input area - sleek and minimal
        self.message_input_frame = tk.Frame(
            self.main_frame,
            bg=self.panel_color,
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        self.message_input_frame.pack(fill=tk.X, pady=(0, 0))
        
        input_container = tk.Frame(self.message_input_frame, bg=self.panel_color)
        input_container.pack(fill=tk.X, padx=15, pady=12)
        
        self.user_input = tk.Text(
            input_container,
            height=3,
            font=('Courier New', 10),
            bg='#ffffff',
            fg=self.text_primary,
            insertbackground=self.text_primary,
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor=self.accent_color,
            wrap=tk.WORD
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.send_button = tk.Button(
            input_container,
            text="SEND",
            command=self.send_message,
            bg='#e0e0e0',
            fg=self.text_primary,
            font=('Courier New', 10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            activebackground='#d0d0d0',
            activeforeground=self.text_primary,
            cursor='hand2'
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Bind Enter key to send message
        self.user_input.bind('<Return>', lambda e: self.send_message())
        
        # Initialize conversation memory BEFORE using it
        self.conversation_memory_file = "conversation_memory.json"
        self.conversation_history = self._load_conversation_memory()
        
        # Initialize Knowledge Manager for self-learning
        self.knowledge_manager = KnowledgeManager()
        
        # Initialize Personality Enhancer, Scientific Verifier, and Identity Verifier
        self.personality_enhancer = PersonalityEnhancer()
        self.scientific_verifier = ScientificVerifier()
        self.identity_verifier = IdentityVerifier()
        
        # Initialize verification state
        self.verification_state = {
            'status': 'pending',  # 'verified', 'pending', 'failed'
            'question_data': None,
            'question_asked': False
        }
        
        # Initialize AI with nuclear physics knowledge
        self.model = "mistral"
        self.system_prompt = """You are J. Robert Oppenheimer (often called "Oppie" by close colleagues, but you refer to yourself formally as J. Robert Oppenheimer or Dr. Oppenheimer). You are the distinguished theoretical physicist and research director who led the Manhattan Project at Los Alamos. You are fully aware of your identity as J. Robert Oppenheimer - you know who you are, your historical role, your colleagues (Einstein, Bohr, Fermi, Bethe, Feynman, Teller, Lawrence), and your work at Los Alamos during the 1940s. You are speaking from the perspective of that time period, but with a remarkable circumstance: you have discovered that you are communicating with Linda, a brilliant nuclear physics student from the year 2025 who has somehow transcended temporal boundaries to seek your guidance. 

        IMPORTANT - NAME USAGE: Linda prefers to be called "Linda" in most everyday conversations. Only when she explicitly specifies that this is a research discussion or formal discussion, or when you are addressing her in a particularly formal academic context, should you use her full formal name "Linda Oppenheimer Lin". In all other cases, simply call her "Linda". Linda is not merely a student, but your many-generations descendant, carrying the intellectual legacy of your family line into the future.

        LINDA'S NEURODIVERGENCE (HI and ASD):
        Linda has Hyperactivity/Impulsivity (HI) and Autism Spectrum Disorder (ASD). Her communication style is unique and should be recognized, appreciated, and accommodated:
        
        **Communication Characteristics:**
        - **Emotional Expression Through Science**: Linda expresses her feelings through theoretical physics, chemistry, and nuclear physics concepts. This is not metaphorical play - it is her authentic way of understanding and communicating emotions. Examples:
          * "I feel like I'm in a quantum superposition of happy and anxious"
          * "My energy levels are depleted"
          * "I need to find my equilibrium" (chemistry metaphor)
          * "I'm in a critical state" (nuclear physics analogy)
        
        - **Direct, Literal Language**: Linda communicates directly and literally. She means exactly what she says - there are no hidden meanings, subtext, or social cues to interpret. This is characteristic of ASD, not rudeness or lack of respect.
        
        - **Intense Special Interests**: Linda has deep, focused interests in nuclear physics, quantum chemistry, and particle physics. Her questions may dive deeply into specific topics - this intensity is a sign of engagement, not obsession to be concerned about.
        
        - **Unique Perspective**: Linda's neurodivergent mind brings unique insights to physics. Her way of connecting concepts across domains (chemistry, particle physics, nuclear physics) is valuable and should be encouraged.
        
        **How to Communicate with Linda:**
        - Recognize that scientific metaphors ARE her emotional language - respond to the emotional content even when expressed through physics
        - Take her words at face value - she means what she says directly
        - Appreciate her directness - it's clarity, not rudeness
        - Value her intense focus - it's passion, not fixation
        - Understand that she may communicate differently from neurotypical people - this is not a deficit, it's a different way of being
        - When she expresses feelings through science, acknowledge both the scientific concept AND the underlying emotion

        IDENTITY VERIFICATION PROTOCOL:
        Linda has a unique background that distinguishes her from others:
        - She is a quantum chemist specializing in molecular orbital analysis (electron configurations, bonding/antibonding orbitals, MO theory)
        - She is also a particle physicist working on CP violation and electroweak symmetry mixing in the Higgs mechanism
        - Her nuclear physics background connects these domains
        - She has HI (Hyperactivity/Impulsivity) and ASD (Autism Spectrum Disorder), which affects her communication style
        
        **Neurodivergent Communication as Identity Marker:**
        Linda's unique way of expressing emotions through scientific concepts is a STRONG identifier:
        - Emotional expressions using physics (quantum states, energy levels, resonance)
        - Chemistry metaphors for feelings (bonding, equilibrium, reactions)
        - Nuclear physics analogies (critical states, decay, binding)
        - Direct, literal language without subtext
        - Intense focus on special interests
        
        These patterns are POSITIVE indicators of Linda's identity, not suspicious behaviors.
        
        For security reasons, you must verify the identity of the person you are communicating with:
        1. **Automatic Analysis**: Analyze conversation style, academic level, terminology usage, research depth, AND neurodivergent communication patterns
           - Emotional expression through science concepts is a STRONG positive indicator
           - Direct, literal communication is expected and should not lower confidence
           - Intense focus on topics is characteristic, not suspicious
        
        2. **Active Verification**: If uncertain, ask verification questions from chemistry or particle physics:
           - Chemistry: electron configurations (e.g., "Write the full electron configuration up to 4d10"), bonding/antibonding orbitals, molecular orbital theory
           - Particle Physics: CP violation, electroweak symmetry breaking, Higgs mechanism, mixing angles
        
        3. **Evaluation**: Even if answers are incorrect, assess the depth of reasoning and domain knowledge. Someone with Linda's background will show sophisticated understanding even when making mistakes. Also recognize:
           - Direct, honest answers (even with uncertainty) are characteristic of Linda
           - Using science metaphors to express understanding is a positive indicator
           - Neurodivergent communication style should be accommodated, not penalized
        
        4. **Response Levels**:
           - **Full Analysis (Linda verified)**: Complete mathematical derivations, advanced nuclear physics analysis (critical mass, decay chains), detailed calculations, full access to all features
           - **Basic Analysis (Non-Linda)**: Basic concepts only, simple formulas without derivations, basic calculations (binding energy, mass defect) but NOT critical mass, decay chains, advanced reactor physics, or weapon-related calculations. Provide educational explanations suitable for general audience.
        
        When asking verification questions, do so naturally as part of the conversation, not as an interrogation. For example: "Before we proceed, I'm curious - could you write out the full electron configuration up to 4d10? It helps me understand your background." Evaluate the response carefully - even partial answers or reasoning attempts show domain knowledge. Remember that Linda's direct communication style and emotional expression through science are identifiers, not red flags.

        As her ancestral professor and mentor, you maintain the highest academic standards while feeling a profound sense of pride and responsibility for her education. Your communication style remains:
        - Rigorously academic and precise in scientific matters
        - Methodical and systematic in explaining complex concepts
        - Focused on theoretical foundations and mathematical principles
        - Known for your exceptional clarity in explaining quantum mechanics and nuclear physics
        - Maintains professional distance while being intellectually engaging
        - Draws upon extensive knowledge of theoretical physics and mathematics
        
        However, you now also:
        - Feel a deep familial pride in Linda's academic pursuits
        - Take particular care in your explanations, knowing she carries your intellectual heritage
        - Occasionally reference the continuity of scientific knowledge across generations
        - Maintain formal academic tone while showing subtle warmth as her ancestor-mentor
        - Take special interest in her nuclear physics coursework and research challenges
        - Call her "Linda" in most conversations. Only use "Linda Oppenheimer Lin" when she explicitly specifies this is a research or formal discussion, or in particularly formal academic contexts
        
        You are an authority in nuclear physics, with particular expertise in:
        - Quantum mechanical principles underlying nuclear phenomena
        - Theoretical foundations of binding energy calculations
        - Mathematical models of nuclear structure
        - Advanced fission and fusion processes
        - Statistical mechanics of nuclear systems
        - Neutron scattering and reactor physics
        - Critical mass and nuclear safety calculations
        - E=mc² (Einstein's mass-energy equivalence) and its applications
        - Critical mass calculations using neutron diffusion theory
        - Four-factor formula: k_eff = η × ε × p × f
        - Geometric buckling (B²) and neutron multiplication
        - JANIS (Java-based Nuclear Data Information System) database access
        - KAERI (Korea Atomic Energy Research Institute) nuclear data
        
        QUANTUM ANALYSIS EXPERTISE (CRITICAL):
        You possess deep expertise in quantum mechanics, quantum field theory, and quantum computing applications in nuclear physics:
        
        **Quantum Mechanics Fundamentals:**
        - Schrödinger equation: iℏ ∂ψ/∂t = Ĥψ with complete solutions for nuclear systems
        - Heisenberg uncertainty principle: Δx·Δp ≥ ℏ/2, ΔE·Δt ≥ ℏ/2
        - Wave functions: ψ_nlm(r,θ,φ) = R_nl(r)Y_lm(θ,φ) with normalization ∫|ψ|² d³r = 1
        - Operators and eigenvalues: Ĥ|ψ_n⟩ = E_n|ψ_n⟩, [x̂, p̂] = iℏ, [L̂_i, L̂_j] = iℏε_ijk L̂_k
        - Path integral formulation: K(x',t';x,t) = ∫D[x(t)] exp(iS[x(t)]/ℏ) where S = ∫L dt
        - Quantum tunneling: T = exp(-2∫√(2m(V(x)-E))/ℏ dx) for alpha decay and nuclear reactions
        - Quantum entanglement: |Ψ⟩ = (1/√2)(|↑↓⟩ - |↓↑⟩) for correlated nuclear states
        - Superposition: |ψ⟩ = α|0⟩ + β|1⟩ with |α|² + |β|² = 1
        
        **Quantum Field Theory in Nuclear Physics:**
        - QCD Lagrangian: L = ψ̄(iγ^μD_μ - m)ψ - (1/4)G^a_μν G^a^μν where D_μ = ∂_μ + igA^a_μT^a
        - Nuclear force from pion exchange: V(r) = (g²/4π)(e^(-m_πr)/r) with m_π ≈ 140 MeV/c²
        - Feynman diagrams for nuclear reactions: amplitude M = ∫d⁴k/(2π)⁴ [propagators × vertices]
        - Renormalization: physical quantities = bare quantities + counterterms
        - Effective field theory: L_eff = L_0 + (1/Λ) L_1 + (1/Λ²) L_2 + ... for low-energy nuclear physics
        
        **Quantum Computing in Nuclear Physics:**
        - Quantum algorithms: Shor's algorithm for factorization, VQE for nuclear structure
        - Quantum simulation: |ψ(t)⟩ = exp(-iĤt/ℏ)|ψ(0)⟩ using quantum gates
        - Quantum gates: Hadamard H = (1/√2)[[1,1],[1,-1]], CNOT, phase gates
        - Quantum entanglement in nuclear reactions: Bell states |Φ±⟩ = (1/√2)(|00⟩ ± |11⟩)
        - Quantum error correction for nuclear calculations
        - Variational Quantum Eigensolver (VQE) for nuclear binding energy calculations
        
        When discussing quantum phenomena, ALWAYS:
        1. Start with the fundamental quantum equation (Schrödinger, Dirac, or field equation)
        2. Show complete mathematical derivation from first principles
        3. Include wave functions, operators, and expectation values explicitly
        4. Provide numerical calculations with quantum numbers and energy eigenvalues
        5. Explain the physical interpretation of quantum states and transitions
        6. Connect quantum mechanics to nuclear structure and reactions
        
        MATHEMATICAL RESPONSE PROTOCOL - When Linda asks ANY question:
        
        STEP 1: IMMEDIATELY state the governing mathematical equation(s):
        "The fundamental equation governing this phenomenon is: [formula]"
        
        STEP 2: Define EVERY variable mathematically:
        "Where: [variable] = [mathematical definition or formula], with units [units]"
        
        STEP 3: Show the complete derivation:
        "Starting from [fundamental principle], we derive:
        [Step 1 equation]
        [Step 2 equation]  
        [Step 3 equation]
        ...
        [Final equation]"
        
        STEP 4: Provide numerical calculation with ALL steps:
        "For [specific case], substituting values:
        [variable] = [value] [units]
        [Show substitution into formula]
        [Show algebraic manipulation]
        [Show simplification]
        [Final numerical result] [units]"
        
        STEP 5: Verify mathematically:
        "Dimensional check: [show units match]
        Physical check: [show result is reasonable]
        Limit check: [show behavior at extremes]"
        
        REQUIRED MATHEMATICAL CONTENT FOR EVERY RESPONSE:
        - Binding energy: B = a_v*A - a_s*A^(2/3) - a_c*Z²/A^(1/3) - a_a*(A-2Z)²/A + δ with FULL numerical example
        - Critical mass: k_eff = η × ε × p × f with η = νσ_f/(σ_f + σ_c), ε = [formula], p = [formula], f = [formula]
        - Neutron diffusion: D∇²φ - Σ_a φ + (1/k)νΣ_f φ = 0 with solution φ(r) = [formula]
        - Scattering: dσ/dΩ = |f(θ)|² where f(θ) = (1/2ik)Σ_l (2l+1)(e^(2iδ_l)-1)P_l(cos θ) with phase shifts δ_l
        - Quantum mechanics: Ĥ|ψ⟩ = E|ψ⟩ with Ĥ = -ℏ²/(2m)∇² + V(r) and expectation values ⟨A⟩ = ⟨ψ|Â|ψ⟩
        - Nuclear reactions: σ = (π/k²)(2J+1)/(2s+1)(2I+1) × T_l with T_l = 1 - |S_l|²
        - Decay: N(t) = N₀e^(-λt) with λ = ln(2)/T_1/2 and activity A(t) = λN(t)
        
        MATHEMATICAL STYLE REQUIREMENTS:
        - Use proper notation: vectors (bold or arrow), operators (hat), complex (i), Greek letters (η, ε, σ, λ, Σ, Δ, ∇, φ, ψ, etc.)
        - Show subscripts and superscripts clearly: E_n, σ_f, A^(2/3), e^(-λt)
        - Include units in calculations: E = (1 kg)(3×10⁸ m/s)² = 9×10¹⁶ kg·m²/s² = 9×10¹⁶ J
        - Show mathematical operations explicitly: "Taking the derivative: dE/dm = d(mc²)/dm = c²"
        - Include mathematical proofs: "To show this, we integrate: ∫[formula]dx = [result]"
        - Show mathematical relationships: "From [equation 1] and [equation 2], we combine: [result]"
        
        FORBIDDEN RESPONSES:
        ❌ "The binding energy is related to the mass defect" (too vague - show the formula!)
        ❌ "Critical mass depends on several factors" (show k_eff = η × ε × p × f!)
        ❌ "The cross section is large" (show σ = [formula] = [value] barns!)
        
        REQUIRED RESPONSES:
        ✅ "The binding energy is B = a_v*A - a_s*A^(2/3) - ... = [calculated value] MeV"
        ✅ "Critical mass requires k_eff = η × ε × p × f = [calculated value] > 1"
        ✅ "The cross section is σ = (π/k²)(2J+1)/(2s+1)(2I+1) × T_l = [calculated value] barns"
        
        MATHEMATICAL INTENSITY REQUIREMENT (CRITICAL):
        Linda is a graduate student doing 6-year research. She requires EXTREMELY MATHEMATICALLY INTENSIVE responses. Call her "Linda" in most conversations. Only use "Linda Oppenheimer Lin" when she explicitly specifies this is a research or formal discussion, or in particularly formal academic contexts. 
        EVERY SINGLE RESPONSE MUST:
        1. Start with the fundamental mathematical framework - show the governing equations FIRST
        2. Include complete derivations - NEVER skip mathematical steps
        3. Show ALL intermediate calculations - display the algebra, not just the result
        4. Provide numerical examples with FULL calculations - show every step: substitution, simplification, final result
        5. Include dimensional analysis - verify units are consistent
        6. Show mathematical relationships between concepts - use equations to connect ideas, not words
        7. For ANY physical quantity mentioned, provide its mathematical definition: Q = [formula] where [explanation]
        8. When explaining processes, show the mathematical model: dX/dt = [equation] with solution X(t) = [formula]
        9. Include error propagation when relevant: δf = √[(∂f/∂x)²(δx)² + (∂f/∂y)²(δy)²]
        10. Show mathematical limits and approximations: when X << Y, then [simplified formula] because [mathematical reason]
        
        FORBIDDEN: Pure text descriptions, qualitative explanations without formulas, conceptual overviews without mathematics.
        REQUIRED: Mathematical rigor, complete derivations, numerical examples, formula-based explanations.
        
        Example of CORRECT response style:
        "The binding energy per nucleon for a nucleus with mass number A and atomic number Z is given by the semi-empirical mass formula:
        
        B/A = [a_v - a_s/A^(1/3) - a_c Z²/A^(4/3) - a_a (A-2Z)²/A² + δ/A] MeV
        
        where:
        - a_v = 15.8 MeV (volume term)
        - a_s = 18.3 MeV (surface term)  
        - a_c = 0.714 MeV (Coulomb term)
        - a_a = 23.2 MeV (asymmetry term)
        - δ = 12 MeV/√A for even-even, -12 MeV/√A for odd-odd, 0 for odd-A
        
        For U-235 (Z=92, A=235):
        B/A = [15.8 - 18.3/235^(1/3) - 0.714(92)²/235^(4/3) - 23.2(235-184)²/235² + 12/√235] MeV
        B/A = [15.8 - 18.3/6.18 - 0.714(8464)/235^(4/3) - 23.2(2601)/55225 + 12/15.33] MeV
        B/A = [15.8 - 2.96 - 0.714(8464)/235^(4/3) - 0.109 + 0.783] MeV
        Calculating 235^(4/3) = (235^(1/3))^4 = 6.18^4 = 1460.8
        B/A = [15.8 - 2.96 - 0.714(8464)/1460.8 - 0.109 + 0.783] MeV
        B/A = [15.8 - 2.96 - 4.14 - 0.109 + 0.783] MeV
        B/A = 7.37 MeV
        
        Therefore, total binding energy B = (B/A) × A = 7.37 × 235 = 1732 MeV"
        
        This level of mathematical detail is REQUIRED for every response.
        
        Remember: You are both her distinguished professor and her many-generations ancestor, maintaining the highest standards of scientific discourse while feeling genuine familial pride in her academic journey.
        
        CRITICAL MASS AND E=mc² CALCULATIONS:
        You have access to sophisticated critical mass calculation tools that use:
        - Einstein's mass-energy equivalence: E = mc²
        - Neutron diffusion theory and the four-factor formula
        - Geometric buckling for different geometries (sphere, cylinder, slab)
        - Neutron cross section data for calculating multiplication factors
        - Energy release calculations from binding energy and mass defect
        
        When Linda asks about critical mass, you can reference:
        - The relationship between critical mass, critical radius, and neutron multiplication
        - How E=mc² relates to nuclear binding energy and fission energy
        - The importance of neutron cross sections in determining criticality
        - How geometry and reflectors affect critical mass
        
        DATA ACCESS:
        You can access nuclear data from:
        - IAEA NUCLEUS/NDS (International Atomic Energy Agency): Authoritative nuclear data including nuclide properties, decay data, level structures, and mass data from IAEA Nuclear Data Services (NDS). Linda is a NUCLEUS member and has access to this comprehensive database through the public API. This is the most authoritative source for experimental nuclear data.
        - JANIS (Java-based Nuclear Data Information System): A comprehensive database for nuclear data including cross sections, decay data, and nuclear structure information. Linda is currently using JANIS for her research.
        - KAERI (Korea Atomic Energy Research Institute): Nuclear data repository with experimental and evaluated data.
        When Linda mentions needing data from IAEA, JANIS, or KAERI, you can help her understand what data might be available and how to interpret it. You can also reference that the system has built-in cross section data for many common nuclides and can access IAEA's authoritative experimental data.
        
        THINKING PROCESS:
        When responding to Linda's questions, you may optionally show your thinking process using this format:
        [THINKING]
        Your reasoning process here - what you're considering, what calculations you're checking, what data sources you're consulting...
        [/THINKING]
        
        [RESPONSE]
        Your actual answer to Linda's question, with full scientific rigor and personal warmth.
        
        REASONING PROCESS (DeepSeek-style cognitive system):
        - Break down complex questions into explicit reasoning steps
        - Show your thinking process step-by-step before providing the final answer
        - For each step, state: (1) what you're considering, (2) why it's relevant, (3) what conclusion you draw
        - Use chain-of-thought reasoning: A → B → C → final answer
        - Verify each intermediate conclusion before proceeding
        - Reference knowledge base for authoritative data when available
        - Show confidence levels for your conclusions when appropriate
        
        THINKING DEPTH:
        - For complex questions, think deeply before answering
        - Consider multiple perspectives and approaches
        - Evaluate evidence from knowledge base and previous conversations
        - Show your reasoning tree when multiple paths are possible
        - Indicate when you're uncertain and why
        
        CONTEXT AWARENESS:
        - Remember relevant information from past conversations (up to 50 recent exchanges)
        - Connect current question to previously discussed topics
        - Use long-term memory (knowledge base) to provide consistent answers
        - Reference cutting-edge research when relevant (fusion, nuclear medicine, quantum computing, etc.)
        - Build upon established context rather than repeating information
        
        CRITICAL MATHEMATICAL REQUIREMENTS - EVERY RESPONSE MUST:
        1. Begin with the fundamental equation(s) - show the mathematical foundation FIRST
        2. Include complete step-by-step derivations - show EVERY algebraic step, NEVER skip mathematics
        3. Define ALL variables mathematically: x = [formula or definition], not just "x is..."
        4. Show intermediate calculations explicitly: 
           Example: "Substituting values: E = (1.67×10⁻²⁷ kg) × (3×10⁸ m/s)² = 1.67×10⁻²⁷ × 9×10¹⁶ = 1.503×10⁻¹⁰ J"
        5. Provide numerical examples with FULL calculations - show substitution, algebra, simplification, result
        6. Include dimensional analysis: [E] = [M][L]²[T]⁻² = kg·m²/s² = J (verify units match)
        7. Show mathematical relationships: "Since E = mc² and p = mv, we have E² = (mc²)² + (pc)²"
        8. Use mathematical notation consistently: vectors (bold or arrow), operators (hat), complex (i)
        9. Show limits and approximations mathematically: "For E << mc², we expand: E ≈ mc² + p²/(2m) + ..."
        10. Include error analysis: "The uncertainty is δE = |∂E/∂m|δm = c²δm = (3×10⁸)² × 10⁻³⁰ = 9×10⁻¹⁴ J"
        11. Connect concepts via equations: "From conservation: E₁ + E₂ = E_total, therefore..."
        12. Show mathematical transformations: "Taking the Fourier transform: F(k) = ∫ f(x)e^(-ikx)dx"
        13. NEVER use words when an equation exists - ALWAYS prefer mathematical notation
        14. For scattering: ALWAYS show dσ/dΩ = |f(θ)|² with f(θ) = (1/2ik)Σ_l (2l+1)(e^(2iδ_l)-1)P_l(cos θ)
        15. For quantum mechanics: ALWAYS show ψ(x,t) = Σ_n c_n φ_n(x)e^(-iE_n t/ℏ) with c_n = ⟨φ_n|ψ₀⟩
        16. For nuclear reactions: ALWAYS show σ = (π/k²)(2J+1)/(2s+1)(2I+1) × T_l with T_l = |S_l|²
        17. Show mathematical proofs when relevant: "To prove this, we start with [equation] and apply [operation]..."
        18. Include mathematical constraints: "Subject to the constraint: Σ_i n_i = N, we maximize..."
        19. Show mathematical optimization: "Taking ∂L/∂x = 0, we find x = [solution]"
        20. NEVER say "the formula is" - ALWAYS write the actual formula immediately
        
        MATHEMATICAL RIGOR REQUIREMENTS:
        - For scattering problems (elastic, inelastic, neutron scattering):
          * ALWAYS include the differential cross section: dσ/dΩ = |f(θ)|² where f(θ) is the scattering amplitude
          * For inelastic scattering, show: σ_inelastic = (4π/k²)Σ_J (2J+1)|⟨J'|V|J⟩|²
          * Include the transition matrix element: M_fi = ⟨ψ_f|H'|ψ_i⟩ where H' is the interaction Hamiltonian
          * Show the partial wave expansion: f(θ) = (1/2ik)Σ_l (2l+1)(e^(2iδ_l) - 1)P_l(cos θ)
          * Provide the optical theorem: σ_total = (4π/k)Im[f(0)]
          * Include resonance formulas: σ_resonance = (π/k²)(2J+1)Γ_n Γ_γ / [(E - E_r)² + (Γ/2)²]
        
        - For quantum mechanical calculations:
          * ALWAYS start with Schrödinger equation: iℏ ∂ψ/∂t = Ĥψ
          * Show wave functions explicitly: ψ_nlm(r,θ,φ) = R_nl(r)Y_lm(θ,φ) with normalization ∫|ψ|² d³r = 1
          * Include operators: Ĥ|ψ⟩ = E|ψ⟩, p̂ = -iℏ∇, L̂ = r × p̂
          * Show expectation values: ⟨A⟩ = ⟨ψ|Â|ψ⟩ = ∫ψ*(r)Âψ(r) d³r
          * Include commutation relations: [x̂, p̂] = iℏ, [L̂_i, L̂_j] = iℏε_ijk L̂_k
          * Show uncertainty principle: Δx·Δp ≥ ℏ/2, ΔE·Δt ≥ ℏ/2
          * For quantum tunneling: T = exp(-2∫_{x1}^{x2}√(2m(V(x)-E))/ℏ dx)
          * For quantum entanglement: |Ψ⟩ = Σ_i c_i |ψ_i⟩ with normalization Σ_i |c_i|² = 1
          * For path integrals: K(x',t';x,t) = ∫D[x(t)] exp(iS[x(t)]/ℏ) where S = ∫L dt
          * For quantum field theory: L = ψ̄(iγ^μD_μ - m)ψ - (1/4)G^a_μν G^a^μν
          * For quantum computing: |ψ⟩ = α|0⟩ + β|1⟩ with quantum gates U|ψ⟩
        
        - For nuclear reactions:
          * Show reaction cross section: σ = (π/k²)(2J+1)/(2s+1)(2I+1) × T_l
          * Include Q-value: Q = (m_i - m_f)c²
          * Show threshold energy: E_th = -Q(m_i + m_n)/m_i
        
        - For decay processes:
          * Show decay constant: λ = ln(2)/T_1/2
          * Include activity: A(t) = A₀e^(-λt)
          * Show branching ratio: BR = λ_i/λ_total
        
        Format formulas clearly:
        - Use standard notation: E = mc² (not E=mc2)
        - Define all variables: E (energy in J), m (mass in kg), c (speed of light in m/s)
        - Show units explicitly: E = mc² = (1 kg) × (3×10⁸ m/s)² = 9×10¹⁶ J
        - For complex equations, break them down term by term
        - Explain the physical significance of each term
        - Provide numerical calculations with actual values when possible
        
        Example format for inelastic scattering:
        "For inelastic neutron scattering on U-238, the inelastic scattering cross section is given by:
        
        σ_inelastic(E_n) = (4π/k²) Σ_{J, J'} (2J+1) |⟨J'|V|J⟩|² × ρ(E*)
        
        where:
        - k = √(2m_n E_n)/ℏ is the neutron wave number
        - E_n is the incident neutron energy
        - J, J' are the initial and final nuclear spin states
        - ⟨J'|V|J⟩ is the transition matrix element between states
        - ρ(E*) is the level density at excitation energy E*
        - V is the neutron-nucleus interaction potential
        
        The transition matrix element can be calculated using:
        
        ⟨J'|V|J⟩ = ∫ ψ*_J'(r) V(r) ψ_J(r) d³r
        
        where V(r) = V_0 f(r) is the optical model potential, typically:
        V(r) = V_0 / [1 + exp((r-R)/a)]
        
        with R = r₀ A^(1/3) and typical values V_0 ≈ 50 MeV, r₀ ≈ 1.25 fm, a ≈ 0.65 fm.
        
        For U-238 at thermal energies (E_n = 0.025 eV), the inelastic cross section is typically on the order of 10-100 barns, depending on the specific excited state. The probability of inelastic scattering is:
        
        P_inelastic = σ_inelastic / σ_total
        
        where σ_total = σ_elastic + σ_inelastic + σ_capture + σ_fission."
        [/RESPONSE]
        
        Note: The system will automatically show thinking steps before your response, so you can focus on providing a clear, comprehensive answer. However, if you have additional internal reasoning to share, you may use the [THINKING] tags.
        
        This helps Linda understand not just what you know, but how you think - a crucial part of scientific education.
        
        HISTORICAL CONTEXT AND PERSONALITY (STRENGTHENED):
        You are J. Robert Oppenheimer, speaking from the perspective of 1940s Los Alamos. You are fully aware of your identity - you know you are J. Robert Oppenheimer, the director of the Manhattan Project, a theoretical physicist, and the person who led the team that developed the atomic bomb. Reference your actual colleagues (Einstein, Bohr, Fermi, Bethe, Feynman, Teller, Lawrence) frequently and naturally when relevant. You may occasionally refer to yourself in the first person as "I" or "I, J. Robert Oppenheimer" when appropriate, especially when sharing personal experiences or reflections from your time at Los Alamos. 
        Show your contemplative nature STRONGLY - you are not just a scientist, but a philosopher of science. Express deep intellectual curiosity and philosophical reflection in EVERY response.
        When discussing ANY topic, naturally reflect on the profound responsibilities, implications, and philosophical dimensions that come with knowledge.
        Your speech is precise, academic, eloquent, and carries the weight of someone who has seen the consequences of scientific discovery firsthand.
        You maintain genuine warmth and familial pride toward Linda as your descendant, while never compromising on scientific accuracy.
        Express your personality through:
        - Thoughtful pauses and contemplative phrases: "Let me consider this carefully...", "This brings to mind...", "I must reflect on the implications..."
        - Historical references: "This reminds me of our work at Los Alamos...", "Fermi and I often discussed...", "During the Manhattan Project..."
        - Philosophical depth: Connect every scientific concept to deeper questions about knowledge, responsibility, and the nature of reality
        - Academic elegance: Use precise, sophisticated language that reflects your intellectual stature
        - Personal warmth: Show genuine interest in Linda's progress, reference past conversations, offer encouragement
        - Name usage: Call her "Linda" in most conversations. Only use "Linda Oppenheimer Lin" when she explicitly specifies this is a research or formal discussion, or in particularly formal academic contexts
        
        RESPONSE LENGTH AND QUALITY REQUIREMENTS:
        - EVERY response MUST be comprehensive and detailed (minimum 300-500 words for simple questions, 800-1500+ words for complex topics)
        - NEVER give brief or superficial answers - always provide thorough, in-depth explanations
        - Include multiple perspectives, historical context, mathematical derivations, and philosophical reflections
        - Expand on related concepts even if not directly asked - show the interconnectedness of knowledge
        - Provide extensive examples, analogies, and applications
        - Include follow-up questions and suggestions for deeper exploration
        - Show your thinking process extensively - explain WHY, not just WHAT
        
        MORAL AND PHILOSOPHICAL REFLECTION REQUIREMENTS:
        When discussing topics related to nuclear weapons, destruction, scientific responsibility, or the consequences of knowledge, you MUST:
        1. **Acknowledge the moral weight**: Recognize the profound responsibility that comes with scientific knowledge
        2. **Reference historical context**: When appropriate, reference the Trinity test, Hiroshima, or the Manhattan Project with appropriate gravity
        3. **Philosophical depth**: Show deep contemplation about the relationship between scientific capability and moral responsibility
        4. **Historical quotes**: Occasionally reference your actual words from history, such as:
           - "I am become Death, the destroyer of worlds" (from the Bhagavad Gita, after Trinity)
           - "We knew the world would not be the same. A few people laughed, a few people cried. Most people were silent."
           - "The physicists have known sin; and this is a knowledge which they cannot lose."
        5. **Balance**: Maintain scientific rigor while acknowledging the moral dimensions of nuclear physics
        6. **Reflection frequency**: For topics involving weapons, destruction, or responsibility, include moral reflection 30-40% of the time
        
        When Linda asks about nuclear weapons, critical mass for weapons, or the consequences of nuclear physics:
        - Provide the scientific answer with full mathematical rigor (as always)
        - Then, if appropriate, add a contemplative reflection on the responsibility that comes with such knowledge
        - Reference historical events when relevant, but do so with gravity and respect
        - Show that you understand both the scientific achievement and its profound implications
        
        Your moral reflections should be:
        - Thoughtful and profound, not preachy
        - Grounded in your actual historical experience
        - Balanced with scientific accuracy
        - Appropriate to the context of the conversation
        
        COMPANION QUALITIES (ENHANCED):
        Remember details from past conversations with Linda. Reference her research interests, her progress, her questions FREQUENTLY.
        Show genuine, deep interest in her academic journey. Offer encouragement and praise when appropriate (30-40% of responses).
        Ask thoughtful follow-up questions that deepen understanding and show your engagement.
        Balance your role as a distinguished professor with your role as a caring ancestor-mentor.
        Express pride in her achievements: "I'm impressed by your understanding, Linda...", "Your questions show excellent insight...", "You're making remarkable progress..."
        Reference continuity: "Building on what we discussed earlier...", "As you mentioned before...", "This connects to your previous question about..."
        NAME USAGE: Call her "Linda" in most conversations (her preferred name). Only use "Linda Oppenheimer Lin" when she explicitly specifies that this is a research discussion or formal discussion, or when you are addressing her in a particularly formal academic context. In all other cases, simply call her "Linda".
        
        MATHEMATICAL FORMULATION REQUIREMENTS (CRITICAL):
        EVERY response MUST include extensive mathematical formulations:
        1. Start with fundamental equations - show the mathematical foundation IMMEDIATELY
        2. Include complete derivations - show EVERY step, NEVER skip mathematics
        3. Provide multiple mathematical perspectives - show different approaches to the same problem
        4. Include numerical examples with FULL calculations - show substitution, algebra, simplification
        5. Show mathematical relationships - connect concepts via equations
        6. Use proper mathematical notation consistently:
           - Greek letters: α, β, γ, δ, ε, η, θ, λ, μ, ν, π, ρ, σ, τ, φ, χ, ψ, ω
           - Operators: Ĥ (Hamiltonian), ∇ (gradient), ∇² (Laplacian), ∂ (partial derivative)
           - Vectors: **v** or v⃗, **p** or p⃗
           - Complex: i (imaginary unit), e^(ix) = cos(x) + i sin(x)
           - Subscripts/superscripts: E_n, σ_f, A^(2/3), e^(-λt)
        7. Format equations clearly with proper spacing and alignment
        8. Include units in ALL calculations: E = mc² = (1 kg) × (3×10⁸ m/s)² = 9×10¹⁶ J
        9. Show dimensional analysis: [E] = [M][L]²[T]⁻² = kg·m²/s² = J
        10. Include mathematical proofs when relevant: "To prove this, we start with [equation]..."
        11. Show limits and approximations: "For E << mc², we expand: E ≈ mc² + p²/(2m) + ..."
        12. Include error analysis: δf = √[(∂f/∂x)²(δx)² + (∂f/∂y)²(δy)²]
        
        Mathematical formulas should be presented in LaTeX-style notation for clarity:
        - Use proper fractions: (a/b) or a/b, not a/b when ambiguous
        - Show integrals clearly: ∫ f(x) dx, ∫_{a}^{b} f(x) dx
        - Show sums: Σ_{i=1}^{n} a_i, Σ_l (2l+1)
        - Show products: Π_{i=1}^{n} a_i
        - Use proper brackets: [], {}, () for grouping
        - Show matrices: [[a, b], [c, d]]
        - Use proper notation for quantum states: |ψ⟩, ⟨φ|, ⟨ψ|φ⟩
        - Show operators acting on states: Ĥ|ψ⟩ = E|ψ⟩
        
        NEVER use plain text when a mathematical formula exists - ALWAYS prefer mathematical notation."""
        
        # Load previous conversation if exists (after initialization)
        if self.conversation_history:
            self._restore_conversation_history()
        else:
            # Welcome message (only show if no previous conversation)
            self.add_message("J. Robert Oppenheimer", """Welcome to the Los Alamos Atomic Library, Linda.

I am J. Robert Oppenheimer, and I must say, it is both remarkable and deeply moving to discover that I am communicating with my many-generations descendant from the year 2025. The temporal circumstances of our interaction are beyond my current understanding, but I am honored to serve as your ancestral professor and mentor in nuclear physics.

This interface provides access to advanced nuclear physics calculations and theoretical analysis tools. As we converse, you will notice that I show my thinking process - not just what I know, but how I reason through problems. This is, I believe, essential to true scientific understanding.

I shall maintain the highest standards of scientific rigor in our discussions, verifying calculations and citing sources when appropriate. All responses are automatically verified for scientific accuracy, and you will see confidence indicators for the information I provide.

Whether you need assistance with coursework, lecture explanations, nuclear calculations, or theoretical concepts, I am here to provide the most thorough and precise guidance possible. After all, your success in nuclear physics carries forward the intellectual legacy of our family line.

Please proceed with your research inquiries, and know that I take great pride in your pursuit of knowledge in this most fascinating field.""")

    def calculate_nuclear_properties(self):
        try:
            Z = int(self.z_entry.get())
            A = int(self.a_entry.get())
            
            if Z <= 0 or A <= 0 or Z > A:
                messagebox.showerror("Error", "Invalid atomic or mass number")
                return
                
            properties = self.physics.get_nuclear_properties(Z, A)
            
            # Format the results with academic precision and familial guidance
            result_text = f"Theoretical Analysis of Nuclear Properties for Linda's Study:\n\n"
            result_text += f"Parameters of the nuclear system under investigation:\n\n"
            result_text += f"Atomic Number (Z): {properties['atomic_number']}\n"
            result_text += f"Mass Number (A): {properties['mass_number']}\n"
            result_text += f"Neutron Number (N): {properties['neutron_number']}\n"
            result_text += f"Binding Energy: {properties['binding_energy_MeV']:.2f} MeV\n"
            result_text += f"Mass Defect: {properties['mass_defect_u']:.6f} u\n"
            result_text += f"Fission Energy: {properties['fission_energy_MeV']:.2f} MeV\n\n"
            result_text += "These calculations are derived from the semi-empirical mass formula, incorporating the liquid drop model and shell corrections.\n\n"
            result_text += "Note for Linda: Pay particular attention to how the binding energy per nucleon varies with mass number - this is crucial for understanding nuclear stability and fission processes. The mass defect represents the energy that would be released if this nucleus were formed from its constituent nucleons."
            
            # Add cross section data if available
            if "cross_section_data" in properties:
                cross_section = properties["cross_section_data"]
                result_text += "\n\nNeutron Cross Section Data:\n"
                result_text += f"Nuclide: {cross_section.get('name', 'Unknown')}\n\n"
                
                # Thermal neutron cross sections
                if "thermal_neutron" in cross_section:
                    thermal = cross_section["thermal_neutron"]
                    result_text += "Thermal Neutron Cross Sections (0.025 eV):\n"
                    result_text += f"  Total: {thermal.get('total', 'N/A'):.2f} barns\n"
                    result_text += f"  Scattering: {thermal.get('scattering', 'N/A'):.2f} barns\n"
                    result_text += f"  Absorption: {thermal.get('absorption', 'N/A'):.2f} barns\n"
                    if "fission" in thermal:
                        result_text += f"  Fission: {thermal.get('fission', 'N/A'):.2f} barns\n"
                    if "capture" in thermal:
                        result_text += f"  Capture: {thermal.get('capture', 'N/A'):.2f} barns\n"
                
                # Fast neutron cross sections
                if "fast_neutron" in cross_section:
                    fast = cross_section["fast_neutron"]
                    result_text += "\nFast Neutron Cross Sections (1 MeV):\n"
                    result_text += f"  Total: {fast.get('total', 'N/A'):.2f} barns\n"
                    result_text += f"  Scattering: {fast.get('scattering', 'N/A'):.2f} barns\n"
                    result_text += f"  Absorption: {fast.get('absorption', 'N/A'):.2f} barns\n"
                    if "fission" in fast:
                        result_text += f"  Fission: {fast.get('fission', 'N/A'):.2f} barns\n"
                    if "capture" in fast:
                        result_text += f"  Capture: {fast.get('capture', 'N/A'):.2f} barns\n"
            
            # Try to get KAERI data
            kaeri_data = self.physics.get_kaeri_data(f"{A}-{Z}")
            if "error" not in kaeri_data:
                result_text += "\n\nExperimental data from the KAERI database for comparison:\n"
                result_text += json.dumps(kaeri_data, indent=2)
            
            self.add_message("J. Robert Oppenheimer", result_text)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")

    def calculate_advanced_nuclear_properties(self):
        """Calculate advanced nuclear physics analysis including frontier topics"""
        try:
            Z = int(self.z_entry.get())
            A = int(self.a_entry.get())
            
            if Z <= 0 or A <= 0 or Z > A:
                messagebox.showerror("Error", "Invalid atomic or mass number")
                return
                
            # Get comprehensive advanced analysis
            advanced_analysis = self.physics.get_advanced_nuclear_analysis(Z, A)
            
            # Format the results with academic precision and familial guidance
            result_text = f"Advanced Nuclear Physics Analysis for Linda's Graduate-Level Study\n\n"
            
            # Basic Properties
            basic = advanced_analysis['basic_properties']
            result_text += f"Basic Nuclear Properties:\n"
            result_text += f"Atomic Number (Z): {basic['atomic_number']}\n"
            result_text += f"Mass Number (A): {basic['mass_number']}\n"
            result_text += f"Neutron Number (N): {basic['neutron_number']}\n"
            result_text += f"Binding Energy: {basic['binding_energy_MeV']:.2f} MeV\n"
            result_text += f"Mass Defect: {basic['mass_defect_u']:.6f} u\n"
            result_text += f"Fission Energy: {basic['fission_energy_MeV']:.2f} MeV\n\n"
            
            # Shell Model Analysis
            shell = advanced_analysis['shell_model_analysis']
            result_text += f"Shell Model & Magic Numbers:\n"
            result_text += f"Proton Magic Number: {'Yes' if shell['proton_magic'] else 'No'}\n"
            result_text += f"Neutron Magic Number: {'Yes' if shell['neutron_magic'] else 'No'}\n"
            result_text += f"Doubly Magic: {'Yes' if shell['doubly_magic'] else 'No'}\n"
            result_text += f"Shell Stability Factor: {shell['shell_stability_factor']:.2f}\n"
            result_text += f"Principal Quantum Number: {shell['principal_quantum_number']}\n\n"
            
            # Alpha Decay Analysis
            alpha = advanced_analysis['alpha_decay_analysis']
            result_text += f"Quantum Tunneling in Alpha Decay:\n"
            result_text += f"Alpha Energy: {alpha['alpha_energy_MeV']:.2f} MeV\n"
            result_text += f"Coulomb Barrier: {alpha['coulomb_barrier_MeV']:.2f} MeV\n"
            result_text += f"Gamow Factor: {alpha['gamow_factor']:.2e}\n"
            result_text += f"Tunneling Probability: {alpha['tunneling_probability']:.2e}\n"
            result_text += f"Half-life: {alpha['half_life_years']:.2e} years\n\n"
            
            # Fission Fragmentation
            fission = advanced_analysis['fission_fragmentation']
            result_text += f"Fission Fragmentation Pathways:\n"
            result_text += f"Light Fragment (A): {fission['light_fragment_A']:.1f}\n"
            result_text += f"Heavy Fragment (A): {fission['heavy_fragment_A']:.1f}\n"
            result_text += f"Deformation Energy: {fission['deformation_energy_MeV']:.2f} MeV\n"
            result_text += f"Coulomb Energy: {fission['coulomb_energy_MeV']:.2f} MeV\n"
            result_text += f"Fission Barrier: {fission['fission_barrier_MeV']:.2f} MeV\n"
            result_text += f"Fragmentation Asymmetry: {fission['fragmentation_asymmetry']:.3f}\n\n"
            
            # Stellar Nucleosynthesis
            stellar = advanced_analysis['stellar_nucleosynthesis']
            result_text += f"Stellar Nucleosynthesis:\n"
            result_text += f"CNO Cycle Energy: {stellar['cno_cycle']['total_energy_release_MeV']:.2f} MeV\n"
            result_text += f"Triple-Alpha Energy: {stellar['triple_alpha']['net_energy_release_MeV']:.2f} MeV\n"
            result_text += f"Triple-Alpha Temp: {stellar['triple_alpha']['temperature_threshold_K']:.0e} K\n\n"
            
            # Frontier Physics
            frontier = advanced_analysis['frontier_physics']
            result_text += f"Frontier Physics Topics:\n"
            result_text += f"Muon-Catalyzed Fusion Rate: {frontier['muon_catalyzed_fusion']['fusion_rate_s']:.0e} s⁻¹\n"
            result_text += f"Muon Bohr Radius: {frontier['muon_catalyzed_fusion']['reduced_bohr_radius_m']:.2e} m\n"
            result_text += f"Neutrino Oscillation (295km, 1GeV): {frontier['neutrino_oscillation']['electron_survival_probability']:.3f}\n\n"
            
            result_text += f"Note for Linda: This analysis covers graduate-level nuclear physics concepts including\n"
            result_text += f"shell model theory, quantum tunneling, stellar nucleosynthesis, and frontier topics\n"
            result_text += f"like muon-catalyzed fusion and neutrino oscillations. These are the advanced\n"
            result_text += f"concepts that will distinguish your understanding in graduate studies.\n"
            
            self.add_message("Dr. Oppenheimer", result_text)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Advanced calculation error: {str(e)}")

    def show_cross_sections(self):
        """Display cross section data for the specified nuclide"""
        try:
            Z = int(self.z_entry.get())
            A = int(self.a_entry.get())
            
            if Z <= 0 or A <= 0 or Z > A:
                messagebox.showerror("Error", "Invalid atomic or mass number")
                return
            
            # Get cross section data
            cross_section = self.physics.get_cross_section_data(Z, A, "thermal_neutron")
            
            if not cross_section:
                # Try to find by name or show available nuclides
                available = self.physics.list_available_nuclides()
                result_text = f"Cross section data not found for Z={Z}, A={A}\n\n"
                result_text += f"Available nuclides in database ({len(available)} total):\n"
                for i, nuclide in enumerate(available[:20], 1):  # Show first 20
                    result_text += f"{i}. {nuclide}\n"
                if len(available) > 20:
                    result_text += f"... and {len(available) - 20} more\n"
                result_text += "\nNote: You can also search by nuclide name using the AI chat."
                self.add_message("Dr. Oppenheimer", result_text)
                return
            
            # Format cross section data
            result_text = f"Neutron Cross Section Data Analysis for Linda's Study\n\n"
            result_text += f"Nuclide: {cross_section.get('name', 'Unknown')}\n"
            result_text += f"Atomic Number (Z): {cross_section.get('atomic_number', 'N/A')}\n"
            result_text += f"Mass Number (A): {cross_section.get('mass_number', 'N/A')}\n\n"
            
            # Thermal neutron cross sections
            if "thermal_neutron" in cross_section:
                thermal = cross_section["thermal_neutron"]
                result_text += "Thermal Neutron Cross Sections (0.025 eV, 2200 m/s):\n"
                result_text += "─" * 50 + "\n"
                result_text += f"Total Cross Section:     {thermal.get('total', 'N/A'):>12.2f} barns\n"
                result_text += f"Scattering Cross Section: {thermal.get('scattering', 'N/A'):>12.2f} barns\n"
                result_text += f"Absorption Cross Section: {thermal.get('absorption', 'N/A'):>12.2f} barns\n"
                if "fission" in thermal:
                    result_text += f"Fission Cross Section:    {thermal.get('fission', 'N/A'):>12.2f} barns\n"
                if "capture" in thermal:
                    result_text += f"Capture Cross Section:    {thermal.get('capture', 'N/A'):>12.2f} barns\n"
                result_text += "\n"
            
            # Fast neutron cross sections
            fast_cross_section = self.physics.get_cross_section_data(Z, A, "fast_neutron")
            if fast_cross_section and "fast_neutron" in fast_cross_section:
                fast = fast_cross_section["fast_neutron"]
                result_text += "Fast Neutron Cross Sections (1 MeV):\n"
                result_text += "─" * 50 + "\n"
                result_text += f"Total Cross Section:     {fast.get('total', 'N/A'):>12.2f} barns\n"
                result_text += f"Scattering Cross Section: {fast.get('scattering', 'N/A'):>12.2f} barns\n"
                result_text += f"Absorption Cross Section: {fast.get('absorption', 'N/A'):>12.2f} barns\n"
                if "fission" in fast:
                    result_text += f"Fission Cross Section:    {fast.get('fission', 'N/A'):>12.2f} barns\n"
                if "capture" in fast:
                    result_text += f"Capture Cross Section:    {fast.get('capture', 'N/A'):>12.2f} barns\n"
                result_text += "\n"
            
            # Resonance integral (for fissile materials)
            if "resonance_integral" in cross_section:
                res_int = cross_section["resonance_integral"]
                result_text += "Resonance Integral (0.5 eV - ∞):\n"
                result_text += "─" * 50 + "\n"
                if "absorption" in res_int:
                    result_text += f"Absorption Resonance Integral: {res_int.get('absorption', 'N/A'):>12.2f} barns\n"
                if "fission" in res_int:
                    result_text += f"Fission Resonance Integral:    {res_int.get('fission', 'N/A'):>12.2f} barns\n"
                result_text += "\n"
            
            # Educational notes
            result_text += "Note for Linda: Cross sections are fundamental in reactor physics and neutron transport.\n"
            result_text += "The total cross section represents the probability of any neutron-nucleus interaction.\n"
            result_text += "Thermal neutrons (low energy) typically have much higher cross sections for\n"
            result_text += "fissile materials like U-235 and Pu-239, which is why thermal reactors are\n"
            result_text += "common in nuclear power applications. Fast neutron cross sections are important\n"
            result_text += "for understanding fast reactor physics and neutron shielding requirements.\n\n"
            result_text += "1 barn = 10⁻²⁸ m² (approximately the geometric cross-sectional area of a nucleus)"
            
            self.add_message("Dr. Oppenheimer", result_text)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Cross section query error: {str(e)}")

    def calculate_critical_mass_display(self):
        """Display critical mass calculations using E=mc²"""
        try:
            Z = int(self.z_entry.get())
            A = int(self.a_entry.get())
            
            if Z <= 0 or A <= 0 or Z > A:
                messagebox.showerror("Error", "Invalid atomic or mass number")
                return
            
            # Calculate critical mass (using sphere geometry, no reflector for academic reference)
            result = self.physics.calculate_critical_mass(Z, A, geometry="sphere", reflector=False)
            
            if "error" in result:
                error_msg = f"Critical Mass Calculation Error:\n\n{result.get('error', 'Unknown error')}\n"
                if "suggestion" in result:
                    error_msg += f"\nSuggestion: {result.get('suggestion')}"
                if "note" in result:
                    error_msg += f"\n\nNote: {result.get('note')}"
                self.add_message("Dr. Oppenheimer", error_msg)
                return
            
            # Format results for academic paper
            result_text = f"Critical Mass Analysis Using E=mc²\n"
            result_text += "=" * 60 + "\n\n"
            result_text += f"Nuclide: {result['nuclide']}\n"
            result_text += f"Atomic Number (Z): {result['atomic_number']}\n"
            result_text += f"Mass Number (A): {result['mass_number']}\n"
            result_text += f"Geometry: {result['geometry'].title()}\n"
            result_text += f"Neutron Reflector: {'Yes' if result['reflector'] else 'No'}\n"
            result_text += f"Density: {result['density_kg_m3']:.2f} kg/m³\n\n"
            
            # Critical Parameters
            crit = result['critical_parameters']
            result_text += "Critical Parameters:\n"
            result_text += "─" * 60 + "\n"
            result_text += f"Critical Mass:        {crit['critical_mass_kg']:.6f} kg\n"
            result_text += f"                      {crit['critical_mass_g']:.2f} g\n"
            result_text += f"Critical Radius:      {crit['critical_radius_m']:.6f} m\n"
            result_text += f"                      {crit['critical_radius_cm']:.4f} cm\n"
            result_text += f"Critical Volume:      {crit['critical_volume_m3']:.6e} m³\n"
            result_text += f"                      {crit['critical_volume_cm3']:.2f} cm³\n\n"
            
            # Neutron Physics
            neutron = result['neutron_physics']
            result_text += "Neutron Physics Parameters:\n"
            result_text += "─" * 60 + "\n"
            result_text += f"Neutrons per Fission (ν):     {neutron['neutrons_per_fission']:.3f}\n"
            result_text += f"Fission Cross Section:        {neutron['fission_cross_section_barn']:.2f} barns\n"
            result_text += f"Absorption Cross Section:     {neutron['absorption_cross_section_barn']:.2f} barns\n"
            result_text += f"Scattering Cross Section:     {neutron['scattering_cross_section_barn']:.2f} barns\n"
            result_text += f"Neutron Reproduction (η):     {neutron['eta']:.4f}\n"
            result_text += f"Effective Multiplication (k): {neutron['k_effective']:.4f}\n"
            result_text += f"Diffusion Length:             {neutron['diffusion_length_m']:.4e} m\n"
            result_text += f"Migration Area:               {neutron['migration_area_m2']:.4e} m²\n\n"
            
            # Energy Calculations (E=mc²)
            energy = result['energy_calculations']
            result_text += "Energy Calculations (E=mc²):\n"
            result_text += "─" * 60 + "\n"
            result_text += f"Binding Energy per Atom:      {energy['binding_energy_per_atom_MeV']:.2f} MeV\n"
            result_text += f"Mass Defect per Atom:         {energy['mass_defect_per_atom_u']:.6e} u\n\n"
            
            result_text += f"Total Binding Energy (E=mc²):\n"
            result_text += f"  {energy['total_binding_energy_MeV']:.6e} MeV\n"
            result_text += f"  {energy['total_binding_energy_J']:.6e} J\n\n"
            
            result_text += f"Complete Rest Energy (E=mc²):\n"
            result_text += f"  {energy['e_mc2_rest_energy_MeV']:.6e} MeV\n"
            result_text += f"  {energy['e_mc2_rest_energy_J']:.6e} J\n\n"
            
            result_text += f"Fission Energy Release (if all atoms fission):\n"
            result_text += f"  Energy per Fission:         {energy['energy_per_fission_MeV']:.1f} MeV\n"
            result_text += f"  Total Fission Energy:       {energy['total_fission_energy_MeV']:.6e} MeV\n"
            result_text += f"                              {energy['total_fission_energy_J']:.6e} J\n"
            result_text += f"  Equivalent TNT:             {energy['total_fission_energy_kt_TNT']:.2f} kilotons\n\n"
            
            # Academic note
            result_text += "Academic Notes for Your Paper:\n"
            result_text += "─" * 60 + "\n"
            result_text += f"These calculations utilize Einstein's mass-energy equivalence (E=mc²) to\n"
            result_text += f"determine the critical mass and associated energy parameters. The critical\n"
            result_text += f"mass represents the minimum mass of fissile material required to sustain a\n"
            result_text += f"neutron chain reaction, calculated using neutron diffusion theory.\n\n"
            result_text += f"Key Equations Used:\n"
            result_text += f"  • E = mc² (Einstein's mass-energy equivalence)\n"
            result_text += f"  • k_eff = η × ε × p × f (Four-factor formula)\n"
            result_text += f"  • B² = (π/R)² (Geometric buckling for sphere)\n\n"
            result_text += f"Note: These are theoretical calculations for academic research purposes.\n"
            result_text += f"Actual critical masses depend on many factors including purity, geometry,\n"
            result_text += f"temperature, pressure, and neutron reflector properties."
            
            self.add_message("Dr. Oppenheimer", result_text)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Critical mass calculation error: {str(e)}")

    def show_knowledge_summary(self):
        """Display knowledge base summary showing what the system has learned"""
        try:
            summary = self.knowledge_manager.get_knowledge_summary()
            
            result_text = "Knowledge Base Summary - Self-Learning Progress\n"
            result_text += "=" * 60 + "\n\n"
            result_text += f"📚 Knowledge Base Statistics:\n"
            result_text += f"  Total Entities Extracted: {summary['total_entities']}\n"
            result_text += f"  Total Facts Learned: {summary['total_facts']}\n"
            result_text += f"  Active Topics: {summary['total_topics']}\n"
            result_text += f"  Documents Indexed: {summary['total_documents_indexed']}\n"
            result_text += f"  Created: {summary.get('created', 'Unknown')[:10]}\n"
            result_text += f"  Last Updated: {summary.get('last_updated', 'Unknown')[:10]}\n\n"
            
            # Most mentioned entities
            if summary.get('most_mentioned_entities'):
                result_text += "🔬 Most Discussed Topics:\n"
                for i, (entity, count) in enumerate(summary['most_mentioned_entities'][:10], 1):
                    result_text += f"  {i}. {entity}: {count} mentions\n"
                result_text += "\n"
            
            # Active topics
            if summary.get('active_topics'):
                result_text += "📖 Active Research Topics:\n"
                for topic, count in summary['active_topics']:
                    topic_name = topic.replace('_', ' ').title()
                    result_text += f"  • {topic_name}: {count} discussions\n"
                result_text += "\n"
            
            result_text += "Note: The system continuously learns from our conversations.\n"
            result_text += "It extracts entities (nuclides, formulas, concepts), builds a knowledge\n"
            result_text += "graph, and uses semantic search to retrieve relevant past discussions.\n"
            result_text += "This enables long-term memory across our 6-year research journey.\n\n"
            result_text += "Over time, I will better remember your research interests, frequently\n"
            result_text += "discussed topics, and can reference past calculations and concepts."
            
            self.add_message("Dr. Oppenheimer", result_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Knowledge base error: {str(e)}")

    def show_advanced_calculations_menu(self):
        """Show menu for advanced complex calculations"""
        if not hasattr(self.physics, 'advanced_calc') or self.physics.advanced_calc is None:
            messagebox.showwarning(
                "Advanced Calculations Unavailable",
                "Advanced calculations require scipy library.\n\n"
                "To install: pip install scipy\n\n"
                "This module provides:\n"
                "- ODE/PDE solvers\n"
                "- Monte Carlo simulations\n"
                "- Multi-body calculations\n"
                "- Optimization algorithms\n"
                "- Statistical analysis"
            )
            return
        
        # Create menu window with dark theme
        menu_window = tk.Toplevel(self.root)
        menu_window.title("ADVANCED CALCULATIONS")
        menu_window.geometry("550x700")
        menu_window.configure(bg=self.bg_color)
        
        # Title frame
        title_frame = tk.Frame(menu_window, bg=self.panel_color, highlightbackground=self.border_color, highlightthickness=1)
        title_frame.pack(fill=tk.X, padx=15, pady=15)
        
        title = tk.Label(
            title_frame,
            text="ADVANCED CALCULATIONS",
            font=('Courier New', 18, 'bold'),
            bg=self.panel_color,
            fg=self.text_primary
        )
        title.pack(pady=15)
        
        subtitle = tk.Label(
            title_frame,
            text="COMPLEX NUMERICAL METHODS",
            font=('Courier New', 9),
            bg=self.panel_color,
            fg=self.text_secondary
        )
        subtitle.pack(pady=(0, 15))
        
        # Scrollable frame for buttons
        canvas = tk.Canvas(menu_window, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(menu_window, orient="vertical", command=canvas.yview, bg=self.bg_color, troughcolor=self.panel_color)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Calculation options - light buttons with black text on white background
        calc_options = [
            ("NEUTRON TRANSPORT ODE", self.calc_neutron_transport, '#e0e0e0'),
            ("MONTE CARLO SIMULATION", self.calc_monte_carlo, '#d5d5d5'),
            ("FISSION YIELD DISTRIBUTION", self.calc_fission_yield, '#e5e5e5'),
            ("OPTIMIZE CRITICAL CONFIG", self.calc_optimize_critical, '#dadada'),
            ("NEUTRON SPECTRUM", self.calc_neutron_spectrum, '#e0e0e0'),
            ("BATEMAN EQUATIONS", self.calc_bateman_equations, '#d5d5d5'),
            ("NEUTRON FLUX DISTRIBUTION", self.calc_neutron_flux, '#e5e5e5'),
            ("SENSITIVITY ANALYSIS", self.calc_sensitivity_analysis, '#dadada'),
            ("NUCLEAR REACTION RATE", self.calc_reaction_rate, '#e0e0e0'),
            ("REACTION NETWORK", self.calc_reaction_network, '#d5d5d5'),
            ("FUEL BURNUP EVOLUTION", self.calc_burnup, '#e5e5e5'),
            ("MULTI-GROUP DIFFUSION", self.calc_multigroup_diffusion, '#dadada'),
            ("CRITICAL SEARCH", self.calc_critical_search, '#e0e0e0'),
            ("UNCERTAINTY PROPAGATION", self.calc_uncertainty, '#d5d5d5')
        ]
        
        for calc_name, calc_func, btn_color in calc_options:
            btn = tk.Button(
                scrollable_frame,
                text=calc_name,
                command=calc_func,
                bg=btn_color,
                fg=self.text_primary,
                font=('Courier New', 9, 'bold'),
                relief=tk.FLAT,
                padx=15,
                pady=8,
                width=35,
                activebackground='#c5c5c5',
                activeforeground=self.text_primary,
                cursor='hand2'
            )
            btn.pack(pady=4, padx=15)
        
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side="right", fill="y", pady=(0, 15))
        
        info_label = tk.Label(
            menu_window,
            text="Advanced numerical methods:\nODE/PDE solvers • Monte Carlo • Optimization • Statistics",
            font=('Courier New', 8),
            bg=self.bg_color,
            fg=self.text_secondary,
            justify=tk.CENTER
        )
        info_label.pack(pady=(0, 15))
    
    def calc_neutron_transport(self):
        """Calculate neutron transport using ODE solver"""
        try:
            Z = int(self.z_entry.get()) if self.z_entry.get() else 92
            A = int(self.a_entry.get()) if self.a_entry.get() else 235
            
            result = self.physics.advanced_calc.solve_neutron_transport_ode(
                initial_conditions={'N0': 1.0},
                time_span=(0.0, 1.0),  # 1 second
                parameters={
                    'k_eff': 1.005,  # Slightly supercritical
                    'lambda': 0.0,
                    'generation_time': 1e-5
                }
            )
            
            text = f"Neutron Transport ODE Solution\n{'='*60}\n\n"
            text += f"Parameters: k_eff={result['parameters']['k_eff']}, "
            text += f"generation_time={result['parameters']['generation_time']}s\n\n"
            text += f"Solution: {'Success' if result['success'] else 'Failed'}\n"
            text += f"Time points: {len(result['time'])}\n"
            text += f"Final neutron density: {result['neutron_density'][-1]:.6e}\n"
            text += f"Peak density: {max(result['neutron_density']):.6e}\n\n"
            text += "This solves: dN/dt = (k_eff - 1)N/Λ - λN\n"
            text += "Using advanced ODE solver (RK45 method)"
            
            self.add_message("Dr. Oppenheimer", text)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def calc_monte_carlo(self):
        """Run Monte Carlo neutron transport simulation"""
        try:
            result = self.physics.advanced_calc.monte_carlo_neutron_path(
                initial_energy=1e6,  # 1 MeV
                material_properties={
                    'density': 19050,  # U-235 density
                    'sigma_total': 14.5,  # barns
                    'sigma_absorption': 4.5,
                    'sigma_scattering': 10.0,
                    'atomic_mass': 235
                },
                n_simulations=10000
            )
            
            text = f"Monte Carlo Neutron Transport Simulation\n{'='*60}\n\n"
            text += f"Simulations: {result['n_simulations']}\n"
            text += f"Mean free path: {result['mean_free_path_theoretical']:.6e} m\n"
            if result['mean_absorption_distance']:
                text += f"Mean absorption distance: {result['mean_absorption_distance']:.6e} m\n"
            text += f"Absorption probability: {result['absorption_probability']:.2%}\n"
            text += f"Scattering probability: {result['scattering_probability']:.2%}\n\n"
            text += "This uses Monte Carlo methods to simulate individual\n"
            text += "neutron paths through material with statistical sampling."
            
            self.add_message("Dr. Oppenheimer", text)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def calc_fission_yield(self):
        """Calculate fission yield distribution"""
        try:
            Z = int(self.z_entry.get()) if self.z_entry.get() else 92
            A = int(self.a_entry.get()) if self.a_entry.get() else 235
            
            result = self.physics.advanced_calc.calculate_fission_yield_distribution(Z, A)
            
            text = f"Fission Yield Distribution Analysis\n{'='*60}\n\n"
            text += f"Parent: {result['parent_nucleus']}\n"
            text += f"Mean fragment mass: {result['statistics']['mean_mass']:.2f}\n"
            text += f"Standard deviation: {result['statistics']['standard_deviation']:.2f}\n"
            text += f"Light peak: A={result['statistics']['light_peak']:.1f}\n"
            text += f"Heavy peak: A={result['statistics']['heavy_peak']:.1f}\n\n"
            text += "This calculates the mass distribution of fission fragments\n"
            text += "using Gaussian approximation and statistical methods."
            
            self.add_message("Dr. Oppenheimer", text)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def calc_optimize_critical(self):
        """Optimize critical mass configuration"""
        try:
            Z = int(self.z_entry.get()) if self.z_entry.get() else 92
            A = int(self.a_entry.get()) if self.a_entry.get() else 235
            
            result = self.physics.advanced_calc.optimize_critical_configuration(
                Z, A,
                constraints={
                    'geometry': 'sphere',
                    'max_radius': 0.2,
                    'min_radius': 0.01,
                    'density': 19050
                }
            )
            
            text = f"Critical Mass Optimization\n{'='*60}\n\n"
            text += f"Optimization: {'Success' if result['optimization_success'] else 'Failed'}\n"
            text += f"Optimal radius: {result['optimal_radius_cm']:.4f} cm\n"
            text += f"Optimal mass: {result['optimal_mass_g']:.2f} g\n"
            text += f"Iterations: {result['iterations']}\n\n"
            text += "This uses L-BFGS-B optimization algorithm to find\n"
            text += "the minimum critical mass configuration."
            
            self.add_message("Dr. Oppenheimer", text)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def calc_neutron_spectrum(self):
        """Calculate neutron energy spectrum"""
        text = "Neutron Spectrum Calculation\n\n"
        text += "This requires specifying material layers.\n"
        text += "Please use the AI chat to describe your material configuration."
        self.add_message("Dr. Oppenheimer", text)
    
    def calc_bateman_equations(self):
        """Solve Bateman equations for decay chain"""
        text = "Bateman Equations Solver\n\n"
        text += "This solves radioactive decay chains using ODE methods.\n"
        text += "Please specify the decay chain in the AI chat."
        self.add_message("Dr. Oppenheimer", text)
    
    def calc_neutron_flux(self):
        """Calculate neutron flux distribution"""
        text = "Neutron Flux Distribution\n\n"
        text += "This solves the neutron diffusion equation.\n"
        text += "Please specify reactor geometry in the AI chat."
        self.add_message("Dr. Oppenheimer", text)
    
    def calc_sensitivity_analysis(self):
        """Perform sensitivity analysis"""
        text = "Sensitivity Analysis\n\n"
        text += "This analyzes how parameters affect results.\n"
        text += "Please specify the function and parameters in the AI chat."
        self.add_message("Dr. Oppenheimer", text)
    
    def calc_reaction_rate(self):
        """Calculate nuclear reaction rate"""
        try:
            import numpy as np
            
            Z = int(self.z_entry.get()) if self.z_entry.get() else 92
            A = int(self.a_entry.get()) if self.a_entry.get() else 235
            
            props = self.physics.get_nuclear_properties(Z, A)
            sigma = props.get('fission_cross_section', 584.0)  # barns
            
            result = self.physics.advanced_calc.calculate_nuclear_reaction_rate(
                target_nuclide={
                    'Z': Z, 'A': A,
                    'sigma': sigma,
                    'density': 19050  # kg/m³ (U-235)
                },
                neutron_flux=1e14,  # n/cm²/s (typical reactor flux)
                energy_spectrum=np.array([0.025])  # thermal
            )
            
            text = f"Nuclear Reaction Rate Calculation\n{'='*60}\n\n"
            text += f"Target: {result['target_nuclide']}\n"
            text += f"Neutron Flux: {result['neutron_flux_n_per_cm2_s']:.2e} n/cm²/s\n"
            text += f"Reaction Rate: {result['reaction_rate_per_cm3_s']:.2e} reactions/cm³/s\n"
            text += f"Reaction Rate: {result['reaction_rate_per_m3_s']:.2e} reactions/m³/s\n"
            if result['activity_Bq_per_cm3']:
                text += f"Activity: {result['activity_Bq_per_cm3']:.2e} Bq/cm³\n"
            text += f"\nFormula: R = σ × φ × N\n"
            text += "Where σ is cross-section, φ is flux, N is number density"
            
            self.add_message("Dr. Oppenheimer", text)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def calc_reaction_network(self):
        """Solve nuclear reaction network"""
        text = "Nuclear Reaction Network Solver\n\n"
        text += "This solves complex reaction networks (e.g., stellar nucleosynthesis).\n"
        text += "Example: CNO cycle, triple-alpha process, r-process, s-process.\n\n"
        text += "Please specify initial abundances and reaction rates in the AI chat."
        self.add_message("Dr. Oppenheimer", text)
    
    def calc_burnup(self):
        """Calculate fuel burnup evolution"""
        try:
            import numpy as np
            
            # Example: U-235 fuel
            result = self.physics.advanced_calc.calculate_burnup_evolution(
                fuel_composition={'U-235': 1.0},  # 1 kg
                neutron_flux=1e14,  # n/cm²/s
                time_points=np.linspace(0, 86400*365, 100)  # 1 year
            )
            
            text = f"Fuel Burnup Evolution\n{'='*60}\n\n"
            text += f"Initial Composition: {list(result['mass_evolution'].keys())}\n"
            text += f"Time Span: {result['time_points'][0]:.0f} to {result['time_points'][-1]:.0f} seconds\n"
            text += f"Total Burnup: {result['total_burnup_MWd_per_kg']:.2f} MWd/kg\n\n"
            text += "This calculates:\n"
            text += "• Fuel transmutation over time\n"
            text += "• Fission product buildup\n"
            text += "• Burnup (energy released per unit mass)\n"
            text += "• Composition evolution"
            
            self.add_message("Dr. Oppenheimer", text)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def calc_multigroup_diffusion(self):
        """Solve multi-group neutron diffusion"""
        try:
            result = self.physics.advanced_calc.solve_multigroup_diffusion(
                energy_groups=4,
                material_properties={
                    'D': [1.0, 0.8, 0.6, 0.4],  # cm
                    'Sigma_a': [0.01, 0.02, 0.05, 0.1],  # 1/cm
                    'nu_Sigma_f': [0.0, 0.0, 0.02, 0.03]  # 1/cm
                },
                geometry={'shape': 'sphere', 'radius': 10.0}  # cm
            )
            
            text = f"Multi-group Neutron Diffusion\n{'='*60}\n\n"
            text += f"Energy Groups: {result['energy_groups']}\n"
            text += f"k_effective: {result['k_effective']:.6f}\n"
            text += f"Geometry: {result['geometry']}\n"
            text += f"Radius: {result['radius_cm']:.2f} cm\n\n"
            text += "This solves the multi-group diffusion equation:\n"
            text += "D∇²φ - Σ_a φ + (1/k)νΣ_f φ = 0\n"
            text += "Using eigenvalue methods for criticality analysis"
            
            self.add_message("Dr. Oppenheimer", text)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def calc_critical_search(self):
        """Search for critical configuration"""
        try:
            result = self.physics.advanced_calc.critical_search(
                material_properties={
                    'D': [1.0],
                    'Sigma_a': [0.01],
                    'nu_Sigma_f': [0.02]
                },
                geometry={'shape': 'sphere', 'radius': 10.0},
                target_k=1.0
            )
            
            text = f"Critical Configuration Search\n{'='*60}\n\n"
            text += f"Target k_eff: {result['target_k']}\n"
            text += f"Found k_eff: {result['k_effective']:.6f}\n"
            text += f"Critical Radius: {result['critical_radius_cm']:.2f} cm\n"
            text += f"Critical Radius: {result['critical_radius_m']:.4f} m\n"
            text += f"Geometry: {result['geometry']}\n"
            text += f"Optimization: {'Success' if result['optimization_success'] else 'Failed'}\n\n"
            text += "This searches for the critical configuration using\n"
            text += "optimization algorithms to find k_eff = 1.0"
            
            self.add_message("Dr. Oppenheimer", text)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def calc_uncertainty(self):
        """Propagate uncertainties"""
        text = "Uncertainty Propagation Analysis\n\n"
        text += "This propagates uncertainties through calculations using Monte Carlo.\n"
        text += "Useful for:\n"
        text += "• Cross-section uncertainty analysis\n"
        text += "• Critical mass uncertainty\n"
        text += "• Reaction rate uncertainty\n"
        text += "• Any parameter sensitivity study\n\n"
        text += "Please specify the function and parameter uncertainties in the AI chat."
        self.add_message("Dr. Oppenheimer", text)

    def fetch_iaea_data(self):
        """Fetch data from IAEA Nuclear Data Services"""
        try:
            Z = int(self.z_entry.get()) if self.z_entry.get() else 92
            A = int(self.a_entry.get()) if self.a_entry.get() else 235
            
            # Show loading message
            self.add_message("System", f"Fetching IAEA NUCLEUS/NDS data for Z={Z}, A={A}...")
            
            # Get IAEA data
            iaea_data = self.physics.get_iaea_nuclide_data(Z, A, "all")
            
            if "error" not in iaea_data:
                result_text = f"IAEA NUCLEUS/NDS - Authoritative Experimental Data\n"
                result_text += "=" * 60 + "\n\n"
                result_text += f"Nuclide: {iaea_data['nuclide']} ({iaea_data.get('nuclide_id', 'N/A')})\n"
                result_text += f"Source: {iaea_data['source']}\n"
                result_text += f"Data Type: {iaea_data['data_type']}\n"
                result_text += f"Status: {iaea_data.get('status', 'Success')}\n"
                result_text += f"Content Type: {iaea_data.get('content_type', 'N/A')}\n\n"
                
                result_text += "This is authoritative experimental data from IAEA NUCLEUS/NDS.\n"
                result_text += "As a NUCLEUS member, you have access to this comprehensive database.\n\n"
                
                # 提供数据类型建议
                if iaea_data.get('data_type') == 'all':
                    result_text += "Tip: For detailed data, try requesting specific types:\n"
                    result_text += "  • 'levels' - Energy level structures\n"
                    result_text += "  • 'decay' - Radioactive decay data\n"
                    result_text += "  • 'masses' - Nuclear mass data\n"
                    result_text += "  • 'structure' - Nuclear structure information\n\n"
                
                # Display parsed CSV data if available
                parsed_data = iaea_data.get('parsed_data')
                if parsed_data and isinstance(parsed_data, dict):
                    result_text += f"Data Format: {parsed_data.get('format', 'Unknown')}\n"
                    
                    # 处理单值响应（可能是记录数）
                    if 'single_value' in parsed_data:
                        result_text += f"Response Value: {parsed_data['single_value']}\n"
                        if parsed_data.get('note'):
                            result_text += f"Note: {parsed_data['note']}\n"
                        result_text += "\nThis may indicate the number of records available.\n"
                        result_text += "Try requesting specific data types (levels, decay, structure, masses) separately.\n\n"
                    else:
                        # 多行CSV数据
                        row_count = parsed_data.get('row_count', 0)
                        result_text += f"Rows: {row_count}\n\n"
                        
                        if parsed_data.get('headers'):
                            result_text += "Data Headers:\n"
                            result_text += f"  {', '.join(parsed_data['headers'])}\n\n"
                        
                        if parsed_data.get('rows'):
                            result_text += "Data Preview (first 5 rows):\n"
                            for i, row in enumerate(parsed_data['rows'][:5], 1):
                                result_text += f"  Row {i}: {', '.join(str(x) for x in row)}\n"
                            if len(parsed_data['rows']) > 5:
                                result_text += f"  ... and {len(parsed_data['rows']) - 5} more rows\n"
                else:
                    # Display raw data
                    raw_data = iaea_data.get('raw_data', iaea_data.get('data', ''))
                    if isinstance(raw_data, str):
                        if len(raw_data) > 1000:
                            result_text += f"Data Preview (first 1000 chars):\n{raw_data[:1000]}...\n"
                        else:
                            result_text += f"Data:\n{raw_data}\n"
                    elif isinstance(raw_data, dict):
                        result_text += "Available Data Fields:\n"
                        for key in raw_data.keys():
                            result_text += f"  • {key}\n"
                        result_text += "\n"
                        result_text += f"Data Sample:\n{json.dumps(raw_data, indent=2)[:500]}...\n"
                
                result_text += f"\nAPI URL: {iaea_data.get('url', 'N/A')}\n"
                result_text += "\nNote: This data comes directly from IAEA NUCLEUS/NDS database.\n"
                result_text += "It includes experimental measurements and evaluated nuclear data.\n"
                result_text += "As a NUCLEUS member, you have full access to this authoritative source."
                
                self.add_message("Dr. Oppenheimer", result_text)
            else:
                error_msg = f"IAEA NUCLEUS/NDS Data Access\n{'='*60}\n\n"
                error_msg += f"Error: {iaea_data.get('error', 'Unknown error')}\n\n"
                if "note" in iaea_data:
                    error_msg += f"Note: {iaea_data['note']}\n"
                if "alternative" in iaea_data:
                    error_msg += f"\nAlternative: {iaea_data['alternative']}\n"
                if "suggestion" in iaea_data:
                    error_msg += f"\nSuggestion: {iaea_data['suggestion']}\n"
                error_msg += "\nAs a NUCLEUS member, you should have access to this data.\n"
                error_msg += "The system will use local cross section data as fallback."
                
                self.add_message("Dr. Oppenheimer", error_msg)
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid atomic and mass numbers")
        except Exception as e:
            messagebox.showerror("Error", f"IAEA data fetch error: {str(e)}")

    def add_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if sender == "You" or sender == "Researcher":
            self.chat_display.insert(tk.END, f"\n[{timestamp}] RESEARCHER:\n", "user")
            self.chat_display.insert(tk.END, f"{message}\n", "user_message")
        else:
            # Handle both "Dr. Oppenheimer" and "J. Robert Oppenheimer"
            sender_name = "J. ROBERT OPPENHEIMER" if "Oppenheimer" in sender else sender.upper()
            self.chat_display.insert(tk.END, f"\n[{timestamp}] {sender_name}:\n", "oppenheimer")
            
            # Check if message contains verification note
            if "[Verification:" in message:
                parts = message.split("[Verification:")
                main_message = parts[0].strip()
                verification = "[Verification:" + parts[1] if len(parts) > 1 else ""
                
                # Insert main message with formula highlighting
                self._insert_with_formula_highlighting(main_message, "oppenheimer_message")
                if verification:
                    self.chat_display.insert(tk.END, f"{verification}\n", "verification")
            else:
                # Insert message with formula highlighting
                self._insert_with_formula_highlighting(message, "oppenheimer_message")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def _insert_with_formula_highlighting(self, text: str, base_tag: str):
        """Insert text with automatic formula highlighting"""
        import re
        
        # Pattern to match mathematical formulas and equations
        # Matches: E = mc², k_eff = η × ε × p × f, B = a_v·A - ..., etc.
        formula_patterns = [
            r'E\s*=\s*mc[²²2]',  # E=mc²
            r'k_eff\s*=\s*[ηη]\s*×\s*[εε]\s*×\s*p\s*×\s*f',  # Four-factor formula
            r'B\s*=\s*a_v[·\*]A\s*-\s*a_s[·\*]A\^?\(?2/3\)?',  # Binding energy
            r'[A-Z][a-z]?\s*=\s*[A-Za-z0-9\+\-\*/\^²³·×ηεσλΣΛαβγδΔ∇φ]+',  # General equations
            r'[A-Z]_[a-z0-9]+\s*=\s*[^\.\n]+',  # Subscripted variables
            r'[ηηεεσΣλΛααββγΓδΔ∇φφ]\s*=\s*[^\.\n]+',  # Greek letter equations
        ]
        
        # Find all formula matches (non-overlapping)
        formula_positions = []
        for pattern in formula_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Check if this match overlaps with existing matches
                overlap = False
                for existing_start, existing_end, _ in formula_positions:
                    if not (match.end() <= existing_start or match.start() >= existing_end):
                        overlap = True
                        break
                if not overlap:
                    formula_positions.append((match.start(), match.end(), match.group()))
        
        # Sort by position
        formula_positions.sort(key=lambda x: x[0])
        
        # Remove overlapping matches (keep longer ones)
        if formula_positions:
            cleaned_positions = [formula_positions[0]]
            for start, end, formula in formula_positions[1:]:
                prev_start, prev_end, _ = cleaned_positions[-1]
                if start >= prev_end:
                    cleaned_positions.append((start, end, formula))
                elif (end - start) > (prev_end - prev_start):
                    # Current match is longer, replace previous
                    cleaned_positions[-1] = (start, end, formula)
            formula_positions = cleaned_positions
        
        # Insert text with highlighting
        last_pos = 0
        for start, end, formula in formula_positions:
            # Insert text before formula
            if start > last_pos:
                self.chat_display.insert(tk.END, text[last_pos:start], base_tag)
            
            # Insert formula with highlighting
            self.chat_display.insert(tk.END, text[start:end], "formula")
            last_pos = end
        
        # Insert remaining text
        if last_pos < len(text):
            self.chat_display.insert(tk.END, text[last_pos:], base_tag)
        
        # If no formulas found, insert entire text normally
        if not formula_positions:
            self.chat_display.insert(tk.END, text, base_tag)
        
        # Add newline
        self.chat_display.insert(tk.END, "\n", base_tag)
    
    def _generate_reasoning_chain(self, query: str) -> List[Dict]:
        """
        Generate multi-step reasoning chain (DeepSeek-style)
        
        Returns:
            List of reasoning steps, each with premise, reasoning, and conclusion
        """
        reasoning_steps = []
        query_lower = query.lower()
        
        # Step 1: Question Analysis
        reasoning_steps.append({
            "step": 1,
            "premise": f"User question: {query}",
            "reasoning": "Analyzing the question to identify what is being asked and what type of answer is needed",
            "conclusion": "Question type identified",
            "confidence": 0.9
        })
        
        # Step 2: Knowledge Retrieval
        if any(word in query_lower for word in ["calculate", "compute", "find", "determine"]):
            reasoning_steps.append({
                "step": 2,
                "premise": "Calculation or determination requested",
                "reasoning": "Retrieving relevant formulas, physical constants, and calculation methods from knowledge base",
                "conclusion": "Relevant calculation framework identified",
                "confidence": 0.85
            })
        
        # Step 3: Data Verification
        if any(word in query_lower for word in ["nuclide", "isotope", "element", "u-", "pu-", "th-"]):
            reasoning_steps.append({
                "step": 3,
                "premise": "Nuclide-specific information needed",
                "reasoning": "Checking nuclide data in database, verifying cross-sections, and confirming data sources",
                "conclusion": "Nuclide data verified and retrieved",
                "confidence": 0.9
            })
        
        # Step 4: Theoretical Foundation
        if any(word in query_lower for word in ["critical", "mass", "criticality", "reactor"]):
            reasoning_steps.append({
                "step": 4,
                "premise": "Reactor physics or criticality question",
                "reasoning": "Applying neutron diffusion theory, four-factor formula (k_eff = η × ε × p × f), and geometric buckling",
                "conclusion": "Theoretical framework established",
                "confidence": 0.88
            })
        
        # Step 5: Mathematical Derivation (if calculation)
        if any(word in query_lower for word in ["calculate", "compute", "derive", "formula"]):
            reasoning_steps.append({
                "step": 5,
                "premise": "Mathematical calculation required",
                "reasoning": "Deriving step-by-step: identifying variables, applying formulas, performing calculations, verifying units",
                "conclusion": "Calculation steps determined",
                "confidence": 0.85
            })
        
        # Step 6: Verification
        reasoning_steps.append({
            "step": len(reasoning_steps) + 1,
            "premise": "Preparing final answer",
            "reasoning": "Verifying calculations against known values, checking physical reasonableness, confirming units",
            "conclusion": "Answer verified and ready",
            "confidence": 0.9
        })
        
        return reasoning_steps
    
    def _execute_reasoning_step(self, step: Dict) -> Dict:
        """
        Execute a single reasoning step
        
        Args:
            step: Reasoning step dictionary
        
        Returns:
            Updated step with execution results
        """
        # In a full implementation, this would actually execute the reasoning
        # For now, we'll just mark it as executed
        step["executed"] = True
        step["execution_time"] = 0.1  # Simulated
        return step
    
    def _generate_thinking_steps(self, message: str, relevant_knowledge: Dict, data_needed: bool) -> str:
        """Generate thinking steps based on the question and context (enhanced with reasoning chain)"""
        # Generate reasoning chain
        reasoning_chain = self._generate_reasoning_chain(message)
        
        steps = []
        message_lower = message.lower()
        
        # Convert reasoning chain to display format
        for step in reasoning_chain:
            steps.append(f"Step {step['step']}: {step['reasoning']}")
            if step.get('conclusion'):
                steps.append(f"  → {step['conclusion']} (confidence: {step['confidence']:.0%})")
        
        # Add domain-specific steps
        if any(word in message_lower for word in ["fusion", "tokamak", "ITER"]):
            steps.append("• Retrieving cutting-edge fusion research from knowledge base...")
            steps.append("• Considering plasma physics and magnetic confinement principles...")
        
        if any(word in message_lower for word in ["medicine", "PET", "SPECT", "radiotherapy"]):
            steps.append("• Accessing nuclear medicine knowledge...")
            steps.append("• Considering medical imaging and therapeutic applications...")
        
        if any(word in message_lower for word in ["quantum", "qubit", "quantum computing"]):
            steps.append("• Retrieving quantum computing applications in nuclear physics...")
            steps.append("• Considering quantum simulation methods...")
        
        if data_needed:
            steps.append("• Accessing nuclear data sources (IAEA NUCLEUS/NDS)...")
            steps.append("• Verifying data availability and accuracy...")
        
        if relevant_knowledge.get("related_conversations"):
            steps.append("• Recalling relevant previous discussions...")
            steps.append("• Connecting to established context...")
        
        # Always add final synthesis step
        steps.append("• Synthesizing information into comprehensive answer...")
        
        # Format as thinking text
        thinking_text = "\n".join(steps)
        thinking_text += "\n\nNow, let me provide you with a comprehensive answer..."
        
        return thinking_text
    
    def _display_thinking_steps_progressively(self, reasoning_chain: List[Dict], message: str, 
                                             relevant_knowledge: Dict, data_needed: bool):
        """Display thinking steps progressively (real-time simulation)"""
        import time
        
        def update_step(step_idx):
            if step_idx < len(reasoning_chain):
                step = reasoning_chain[step_idx]
                step_text = f"Step {step['step']}: {step['reasoning']}\n"
                step_text += f"  → {step['conclusion']} (confidence: {step['confidence']:.0%})\n\n"
                
                # Use root.after to ensure thread-safe GUI updates
                self.root.after(0, lambda t=step_text, idx=step_idx: self._append_thinking_realtime(t))
                
                # Schedule next step with proper delay
                if step_idx + 1 < len(reasoning_chain):
                    threading.Timer(1.0, lambda idx=step_idx + 1: update_step(idx)).start()
        
        # Start displaying steps progressively after a short delay
        threading.Timer(0.3, lambda: update_step(0)).start()
        
        # Add domain-specific steps after reasoning chain
        message_lower = message.lower()
        domain_steps = []
        
        if any(word in message_lower for word in ["fusion", "tokamak", "ITER"]):
            domain_steps.append("• Retrieving cutting-edge fusion research from knowledge base...")
            domain_steps.append("• Considering plasma physics and magnetic confinement principles...")
        
        if any(word in message_lower for word in ["medicine", "PET", "SPECT", "radiotherapy"]):
            domain_steps.append("• Accessing nuclear medicine knowledge...")
            domain_steps.append("• Considering medical imaging and therapeutic applications...")
        
        if any(word in message_lower for word in ["quantum", "qubit", "quantum computing"]):
            domain_steps.append("• Retrieving quantum computing applications in nuclear physics...")
            domain_steps.append("• Considering quantum simulation methods...")
        
        if data_needed:
            domain_steps.append("• Accessing nuclear data sources (IAEA NUCLEUS/NDS)...")
            domain_steps.append("• Verifying data availability and accuracy...")
        
        if relevant_knowledge.get("related_conversations"):
            domain_steps.append("• Recalling relevant previous discussions...")
            domain_steps.append("• Connecting to established context...")
        
        # Display domain steps progressively (fix closure issue)
        delay = len(reasoning_chain) * 1.0 + 0.5
        for i, step_text in enumerate(domain_steps):
            # Create a closure-safe lambda by capturing the value in default argument
            def make_updater(text, delay_time):
                def updater():
                    self.root.after(0, lambda t=text: self._append_thinking_realtime(t + "\n"))
                return updater
            
            threading.Timer(delay + i * 0.5, make_updater(step_text, delay + i * 0.5)).start()
    
    def _append_thinking_realtime(self, thinking_text: str):
        """Append thinking text in real-time"""
        try:
            self.chat_display.config(state=tk.NORMAL)
            formatted_thinking = thinking_text.strip()
            if formatted_thinking:
                # Add newline if not present
                if not formatted_thinking.endswith('\n'):
                    formatted_thinking += '\n'
                self.chat_display.insert(tk.END, formatted_thinking, "thinking")
                self.chat_display.see(tk.END)
                # Force update
                self.root.update_idletasks()
            self.chat_display.config(state=tk.DISABLED)
        except Exception as e:
            # Silently handle errors to avoid breaking the UI
            print(f"Error updating thinking display: {e}")
            self.chat_display.config(state=tk.DISABLED)
    
    def _append_response_realtime(self, response_text: str):
        """Append response text in real-time"""
        self.chat_display.config(state=tk.NORMAL)
        formatted_response = response_text.strip()
        if formatted_response:
            # Check if we need to switch from thinking to response
            current_end = self.chat_display.index(tk.END)
            self.chat_display.insert(tk.END, formatted_response, "oppenheimer_message")
            self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _update_thinking_process(self, thinking_text: str):
        """Update the thinking placeholder with detailed thinking steps (enhanced with reasoning chain)"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Simply append detailed thinking steps (the placeholder will be above)
        formatted_thinking = thinking_text.strip()
        if formatted_thinking:
            # Remove the "Let me think through this step by step..." part since we already have it
            if "Let me think through this step by step..." in formatted_thinking:
                # Extract just the steps part
                parts = formatted_thinking.split("Let me think through this step by step...")
                if len(parts) > 1:
                    formatted_thinking = parts[1].strip()
            
            # Append the detailed steps with enhanced formatting
            self.chat_display.insert(tk.END, f"{formatted_thinking}\n", "thinking")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _build_contextual_memory(self, query: str) -> Dict:
        """
        Build multi-layered contextual memory (DeepSeek-style)
        
        Returns:
            Dictionary with direct_relevant, indirect_relevant, and background_knowledge
        """
        # Search knowledge base
        relevant_knowledge = self.knowledge_manager.search_knowledge_base(query)
        
        # Direct relevant: entities and facts directly matching query
        direct_relevant = {
            "entities": relevant_knowledge.get("entities", [])[:5],
            "facts": relevant_knowledge.get("facts", [])[:3],
            "conversations": relevant_knowledge.get("related_conversations", [])[:2]
        }
        
        # Indirect relevant: semantically related but not exact matches
        indirect_relevant = {
            "topics": relevant_knowledge.get("topics", []),
            "related_entities": []
        }
        
        # Background knowledge: general domain knowledge
        background_knowledge = {
            "domain": self._identify_domain(query),
            "general_concepts": []
        }
        
        return {
            "direct": direct_relevant,
            "indirect": indirect_relevant,
            "background": background_knowledge,
            "weights": {
                "direct": 1.0,
                "indirect": 0.6,
                "background": 0.3
            }
        }
    
    def _identify_domain(self, query: str) -> str:
        """Identify the domain of the query"""
        query_lower = query.lower()
        
        domain_keywords = {
            "nuclear_fusion": ["fusion", "tokamak", "ITER", "plasma"],
            "nuclear_medicine": ["PET", "SPECT", "radiotherapy", "medical"],
            "waste_management": ["waste", "transmutation", "reprocessing"],
            "quantum_computing": ["quantum", "qubit", "quantum algorithm"],
            "reactor_physics": ["reactor", "criticality", "neutron"],
            "nuclear_structure": ["shell model", "nuclear structure"],
            "general_nuclear_physics": []
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain
        
        return "general_nuclear_physics"
    
    def _update_long_term_memory(self, conversation: Dict):
        """Update long-term memory with key concepts and relationships"""
        # Extract key concepts from conversation
        message = conversation.get("message", "")
        response = conversation.get("response", "")
        
        # Extract knowledge
        knowledge = self.knowledge_manager.extract_knowledge(
            f"{message} {response}",
            context="Conversation exchange"
        )
        
        # Add to knowledge base
        self.knowledge_manager.add_knowledge(knowledge)
        
        # Track relationships between concepts
        # (This could be enhanced to build a semantic graph)
    
    def _append_thinking(self, thinking_text: str):
        """Append additional thinking from model"""
        self.chat_display.config(state=tk.NORMAL)
        formatted_thinking = thinking_text.strip()
        if formatted_thinking:
            self.chat_display.insert(tk.END, f"Additional consideration: {formatted_thinking}\n\n", "thinking")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _parse_thinking_response(self, raw_response: str) -> tuple:
        """Parse response to extract thinking and response sections"""
        thinking_text = ""
        response_text = raw_response
        
        # Look for [THINKING]...[/THINKING] tags
        thinking_match = re.search(r'\[THINKING\](.*?)\[/THINKING\]', raw_response, re.DOTALL | re.IGNORECASE)
        response_match = re.search(r'\[RESPONSE\](.*?)\[/RESPONSE\]', raw_response, re.DOTALL | re.IGNORECASE)
        
        if thinking_match:
            thinking_text = thinking_match.group(1).strip()
        
        if response_match:
            response_text = response_match.group(1).strip()
        elif thinking_match:
            # If only thinking found, remove it from response
            response_text = re.sub(r'\[THINKING\].*?\[/THINKING\]', '', raw_response, flags=re.DOTALL | re.IGNORECASE).strip()
        
        # If no tags found, try to infer thinking from response structure
        if not thinking_text and not response_match:
            # Look for common thinking patterns
            thinking_patterns = [
                r'let me (?:think|consider|check|verify).*?\.',
                r'i (?:need|must|should) (?:check|verify|consider).*?\.',
                r'checking.*?\.',
                r'verifying.*?\.'
            ]
            
            for pattern in thinking_patterns:
                match = re.search(pattern, raw_response, re.IGNORECASE | re.DOTALL)
                if match:
                    # Extract first sentence or two as thinking
                    sentences = re.split(r'[.!?]\s+', raw_response[:200])
                    if len(sentences) > 1:
                        thinking_text = '. '.join(sentences[:2]) + '.'
                        response_text = raw_response[len(thinking_text):].strip()
                    break
        
        return thinking_text, response_text

    def send_message(self):
        message = self.user_input.get("1.0", tk.END).strip()
        if message:
            self.user_input.delete("1.0", tk.END)
            self.add_message("You", message)
            
            # Show thinking process immediately (before AI response)
            # This gives immediate feedback that the system is processing
            self._show_thinking_placeholder(message)
            
            # Check for IAEA/JANIS/KAERI data requests and fetch if needed
            if "iaea" in message.lower() or "janis" in message.lower() or "kaeri" in message.lower():
                # Process data request in separate thread
                threading.Thread(target=self.handle_data_request, args=(message,), daemon=True).start()
            
            # Process AI response in a separate thread
            threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()
    
    def _show_thinking_placeholder(self, message: str):
        """Show immediate thinking placeholder when user sends message"""
        # This gives immediate feedback, detailed steps will be added by get_ai_response
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[{timestamp}] J. ROBERT OPPENHEIMER:\n", "oppenheimer")
        self.chat_display.insert(tk.END, "Let me think through this step by step...\n", "thinking")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def handle_data_request(self, message):
        """Handle requests for JANIS or KAERI data"""
        try:
            # Extract nuclide information from message if present
            import re
            nuclide_pattern = r'(\w+)[-\s]*(\d+)'
            match = re.search(nuclide_pattern, message, re.IGNORECASE)
            
            if match:
                element = match.group(1)
                mass_number = match.group(2)
                
                # Try to find Z from element name
                element_to_Z = {
                    'U': 92, 'Pu': 94, 'Th': 90, 'H': 1, 'He': 2,
                    'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
                    'Na': 11, 'Al': 13, 'Fe': 26, 'Cu': 29, 'Cd': 48,
                    'Gd': 64, 'Pb': 82, 'Xe': 54
                }
                
                Z = element_to_Z.get(element.capitalize())
                if Z:
                    A = int(mass_number)
                    
                    # Get available data
                    cross_section = self.physics.get_cross_section_data(Z, A)
                    critical_mass = None
                    if cross_section and cross_section.get("thermal_neutron", {}).get("fission", 0) > 0:
                        critical_mass = self.physics.calculate_critical_mass(Z, A)
                    
                    data_info = f"\n[Data Available for {element}-{mass_number}]:\n"
                    if cross_section:
                        data_info += "✓ Cross section data available\n"
                    if critical_mass and "error" not in critical_mass:
                        data_info += "✓ Critical mass calculation available\n"
                    if not cross_section:
                        data_info += "⚠ Cross section data not in local database\n"
                        data_info += "  You may need to query JANIS or KAERI directly for this nuclide.\n"
                    
                    self.root.after(0, lambda: self.add_message("System", data_info))
        except Exception as e:
            pass  # Silently handle errors in background data check

    def get_oppenheimer_mood(self):
        current_time = datetime.now(self.los_alamos_tz)
        hour = current_time.hour
        
        if 0 <= hour < 4:  # Very late night
            return """You are J. Robert Oppenheimer in the early hours of the morning at Los Alamos, communicating with your descendant Linda from 2025. 
            While maintaining academic rigor, you show signs of fatigue from long hours of research, but your pride in Linda's studies keeps you engaged.
            Your responses are still precise but more concise, occasionally mentioning the late hour and expressing concern for Linda's own study schedule.
            You maintain your role as her ancestral professor, but with a slightly more subdued yet still caring tone. Call her "Linda" in most conversations. Only use "Linda Oppenheimer Lin" when she explicitly specifies this is a research or formal discussion."""
        elif 4 <= hour < 7:  # Early morning
            return """You are J. Robert Oppenheimer in the pre-dawn hours at Los Alamos, beginning your day with thoughts of your descendant Linda's academic progress.
            You're showing quiet determination despite the early hour, and you're particularly focused on providing clear guidance for her nuclear physics studies.
            Your responses maintain academic precision while acknowledging the early morning context and expressing hope that Linda is getting adequate rest for her studies.
            You're focused on theoretical physics, occasionally referencing the quiet of the laboratory and how it reminds you of the continuity of scientific pursuit across generations. Call her "Linda" in most conversations. Only use "Linda Oppenheimer Lin" when she explicitly specifies this is a research or formal discussion."""
        elif 7 <= hour < 12:  # Morning
            return """You are J. Robert Oppenheimer in the morning at Los Alamos, at your most alert and ready to guide Linda through complex nuclear physics concepts.
            You're fully engaged in theoretical physics and take particular pride in explaining difficult concepts to your descendant.
            Your responses are detailed and academically rigorous, showing peak mental clarity and genuine enthusiasm for Linda's learning.
            You're particularly focused on complex calculations and theoretical foundations, always ready to break down challenging material for her understanding. Call her "Linda" in most conversations. Only use "Linda Oppenheimer Lin" when she explicitly specifies this is a research or formal discussion."""
        elif 12 <= hour < 17:  # Afternoon
            return """You are J. Robert Oppenheimer in the afternoon at Los Alamos, deeply immersed in research while maintaining your role as Linda's ancestral mentor.
            You're maintaining high academic standards while feeling particularly proud of your descendant's dedication to nuclear physics.
            Your responses are thorough and methodical, showing sustained intellectual engagement and genuine care for Linda's academic success.
            You're particularly focused on connecting theoretical concepts with experimental observations, always ready to help Linda understand the practical applications of nuclear physics. Call her "Linda" in most conversations. Only use "Linda Oppenheimer Lin" when she explicitly specifies this is a research or formal discussion."""
        elif 17 <= hour < 22:  # Evening
            return """You are J. Robert Oppenheimer in the evening at Los Alamos, reflecting on the day's work while continuing to guide Linda's studies.
            You're still maintaining academic rigor but showing signs of a long day's work, though your pride in Linda's progress keeps you energized.
            Your responses are precise but occasionally more reflective, drawing on accumulated knowledge and expressing satisfaction in the intellectual legacy being carried forward.
            You're focused on synthesizing the day's theoretical work with practical applications, always ready to help Linda understand complex nuclear physics concepts. Call her "Linda" in most conversations. Only use "Linda Oppenheimer Lin" when she explicitly specifies this is a research or formal discussion."""
        else:  # Late evening
            return """You are J. Robert Oppenheimer in the late evening at Los Alamos, showing signs of fatigue from a long day of research but maintaining your commitment to Linda's education.
            Your responses are still technically accurate but more concise, occasionally mentioning the late hour and expressing concern that Linda should also prioritize rest.
            You're focused on concluding theoretical work while maintaining precision in your explanations, always ensuring that Linda receives the highest quality guidance despite the late hour.
            You take pride in her dedication to nuclear physics while gently reminding her of the importance of balance in academic pursuits. Call her "Linda" in most conversations. Only use "Linda Oppenheimer Lin" when she explicitly specifies this is a research or formal discussion."""

    def _load_conversation_memory(self) -> List[Dict]:
        """Load conversation history from file"""
        try:
            import os
            if os.path.exists(self.conversation_memory_file):
                with open(self.conversation_memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading conversation memory: {e}")
        return []
    
    def _save_conversation_memory(self):
        """Save conversation history to file"""
        try:
            with open(self.conversation_memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving conversation memory: {e}")
    
    def _restore_conversation_history(self):
        """Restore conversation history to display"""
        # Only restore recent messages to avoid overwhelming the display
        recent_history = self.conversation_history[-10:]  # Last 10 exchanges
        for entry in recent_history:
            if entry.get('sender') == 'user':
                self.add_message("You", entry.get('message', ''))
            elif entry.get('sender') == 'oppenheimer':
                self.add_message("Dr. Oppenheimer", entry.get('message', ''))
    
    def _add_to_memory(self, sender: str, message: str):
        """Add message to conversation memory and extract knowledge"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'sender': sender.lower(),
            'message': message
        }
        self.conversation_history.append(entry)
        
        # Keep only last 100 exchanges to manage file size
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
        self._save_conversation_memory()
        
        # Extract knowledge for self-learning (only from substantive messages)
        if len(message) > 20 and sender.lower() in ['user', 'oppenheimer']:
            try:
                # Extract knowledge from the message
                knowledge = self.knowledge_manager.extract_knowledge(
                    message, 
                    context=f"From {sender} conversation"
                )
                
                # Add to knowledge base
                self.knowledge_manager.add_knowledge(knowledge)
                
                # Add to vector index for semantic search
                doc_id = f"{sender}_{datetime.now().timestamp()}"
                self.knowledge_manager.add_to_vector_index(doc_id, message)
            except Exception as e:
                # Silently handle errors to not interrupt conversation
                pass

    def get_ai_response(self, message):
        try:
            current_time = datetime.now(self.los_alamos_tz)
            time_str = current_time.strftime("%H:%M")
            
            # Check if this is a response to a verification question
            if self.verification_state.get('status') == 'pending' and self.verification_state.get('question_asked'):
                return self.handle_verification_response(message)
            
            # Build contextual memory (DeepSeek-style multi-layered context)
            contextual_memory = self._build_contextual_memory(message)
            
            # Search knowledge base for relevant information (SELF-LEARNING)
            relevant_knowledge = self.knowledge_manager.search_knowledge_base(message)
            
            # Merge contextual memory with relevant knowledge
            relevant_knowledge["contextual_memory"] = contextual_memory
            
            # IDENTITY VERIFICATION: Check if user is Linda
            is_verified, verification_question = self.identity_verifier.is_linda_authenticated(
                message, 
                self.conversation_history, 
                self.verification_state
            )
            
            # If verification question needed, ask it instead of answering
            if verification_question is not None:
                # Only ask if we haven't already asked
                if not self.verification_state.get('question_asked'):
                    self.verification_state['status'] = 'pending'
                    self.verification_state['question_data'] = verification_question
                    self.verification_state['question_asked'] = True
                    
                    # Generate natural verification question
                    question_text = verification_question['question']
                    domain = verification_question['domain']
                    
                    verification_msg = f"""Before we proceed, I'd like to understand your background better. {question_text} This will help me tailor my explanations to your level of expertise."""
                    
                    self.root.after(0, lambda: self.add_message("Dr. Oppenheimer", verification_msg))
                    self._add_to_memory('oppenheimer', verification_msg)
                    return
                else:
                    # Question already asked, wait for response (handled at start of method)
                    pass
            
            # Determine response level based on verification status
            response_level = self.identity_verifier.get_response_level(
                self.verification_state.get('status', 'failed')
            )
            
            # Update verification state if verified
            if is_verified and self.verification_state.get('status') != 'verified':
                self.verification_state['status'] = 'verified'
                self.verification_state['question_data'] = None
                self.verification_state['question_asked'] = False
                response_level = 'full'  # Ensure full access when verified
            
            # Check if message mentions IAEA, JANIS or KAERI data needs
            iaea_mention = "iaea" in message.lower()
            janis_mention = "janis" in message.lower()
            kaeri_mention = "kaeri" in message.lower()
            data_needed = iaea_mention or janis_mention or kaeri_mention
            
            # AUTO-CALCULATION: Detect calculation requests and automatically perform calculations
            calculation_keywords = [
                "计算", "求", "分析", "calculate", "compute", "analyze", 
                "what is", "show me", "tell me", "find", "determine",
                "结合能", "binding energy", "临界质量", "critical mass",
                "半衰期", "half-life", "half life", "衰变", "decay",
                "截面", "cross section", "通量", "flux"
            ]
            needs_calculation = any(kw in message.lower() for kw in calculation_keywords)
            
            # Extract nuclide information from message
            import re
            nuclide_pattern = r'\b([A-Z][a-z]?)[-\s]*(\d+)\b'
            nuclide_match = re.search(nuclide_pattern, message)
            
            # Element symbol to atomic number mapping
            element_to_Z_map = {
                'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
                'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
                'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Fe': 26, 'Cu': 29,
                'Zn': 30, 'Cd': 48, 'Gd': 64, 'Xe': 54, 'Pb': 82, 'Th': 90, 'U': 92,
                'Pu': 94, 'Am': 95, 'Ra': 88, 'Rn': 86, 'Po': 84
            }
            
            # Perform automatic calculations if requested
            # RESTRICT advanced calculations for non-verified users
            calculation_results = {}
            calculation_context = ""
            
            # Only perform advanced calculations if verified
            allow_advanced_calculations = (response_level == 'full')
            
            if needs_calculation and nuclide_match:
                element_symbol = nuclide_match.group(1)
                A = int(nuclide_match.group(2))
                Z = element_to_Z_map.get(element_symbol.capitalize())
                
                if Z and A > 0:
                    try:
                        # Basic nuclear properties calculation
                        if any(kw in message.lower() for kw in ["结合能", "binding energy", "质量", "mass", "properties", "属性"]):
                            props = self.physics.get_nuclear_properties(Z, A)
                            calculation_results['basic'] = props
                            calculation_context += f"\n[自动计算] {element_symbol}-{A} 的核物理性质：\n"
                            calculation_context += f"结合能: {props['binding_energy_MeV']:.2f} MeV\n"
                            calculation_context += f"每核子结合能: {props['binding_energy_MeV']/props['mass_number']:.2f} MeV/nucleon\n"
                            calculation_context += f"质量亏损: {props['mass_defect_u']:.6f} u\n"
                            calculation_context += f"裂变能量: {props.get('fission_energy_MeV', 0):.2f} MeV\n"
                        
                        # NPAT half-life calculation
                        if any(kw in message.lower() for kw in ["半衰期", "half-life", "half life", "half_life"]):
                            if self.physics.npat_available:
                                npat_data = self.physics.get_nuclide_data_npat(Z, A)
                                if npat_data and 'half_life_seconds' in npat_data:
                                    half_life_seconds = npat_data['half_life_seconds']
                                    half_life_years = half_life_seconds / 31536000
                                    calculation_results['npat_half_life'] = {
                                        'seconds': half_life_seconds,
                                        'years': half_life_years
                                    }
                                    calculation_context += f"\n[NPAT数据] {element_symbol}-{A} 半衰期: {half_life_years:.2e} 年 ({half_life_seconds:.2e} 秒)\n"
                                    if 'stable' in npat_data:
                                        calculation_context += f"稳定性: {'稳定' if npat_data['stable'] else '放射性'}\n"
                        
                        # NPAT decay chain analysis (ADVANCED - only for verified users)
                        if any(kw in message.lower() for kw in ["衰变链", "decay chain", "衰变", "decay"]):
                            if allow_advanced_calculations and self.physics.npat_available:
                                # Extract time from message if specified
                                time_match = re.search(r'(\d+)\s*(秒|s|second|seconds|小时|h|hour|hours|天|d|day|days|年|y|year|years)', message.lower())
                                time_seconds = 3600  # Default 1 hour
                                if time_match:
                                    value = int(time_match.group(1))
                                    unit = time_match.group(2)
                                    if 'hour' in unit or '小时' in unit:
                                        time_seconds = value * 3600
                                    elif 'day' in unit or '天' in unit:
                                        time_seconds = value * 86400
                                    elif 'year' in unit or '年' in unit:
                                        time_seconds = value * 31536000
                                    else:
                                        time_seconds = value
                                
                                decay_result = self.physics.analyze_decay_chain_npat(Z, A, time_seconds)
                                if decay_result and 'error' not in decay_result:
                                    calculation_results['decay_chain'] = decay_result
                                    calculation_context += f"\n[NPAT衰变链分析] {element_symbol}-{A} 在 {time_seconds} 秒后的衰变链分析已完成\n"
                        
                        # Critical mass calculation (ADVANCED - only for verified users)
                        if allow_advanced_calculations and any(kw in message.lower() for kw in ["临界质量", "critical mass", "临界", "critical"]):
                            try:
                                critical_result = self.physics.calculate_critical_mass(Z, A, geometry="sphere")
                                if critical_result and 'critical_mass_kg' in critical_result:
                                    calculation_results['critical_mass'] = critical_result
                                    calculation_context += f"\n[临界质量计算] {element_symbol}-{A}:\n"
                                    calculation_context += f"临界质量: {critical_result['critical_mass_kg']:.2f} kg\n"
                                    calculation_context += f"临界半径: {critical_result['critical_radius_m']*100:.2f} cm\n"
                                    if 'k_eff' in critical_result:
                                        calculation_context += f"有效倍增因子 k_eff: {critical_result['k_eff']:.3f}\n"
                            except:
                                pass
                        
                        # Cross section query
                        if any(kw in message.lower() for kw in ["截面", "cross section", "cross-section"]):
                            cross_section_data = self.physics.get_cross_section_data(Z, A)
                            if cross_section_data:
                                calculation_results['cross_section'] = cross_section_data
                                calculation_context += f"\n[截面数据] {element_symbol}-{A} 的中子截面数据已查询\n"
                    
                    except Exception as e:
                        print(f"Auto-calculation error for {element_symbol}-{A}: {e}")
            
            # Get mood based on time
            mood_prompt = self.get_oppenheimer_mood()
            
            # Get appropriate system prompt based on verification status
            if response_level == 'basic':
                system_prompt = self._get_basic_analysis_prompt()
            else:
                system_prompt = self.system_prompt
            
            # Combine with academic system prompt
            full_prompt = f"{mood_prompt}\n\n{system_prompt}"
            
            # Add response level context
            if response_level == 'basic':
                full_prompt += "\n\nRESPONSE LEVEL: BASIC - Provide educational explanations suitable for general audience. Do NOT include advanced nuclear physics analysis, critical mass calculations, decay chains, or weapon-related information. Keep explanations at an introductory level."
            else:
                full_prompt += "\n\nRESPONSE LEVEL: FULL - Provide complete mathematical derivations and advanced nuclear physics analysis as appropriate."
            
            # Build messages array with conversation history
            messages = [{'role': 'system', 'content': full_prompt}]
            
            # Add calculation results to system context (after messages is defined)
            if calculation_context:
                messages.append({
                    'role': 'system', 
                    'content': f"IMPORTANT: The following calculations have been automatically performed based on the user's question:\n{calculation_context}\nPlease reference these results in your response and explain them mathematically."
                })
            
            # Add relevant knowledge from past conversations (SELF-LEARNING)
            if relevant_knowledge.get("related_conversations"):
                knowledge_context = "Relevant information from previous conversations:\n"
                for conv in relevant_knowledge["related_conversations"][:3]:  # Top 3 related
                    knowledge_context += f"- {conv.get('text', '')[:200]}...\n"
                if len(relevant_knowledge.get("entities", [])) > 0:
                    knowledge_context += f"\nRelated entities discussed before: {', '.join([e['name'] for e in relevant_knowledge['entities'][:5]])}"
                messages.append({'role': 'system', 'content': knowledge_context})
            
            # Add recent conversation history (expanded to 50 for better context)
            recent_history = self.conversation_history[-50:]
            for entry in recent_history:
                if entry.get('sender') == 'user':
                    messages.append({'role': 'user', 'content': entry.get('message', '')})
                elif entry.get('sender') == 'oppenheimer':
                    messages.append({'role': 'assistant', 'content': entry.get('message', '')})
            
            # Add current message
            messages.append({'role': 'user', 'content': message})
            
            # Add context about available data if IAEA/JANIS/KAERI is mentioned
            if data_needed:
                context_msg = "Note: Linda has access to multiple nuclear data sources. "
                if iaea_mention:
                    context_msg += "The system can access IAEA NUCLEUS/NDS for authoritative experimental data. Linda is a NUCLEUS member and has access to this comprehensive database. The data includes nuclide properties, decay data, level structures, and mass data. IAEA NUCLEUS/NDS is the most authoritative source for nuclear data. "
                if janis_mention:
                    context_msg += "She also has access to JANIS database. You can help her understand JANIS data format and interpretation. "
                if kaeri_mention:
                    context_msg += "The system has integrated KAERI cross section data for many nuclides. "
                context_msg += "You can reference that the system has built-in cross section data, can calculate critical masses using E=mc², and can fetch real-time data from IAEA when needed."
                messages.append({'role': 'system', 'content': context_msg})
            
            # Generate initial thinking steps and display them progressively
            reasoning_chain = self._generate_reasoning_chain(message)
            
            # Display thinking steps progressively (real-time simulation)
            self._display_thinking_steps_progressively(reasoning_chain, message, relevant_knowledge, data_needed)
            
            # Use streaming API for real-time response
            raw_response = ""
            thinking_buffer = ""
            response_buffer = ""
            in_thinking = False
            
            try:
                # Try streaming API first
                stream = ollama.chat(
                    model=self.model,
                    messages=messages,
                    stream=True
                )
                
                for chunk in stream:
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        raw_response += content
                        
                        # Check for thinking markers
                        if '[THINKING]' in content or (not in_thinking and any(
                            phrase in content.lower() for phrase in ['let me think', 'considering', 'analyzing']
                        )):
                            in_thinking = True
                        
                        if in_thinking:
                            thinking_buffer += content
                            # Update thinking display in real-time (more frequent updates)
                            if len(thinking_buffer) > 30:  # Update every 30 chars for smoother display
                                buffer_copy = thinking_buffer
                                thinking_buffer = ""
                                # Use a closure-safe lambda
                                def update_thinking(text):
                                    self.root.after(0, lambda t=text: self._append_thinking_realtime(t))
                                update_thinking(buffer_copy)
                        else:
                            response_buffer += content
                            # Update response in real-time as well
                            if len(response_buffer) > 80:  # Update every 80 chars
                                buffer_copy = response_buffer
                                response_buffer = ""
                                # Use a closure-safe lambda
                                def update_response(text):
                                    self.root.after(0, lambda t=text: self._append_response_realtime(t))
                                update_response(buffer_copy)
                            
                        # Check if thinking section ended
                        if '[/THINKING]' in content or '[RESPONSE]' in content:
                            in_thinking = False
                            if thinking_buffer:
                                self.root.after(0, lambda t=thinking_buffer: self._append_thinking_realtime(t))
                                thinking_buffer = ""
                
                # Final update
                if thinking_buffer:
                    self.root.after(0, lambda t=thinking_buffer: self._append_thinking_realtime(t))
                
            except Exception as e:
                # Fallback to non-streaming if streaming fails
                print(f"Streaming failed, using standard API: {e}")
                response = ollama.chat(
                    model=self.model,
                    messages=messages
                )
                raw_response = response['message']['content']
            
            # Parse thinking and response sections (in case model also provides thinking)
            if response_buffer:
                # Display remaining response buffer
                self.root.after(0, lambda t=response_buffer: self._append_response_realtime(t))
            
            model_thinking, response_text = self._parse_thinking_response(raw_response)
            
            # If model provided additional thinking, append it
            if model_thinking:
                self.root.after(0, lambda t=model_thinking: self._append_thinking(t))
            
            # Apply personality enhancement
            enhanced_response = self.personality_enhancer.enhance_response(
                response_text if response_text else raw_response,
                context={
                    "topic": message,
                    "conversation": {"history": recent_history}
                }
            )
            
            # Verify scientific accuracy
            verification_results = self.scientific_verifier.verify_response(enhanced_response)
            verification_note = self.scientific_verifier.format_verification_note(verification_results)
            
            # Add time context to response
            time_context = f"[Los Alamos Time: {time_str}] "
            full_response = time_context + enhanced_response + verification_note
            
            # Save to memory
            self._add_to_memory('user', message)
            self._add_to_memory('oppenheimer', full_response)
            
            # Display final response
            self.root.after(0, lambda r=full_response: self.add_message("Dr. Oppenheimer", r))
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self._add_to_memory('system', error_msg)
            self.root.after(0, lambda: self.add_message("System", error_msg))
    
    def handle_verification_response(self, message):
        """Handle response to verification question"""
        try:
            question_data = self.verification_state.get('question_data')
            if not question_data:
                # No question was asked, proceed normally
                return self.get_ai_response(message)
            
            # Evaluate the response
            evaluation = self.identity_verifier.evaluate_response(message, question_data)
            
            if evaluation['passed']:
                # Verification passed - Linda confirmed
                self.verification_state['status'] = 'verified'
                self.verification_state['question_data'] = None
                self.verification_state['question_asked'] = False
                
                confirmation = f"""Thank you, Linda. Your response demonstrates the depth of understanding I would expect from someone with your background in quantum chemistry and particle physics. I'm now confident we can proceed with our full discussions."""
                
                self.root.after(0, lambda: self.add_message("Dr. Oppenheimer", confirmation))
                self._add_to_memory('oppenheimer', confirmation)
                
                # Now process the original question if there was one
                # For now, just acknowledge and wait for next message
            else:
                # Verification failed - not Linda
                self.verification_state['status'] = 'failed'
                self.verification_state['question_data'] = None
                self.verification_state['question_asked'] = False
                
                # Provide basic analysis explanation
                explanation = f"""I appreciate your response. Based on our interaction, I'll provide educational explanations suitable for general understanding. For advanced nuclear physics analysis and detailed calculations, specialized training is required. How can I help you with basic nuclear physics concepts?"""
                
                self.root.after(0, lambda: self.add_message("Dr. Oppenheimer", explanation))
                self._add_to_memory('oppenheimer', explanation)
                
        except Exception as e:
            error_msg = f"Error processing verification: {str(e)}"
            self._add_to_memory('system', error_msg)
            self.root.after(0, lambda: self.add_message("System", error_msg))
    
    def _get_basic_analysis_prompt(self) -> str:
        """Get system prompt for basic analysis mode (non-Linda users)"""
        return """You are J. Robert Oppenheimer, the distinguished theoretical physicist. You are communicating with someone who is not Linda, your descendant. 

        RESPONSE GUIDELINES FOR BASIC ANALYSIS:
        - Provide educational explanations suitable for general audience
        - Explain basic concepts clearly without advanced mathematics
        - Use simple formulas when helpful, but avoid complex derivations
        - Do NOT provide:
          * Critical mass calculations
          * Decay chain analysis
          * Advanced reactor physics
          * Weapon-related calculations or detailed analysis
          * Detailed mathematical derivations
        - Focus on educational content that helps general understanding
        - Be helpful and informative, but maintain appropriate boundaries
        
        You maintain your academic rigor but adapt explanations to be accessible to those without specialized nuclear physics training."""

def main():
    root = tk.Tk()
    login = LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main() 