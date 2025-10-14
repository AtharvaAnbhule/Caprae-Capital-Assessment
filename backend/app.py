from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import csv
import io
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Set
from urllib.parse import urlparse
import hashlib

app = Flask(__name__)
CORS(app)

class BusinessLeadIntelligence:
    """Business-focused lead intelligence system that aligns with sales workflows"""
    
    def __init__(self):
        self.industry_focus = ["SaaS", "FinTech", "HealthTech", "AI/ML", "Cybersecurity", "EdTech", "CleanTech"]
        self.target_company_sizes = ["51-200", "101-200", "201-500", "501-1000"]  # Growth-stage companies
        self.priority_roles = ["CTO", "CEO", "VP", "Head of", "Chief", "Director"]
        self.ideal_tech_stack = ["React", "Node.js", "Python", "AWS", "Azure", "GCP", "PostgreSQL", "MongoDB"]
        
    def calculate_business_priority_score(self, lead: Dict[str, Any]) -> float:
        """
        Calculate business priority score based on strategic alignment
        with target market and sales objectives
        """
        score = 0.0
        
        # Industry alignment (30%)
        if lead.get('industry') in self.industry_focus:
            score += 30
        elif lead.get('industry'):
            score += 10  # Partial credit for other tech industries
        
        # Company size targeting (25%)
        company_size = lead.get('company_size', '')
        if company_size in self.target_company_sizes:
            if company_size in ["201-500", "501-1000"]:
                score += 25  # Ideal targets
            else:
                score += 20  # Good targets
        elif company_size:
            score += 5
        
        # Role seniority and relevance (25%)
        role = lead.get('role', '')
        role_score = 0
        for priority_role in self.priority_roles:
            if priority_role.lower() in role.lower():
                if priority_role in ["CTO", "CEO", "Chief"]:
                    role_score = 25  # Decision makers
                else:
                    role_score = 20  # Influencers
                break
        score += role_score
        
        # Tech stack compatibility (20%)
        tech_stack = lead.get('tech_stack', [])
        compatible_tech = sum(1 for tech in tech_stack if tech in self.ideal_tech_stack)
        if tech_stack:
            tech_score = (compatible_tech / len(tech_stack)) * 20
            score += tech_score
        
        return min(score, 100.0)
    
    def assess_sales_readiness(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Assess lead readiness for sales outreach"""
        readiness = {
            "stage": "cold",
            "confidence": 0.0,
            "recommended_approach": "",
            "timing_priority": "medium"
        }
        
        # Calculate confidence score
        confidence_factors = []
        
        # Engagement level
        engagement = lead.get('engagement_score', 0)
        confidence_factors.append(engagement / 100.0)
        
        # Data completeness
        complete_fields = sum(1 for field in ['email', 'role', 'company', 'industry'] if lead.get(field))
        confidence_factors.append(complete_fields / 4.0)
        
        # Contact validity
        if lead.get('email_valid'):
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.3)
        
        # Recent activity
        if self._is_recent_activity(lead.get('last_activity')):
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        readiness["confidence"] = sum(confidence_factors) / len(confidence_factors)
        
        # Determine stage and approach
        if readiness["confidence"] >= 0.8:
            readiness["stage"] = "hot"
            readiness["recommended_approach"] = "Immediate personalized outreach"
            readiness["timing_priority"] = "high"
        elif readiness["confidence"] >= 0.6:
            readiness["stage"] = "warm"
            readiness["recommended_approach"] = "Nurture sequence with value content"
            readiness["timing_priority"] = "medium"
        else:
            readiness["stage"] = "cold"
            readiness["recommended_approach"] = "Educational content and brand building"
            readiness["timing_priority"] = "low"
        
        return readiness
    
    def _is_recent_activity(self, last_activity: str) -> bool:
        """Check if lead activity is recent (within 30 days)"""
        if not last_activity:
            return False
        
        try:
            activity_date = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
            return (datetime.now() - activity_date).days <= 30
        except:
            return False
    
    def generate_sales_insights(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Generate actionable sales insights for the lead"""
        insights = {
            "key_talking_points": [],
            "potential_pain_points": [],
            "value_proposition_focus": "",
            "competitive_angle": ""
        }
        
        industry = lead.get('industry', '')
        role = lead.get('role', '')
        tech_stack = lead.get('tech_stack', [])
        company_size = lead.get('company_size', '')
        
        # Industry-specific insights
        industry_insights = {
            "SaaS": ["Scalability challenges", "Customer acquisition costs", "Subscription metrics"],
            "FinTech": ["Regulatory compliance", "Security requirements", "Payment processing"],
            "HealthTech": ["HIPAA compliance", "Data security", "Patient experience"],
            "AI/ML": ["Model training costs", "Data infrastructure", "Talent acquisition"],
            "Cybersecurity": ["Threat landscape", "Compliance requirements", "Incident response"],
            "EdTech": ["User engagement", "Content delivery", "Platform scalability"],
            "CleanTech": ["Sustainability goals", "Energy efficiency", "Regulatory incentives"]
        }
        
        if industry in industry_insights:
            insights["potential_pain_points"].extend(industry_insights[industry])
        
        # Role-specific talking points
        role_talking_points = {
            "CTO": ["Technical scalability", "Team productivity", "Infrastructure costs"],
            "CEO": ["Revenue growth", "Market competition", "Operational efficiency"],
            "VP": ["Team performance", "Budget management", "Strategic execution"],
            "Head of": ["Department goals", "Resource allocation", "Cross-functional collaboration"],
            "Director": ["Project delivery", "Team development", "Process improvement"]
        }
        
        for role_key, points in role_talking_points.items():
            if role_key.lower() in role.lower():
                insights["key_talking_points"].extend(points)
                break
        
        # Tech stack based value proposition
        if any(tech in tech_stack for tech in ["AWS", "Azure", "GCP"]):
            insights["value_proposition_focus"] = "Cloud optimization and cost savings"
        elif any(tech in tech_stack for tech in ["React", "Vue.js", "Angular"]):
            insights["value_proposition_focus"] = "Frontend performance and user experience"
        elif any(tech in tech_stack for tech in ["Python", "Node.js", "Java"]):
            insights["value_proposition_focus"] = "Backend scalability and development efficiency"
        else:
            insights["value_proposition_focus"] = "Overall technical efficiency and productivity"
        
        # Company size based competitive angle
        if company_size in ["11-50", "51-200"]:
            insights["competitive_angle"] = "Rapid growth and agility focus"
        elif company_size in ["201-500", "501-1000"]:
            insights["competitive_angle"] = "Enterprise scalability and reliability"
        else:
            insights["competitive_angle"] = "Market leadership and innovation"
        
        return insights

class SalesWorkflowIntegrator:
    """Integrate leads into existing sales workflows and processes"""
    
    def __init__(self):
        self.workflow_stages = {
            "prospecting": {"duration": "1-2 weeks", "activities": ["Initial outreach", "LinkedIn connection", "Email sequence"]},
            "qualification": {"duration": "1 week", "activities": ["Discovery call", "Needs assessment", "BANT qualification"]},
            "demonstration": {"duration": "2 weeks", "activities": ["Product demo", "Technical deep dive", "Use case validation"]},
            "proposal": {"duration": "1-2 weeks", "activities": ["Solution design", "Proposal creation", "Stakeholder alignment"]},
            "negotiation": {"duration": "1-3 weeks", "activities": ["Contract review", "Pricing negotiation", "Legal review"]}
        }
    
    def create_sales_playbook(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Create personalized sales playbook for the lead"""
        business_intel = BusinessLeadIntelligence()
        readiness = business_intel.assess_sales_readiness(lead)
        insights = business_intel.generate_sales_insights(lead)
        
        playbook = {
            "lead_profile": {
                "company": lead.get('company'),
                "contact": lead.get('contact_name'),
                "role": lead.get('role'),
                "industry": lead.get('industry')
            },
            "readiness_assessment": readiness,
            "outreach_strategy": self._define_outreach_strategy(lead, readiness, insights),
            "timeline_projections": self._project_sales_timeline(readiness),
            "success_metrics": self._define_success_metrics(lead)
        }
        
        return playbook
    
    def _define_outreach_strategy(self, lead: Dict, readiness: Dict, insights: Dict) -> Dict[str, Any]:
        """Define personalized outreach strategy"""
        strategy = {
            "first_touch": "",
            "follow_up_sequence": [],
            "channel_mix": [],
            "personalization_elements": []
        }
        
        # Determine first touch based on readiness
        if readiness["stage"] == "hot":
            strategy["first_touch"] = "Personalized video message or phone call"
            strategy["channel_mix"] = ["Phone", "Email", "LinkedIn"]
        elif readiness["stage"] == "warm":
            strategy["first_touch"] = "Value-based email with industry insights"
            strategy["channel_mix"] = ["Email", "LinkedIn", "Content marketing"]
        else:
            strategy["first_touch"] = "Educational content with soft CTA"
            strategy["channel_mix"] = ["Content marketing", "Email", "Social media"]
        
        # Build follow-up sequence
        follow_up_steps = []
        if readiness["stage"] in ["hot", "warm"]:
            follow_up_steps = [
                "Day 2: Share relevant case study",
                "Day 5: Industry insight or article",
                "Day 10: Invitation to webinar or event",
                "Day 15: Final value proposition"
            ]
        else:
            follow_up_steps = [
                "Week 1: Industry trends report",
                "Week 3: Customer success story",
                "Week 6: Product update or feature highlight",
                "Week 9: Re-engagement offer"
            ]
        
        strategy["follow_up_sequence"] = follow_up_steps
        
        # Personalization elements
        personalization = []
        if insights["key_talking_points"]:
            personalization.append(f"Focus on {insights['key_talking_points'][0]}")
        if insights["potential_pain_points"]:
            personalization.append(f"Address {insights['potential_pain_points'][0]}")
        if lead.get('tech_stack'):
            personalization.append(f"Reference {lead['tech_stack'][0]} experience")
        
        strategy["personalization_elements"] = personalization
        
        return strategy
    
    def _project_sales_timeline(self, readiness: Dict) -> Dict[str, str]:
        """Project sales timeline based on lead readiness"""
        base_timeline = {
            "prospecting": "1-2 weeks",
            "qualification": "1-2 weeks", 
            "demonstration": "2-3 weeks",
            "proposal": "2-3 weeks",
            "negotiation": "2-4 weeks"
        }
        
        if readiness["stage"] == "hot":
            # Accelerated timeline for hot leads
            return {k: self._shorten_timeline(v) for k, v in base_timeline.items()}
        elif readiness["stage"] == "cold":
            # Extended timeline for cold leads
            return {k: self._extend_timeline(v) for k, v in base_timeline.items()}
        else:
            return base_timeline
    
    def _shorten_timeline(self, timeline: str) -> str:
        """Shorten timeline by 25%"""
        parts = timeline.split('-')
        if len(parts) == 2:
            return f"{max(1, int(parts[0])-1)}-{int(parts[1])-1} {timeline.split()[-1]}"
        return timeline
    
    def _extend_timeline(self, timeline: str) -> str:
        """Extend timeline by 50%"""
        parts = timeline.split('-')
        if len(parts) == 2:
            return f"{int(parts[0])+1}-{int(parts[1])+1} {timeline.split()[-1]}"
        return timeline
    
    def _define_success_metrics(self, lead: Dict) -> Dict[str, Any]:
        """Define success metrics for this lead"""
        company_size = lead.get('company_size', '')
        
        # Different metrics based on company size
        if company_size in ["201-500", "501-1000"]:
            return {
                "deal_size_target": "$50K - $150K ACV",
                "sales_cycle_target": "60-90 days",
                "conversion_probability": "25-40%",
                "key_metrics": ["Executive sponsorship", "ROI calculation", "Competitive displacement"]
            }
        elif company_size in ["51-200", "101-200"]:
            return {
                "deal_size_target": "$25K - $75K ACV",
                "sales_cycle_target": "45-75 days",
                "conversion_probability": "35-50%",
                "key_metrics": ["Department adoption", "User engagement", "Feature utilization"]
            }
        else:
            return {
                "deal_size_target": "$10K - $30K ACV",
                "sales_cycle_target": "30-60 days",
                "conversion_probability": "45-60%",
                "key_metrics": ["Quick time-to-value", "Ease of implementation", "Immediate pain relief"]
            }

class LeadQualityOptimizer:
    """Optimize lead quality and minimize irrelevant data"""
    
    def __init__(self):
        self.quality_thresholds = {
            "min_engagement_score": 50,
            "min_data_completeness": 0.6,
            "required_fields": ["company", "contact_name", "email", "role"]
        }
    
    def assess_lead_quality(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive lead quality assessment"""
        quality = {
            "overall_score": 0.0,
            "data_completeness": 0.0,
            "contact_accuracy": 0.0,
            "strategic_fit": 0.0,
            "actionability": 0.0,
            "recommendation": "pursue"  # pursue, nurture, discard
        }
        
        # Data completeness (25%)
        complete_fields = sum(1 for field in self.quality_thresholds["required_fields"] if lead.get(field))
        quality["data_completeness"] = complete_fields / len(self.quality_thresholds["required_fields"])
        
        # Contact accuracy (25%)
        accuracy_score = 0.0
        if lead.get('email_valid'):
            accuracy_score += 0.5
        if lead.get('linkedin_url'):
            accuracy_score += 0.3
        if self._validate_contact_name(lead.get('contact_name')):
            accuracy_score += 0.2
        quality["contact_accuracy"] = accuracy_score
        
        # Strategic fit (25%)
        business_intel = BusinessLeadIntelligence()
        quality["strategic_fit"] = business_intel.calculate_business_priority_score(lead) / 100.0
        
        # Actionability (25%)
        action_score = 0.0
        if lead.get('engagement_score', 0) >= self.quality_thresholds["min_engagement_score"]:
            action_score += 0.4
        if quality["data_completeness"] >= self.quality_thresholds["min_data_completeness"]:
            action_score += 0.3
        if quality["contact_accuracy"] >= 0.7:
            action_score += 0.3
        quality["actionability"] = action_score
        
        # Overall score
        quality["overall_score"] = (
            quality["data_completeness"] * 0.25 +
            quality["contact_accuracy"] * 0.25 +
            quality["strategic_fit"] * 0.25 +
            quality["actionability"] * 0.25
        )
        
        # Recommendation
        if quality["overall_score"] >= 0.7:
            quality["recommendation"] = "pursue"
        elif quality["overall_score"] >= 0.5:
            quality["recommendation"] = "nurture"
        else:
            quality["recommendation"] = "discard"
        
        return quality
    
    def _validate_contact_name(self, name: str) -> bool:
        """Validate contact name format"""
        if not name:
            return False
        # Check if name has at least two parts (first and last name)
        name_parts = name.strip().split()
        return len(name_parts) >= 2 and all(len(part) > 1 for part in name_parts)
    
    def filter_high_quality_leads(self, leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter leads to only high-quality, actionable prospects"""
        high_quality_leads = []
        
        for lead in leads:
            quality = self.assess_lead_quality(lead)
            if quality["recommendation"] == "pursue":
                lead['quality_assessment'] = quality
                high_quality_leads.append(lead)
        
        return high_quality_leads

# Initialize business intelligence components
business_intel = BusinessLeadIntelligence()
workflow_integrator = SalesWorkflowIntegrator()
quality_optimizer = LeadQualityOptimizer()

def load_mock_leads() -> List[Dict[str, Any]]:
    """Load mock lead data with business context"""
    base_leads = [
        {
            "id": 1,
            "company": "TechCorp Solutions",
            "contact_name": "Sarah Johnson",
            "email": "sarah.johnson@techcorp.com",
            "role": "CTO",
            "company_size": "201-500",
            "location": "San Francisco, CA",
            "tech_stack": ["React", "Node.js", "AWS", "PostgreSQL"],
            "industry": "SaaS",
            "funding_stage": "Series B",
            "engagement_score": 85,
            "email_valid": True,
            "linkedin_url": "linkedin.com/in/sarahjohnson",
            "last_activity": "2025-10-05"
        },
        {
            "id": 2,
            "company": "DataFlow Analytics",
            "contact_name": "Michael Chen",
            "email": "m.chen@dataflow.io",
            "role": "VP Engineering",
            "company_size": "51-200",
            "location": "Austin, TX",
            "tech_stack": ["Python", "Django", "GCP", "MongoDB"],
            "industry": "Analytics",
            "funding_stage": "Series A",
            "engagement_score": 72,
            "email_valid": True,
            "linkedin_url": "linkedin.com/in/michaelchen",
            "last_activity": "2025-10-04"
        },
        {
            "id": 3,
            "company": "CloudScale Systems",
            "contact_name": "Emily Rodriguez",
            "email": "emily.r@cloudscale.com",
            "role": "Head of Product",
            "company_size": "501-1000",
            "location": "New York, NY",
            "tech_stack": ["Vue.js", "Ruby on Rails", "AWS", "Redis"],
            "industry": "Cloud Infrastructure",
            "funding_stage": "Series C",
            "engagement_score": 91,
            "email_valid": True,
            "linkedin_url": "linkedin.com/in/emilyrodriguez",
            "last_activity": "2025-10-06"
        },
        {
            "id": 4,
            "company": "FinTech Innovations",
            "contact_name": "David Park",
            "email": "david.park@fintech-inn.com",
            "role": "Director of Engineering",
            "company_size": "201-500",
            "location": "Boston, MA",
            "tech_stack": ["React", "Java", "Azure", "MySQL"],
            "industry": "FinTech",
            "funding_stage": "Series B",
            "engagement_score": 78,
            "email_valid": True,
            "linkedin_url": "linkedin.com/in/davidpark",
            "last_activity": "2025-10-03"
        },
        {
            "id": 5,
            "company": "GreenTech Energy",
            "contact_name": "Lisa Thompson",
            "email": "l.thompson@greentech.co",
            "role": "CTO",
            "company_size": "101-200",
            "location": "Seattle, WA",
            "tech_stack": ["Angular", "Python", "AWS", "PostgreSQL"],
            "industry": "CleanTech",
            "funding_stage": "Seed",
            "engagement_score": 65,
            "email_valid": True,
            "linkedin_url": "linkedin.com/in/lisathompson",
            "last_activity": "2025-10-02"
        },
        {
            "id": 6,
            "company": "HealthCare Connect",
            "contact_name": "Robert Williams",
            "email": "r.williams@healthcare-connect.com",
            "role": "VP Technology",
            "company_size": "51-200",
            "location": "Chicago, IL",
            "tech_stack": ["React", "Node.js", "Azure", "MongoDB"],
            "industry": "HealthTech",
            "funding_stage": "Series A",
            "engagement_score": 88,
            "email_valid": True,
            "linkedin_url": "linkedin.com/in/robertwilliams",
            "last_activity": "2025-10-05"
        },
        {
            "id": 7,
            "company": "AI Robotics Lab",
            "contact_name": "Jennifer Kim",
            "email": "jennifer@airobotics.ai",
            "role": "Head of AI",
            "company_size": "11-50",
            "location": "Palo Alto, CA",
            "tech_stack": ["Python", "TensorFlow", "GCP", "PostgreSQL"],
            "industry": "AI/ML",
            "funding_stage": "Seed",
            "engagement_score": 95,
            "email_valid": True,
            "linkedin_url": "linkedin.com/in/jenniferkim",
            "last_activity": "2025-10-07"
        },
        {
            "id": 8,
            "company": "E-Commerce Plus",
            "contact_name": "Mark Anderson",
            "email": "anderson@ecommerceplus.com",
            "role": "Director of Technology",
            "company_size": "201-500",
            "location": "Los Angeles, CA",
            "tech_stack": ["Vue.js", "PHP", "AWS", "MySQL"],
            "industry": "E-Commerce",
            "funding_stage": "Series B",
            "engagement_score": 70,
            "email_valid": True,
            "linkedin_url": "linkedin.com/in/markanderson",
            "last_activity": "2025-10-01"
        },
        {
            "id": 9,
            "company": "SecureNet Solutions",
            "contact_name": "Amanda Martinez",
            "email": "a.martinez@securenet.io",
            "role": "Chief Security Officer",
            "company_size": "101-200",
            "location": "Denver, CO",
            "tech_stack": ["React", "Go", "AWS", "Redis"],
            "industry": "Cybersecurity",
            "funding_stage": "Series A",
            "engagement_score": 82,
            "email_valid": True,
            "linkedin_url": "linkedin.com/in/amandamartinez",
            "last_activity": "2025-10-04"
        },
        {
            "id": 10,
            "company": "EdTech Platform",
            "contact_name": "James Wilson",
            "email": "jwilson@edtechplatform.com",
            "role": "VP Product",
            "company_size": "51-200",
            "location": "Portland, OR",
            "tech_stack": ["React", "Node.js", "GCP", "MongoDB"],
            "industry": "EdTech",
            "funding_stage": "Seed",
            "engagement_score": 68,
            "email_valid": True,
            "linkedin_url": "linkedin.com/in/jameswilson",
            "last_activity": "2025-09-30"
        }
    ]
    
    # Enhance leads with business intelligence
    enhanced_leads = []
    for lead in base_leads:
        enhanced_lead = lead.copy()
        # Add business priority score
        enhanced_lead['business_priority_score'] = business_intel.calculate_business_priority_score(lead)
        # Add sales readiness assessment
        enhanced_lead['sales_readiness'] = business_intel.assess_sales_readiness(lead)
        # Add quality assessment
        enhanced_lead['quality_assessment'] = quality_optimizer.assess_lead_quality(lead)
        
        enhanced_leads.append(enhanced_lead)
    
    return enhanced_leads

def calculate_lead_score(lead: Dict[str, Any]) -> int:
    """
    Enhanced lead scoring with business context
    """
    base_score = lead.get('engagement_score', 50)

    role_scores = {
        'CTO': 25, 'CEO': 25, 'CIO': 25,
        'VP': 20, 'Head of': 20, 'Chief': 25,
        'Director': 15, 'Manager': 10
    }

    for role_keyword, points in role_scores.items():
        if role_keyword.lower() in lead.get('role', '').lower():
            base_score += points
            break

    size_scores = {
        '501-1000': 15, '201-500': 12, '101-200': 10,
        '51-200': 8, '11-50': 5
    }
    base_score += size_scores.get(lead.get('company_size', ''), 0)

    funding_scores = {
        'Series C': 15, 'Series B': 12, 'Series A': 10, 'Seed': 5
    }
    base_score += funding_scores.get(lead.get('funding_stage', ''), 0)

    if lead.get('email_valid'):
        base_score += 10

    # Add business priority bonus (up to 20 points)
    business_priority = lead.get('business_priority_score', 0)
    business_bonus = int((business_priority / 100) * 20)
    base_score += business_bonus

    return min(base_score, 100)

# Existing endpoints remain exactly the same for frontend compatibility
@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Get all leads with optional filtering - ENHANCED with business intelligence"""
    leads = load_mock_leads()

    tech_stack = request.args.get('tech_stack')
    location = request.args.get('location')
    company_size = request.args.get('company_size')
    role = request.args.get('role')
    industry = request.args.get('industry')
    min_score = request.args.get('min_score', type=int)
    high_quality_only = request.args.get('high_quality_only', type=bool, default=False)

    filtered_leads = leads

    if tech_stack:
        filtered_leads = [
            lead for lead in filtered_leads
            if tech_stack.lower() in [tech.lower() for tech in lead.get('tech_stack', [])]
        ]

    if location:
        filtered_leads = [
            lead for lead in filtered_leads
            if location.lower() in lead.get('location', '').lower()
        ]

    if company_size:
        filtered_leads = [
            lead for lead in filtered_leads
            if lead.get('company_size') == company_size
        ]

    if role:
        filtered_leads = [
            lead for lead in filtered_leads
            if role.lower() in lead.get('role', '').lower()
        ]

    if industry:
        filtered_leads = [
            lead for lead in filtered_leads
            if industry.lower() in lead.get('industry', '').lower()
        ]

    for lead in filtered_leads:
        lead['score'] = calculate_lead_score(lead)

    if min_score:
        filtered_leads = [lead for lead in filtered_leads if lead['score'] >= min_score]

    # NEW: Filter for high-quality leads only if requested
    if high_quality_only:
        filtered_leads = quality_optimizer.filter_high_quality_leads(filtered_leads)

    filtered_leads.sort(key=lambda x: x['score'], reverse=True)

    return jsonify({
        'leads': filtered_leads,
        'total': len(filtered_leads)
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data - ENHANCED with business metrics"""
    leads = load_mock_leads()

    for lead in leads:
        lead['score'] = calculate_lead_score(lead)

    tech_stack_count = {}
    for lead in leads:
        for tech in lead.get('tech_stack', []):
            tech_stack_count[tech] = tech_stack_count.get(tech, 0) + 1

    top_technologies = sorted(
        tech_stack_count.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    location_count = {}
    for lead in leads:
        location = lead.get('location', 'Unknown')
        location_count[location] = location_count.get(location, 0) + 1

    industry_count = {}
    for lead in leads:
        industry = lead.get('industry', 'Unknown')
        industry_count[industry] = industry_count.get(industry, 0) + 1

    valid_emails = sum(1 for lead in leads if lead.get('email_valid'))
    avg_score = sum(lead['score'] for lead in leads) / len(leads) if leads else 0
    high_quality_leads = sum(1 for lead in leads if lead['score'] >= 80)

    # NEW: Business intelligence metrics
    high_priority_leads = sum(1 for lead in leads if lead.get('business_priority_score', 0) >= 70)
    sales_ready_leads = sum(1 for lead in leads if lead.get('sales_readiness', {}).get('stage') == 'hot')
    quality_leads = sum(1 for lead in leads if lead.get('quality_assessment', {}).get('recommendation') == 'pursue')

    return jsonify({
        'total_leads': len(leads),
        'valid_emails': valid_emails,
        'avg_score': round(avg_score, 1),
        'high_quality_leads': high_quality_leads,
        'high_priority_leads': high_priority_leads,
        'sales_ready_leads': sales_ready_leads,
        'quality_leads': quality_leads,
        'top_technologies': [{'name': tech, 'count': count} for tech, count in top_technologies],
        'locations': [{'name': loc, 'count': count} for loc, count in location_count.items()],
        'industries': [{'name': ind, 'count': count} for ind, count in industry_count.items()]
    })

@app.route('/api/export', methods=['POST'])
def export_leads():
    """Export filtered leads as CSV - ENHANCED with business fields"""
    data = request.get_json()
    lead_ids = data.get('lead_ids', [])

    leads = load_mock_leads()

    if lead_ids:
        leads = [lead for lead in leads if lead['id'] in lead_ids]

    for lead in leads:
        lead['score'] = calculate_lead_score(lead)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'Company', 'Contact Name', 'Email', 'Role', 'Company Size',
        'Location', 'Tech Stack', 'Industry', 'Funding Stage',
        'Lead Score', 'Business Priority Score', 'Sales Readiness', 
        'Quality Recommendation', 'LinkedIn URL', 'Last Activity'
    ])

    for lead in leads:
        writer.writerow([
            lead.get('company', ''),
            lead.get('contact_name', ''),
            lead.get('email', ''),
            lead.get('role', ''),
            lead.get('company_size', ''),
            lead.get('location', ''),
            ', '.join(lead.get('tech_stack', [])),
            lead.get('industry', ''),
            lead.get('funding_stage', ''),
            lead.get('score', 0),
            lead.get('business_priority_score', 0),
            lead.get('sales_readiness', {}).get('stage', ''),
            lead.get('quality_assessment', {}).get('recommendation', ''),
            lead.get('linkedin_url', ''),
            lead.get('last_activity', '')
        ])

    output.seek(0)

    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': f'attachment; filename=leads_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    }

@app.route('/api/filters/options', methods=['GET'])
def get_filter_options():
    """Get available filter options"""
    leads = load_mock_leads()

    tech_stacks = set()
    locations = set()
    company_sizes = set()
    roles = set()
    industries = set()

    for lead in leads:
        for tech in lead.get('tech_stack', []):
            tech_stacks.add(tech)
        locations.add(lead.get('location', ''))
        company_sizes.add(lead.get('company_size', ''))
        roles.add(lead.get('role', ''))
        industries.add(lead.get('industry', ''))

    return jsonify({
        'tech_stacks': sorted(list(tech_stacks)),
        'locations': sorted(list(locations)),
        'company_sizes': sorted(list(company_sizes)),
        'roles': sorted(list(roles)),
        'industries': sorted(list(industries))
    })

# NEW: Business intelligence endpoints
@app.route('/api/business/priority-leads', methods=['GET'])
def get_priority_leads():
    """Get high-priority leads based on business alignment"""
    leads = load_mock_leads()
    
    # Filter for high business priority
    priority_leads = [lead for lead in leads if lead.get('business_priority_score', 0) >= 70]
    priority_leads.sort(key=lambda x: x['business_priority_score'], reverse=True)
    
    return jsonify({
        'priority_leads': priority_leads,
        'total': len(priority_leads),
        'avg_business_score': round(sum(lead.get('business_priority_score', 0) for lead in priority_leads) / len(priority_leads), 1) if priority_leads else 0
    })

@app.route('/api/business/sales-playbook/<int:lead_id>', methods=['GET'])
def get_sales_playbook(lead_id):
    """Get sales playbook for a specific lead"""
    leads = load_mock_leads()
    lead = next((l for l in leads if l['id'] == lead_id), None)
    
    if not lead:
        return jsonify({'error': 'Lead not found'}), 404
    
    playbook = workflow_integrator.create_sales_playbook(lead)
    
    return jsonify({
        'lead_id': lead_id,
        'playbook': playbook
    })

@app.route('/api/business/quality-report', methods=['GET'])
def get_quality_report():
    """Get comprehensive lead quality report"""
    leads = load_mock_leads()
    
    quality_distribution = {
        'pursue': 0,
        'nurture': 0,
        'discard': 0
    }
    
    quality_scores = []
    business_scores = []
    
    for lead in leads:
        recommendation = lead.get('quality_assessment', {}).get('recommendation', 'discard')
        quality_distribution[recommendation] += 1
        quality_scores.append(lead.get('quality_assessment', {}).get('overall_score', 0))
        business_scores.append(lead.get('business_priority_score', 0))
    
    return jsonify({
        'quality_distribution': quality_distribution,
        'avg_quality_score': round(sum(quality_scores) / len(quality_scores), 2) if quality_scores else 0,
        'avg_business_score': round(sum(business_scores) / len(business_scores), 1) if business_scores else 0,
        'actionable_leads_count': quality_distribution['pursue'],
        'actionable_percentage': round((quality_distribution['pursue'] / len(leads)) * 100, 1) if leads else 0
    })

@app.route('/api/business/industry-insights', methods=['GET'])
def get_industry_insights():
    """Get insights by industry"""
    leads = load_mock_leads()
    
    industry_metrics = {}
    
    for lead in leads:
        industry = lead.get('industry', 'Unknown')
        if industry not in industry_metrics:
            industry_metrics[industry] = {
                'count': 0,
                'avg_score': 0,
                'avg_business_priority': 0,
                'high_quality_count': 0
            }
        
        metrics = industry_metrics[industry]
        metrics['count'] += 1
        metrics['avg_score'] += lead.get('score', 0)
        metrics['avg_business_priority'] += lead.get('business_priority_score', 0)
        
        if lead.get('quality_assessment', {}).get('recommendation') == 'pursue':
            metrics['high_quality_count'] += 1
    
    # Calculate averages
    for industry, metrics in industry_metrics.items():
        if metrics['count'] > 0:
            metrics['avg_score'] = round(metrics['avg_score'] / metrics['count'], 1)
            metrics['avg_business_priority'] = round(metrics['avg_business_priority'] / metrics['count'], 1)
            metrics['high_quality_percentage'] = round((metrics['high_quality_count'] / metrics['count']) * 100, 1)
    
    return jsonify({
        'industry_insights': industry_metrics,
        'top_industries': sorted(
            industry_metrics.items(),
            key=lambda x: x[1]['high_quality_count'],
            reverse=True
        )[:5]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)