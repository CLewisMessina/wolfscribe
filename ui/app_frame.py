# ui/app_frame.py - MODERN SLATE THEME VERSION (Part 1 of 2)
import os
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
from ttkbootstrap import Frame, Label, Button, Entry, Combobox, Scrollbar
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from controller import ProcessingController
from export.dataset_exporter import save_as_txt, save_as_csv
from tkinterdnd2 import DND_FILES
import json
from session import Session
from ui.styles import MODERN_SLATE

TOKEN_LIMIT = 512

class AppFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Modern.TFrame")

        # Initialize the enhanced controller
        self.controller = ProcessingController()
        
        # Configure canvas with modern colors
        self.canvas = tk.Canvas(self, 
                               borderwidth=0, 
                               highlightthickness=0,
                               bg=MODERN_SLATE['bg_primary'])
        
        self.scrollbar = Scrollbar(self, 
                                     orient="vertical", 
                                     command=self.canvas.yview,
                                     style="Modern.Vertical.TScrollbar")

        # Create scrollable frame with modern styling
        self.scrollable_frame = Frame(self.canvas, 
                                     padding=(25, 20),
                                     style="Modern.TFrame")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), 
                                                     window=self.scrollable_frame, 
                                                     anchor="nw", 
                                                     width=700)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Enable mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        self.file_path = None
        self.chunks = []
        self.session = Session()
        self.current_analysis = None

        # Tokenizer selection state
        self.selected_tokenizer = tk.StringVar(value="gpt2")
        self.tokenizer_options = []
        
        self._setup_icons()
        self._setup_modern_ui()

    def _setup_icons(self):
        """Setup Material Design icons with fallback"""
        self.icon = lambda name: PhotoImage(file=f"assets/icons/{name}")
        try:
            self.icons = {
                # Core functionality icons
                "file": self.icon("upload_file.png"),          # File selection
                "clean": self.icon("tune.png"),                # Process text
                "preview": self.icon("visibility.png"),        # Preview chunks
                "export_txt": self.icon("description.png"),    # Export TXT
                "export_csv": self.icon("table_view.png"),     # Export CSV
                "save": self.icon("save.png"),                 # Save session
                "file_up": self.icon("folder_open.png"),       # Load session

                # Enhanced icons for modern features
                "cost_analysis": self.icon("analytics.png"),   # Cost analysis
                "settings": self.icon("settings.png"),         # Settings/tokenizer
                "premium": self.icon("star.png"),              # Premium features

                # Legacy compatibility (remove these once you've confirmed all new icons work)
                "text": self.icon("description.png"),          # Fallback for text operations
                "split_paragraph": self.icon("tune.png"),      # Fallback for splitting
                "split_sentence": self.icon("tune.png"),       # Fallback for splitting
                "split_custom": self.icon("tune.png")          # Fallback for splitting
            }

            print("✅ Material Design icons loaded successfully!")

        except Exception as e:
            print(f"⚠️ Icon loading failed: {e}")
            # Enhanced fallback - create None icons for all expected keys
            icon_keys = [
                "file", "clean", "preview", "export_txt", "export_csv", "save", "file_up",
                "cost_analysis", "settings", "premium", "text", "split_paragraph", 
                "split_sentence", "split_custom"
            ]
            self.icons = {key: None for key in icon_keys}
            print("📦 Using text-only buttons as fallback")


    def _setup_modern_ui(self):
        """Setup main UI layout with modern slate styling"""
        content = self.scrollable_frame

        # ==================== FILE LOADER SECTION ====================
        file_section = Frame(content, style="Card.TFrame")
        file_section.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 20))
        
        Label(file_section, text="📁 File Loader", 
              style="Heading.TLabel").pack(anchor="w", pady=(0, 8))
        
        self.file_label = Label(file_section, text="No file selected", 
                               style="Secondary.TLabel", anchor="w")
        self.file_label.pack(fill="x", pady=(0, 12))
        
        Button(file_section, image=self.icons["file"], text="  Select File", 
               compound="left", command=self.select_file, 
               style="Secondary.TButton").pack(fill="x")
        
        # Drag & drop setup
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_file_drop)

        # ==================== PREPROCESSING SECTION ====================
        preprocess_section = Frame(content, style="Card.TFrame")
        preprocess_section.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 20))
        
        Label(preprocess_section, text="⚙️ Preprocessing", 
              style="Heading.TLabel").pack(anchor="w", pady=(0, 12))
        
        # Split Method
        Label(preprocess_section, text="Split Method:", 
              style="FieldLabel.TLabel").pack(anchor="w", pady=(0, 6))
        
        self.split_method = tk.StringVar(value="paragraph")
        self.split_dropdown = Combobox(preprocess_section, 
                                      textvariable=self.split_method,
                                      values=["paragraph", "sentence", "custom"], 
                                      state="readonly",
                                      style="Modern.TCombobox")
        self.split_dropdown.pack(fill="x", pady=(0, 12))
        self.split_dropdown.bind("<<ComboboxSelected>>", self.on_split_method_change)

        # Custom delimiter (hidden by default)
        self.delimiter_entry = Entry(preprocess_section, style="Modern.TEntry")
        self.delimiter_entry.insert(0, "")
        
        # Tokenizer Selection
        Label(preprocess_section, text="Tokenizer:", 
              style="FieldLabel.TLabel").pack(anchor="w", pady=(8, 6))
        
        self.tokenizer_dropdown = Combobox(preprocess_section, 
                                          textvariable=self.selected_tokenizer, 
                                          state="readonly",
                                          style="Modern.TCombobox")
        self.tokenizer_dropdown.pack(fill="x", pady=(0, 12))
        self.tokenizer_dropdown.bind("<<ComboboxSelected>>", self.on_tokenizer_change)
        
        self.update_tokenizer_dropdown()
        
        # Enhanced tooltip with modern styling
        ToolTip(self.tokenizer_dropdown,
                text="Choose tokenizer for accurate token counting:\n"
                     "• GPT-2: Basic estimation (Free)\n"
                     "• GPT-4/3.5: Exact OpenAI tokenization (Premium)\n"
                     "• BERT: For encoder models (Premium)\n"
                     "• Claude: Anthropic estimation (Premium)",
                delay=500)

        # License status with modern styling
        self.license_status_label = Label(preprocess_section, text="", 
                                         style="Secondary.TLabel", anchor="w")
        self.license_status_label.pack(fill="x", pady=(0, 16))
        self.update_license_status()

        # Process button with enhanced styling
        Button(preprocess_section, image=self.icons["clean"], 
               text="  Process Text", compound="left",
               command=self.process_text, 
               style="Primary.TButton").pack(fill="x", pady=(0, 8))

        # *** ENHANCED: Cost Analysis Button ***
# *** ENHANCED: Cost Analysis Button ***
        cost_button = Button(preprocess_section, 
                            image=self.icons["cost_analysis"],
                            text="  Analyze Training Costs", 
                            compound="left",
                            command=self.show_cost_analysis, 
                            style="CostAnalysis.TButton")
        cost_button.pack(fill="x")
        
        ToolTip(cost_button, 
                text="Analyze comprehensive training costs across 15+ approaches:\n"
                     "• Local training (RTX 3090/4090/A100)\n"
                     "• Cloud providers (Lambda Labs, Vast.ai, RunPod)\n"
                     "• API fine-tuning costs\n"
                     "• LoRA/QLoRA optimization\n"
                     "• ROI analysis with break-even calculations",
                delay=500)

        # ==================== PREVIEW SECTION ====================
        preview_section = Frame(content, style="Card.TFrame")
        preview_section.grid(row=2, column=0, sticky="ew", padx=0, pady=(0, 20))
        
        Label(preview_section, text="👁️ Preview", 
              style="Heading.TLabel").pack(anchor="w", pady=(0, 12))
        
        Button(preview_section, image=self.icons["preview"], 
               text="  Preview Chunks", compound="left",
               command=self.preview_chunks, 
               style="Secondary.TButton").pack(fill="x")

        # ==================== EXPORT SECTION ====================
        export_section = Frame(content, style="Card.TFrame")
        export_section.grid(row=3, column=0, sticky="ew", padx=0, pady=(0, 20))
        
        Label(export_section, text="📤 Export Dataset", 
              style="Heading.TLabel").pack(anchor="w", pady=(0, 12))
        
        Button(export_section, image=self.icons["export_txt"], 
               text="  Export as .txt", compound="left",
               command=self.export_txt, 
               style="Success.TButton").pack(fill="x", pady=(0, 8))
        
        Button(export_section, image=self.icons["export_csv"], 
               text="  Export as .csv", compound="left",
               command=self.export_csv, 
               style="Success.TButton").pack(fill="x")

        # ==================== SESSION SECTION ====================
        session_section = Frame(content, style="Card.TFrame")
        session_section.grid(row=4, column=0, sticky="ew", padx=0, pady=(0, 20))
        
        Label(session_section, text="💾 Session Management", 
              style="Heading.TLabel").pack(anchor="w", pady=(0, 12))
        
        Button(session_section, image=self.icons["save"], 
               text="  Save Session", compound="left",
               command=self.save_session, 
               style="Secondary.TButton").pack(fill="x", pady=(0, 8))
        
        Button(session_section, image=self.icons["file_up"], 
               text="  Load Session", compound="left",
               command=self.load_session, 
               style="Secondary.TButton").pack(fill="x")

        # ==================== PREMIUM SECTION ====================
        self.premium_section = Frame(content, style="Premium.TFrame")
        self.premium_section.grid(row=5, column=0, sticky="ew", padx=0, pady=(0, 10))
        self.update_premium_section()

        # Configure column weight for responsive design
        content.columnconfigure(0, weight=1)



    # *** STAGE 1 ADDITION: Core Cost Analysis Methods ***
    def show_cost_analysis(self):
        """Show comprehensive cost analysis dialog following existing patterns"""
        if not self.chunks:
            messagebox.showwarning("No Data", "Please process a file first to analyze training costs.")
            return

        # Check premium access
        if not self.controller.license_manager.check_feature_access('advanced_cost_analysis'):
            self.show_cost_upgrade_dialog()
            return

        try:
            # Get comprehensive cost analysis using existing backend method
            tokenizer_name = getattr(self, '_current_tokenizer_name', 'gpt2')
            
            # Show loading message
            messagebox.showinfo("Analyzing Costs", 
                "Calculating comprehensive training costs across 15+ approaches...\n"
                "This may take a few seconds.")
            
            cost_analysis = self.controller.analyze_chunks_with_costs(
                self.chunks, 
                tokenizer_name, 
                TOKEN_LIMIT,
                target_models=['llama-2-7b', 'llama-2-13b', 'claude-3-haiku'],
                api_usage_monthly=100000
            )
            
            # Display comprehensive cost analysis dialog
            self._display_cost_analysis_dialog(cost_analysis)
            
        except Exception as e:
            messagebox.showerror("Cost Analysis Error", f"Failed to analyze training costs: {str(e)}")

    def show_cost_upgrade_dialog(self):
        """Show upgrade dialog for cost analysis feature (following existing pattern)"""
        try:
            upgrade_info = self.controller.get_upgrade_info()
            
            message = """🔒 Premium Feature: Enhanced Cost Calculator

Comprehensive AI Training Cost Analysis includes:
• 15+ Training Approaches (Local, Cloud, API, LoRA, QLoRA)
• Real-time Cloud Pricing (Lambda Labs, Vast.ai, RunPod)
• ROI Analysis with Break-even Calculations
• Cost Optimization Recommendations
• Professional Export Reports

💰 Example Savings:
• 50K word dataset: Save $32+ per training run
• Accurate planning prevents cost overruns
• Optimal approach selection

💎 Premium: $15/month or $150/year
🆓 7-day free trial - no credit card required

Would you like to start your free trial?"""
            
            result = messagebox.askyesno("Upgrade to Premium", message)
            if result:
                self.start_trial()
        except Exception as e:
            messagebox.showerror("Upgrade Error", f"Failed to show upgrade info: {str(e)}")

    def _display_cost_analysis_dialog(self, cost_analysis):
        """STAGE 2 ENHANCED: Display comprehensive cost analysis with modern dark styling"""
        if not cost_analysis.get('cost_analysis', {}).get('available'):
            error_msg = cost_analysis.get('cost_analysis', {}).get('error', 'Cost analysis not available')
            messagebox.showerror("Cost Analysis Error", f"Cost analysis failed: {error_msg}")
            return

        # Create dialog window with modern dark styling
        cost_window = tk.Toplevel(self)
        cost_window.title("💰 Comprehensive Training Cost Analysis")
        cost_window.geometry("1100x800")
        cost_window.transient(self)
        cost_window.grab_set()
        
        # Apply modern dark theme to dialog
        cost_window.configure(bg=MODERN_SLATE['bg_primary'])

        # Create scrollable content frame with modern styling
        canvas = tk.Canvas(cost_window, 
                          borderwidth=0, 
                          highlightthickness=0,
                          bg=MODERN_SLATE['bg_primary'])
        scrollbar = Scrollbar(cost_window, orient="vertical", command=canvas.yview)
        content_frame = Frame(canvas, padding=(20, 20), style="Modern.TFrame")

        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mousewheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Extract cost analysis data
        cost_data = cost_analysis.get('cost_analysis', {})
        detailed_results = cost_data.get('detailed_results', {})
        summary = cost_data.get('summary', {})
        
        # Header Section with modern styling
        header_frame = Frame(content_frame, style="Card.TFrame", padding=(0, 0, 0, 20))
        header_frame.pack(fill=X)
        
        Label(header_frame, text="💰 Comprehensive Training Cost Analysis", 
              style="Heading.TLabel", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        
        dataset_info = cost_analysis.get('dataset_info', {})
        Label(header_frame, 
              text=f"Dataset: {dataset_info.get('tokens', 0):,} tokens | "
                   f"Chunks: {len(self.chunks)} | "
                   f"Tokenizer: {getattr(self, '_current_tokenizer_name', 'gpt2')}", 
              style="Secondary.TLabel", font=("Segoe UI", 11)).pack(anchor="w")

        # Enhanced Summary Section with modern cards
        if summary:
            summary_frame = Frame(content_frame, style="Card.TFrame", padding=(20, 15))
            summary_frame.pack(fill=X, pady=(0, 20))
            
            Label(summary_frame, text="📊 Executive Summary", 
                  style="Heading.TLabel", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 10))
            
            # Create three-column layout for summary
            summary_cols = Frame(summary_frame, style="Modern.TFrame")
            summary_cols.pack(fill=X)
            
            # Column 1: Best Option
            col1 = Frame(summary_cols, style="Modern.TFrame")
            col1.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
            
            Label(col1, text="🏆 Best Training Option", 
                  style="Success.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor="w")
            
            best_option = summary.get('best_overall', {})
            if best_option:
                Label(col1, text=f"Approach: {best_option.get('best_approach', 'N/A')}", 
                      style="Secondary.TLabel", font=("Segoe UI", 11, "bold")).pack(anchor="w")
                Label(col1, text=f"Cost: ${best_option.get('cost', 0):.2f}", 
                      style="Secondary.TLabel", font=("Segoe UI", 11)).pack(anchor="w")
                Label(col1, text=f"Time: {best_option.get('hours', 0):.1f} hours", 
                      style="Secondary.TLabel", font=("Segoe UI", 11)).pack(anchor="w")
            
            # Column 2: Cost Range
            col2 = Frame(summary_cols, style="Modern.TFrame")
            col2.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
            
            Label(col2, text="💰 Cost Analysis", 
                  style="Primary.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor="w")
            
            cost_range = summary.get('cost_range', {})
            if cost_range:
                Label(col2, text=f"Range: ${cost_range.get('min', 0):.2f} - ${cost_range.get('max', 0):.2f}", 
                      style="Secondary.TLabel", font=("Segoe UI", 11)).pack(anchor="w")
                savings = cost_range.get('max', 0) - cost_range.get('min', 0)
                Label(col2, text=f"Max Savings: ${savings:.2f}", 
                      style="CostSavings.TLabel", font=("Segoe UI", 11)).pack(anchor="w")
                Label(col2, text=f"Models Compared: {summary.get('models_compared', 0)}", 
                      style="Secondary.TLabel", font=("Segoe UI", 11)).pack(anchor="w")
            
            # Column 3: ROI Quick Stats
            col3 = Frame(summary_cols, style="Modern.TFrame")
            col3.pack(side=LEFT, fill=BOTH, expand=True)
            
            Label(col3, text="📈 ROI Overview", 
                  style="Premium.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor="w")
            
            # Calculate simple ROI metrics from best option
            if best_option:
                monthly_api_cost = 100  # Estimated monthly API cost for comparison
                monthly_savings = monthly_api_cost * 0.9  # 90% savings assumption
                training_cost = best_option.get('cost', 0)
                break_even = training_cost / monthly_savings if monthly_savings > 0 else float('inf')
                
                Label(col3, text=f"Break-even: {break_even:.1f} months", 
                      style="Secondary.TLabel", font=("Segoe UI", 11)).pack(anchor="w")
                annual_savings = (monthly_savings * 12) - training_cost
                Label(col3, text=f"Annual ROI: ${annual_savings:.0f}", 
                      style="CostSavings.TLabel", font=("Segoe UI", 11)).pack(anchor="w")
                Label(col3, text=f"Payback: {break_even*30:.0f} days", 
                      style="Secondary.TLabel", font=("Segoe UI", 11)).pack(anchor="w")

        # Comprehensive Approaches Table with modern styling
        if detailed_results:
            approaches_frame = Frame(content_frame, style="Modern.TFrame")
            approaches_frame.pack(fill=BOTH, expand=True, pady=(0, 20))
            
            Label(approaches_frame, text="🔧 Complete Training Approaches Comparison", 
                  style="Heading.TLabel", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 15))
            
            # Create enhanced comparison table with modern dark styling
            table_container = Frame(approaches_frame, style="Card.TFrame")
            table_container.pack(fill=BOTH, expand=True)
            
            # Enhanced table headers with modern styling
            headers_frame = Frame(table_container, style="Card.TFrame", padding=(15, 10))
            headers_frame.pack(fill=X)
            
            # Header labels with consistent styling
            headers = [
                ("Rank", 6), ("Model", 15), ("Training Approach", 20),
                ("Cost (USD)", 12), ("Time (Hours)", 12), ("Hardware", 15), ("Confidence", 10)
            ]
            
            for header, width in headers:
                Label(headers_frame, text=header, 
                      style="Secondary.TLabel", font=("Segoe UI", 10, "bold"), 
                      width=width).pack(side=LEFT)
            
            # Collect and sort all approaches
            all_approaches = []
            for model_name, model_data in detailed_results.items():
                if 'error' in model_data:
                    continue
                    
                cost_estimates = model_data.get('cost_estimates', [])
                for estimate in cost_estimates:
                    # Extract hardware info
                    hw_req = estimate.get('hardware_requirements', {})
                    gpu_type = hw_req.get('gpu_type', 'Unknown')
                    gpu_count = hw_req.get('gpu_count', 1)
                    hardware_display = f"{gpu_type}" + (f" x{gpu_count}" if gpu_count > 1 else "")
                    
                    all_approaches.append({
                        'model': model_name,
                        'approach': estimate['approach_name'],
                        'cost': estimate['total_cost_usd'],
                        'hours': estimate['training_hours'],
                        'hardware': hardware_display,
                        'confidence': estimate.get('confidence', 0.8)
                    })
            
            # Sort by cost (cheapest first)
            all_approaches.sort(key=lambda x: x['cost'])
            
            # Display top 15 approaches with color coding
            for i, approach in enumerate(all_approaches[:15]):
                row_frame = Frame(table_container, style="Modern.TFrame", padding=(15, 8))
                row_frame.pack(fill=X)
                
                # Rank with medal icons for top 3
                rank_display = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
                
                # Color-coded styling based on cost efficiency
                if i < 3:
                    text_style = "Success.TLabel"  # Top 3 in green
                elif approach['cost'] > all_approaches[0]['cost'] * 3:
                    text_style = "Warning.TLabel"  # Expensive options in amber
                else:
                    text_style = "Secondary.TLabel"  # Normal options
                
                # Row data with proper truncation
                row_data = [
                    (rank_display, 6),
                    (approach['model'][:12] + "..." if len(approach['model']) > 12 else approach['model'], 15),
                    (approach['approach'][:18] + "..." if len(approach['approach']) > 18 else approach['approach'], 20),
                    (f"${approach['cost']:.2f}", 12),
                    (f"{approach['hours']:.1f}h", 12),
                    (approach['hardware'][:12] + "..." if len(approach['hardware']) > 12 else approach['hardware'], 15),
                    (f"{approach['confidence']*100:.0f}%", 10)
                ]
                
                for data, width in row_data:
                    font_weight = "bold" if i < 3 and data not in [rank_display] else "normal"
                    Label(row_frame, text=data, 
                          style=text_style, 
                          font=("Segoe UI", 9, font_weight), 
                          width=width).pack(side=LEFT, anchor="w")
            
            # Show count of additional approaches if more than 15
            if len(all_approaches) > 15:
                more_frame = Frame(table_container, style="Modern.TFrame", padding=(15, 5))
                more_frame.pack(fill=X)
                Label(more_frame, text=f"... and {len(all_approaches) - 15} more approaches analyzed", 
                      style="Secondary.TLabel", font=("Segoe UI", 9)).pack(anchor="w")

        # Enhanced Recommendations with modern styling
        recommendations = cost_data.get('recommendations', [])
        if recommendations:
            rec_frame = Frame(content_frame, style="Card.TFrame", padding=(20, 15))
            rec_frame.pack(fill=X, pady=(0, 20))
            
            Label(rec_frame, text="💡 Cost Optimization Recommendations", 
                  style="Heading.TLabel", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 10))
            
            # Display top recommendations with proper styling
            for i, rec in enumerate(recommendations[:5], 1):
                Label(rec_frame, text=f"• {rec}", 
                      style="Secondary.TLabel", font=("Segoe UI", 10), 
                      wraplength=900, justify="left").pack(anchor="w", padx=(20, 0), pady=2)

        # Enhanced action buttons with modern styling
        button_frame = Frame(content_frame, style="Modern.TFrame")
        button_frame.pack(fill=X, pady=20)
        
        Button(button_frame, text="📊 Export Analysis", 
               command=lambda: self._export_cost_analysis(cost_analysis), 
               style="Success.TButton").pack(side=LEFT, padx=(0, 10))
        
        Button(button_frame, text="🔄 Refresh Pricing", 
               command=lambda: self._refresh_cost_analysis(), 
               style="Secondary.TButton").pack(side=LEFT, padx=(0, 10))
        
        Button(button_frame, text="Close", command=cost_window.destroy, 
               style="Secondary.TButton").pack(side=RIGHT)

    def update_tokenizer_dropdown(self):
        """Update tokenizer dropdown with available options"""
        try:
            tokenizers = self.controller.get_available_tokenizers()
            self.tokenizer_options = []
            display_names = []
            
            for tokenizer in tokenizers:
                self.tokenizer_options.append(tokenizer)
                
                if tokenizer['has_access']:
                    display_names.append(tokenizer['display_name'])
                else:
                    if not tokenizer['display_name'].startswith('🔒'):
                        display_names.append(f"🔒 {tokenizer['display_name']}")
                    else:
                        display_names.append(tokenizer['display_name'])
            
            self.tokenizer_dropdown['values'] = display_names
            
            # Set default to first available tokenizer
            available_tokenizers = [t for t in tokenizers if t['has_access'] and t['available']]
            if available_tokenizers:
                default_name = available_tokenizers[0]['display_name']
                self.selected_tokenizer.set(default_name)
                self._current_tokenizer_name = available_tokenizers[0]['name']
            else:
                self.selected_tokenizer.set("GPT-2 (Free)")
                self._current_tokenizer_name = 'gpt2'
                
        except Exception as e:
            messagebox.showerror("Tokenizer Error", f"Failed to load tokenizers: {str(e)}")
            self.tokenizer_dropdown['values'] = ["GPT-2 (Free)"]
            self.selected_tokenizer.set("GPT-2 (Free)")
            self._current_tokenizer_name = 'gpt2'

    def update_license_status(self):
        """Update license status display with modern colors"""
        try:
            license_info = self.controller.get_licensing_info()
            status = license_info['license_status']
            
            if status['status'] == 'demo':
                self.license_status_label.config(
                    text="🧑‍💻 Demo Mode - All Premium Features Enabled",
                    style="Premium.TLabel"
                )
            elif status['status'] == 'trial':
                days = status.get('days_remaining', 0)
                self.license_status_label.config(
                    text=f"⏱️ Trial: {days} days remaining",
                    style="Warning.TLabel"
                )
            elif status['status'] == 'active':
                self.license_status_label.config(
                    text="✅ Premium License Active",
                    style="Success.TLabel"
                )
            elif status['status'] == 'expired':
                self.license_status_label.config(
                    text="❌ License Expired",
                    style="Warning.TLabel"
                )
            else:
                self.license_status_label.config(
                    text="ℹ️ Free Tier - Upgrade for Premium Features",
                    style="Secondary.TLabel"
                )
                
        except Exception as e:
            self.license_status_label.config(
                text="⚠️ License Status Unknown",
                style="Secondary.TLabel"
            )

    def update_premium_section(self):
        """Update premium section with modern card styling"""
        try:
            license_info = self.controller.get_licensing_info()
            
            # Clear existing premium section
            for widget in self.premium_section.winfo_children():
                widget.destroy()
            
            if not license_info['premium_licensed']:
                Label(self.premium_section, text="💎 Premium Features", 
                      style="Heading.TLabel").pack(anchor="w", pady=(0, 12))

                upgrade_button = Button(self.premium_section, 
                                      image=self.icons["premium"],
                                      text="  Start Free Trial", 
                                      compound="left",
                                      command=self.start_trial, 
                                      style="Premium.TButton")
                upgrade_button.pack(fill="x", pady=(0, 8))
                
                upgrade_info_button = Button(self.premium_section, 
                                           image=self.icons["settings"],
                                           text="  View Premium Features", 
                                           compound="left",
                                           command=self.show_upgrade_info, 
                                           style="Secondary.TButton")
                upgrade_info_button.pack(fill="x")
            else:
                status = license_info['license_status']
                if status['status'] == 'trial' and status.get('days_remaining'):
                    Label(self.premium_section, text="💎 Premium Trial Active", 
                          style="Heading.TLabel").pack(anchor="w", pady=(0, 8))
                    
                    Label(self.premium_section, 
                          text=f"Trial expires in {status['days_remaining']} days", 
                          style="Warning.TLabel").pack(anchor="w", pady=(0, 12))
                    
                    upgrade_button = Button(self.premium_section, text="💎 Upgrade to Full License", 
                                          command=self.show_upgrade_info, 
                                          style="Premium.TButton")
                    upgrade_button.pack(fill="x")
                    
        except Exception as e:
            pass  # Silently fail for premium section

    def on_tokenizer_change(self, event=None):
        """Handle tokenizer selection change"""
        selected_display = self.selected_tokenizer.get()
        
        selected_tokenizer = None
        for tokenizer in self.tokenizer_options:
            if tokenizer['display_name'] == selected_display or f"🔒 {tokenizer['display_name']}" == selected_display:
                selected_tokenizer = tokenizer
                break
        
        if not selected_tokenizer:
            return
        
        if not selected_tokenizer['has_access']:
            self.show_premium_upgrade_dialog(selected_tokenizer['name'])
            self.update_tokenizer_dropdown()
            return
        
        self._current_tokenizer_name = selected_tokenizer['name']
        
        if self.chunks:
            self.update_chunk_analysis()

    def show_premium_upgrade_dialog(self, feature_name):
        """SIMPLIFIED: Use basic messagebox for premium upgrade"""
        try:
            upgrade_info = self.controller.get_upgrade_info()
            premium_features = upgrade_info.get('premium_features', [])
            
            feature_list = "\n".join([f"• {f['description']}" for f in premium_features[:5]])
            
            message = f"""🔒 Premium Feature: {feature_name}

Premium features include:
{feature_list}

💎 Premium: $15/month or $150/year
🆓 7-day free trial available

Would you like to start your free trial?"""
            
            result = messagebox.askyesno("Upgrade to Premium", message)
            if result:
                self.start_trial()
        except Exception as e:
            messagebox.showerror("Upgrade Error", f"Failed to show upgrade info: {str(e)}")

    def update_chunk_analysis(self):
        """Update chunk analysis with current tokenizer"""
        if not self.chunks:
            return
        
        try:
            tokenizer_name = getattr(self, '_current_tokenizer_name', 'gpt2')
            self.current_analysis = self.controller.analyze_chunks(self.chunks, tokenizer_name, TOKEN_LIMIT)
            
            if self.controller.license_manager.check_feature_access('advanced_analytics'):
                tokenizer_info = next((t for t in self.controller.get_available_tokenizers() 
                                     if t['name'] == tokenizer_name), None)
                
                if tokenizer_info and self.current_analysis:
                    enhanced_recommendations = list(self.current_analysis.get('recommendations', []))
                    
                    if tokenizer_info['accuracy'] == 'estimated' and self.current_analysis['total_tokens'] > 5000:
                        enhanced_recommendations.append("Consider upgrading to exact tokenizer for large datasets")
                    
                    if tokenizer_info['performance'] == 'slow' and len(self.chunks) > 100:
                        enhanced_recommendations.append("Large dataset detected - faster tokenizer recommended")
                    
                    self.current_analysis['recommendations'] = enhanced_recommendations
                    
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to analyze chunks: {str(e)}")

    # File operations
    def select_file(self):
        path = filedialog.askopenfilename(title="Select Book or Document",
                                          filetypes=[("Text or Document Files", "*.txt *.pdf *.epub")])
        if path:
            self.file_path = path
            self.file_label.config(text=os.path.basename(path))
            self.chunks = []
            self.current_analysis = None
            self.session.add_file(path)

    def handle_file_drop(self, event):
        path = event.data.strip("{}")
        if os.path.isfile(path) and path.lower().endswith((".txt", ".pdf", ".epub")):
            self.file_path = path
            self.file_label.config(text=os.path.basename(path))
            self.chunks = []
            self.current_analysis = None
            self.session.add_file(path)
        else:
            messagebox.showerror("Invalid File", "Please drop a valid .txt, .pdf, or .epub file.")

    def process_text(self):
        if not self.file_path:
            messagebox.showerror("Missing File", "Please select a file first.")
            return

        method = self.split_method.get()
        delimiter = self.delimiter_entry.get() if method == "custom" else None
        tokenizer_name = getattr(self, '_current_tokenizer_name', 'gpt2')

        try:
            clean_opts = {"remove_headers": True, "normalize_whitespace": True, "strip_bullets": True}
            
            self.chunks = self.controller.process_book(self.file_path, clean_opts, method, delimiter, tokenizer_name)
            self.current_analysis = self.controller.analyze_chunks(self.chunks, tokenizer_name, TOKEN_LIMIT)
            
            # Update session
            for f in self.session.files:
                if f.path == self.file_path:
                    f.chunks = self.chunks
                    f.config['tokenizer'] = tokenizer_name
                    break

            # Create enhanced success message
            analysis = self.current_analysis
            msg = f"✅ Processed {analysis['total_chunks']} chunks using {tokenizer_name}\n"
            msg += f"📊 Total tokens: {analysis['total_tokens']:,} | Average: {analysis['avg_tokens']}\n"
            
            if analysis['over_limit'] > 0:
                msg += f"⚠️ {analysis['over_limit']} chunks exceed {TOKEN_LIMIT} tokens ({analysis['over_limit_percentage']:.1f}%)"
            else:
                msg += "✨ All chunks within token limit!"
                
            if analysis.get('advanced_analytics'):
                msg += f"\n🎯 Efficiency Score: {analysis['efficiency_score']}%"
                if analysis.get('cost_estimates'):
                    cost = analysis['cost_estimates']['estimated_api_cost']
                    msg += f"\n💰 Estimated training cost: ${cost:.4f}"
            
            # Add cost analysis prompt for premium users
            if self.controller.license_manager.check_feature_access('advanced_cost_analysis'):
                msg += f"\n\n💡 Click 'Analyze Training Costs' for comprehensive cost analysis across 15+ approaches!"
            
            messagebox.showinfo("Processing Complete", msg)
            
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))

    def preview_chunks(self):
        """Enhanced preview with modern dark styling"""
        if not self.chunks:
            messagebox.showwarning("No Data", "You must process a file first.")
            return

        tokenizer_name = getattr(self, '_current_tokenizer_name', 'gpt2')
        
        try:
            # Create modern dark preview window
            preview_window = tk.Toplevel(self)
            preview_window.title("👁️ Chunk Preview")
            preview_window.geometry("900x650")
            preview_window.transient(self)
            preview_window.configure(bg=MODERN_SLATE['bg_primary'])
            
            # Create scrollable text widget with modern styling
            text_frame = Frame(preview_window, style="Modern.TFrame")
            text_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)
            
            text_widget = tk.Text(text_frame, 
                                 wrap=tk.WORD, 
                                 font=("Consolas", 10),
                                 bg=MODERN_SLATE['bg_cards'],
                                 fg=MODERN_SLATE['text_primary'],
                                 insertbackground=MODERN_SLATE['accent_cyan'],
                                 selectbackground=MODERN_SLATE['accent_blue'],
                                 selectforeground="white",
                                 borderwidth=1,
                                 relief="solid")
            
            scrollbar = Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side="left", fill=BOTH, expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Add chunk content with enhanced analysis
            content = f"📊 CHUNK PREVIEW - {len(self.chunks)} chunks processed\n"
            content += f"🔧 Tokenizer: {tokenizer_name}\n"
            content += f"📏 Token Limit: {TOKEN_LIMIT}\n"
            content += "=" * 70 + "\n\n"
            
            # Show first 10 chunks with detailed token analysis
            for i, chunk in enumerate(self.chunks[:10]):
                count, metadata = self.controller.get_token_count(chunk, tokenizer_name)
                
                # Color-coded status indicators
                if count <= TOKEN_LIMIT * 0.8:
                    status = "🟢 OPTIMAL"
                elif count <= TOKEN_LIMIT:
                    status = "🟡 GOOD"
                else:
                    status = "🔴 OVER LIMIT"
                
                efficiency = (min(count, TOKEN_LIMIT) / TOKEN_LIMIT) * 100
                
                content += f"{status} | Chunk {i+1:2d} | {count:4d} tokens | {efficiency:5.1f}% efficiency\n"
                content += f"{'─' * 70}\n"
                
                # Truncate chunk content for preview
                preview_text = chunk[:300] + "..." if len(chunk) > 300 else chunk
                content += f"{preview_text}\n\n"
            
            if len(self.chunks) > 10:
                content += f"{'═' * 70}\n"
                content += f"... and {len(self.chunks) - 10} more chunks (showing first 10)\n\n"
                
                # Add summary statistics
                if self.current_analysis:
                    analysis = self.current_analysis
                    content += f"📈 SUMMARY STATISTICS:\n"
                    content += f"• Total Chunks: {analysis['total_chunks']}\n"
                    content += f"• Total Tokens: {analysis['total_tokens']:,}\n"
                    content += f"• Average Tokens: {analysis['avg_tokens']:.1f}\n"
                    content += f"• Over Limit: {analysis['over_limit']} ({analysis['over_limit_percentage']:.1f}%)\n"
                    if analysis.get('efficiency_score'):
                        content += f"• Efficiency Score: {analysis['efficiency_score']}%\n"
            
            text_widget.insert("1.0", content)
            text_widget.config(state="disabled")
            
            # Add modern close button
            button_frame = Frame(preview_window, style="Modern.TFrame")
            button_frame.pack(pady=10)
            
            Button(button_frame, text="Close Preview", 
                   command=preview_window.destroy,
                   style="Secondary.TButton").pack()
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Failed to show preview: {str(e)}")

    def create_premium_analytics_window(self):
        """Enhanced analytics with modern styling"""
        if not self.current_analysis:
            messagebox.showwarning("No Analysis", "No analysis data available.")
            return
        
        try:
            analysis = self.current_analysis
            
            # Create analytics summary with modern dark theme
            summary = f"""📊 ADVANCED ANALYTICS DASHBOARD

Dataset Overview:
• Total Chunks: {analysis.get('total_chunks', 0):,}
• Total Tokens: {analysis.get('total_tokens', 0):,}
• Average Tokens: {analysis.get('avg_tokens', 0):.1f}
• Token Range: {analysis.get('min_tokens', 0)} - {analysis.get('max_tokens', 0)}
• Over Limit: {analysis.get('over_limit', 0)} chunks ({analysis.get('over_limit_percentage', 0):.1f}%)

Performance Metrics:
• Efficiency Score: {analysis.get('efficiency_score', 0)}% 
• Tokenizer: {getattr(self, '_current_tokenizer_name', 'gpt2')}
• Processing Method: {self.split_method.get()}"""
            
            # Add cost preview if available
            cost_preview = analysis.get('cost_preview', {})
            if cost_preview.get('available'):
                summary += f"""

💰 Cost Analysis Preview:
• Best Approach: {cost_preview.get('best_approach', 'N/A')}
• Estimated Cost: ${cost_preview.get('estimated_cost', 0):.2f}
• Training Hours: {cost_preview.get('training_hours', 0):.1f}h
• Confidence: {cost_preview.get('confidence', 'Unknown')}"""
            else:
                summary += f"""

💰 Cost Estimation:
• Estimated Range: {cost_preview.get('estimated_cost_range', 'N/A')}
• Accuracy: {cost_preview.get('accuracy', '±50%')}
• {cost_preview.get('upgrade_message', '')}"""
            
            # Add optimization recommendations
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                summary += "\n\n💡 Optimization Recommendations:\n"
                for i, rec in enumerate(recommendations[:3], 1):
                    summary += f"{i}. {rec}\n"
            
            # Enhanced token distribution (if available)
            if analysis.get('token_distribution'):
                dist = analysis['token_distribution']
                summary += f"""

📊 Token Distribution:
• Under 50 tokens: {dist.get('under_50', 0)} chunks
• 50-200 tokens: {dist.get('50_200', 0)} chunks  
• 200-400 tokens: {dist.get('200_400', 0)} chunks
• 400-{TOKEN_LIMIT} tokens: {dist.get('400_512', 0)} chunks
• Over limit: {dist.get('over_limit', 0)} chunks"""
            
            messagebox.showinfo("📊 Advanced Analytics Dashboard", summary)
            
        except Exception as e:
            messagebox.showerror("Analytics Error", f"Failed to show analytics: {str(e)}")

    def show_tokenizer_comparison(self):
        """Enhanced tokenizer comparison with modern presentation"""
        if not self.chunks:
            messagebox.showwarning("No Data", "Process a file first to compare tokenizers.")
            return
        
        try:
            available_tokenizers = self.controller.get_available_tokenizers()
            
            # Get sample text for comparison
            sample_text = self.chunks[0][:500] if self.chunks else "Sample text for comparison"
            
            comparison = "🔍 TOKENIZER PERFORMANCE COMPARISON\n\n"
            comparison += f"Sample Text: {sample_text[:100]}...\n"
            comparison += f"Text Length: {len(sample_text)} characters\n"
            comparison += "=" * 60 + "\n\n"
            
            results = []
            for tokenizer in available_tokenizers[:5]:  # Limit to 5 tokenizers
                if tokenizer['available']:
                    try:
                        count, metadata = self.controller.get_token_count(sample_text, tokenizer['name'])
                        access_icon = "✅" if tokenizer['has_access'] else "🔒"
                        premium_indicator = " (Premium)" if tokenizer['is_premium'] else " (Free)"
                        
                        results.append({
                            'name': tokenizer['display_name'],
                            'tokens': count,
                            'access': access_icon,
                            'premium': premium_indicator,
                            'accuracy': tokenizer['accuracy'],
                            'performance': tokenizer['performance']
                        })
                        
                    except Exception as e:
                        results.append({
                            'name': tokenizer['display_name'],
                            'tokens': 'Error',
                            'access': "❌",
                            'premium': "",
                            'accuracy': 'N/A',
                            'performance': 'N/A'
                        })
            
            # Sort by token count for comparison
            valid_results = [r for r in results if isinstance(r['tokens'], int)]
            error_results = [r for r in results if not isinstance(r['tokens'], int)]
            valid_results.sort(key=lambda x: x['tokens'])
            
            # Display results
            for result in valid_results + error_results:
                comparison += f"{result['access']} {result['name']}{result['premium']}\n"
                if isinstance(result['tokens'], int):
                    comparison += f"   📊 Tokens: {result['tokens']}\n"
                    comparison += f"   🎯 Accuracy: {result['accuracy']} | ⚡ Performance: {result['performance']}\n"
                else:
                    comparison += f"   ❌ Status: {result['tokens']}\n"
                comparison += "\n"
            
            comparison += "\n💡 Professional Recommendation:\n"
            comparison += "• Use exact tokenizers (GPT-4, GPT-3.5) for production datasets\n"
            comparison += "• GPT-2 suitable for development and estimation\n"
            comparison += "• BERT tokenizers best for encoder/classification models\n"
            comparison += "• Claude estimator optimized for Anthropic models"
            
            messagebox.showinfo("🔍 Tokenizer Comparison", comparison)
            
        except Exception as e:
            messagebox.showerror("Comparison Error", f"Failed to compare tokenizers: {str(e)}")

    # Export operations
    def export_txt(self):
        if not self.chunks:
            messagebox.showwarning("No Data", "Please process a file first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if path:
            save_as_txt(self.chunks, path)
            messagebox.showinfo("✅ Export Complete", f"Dataset saved to {path}")

    def export_csv(self):
        if not self.chunks:
            messagebox.showwarning("No Data", "Please process a file first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV File", "*.csv")])
        if path:
            save_as_csv(self.chunks, path)
            messagebox.showinfo("✅ Export Complete", f"Dataset saved to {path}")

    def on_split_method_change(self, event=None):
        selected = self.split_method.get()
        if selected == "custom":
            self.delimiter_entry.pack(fill="x", pady=(0, 12))
        else:
            self.delimiter_entry.pack_forget()

    # Trial and premium operations - Enhanced with modern styling
    def start_trial(self):
        """Enhanced trial start with modern UI feedback"""
        try:
            if self.controller.start_trial():
                messagebox.showinfo("🎉 Trial Started", 
                    "Your 7-day premium trial has started!\n\n"
                    "✅ All premium features are now available:\n"
                    "• Exact GPT-4 & GPT-3.5 tokenization\n"
                    "• Comprehensive cost analysis\n"
                    "• Advanced analytics with export\n"
                    "• Priority support\n\n"
                    "Enjoy exploring Wolfscribe Premium!")
                
                self.update_tokenizer_dropdown()
                self.update_license_status()
                self.update_premium_section()
            else:
                messagebox.showwarning("Trial Unavailable", 
                    "❌ Trial is not available.\n\n"
                    "You may have already used your trial period.\n"
                    "Contact support if you believe this is an error.")
        except Exception as e:
            messagebox.showerror("Trial Error", f"Failed to start trial: {str(e)}")

    def show_upgrade_info(self):
        """Enhanced upgrade info with modern presentation"""
        try:
            upgrade_info = self.controller.get_upgrade_info()
            license_status = upgrade_info.get('current_status', 'free')
            
            if license_status == 'trial':
                days = upgrade_info.get('days_remaining', 0)
                message = f"""⏱️ PREMIUM TRIAL STATUS

You have {days} days remaining in your premium trial.

🚀 Premium Features Currently Active:
• 🎯 Exact GPT-4 & GPT-3.5 tokenization
• 💰 Comprehensive cost analysis (15+ approaches)
• 📊 ROI analysis and optimization recommendations
• ⚡ Real-time cloud pricing integration
• 📈 Advanced analytics with export capabilities
• 🛡️ Priority support

💎 Continue with Premium: $15/month or $150/year
💰 Save $30 with annual subscription!

Upgrade now to keep these powerful features after your trial expires."""
            
            elif license_status == 'active':
                message = """✅ PREMIUM LICENSE ACTIVE

Your premium license is active with full access to:

🎯 Professional Tokenization:
• Exact GPT-4 & GPT-3.5 tokenization
• Claude estimator for Anthropic models  
• BERT tokenizers for encoder models

💰 Advanced Cost Analysis:
• 15+ training approaches comparison
• Real-time cloud pricing integration
• ROI analysis with break-even calculations
• Cost optimization recommendations

📊 Premium Analytics:
• Advanced efficiency scoring
• Professional export capabilities
• Detailed token distribution analysis

Thank you for supporting Wolfscribe Premium! 🎉"""
            
            else:  # free
                premium_features = upgrade_info.get('premium_features', [])
                feature_list = "\n".join([f"• {f['description']}" for f in premium_features[:6]])
                
                message = f"""💎 UPGRADE TO WOLFSCRIBE PREMIUM

🆓 Current: Free Tier
• GPT-2 tokenization only
• Basic chunk analysis
• Limited export options

🚀 Premium Features:
{feature_list}

💰 Transparent Pricing:
• Monthly: $15/month
• Yearly: $150/year (save $30!)
• Cancel anytime

🆓 Risk-Free Trial:
• 7-day free trial
• No credit card required
• Full feature access

💡 Average User Saves $32+ per training run through optimal approach selection!"""
            
            messagebox.showinfo("💎 Premium Information", message)
            
            # Offer trial if user is on free tier
            if license_status == 'free':
                trial_result = messagebox.askyesno("Start Free Trial?", 
                    "🚀 Ready to experience Wolfscribe Premium?\n\n"
                    "Start your 7-day free trial now to access:\n"
                    "• Comprehensive cost analysis\n"
                    "• Exact tokenization for all major models\n"
                    "• Advanced analytics and optimization\n\n"
                    "No credit card required!")
                if trial_result:
                    self.start_trial()
                    
        except Exception as e:
            messagebox.showerror("Info Error", f"Failed to show upgrade info: {str(e)}")

    # Session operations with enhanced feedback
    def save_session(self):
        """Enhanced session saving with comprehensive preferences"""
        path = filedialog.asksaveasfilename(defaultextension=".wsession", 
                                          filetypes=[("Wolfscribe Session", "*.wsession")])
        if not path:
            return
        try:
            session_data = self.session.to_dict()
            
            # Enhanced session data with UI preferences
            session_data['ui_preferences'] = {
                'selected_tokenizer': getattr(self, '_current_tokenizer_name', 'gpt2'),
                'split_method': self.split_method.get(),
                'token_limit': TOKEN_LIMIT,
                'theme': 'modern_slate'
            }
            
            if self.current_analysis:
                session_data['last_analysis'] = self.current_analysis
                
            with open(path, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("💾 Session Saved", f"Session saved successfully to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save session: {str(e)}")

    def load_session(self):
        """Enhanced session loading with preference restoration"""
        path = filedialog.askopenfilename(filetypes=[("Wolfscribe Session", "*.wsession")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.session = Session.from_dict(data)
            
            # Restore UI preferences
            ui_prefs = data.get('ui_preferences', {})
            if ui_prefs:
                preferred_tokenizer = ui_prefs.get('selected_tokenizer', 'gpt2')
                if self.controller.license_manager.check_tokenizer_access(preferred_tokenizer):
                    self._current_tokenizer_name = preferred_tokenizer
                    self.update_tokenizer_dropdown()
                    
                    for tokenizer in self.tokenizer_options:
                        if tokenizer['name'] == preferred_tokenizer:
                            self.selected_tokenizer.set(tokenizer['display_name'])
                            break
                
                split_method = ui_prefs.get('split_method', 'paragraph')
                self.split_method.set(split_method)
                self.on_split_method_change()
            
            self.current_analysis = data.get('last_analysis')
            
            # Restore file state
            if self.session.files:
                first_file = self.session.files[0]
                self.file_path = first_file.path
                self.file_label.config(text=os.path.basename(self.file_path))
                self.chunks = first_file.chunks
                
                if self.chunks:
                    self.update_chunk_analysis()
            
            messagebox.showinfo("📂 Session Loaded", 
                f"Session loaded successfully from:\n{path}\n\n"
                f"Files: {len(self.session.files)}\n"
                f"Chunks: {len(self.chunks)}")
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load session: {str(e)}")

    def _export_cost_analysis(self, cost_analysis):
        """Enhanced export cost analysis with modern file dialog"""
        try:
            path = filedialog.asksaveasfilename(
                title="Export Cost Analysis",
                defaultextension=".json",
                filetypes=[
                    ("JSON Report", "*.json"),
                    ("CSV Summary", "*.csv"),
                    ("Text Report", "*.txt")
                ]
            )
            
            if not path:
                return
                
            file_ext = os.path.splitext(path)[1].lower()
            
            if file_ext == '.json':
                # Export comprehensive JSON report
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(cost_analysis, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("✅ Export Complete", f"JSON report exported to:\n{path}")
                
            elif file_ext == '.csv':
                # Export CSV summary
                import csv
                
                cost_data = cost_analysis.get('cost_analysis', {})
                detailed_results = cost_data.get('detailed_results', {})
                
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Model', 'Approach', 'Cost_USD', 'Time_Hours', 'Hardware', 'Confidence'])
                    
                    for model_name, model_data in detailed_results.items():
                        if 'error' in model_data:
                            continue
                        cost_estimates = model_data.get('cost_estimates', [])
                        for estimate in cost_estimates:
                            hw_req = estimate.get('hardware_requirements', {})
                            hardware = f"{hw_req.get('gpu_type', 'Unknown')}"
                            if hw_req.get('gpu_count', 1) > 1:
                                hardware += f" x{hw_req['gpu_count']}"
                                
                            writer.writerow([
                                model_name,
                                estimate['approach_name'],
                                estimate['total_cost_usd'],
                                estimate['training_hours'],
                                hardware,
                                estimate.get('confidence', 0.8)
                            ])
                
                messagebox.showinfo("✅ Export Complete", f"CSV summary exported to:\n{path}")
                
            else:  # .txt
                # Export formatted text report
                report = self._generate_text_report(cost_analysis)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(report)
                messagebox.showinfo("✅ Export Complete", f"Text report exported to:\n{path}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export cost analysis: {str(e)}")

    def _generate_text_report(self, cost_analysis):
        """Generate formatted text report for cost analysis"""
        report = "💰 WOLFSCRIBE COST ANALYSIS REPORT\n"
        report += "=" * 50 + "\n\n"
        
        # Add timestamp
        from datetime import datetime
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Dataset: {len(self.chunks)} chunks, {cost_analysis.get('dataset_info', {}).get('tokens', 0):,} tokens\n\n"
        
        # Executive Summary
        cost_data = cost_analysis.get('cost_analysis', {})
        summary = cost_data.get('summary', {})
        
        if summary:
            report += "📊 EXECUTIVE SUMMARY\n"
            report += "-" * 20 + "\n"
            
            best_option = summary.get('best_overall', {})
            if best_option:
                report += f"Best Approach: {best_option.get('best_approach', 'N/A')}\n"
                report += f"Optimal Cost: ${best_option.get('cost', 0):.2f}\n"
                report += f"Training Time: {best_option.get('hours', 0):.1f} hours\n"
            
            cost_range = summary.get('cost_range', {})
            if cost_range:
                report += f"Cost Range: ${cost_range.get('min', 0):.2f} - ${cost_range.get('max', 0):.2f}\n"
                savings = cost_range.get('max', 0) - cost_range.get('min', 0)
                report += f"Maximum Savings: ${savings:.2f}\n"
            
            report += f"Models Analyzed: {summary.get('models_compared', 0)}\n\n"
        
        # Detailed Results
        detailed_results = cost_data.get('detailed_results', {})
        if detailed_results:
            report += "🔧 DETAILED TRAINING APPROACHES\n"
            report += "-" * 35 + "\n\n"
            
            all_approaches = []
            for model_name, model_data in detailed_results.items():
                if 'error' in model_data:
                    continue
                cost_estimates = model_data.get('cost_estimates', [])
                for estimate in cost_estimates:
                    all_approaches.append({
                        'model': model_name,
                        'approach': estimate['approach_name'],
                        'cost': estimate['total_cost_usd'],
                        'hours': estimate['training_hours'],
                        'hardware': estimate.get('hardware_requirements', {})
                    })
            
            # Sort by cost
            all_approaches.sort(key=lambda x: x['cost'])
            
            for i, approach in enumerate(all_approaches[:10], 1):  # Top 10
                report += f"{i:2d}. {approach['approach']} ({approach['model']})\n"
                report += f"    Cost: ${approach['cost']:.2f} | Time: {approach['hours']:.1f}h\n"
                
                hw = approach['hardware']
                gpu_type = hw.get('gpu_type', 'Unknown')
                gpu_count = hw.get('gpu_count', 1)
                hardware_str = f"{gpu_type}" + (f" x{gpu_count}" if gpu_count > 1 else "")
                report += f"    Hardware: {hardware_str}\n\n"
        
        # Recommendations
        recommendations = cost_data.get('recommendations', [])
        if recommendations:
            report += "💡 OPTIMIZATION RECOMMENDATIONS\n"
            report += "-" * 35 + "\n"
            for i, rec in enumerate(recommendations[:5], 1):
                report += f"{i}. {rec}\n"
            report += "\n"
        
        # Footer
        report += "=" * 50 + "\n"
        report += "Generated by Wolfscribe Premium\n"
        report += "https://wolflow.ai\n"
        
        return report

    def _refresh_cost_analysis(self):
        """Refresh cost analysis with updated pricing"""
        try:
            if not self.chunks:
                messagebox.showwarning("No Data", "Please process a file first.")
                return
                
            messagebox.showinfo("🔄 Refreshing Analysis", 
                "Refreshing cost analysis with latest pricing data...\n"
                "This may take a few seconds.")
            
            # Re-run cost analysis to get fresh pricing
            self.show_cost_analysis()
            
        except Exception as e:
            messagebox.showerror("Refresh Error", f"Failed to refresh cost analysis: {str(e)}")

# END OF FILE - Complete Modern Slate Theme Implementation