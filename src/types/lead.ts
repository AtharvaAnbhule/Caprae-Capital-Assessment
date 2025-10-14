export interface Lead {
  id: number;
  company: string;
  contact_name: string;
  email: string;
  role: string;
  company_size: string;
  location: string;
  tech_stack: string[];
  industry: string;
  funding_stage: string;
  engagement_score: number;
  email_valid: boolean;
  linkedin_url: string;
  last_activity: string;
  score?: number;
}

export interface FilterOptions {
  tech_stacks: string[];
  locations: string[];
  company_sizes: string[];
  roles: string[];
  industries: string[];
}

export interface Analytics {
  total_leads: number;
  valid_emails: number;
  avg_score: number;
  high_quality_leads: number;
  top_technologies: { name: string; count: number }[];
  locations: { name: string; count: number }[];
  industries: { name: string; count: number }[];
}
