import json
import random
import time
import os
import hashlib
import re
import math
from datetime import datetime
from pdf_report_generator import generate_detailed_pdf

class SimulationEngine:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.load_knowledge_base()
        self.report_cache = {} 
        self.nlp = None
        self.load_nlp()

    def load_nlp(self):
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            print("spaCy model loaded successfully.")
        except Exception as e:
            print(f"spaCy load failed: {e}. Using regex fallback.")
            self.nlp = None

    def load_knowledge_base(self):
        try:
            with open(os.path.join(self.data_path, 'indian_demographics.json')) as f:
                self.demographics = json.load(f)
            with open(os.path.join(self.data_path, 'industry_benchmarks.json')) as f:
                self.benchmarks = json.load(f)
            with open(os.path.join(self.data_path, 'infrastructure_readiness.json')) as f:
                self.infrastructure = json.load(f)
            with open(os.path.join(self.data_path, 'persona_library.json')) as f:
                self.personas = json.load(f)
            with open(os.path.join(self.data_path, 'solution_templates.json')) as f:
                self.solutions = json.load(f)
            # Load new strict caps
            with open(os.path.join(self.data_path, 'income_spend_caps.json')) as f:
                self.income_caps = json.load(f)
            # Load Competitor DB
            with open(os.path.join(self.data_path, 'competitor_database.json')) as f:
                self.competitors_db = json.load(f)
        except Exception as e:
            print(f"CRITICAL ERROR in load_knowledge_base: {e}")
            import traceback
            traceback.print_exc()
            self.income_caps = {"middle_class": 800} 
            self.competitors_db = {}

    def run_simulation(self, idea_text):
        # 1. Parsing
        dna = self.stage1_parsing(idea_text)
        # 2. Modeling
        model = self.stage2_model_construction(dna)
        # 3. Env Factors
        env_factors = self.stage3_env_calc(model, dna)
        # 4. Collisions
        blocker_analysis = self.stage4_collision(model, env_factors)
        # 5. Mutations
        mutations = self.stage5_mutations(blocker_analysis)
        # 6. COMPETITOR ANALYSIS (Replaces Financials)
        competitor_map = self.analyze_competitors(dna, env_factors)
        # 7. North Star
        north_star = self.stage7_north_star(dna)
        # 8. Assembly
        final_output = self.stage8_assembly(dna, north_star, model, blocker_analysis, mutations, competitor_map, env_factors)
        
        # Generator PDF
        self.save_report_for_download(final_output)
        
        return final_output

    def stage1_parsing(self, text):
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        action =  "enable"
        target_user = "General User"
        domain = "Tech & SaaS" 

        if self.nlp:
            doc = self.nlp(text)
            verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
            if verbs: action = verbs[0]
            for chunk in doc.noun_chunks:
                if any(k in chunk.text for k in ["user", "people", "business", "student", "farmer", "doctor"]):
                     target_user = chunk.text
                     break
        else:
            user_match = re.search(r'for\s+([\w\s]+?)(?:to|\s|$)', text, re.IGNORECASE)
            if user_match: target_user = user_match.group(1).strip()
            
        found_match = False
        for p in self.personas:
            if p['name'].split()[0].lower() in text.lower() or p['type'].lower() in text.lower():
                target_user = p['type']
                found_match = True
                break
        if not found_match:
             if "student" in text.lower(): target_user = "Student"
             elif "business" in text.lower() or "sme" in text.lower(): target_user = "Small Business Owner"
             elif "farmer" in text.lower(): target_user = "Farmer"
             elif "doctor" in text.lower(): target_user = "Doctor"
        
        is_b2b = False
        if "business" in target_user.lower() or "sme" in target_user.lower() or "enterprise" in text.lower():
            is_b2b = True

        if "food" in text.lower(): domain = "Food & Hospitality"
        elif "health" in text.lower(): domain = "Health & Wellness"
        elif "shop" in text.lower() or "retail" in text.lower(): domain = "E-commerce & Retail"
        elif "finance" in text.lower(): domain = "FinTech"
        elif "education" in text.lower() or "learn" in text.lower(): domain = "EdTech"
        
        return {
            "action": action,
            "target_user": target_user,
            "domain": domain,
            "is_b2b": is_b2b,
            "original_text": text
        }

    def stage2_model_construction(self, dna):
        value_prop = f"{dna['action'].capitalize()} solution for {dna['target_user']}."
        selected_personas = []
        scored_personas = []
        for p in self.personas:
            score = 0
            if dna['target_user'].lower() in p['name'].lower() or dna['target_user'].lower() in p['type'].lower():
                score += 5
            scored_personas.append((score, p))
        scored_personas.sort(key=lambda x: x[0], reverse=True)
        
        primary = scored_personas[0][1]
        selected_personas.append(primary)
        
        types_needed = ["Early Adopter", "Economic Buyer"]
        if primary['type'] in types_needed: types_needed.remove(primary['type'])
        for t in types_needed:
            found = next((p for p in self.personas if p['type'] == t and p['id'] != primary['id']), self.personas[0])
            selected_personas.append(found)

        return {"value_prop": value_prop, "personas": selected_personas}

    def stage3_env_calc(self, model, dna):
        # Deterministic scoring
        trust_score = random.randint(60, 90) # Baseline
        if dna['domain'] == "FinTech" or dna['domain'] == "Health & Wellness":
            trust_score -= 20 # Harder to get trust
            
        income_map = {"Deprived": 90, "Aspirers": 70, "Middle Class": 50, "Affluent": 30, "Elite": 10}
        primary_persona = model['personas'][0]
        income_idx = income_map.get(primary_persona['income_level'], 50)
        
        price_fit = 100 - (income_idx * 1.0)
        
        return {
            "trust": trust_score,
            "price_fit": int(price_fit),
            "market_size": 75,
            "digital_literacy": primary_persona['digital_literacy'],
            "competition": 60,
            "infrastructure": 70,
            "avg_score": (trust_score + int(price_fit) + 60 + primary_persona['digital_literacy']) / 4
        }

    def stage4_collision(self, model, env):
        # 1000 Run Simulation
        failures = { "Trust Collisions": 0, "Adoption Friction": 0, "Price Misfits": 0, "Timing Misfires": 0 }
        p_trust = (100 - env['trust']) / 100.0
        p_price = (100 - env['price_fit']) / 100.0
        
        for _ in range(1000):
            r = random.random()
            if r < p_trust: failures["Trust Collisions"] += 1
            if r < p_price: failures["Price Misfits"] += 1
            
        top_blocker = max(failures, key=failures.get)
        severity = failures[top_blocker] / 1000.0 * 10
        
        descriptions = {
            "Trust Collisions": "Users unsure about data prop.",
            "Price Misfits": "Value perception mismatch."
        }
        
        return {
            "primary_blocker": {
                "type": top_blocker,
                "severity": round(severity, 1),
                "affected_percent": int((failures[top_blocker]/1000)*100),
                "description": descriptions.get(top_blocker, "General Friction")
            }
        }

    def stage5_mutations(self, blocker_analysis):
        return {
            "urgent_action": {"description": "Launch Pilot Program", "cost_inr": 50000, "complexity": 2},
            "next_step": {"description": "Scale Partnerships", "cost_inr": 200000, "complexity": 3}
        }

    def analyze_competitors(self, dna, env):
        # -- STEP 2: COMPETITOR WEAKNESS ENGINE --
        domain_map = {
            "Tech & SaaS": "tech_saas",
            "Food & Hospitality": "food_hospitality",
            "EdTech": "edtech",
            "FinTech": "fintech",
            "Health & Wellness": "health_wellness",
            "E-commerce & Retail": "retail_ecommerce"
        }
        
        db_key = domain_map.get(dna['domain'], "tech_saas")
        competitors = self.competitors_db.get(db_key, self.competitors_db.get("tech_saas"))
        
        # Fallback if still None or empty
        if not competitors:
            print(f"WARNING: No competitors found for {dna['domain']} (mapped to {db_key}). check competitor_database.json")
            competitors = []

        # Select 3 relevant
        selected = competitors[:3] if competitors else []
        
        # Create a dummy competitor if absolutely nothing exists to prevent crash
        if not selected:
             selected = [{
                 "name": "Generic Incumbent",
                 "weaknesses": {
                     "pricing": {"score": 5, "desc": "Standard market pricing"},
                     "features": {"score": 5, "desc": "Standard feature set"},
                     "ux": {"score": 5, "desc": "Average UX"},
                     "coverage": {"score": 5, "desc": "Average coverage"}
                 }
             }]
        
        # Analyze Weaknesses
        total_exploitable_score = 0
        analyzed_competitors = []
        
        for comp in selected:
            # Calculate aggregate weakness score
            w = comp['weaknesses']
            avg_weakness = (w['pricing']['score'] + w['features']['score'] + w['ux']['score'] + w['coverage']['score']) / 4
            
            # Impact Score (How much it matters to THIS user)
            # If user is price sensitive (e.g. Student), Pricing weakness matters more
            impact = 1.0
            if "Student" in dna['target_user'] and w['pricing']['score'] > 6: impact = 1.5
            
            exploitability = avg_weakness * impact
            total_exploitable_score += exploitability
            
            analyzed_competitors.append({
                "name": comp['name'],
                "weakness_score": round(avg_weakness, 1),
                "exploitability": round(exploitability, 1),
                "primary_weakness": max(w.items(), key=lambda x: x[1]['score'])[0], # key with max score
                "details": w
            })
            
        # Market Share Potential (0-100%)
        # Higher total exploitable score -> Higher capture potential
        capture_potential = min(int(total_exploitable_score * 2.5), 85)
        
        # Recommended Attack Vector
        # Find the most common weakness type across competitors
        weakness_counts = {"pricing": 0, "features": 0, "ux": 0, "coverage": 0}
        for c in analyzed_competitors:
             weakness_counts[c['primary_weakness']] += 1
             
        primary_vector_key = max(weakness_counts, key=weakness_counts.get)
        vectors = {
            "pricing": "Disruptive Pricing Model (Undercut by 20%)",
            "features": "Niche Feature Specialization",
            "ux": "Radical Simplicity & Design First",
            "coverage": "Hyper-local / Vertical Focus"
        }
        
        return {
            "competitors": analyzed_competitors,
            "market_share_potential": capture_potential,
            "primary_attack_vector": vectors[primary_vector_key],
            "total_exploitable_score": round(total_exploitable_score, 1),
            "domain_key": db_key
        }

    def stage7_north_star(self, dna):
        return {"metric": "Competitor Disruption Score", "badge_level": 5, "justification": "Market Share Velocity"}

    def stage8_assembly(self, dna, north_star, model, blocker, mutations, competitor_map, env):
        report_id = f"SIM_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8].upper()}"
        
        # --- Lightweight Market Calc (Restoring missing PDF keys) ---
        tam = 50000000 # 50M Base
        if dna['is_b2b']: tam = 8000000
        elif "Student" in dna['target_user']: tam = 40000000
        
        # Simple RPU estimate
        inc_level = model['personas'][0]['income_level']
        rpu = 500 # Fallback
        if "High" in inc_level or "Affluent" in inc_level: rpu = 1500
        elif "Deprived" in inc_level: rpu = 50
        
        # User Estimate
        adoption = 0.05 # 5% capture of weaknesses
        users = int(tam * adoption * (competitor_map['market_share_potential']/100))
        
        # Prepare flat dictionary for PDF Generator
        sim_data = {
            "report_id": report_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "idea_title": dna['original_text'],
            "target_user": dna['target_user'],
            "target_user_segment": model['personas'][0]['name'],
            "tam": tam,
            "users": users,
            "rpu": rpu,
            "income_level": inc_level,
            "competitor_count": 12, 
            
            # Re-add other keys PDF expects
            "simulation_runs": 1000,
            "blocker_impact_pct": blocker['primary_blocker']['affected_percent'],
            "market_timing": "Opportunistic",
            "infrastructure_score": env['infrastructure'],
            "competition_score": env['competition'],
            "competition_density": "Fragmented",
            "key_growth_driver": "Community Referrals",
            "risk_count": 3,
            "top_risk": blocker['primary_blocker']['type'],
            "top_risk_severity": blocker['primary_blocker']['severity'],
            "mitigation_focus": "Trust & Transparency",
            "mitigation": "Bite-sized trials and testimonials.",
            "spend_allocation_pct": 15, # Constant
            "friction_score": int(env['avg_score']), # Added back
            
            "urgent_action": mutations['urgent_action'],
            "next_step": mutations['next_step'],
            
            "domain": dna['domain'],
            "market_gap": competitor_map['primary_attack_vector'],
            
            # Competitor Data
            "competitors": competitor_map['competitors'],
            "capture_potential": competitor_map['market_share_potential'],
            "attack_vector": competitor_map['primary_attack_vector'],
            
            # Standard
            # Standard
            "primary_blocker": blocker['primary_blocker']['type'],
            "blocker_severity": blocker['primary_blocker']['severity'],
            
            # REPLACED FINANCIALS WITH MAP DATA
            "revenue": "N/A", 
            "conservative_revenue": "N/A",
            "blue_sky_revenue": "N/A"
        }

        # Return structured checks for Frontend
        return {
            "idea_dna": dna,
            "summary": f"Competitive Analysis for {dna['target_user']} in {dna['domain']}.",
            "north_star": north_star,
            "environmental_factors": env,
            "blocker_analysis": blocker,
            "competitor_map": competitor_map, # NEW
            "urgent_action": mutations['urgent_action'],
            "next_step": mutations['next_step'],
            "persona_snapshots": model['personas'],
            "report_id": report_id,
            "sim_data_flat": sim_data
        }

    def save_report_for_download(self, final_output):
        sim_data = final_output['sim_data_flat']
        filename = f"Report_{sim_data['report_id']}.pdf"
        filepath = os.path.join('/tmp', filename)
        generate_detailed_pdf(sim_data, filepath)
        self.report_cache[sim_data['report_id']] = filepath
        self.report_cache[final_output['report_id']] = filepath

    def get_report_path(self, report_id):
        return self.report_cache.get(report_id)
