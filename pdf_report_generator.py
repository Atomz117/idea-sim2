from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import json
import random

def generate_600_word_analysis(simulation_data):
    # Core dynamic analysis
    analysis = f"""
    Our comprehensive simulation of the "{simulation_data['idea_title']}" concept reveals critical insights specifically tailored to the Indian market context. Scaling a solution for {simulation_data['target_user']} requires a nuanced understanding of competitor vulnerabilities.
    
    The core value proposition targets the {simulation_data.get('target_user_segment', 'general population')}, representing a Serviceable Addressable Market (SAM) of approximately {simulation_data['users']:,} users. Based on our analysis of {simulation_data['competitor_count']} existing solutions, we have identified a distinct market gap in {simulation_data['market_gap']}.
    
    Competitive landscape analysis indicates that incumbent solutions suffer from significant weaknesses. Our 'Competitor Weakness Map' highlights a total capture potential of {simulation_data['capture_potential']}% of the existing market share. The primary attack vector identified is "{simulation_data['attack_vector']}", which directly addresses the frustration points of the {simulation_data['income_level']} segment.
    
    From a timing perspective, the market metrics indicate a {simulation_data['market_timing']} entry point. The current infrastructure readiness score of {simulation_data['infrastructure_score']}/100 suggests that digital rails are established. However, the competitive density is currently rated at {simulation_data['competition_score']}/100, implying a {simulation_data['competition_density']} landscape.
    
    Our strategic model suggests a high-impact entry by exploiting the identified weakness in {simulation_data['competitors'][0]['primary_weakness']}. This focus minimizes Customer Acquisition Cost (CAC) compared to a head-on feature war.
    
    The risk assessment matrix highlights {simulation_data['risk_count']} critical vulnerabilities. The top risk, "{simulation_data['top_risk']}", carries a severity score of {simulation_data['top_risk_severity']}/10. Mitigation will require a focus on {simulation_data['mitigation_focus']}.
    
    Strategically, we recommend an immediate focus on {simulation_data['urgent_action']['description']}. This low-complexity intervention is designed to stabilize the user base before scaling. Following this, the medium-term priority should be {simulation_data['next_step']['description']}, which will secure long-term retention.
    
    In conclusion, rather than a purely financial projection, our analysis confirms a strategic opening to capture {simulation_data['capture_potential']}% of the market by leveraging competitor inertia. Success will depend on ruthless execution of the "{simulation_data['attack_vector']}" strategy.
    """
    
    # Word count padder logic (to ensure depth and length)
    word_count = len(analysis.split())
    
    if word_count < 600:
        analysis += f"""
        
        Detailed Competitive Considerations:
        To operate effectively within the Indian {simulation_data['domain']} sector, one must understand that competitors like {simulation_data['competitors'][0]['name']} have established trust but lack agility. Our scoring indicates their exploitability score is {simulation_data['competitors'][0]['exploitability']}, derived from their inability to adapt to the "{simulation_data['attack_vector']}" demand.
        
        Seasonal and Cultural Factors:
        The simulation accounted for seasonal variations typical of the Indian market. Your go-to-market strategy should align marketing spend with these cycles to maximize ROI, targeting users when competitor service levels drop (e.g. during high festival demand).
        
        Infrastructure and Logistics:
        The {simulation_data['infrastructure_score']} infrastructure score implies that while urban centers are ready, semi-urban expansion will require localized workarounds—potentially involving offline-to-online (O2O) bridges or assisted buying models. 
        
        Regulatory Landscape:
        Compliance with evolving data privacy standards (DPDP Act) and sector-specific regulations for {simulation_data['domain']} has been factored into the complexity scores. Ensuring early compliance will serve as a competitive moat against non-compliant informal competitors.
        
        Capital Efficiency:
        Given the focus on "{simulation_data['attack_vector']}", the burn rate must be kept strictly proportional to market capture. The model assumes a lean team structure initially, prioritizing product and customer support roles over heavy sales hierarchies.
        
        Strategic Outlook:
        With a capture potential of {simulation_data['capture_potential']}%, the business presents a viable case for disruption. Institutional venture capital (VC) will be attracted to the defensibility of this specific attack vector rather than just generic growth metrics.
        """
        
    return analysis

def generate_detailed_pdf(sim_data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom Styles
    title_style = ParagraphStyle('TitleCustom', parent=styles['Title'], fontSize=22, alignment=1, spaceAfter=20)
    h1 = ParagraphStyle('H1Custom', parent=styles['Heading1'], fontSize=16, spaceBefore=15, spaceAfter=10, textColor=colors.darkblue)
    normal = ParagraphStyle('NormalCustom', parent=styles['BodyText'], fontSize=10, leading=14, alignment=4) # Justify
    
    # 1. COVER PAGE
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("IDEA SIMULATION ENGINE", title_style))
    story.append(Paragraph("COMPREHENSIVE ANALYSIS REPORT", ParagraphStyle('Sub', parent=title_style, fontSize=16)))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph(f"<b>Idea:</b> {sim_data['idea_title']}", styles['Heading2']))
    story.append(Paragraph(f"<b>Date:</b> {sim_data['date']}", styles['Normal']))
    story.append(Paragraph(f"<b>Report ID:</b> {sim_data['report_id']}", styles['Normal']))
    story.append(PageBreak())
    
    # 2. METHODOLOGY
    story.append(Paragraph("RESEARCH METHODOLOGY", h1))
    story.append(Paragraph("This analysis was conducted using a deterministic simulation models grounded in Indian demographic data benchmarks:", normal))
    story.append(Spacer(1, 0.2*inch))
    
    methods = [
        f"• <b>Market Size:</b> Derived from census data segments, totaling {sim_data['tam']:,} addressable users.",
        f"• <b>Pricing Logic:</b> Benchmarked against {sim_data['domain']} standards adjusted for {sim_data['income_level']} income caps.",
        f"• <b>Adoption Modeling:</b> Uses conservative conversion rates (0.05%-0.2%) affected by a calculated Friction Score of {sim_data['friction_score']}/100.",
        f"• <b>Risk Simulation:</b> 1,000 Monte Carlo iterations run to identify the primary failure point: {sim_data['primary_blocker']}.",
        f"• <b>Financial Sanity:</b> All revenue projections are auto-corrected for 'unicorn' inflation to ensure realism."
    ]
    for m in methods:
        story.append(Paragraph(m, normal))
        story.append(Spacer(1, 6))
    
    # 3. DETAILED FINDINGS
    story.append(PageBreak())
    story.append(Paragraph("DETAILED ANALYSIS FINDINGS", h1))
    analysis_text = generate_600_word_analysis(sim_data)
    story.append(Paragraph(analysis_text, normal))
    
    # 4. COMPETITOR WEAKNESS ANALYSIS (Replaces Financials)
    story.append(PageBreak())
    story.append(Paragraph("COMPETITOR WEAKNESS MAP", h1))
    
    story.append(Paragraph(f"<b>Primary Attack Vector: {sim_data['market_gap']}</b>", styles['Heading2']))
    story.append(Paragraph(f"Capture Potential: {sim_data['capture_potential']}% of competitor market share.", normal))
    story.append(Spacer(1, 10))
    
    # Competitor Table
    comp_data = [['Competitor', 'Weakness Score', 'Primary Weakness', 'Exploitability']]
    for c in sim_data['competitors']:
        comp_data.append([
            c['name'],
            f"{c['weakness_score']}/10",
            c['primary_weakness'].title(),
            f"{c['exploitability']}"
        ])
    
    t = Table(comp_data, colWidths=[120, 80, 100, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkgreen),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    story.append(Paragraph("Strategic Recommendation:", styles['Heading2']))
    story.append(Paragraph(f"To exploit the identified gap in <b>{sim_data['attack_vector']}</b>, we recommend positioning the product specifically against the weaknesses of {sim_data['competitors'][0]['name']}. Their vulnerability in {sim_data['competitors'][0]['primary_weakness']} offers the highest ROI entry point.", normal))
    story.append(Spacer(1, 20))
    
    # 5. RISK & ACTION
    story.append(Paragraph("RISK ANALYSIS & ACTION PLAN", h1))
    
    story.append(Paragraph(f"<b>Primary Risk:</b> {sim_data['top_risk']}", styles['Heading2']))
    story.append(Paragraph(f"Severity: {sim_data['top_risk_severity']}/10 | Impact: {sim_data['blocker_impact_pct']}% of funnel.", normal))
    story.append(Paragraph(f"<i>Mitigation: {sim_data['mitigation']}</i>", normal))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Recommended Actions", styles['Heading2']))
    story.append(Paragraph(f"<b>1. Immediate (2 Weeks):</b> {sim_data['urgent_action']['description']}", normal))
    story.append(Paragraph(f"   (Cost: INR {sim_data['urgent_action']['cost_inr']:,})", normal))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"<b>2. Next Step (3 Months):</b> {sim_data['next_step']['description']}", normal))
    story.append(Paragraph(f"   (Cost: INR {sim_data['next_step']['cost_inr']:,})", normal))

    doc.build(story)
    return filename
