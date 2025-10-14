import { Lead, FilterOptions, Analytics } from '../types/lead';

const API_BASE_URL = 'http://localhost:5000/api';

export const api = {
  async getLeads(filters?: {
    tech_stack?: string;
    location?: string;
    company_size?: string;
    role?: string;
    industry?: string;
    min_score?: number;
  }): Promise<{ leads: Lead[]; total: number }> {
    const params = new URLSearchParams();

    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value.toString());
        }
      });
    }

    const response = await fetch(`${API_BASE_URL}/leads?${params}`);
    if (!response.ok) throw new Error('Failed to fetch leads');
    return response.json();
  },

  async getAnalytics(): Promise<Analytics> {
    const response = await fetch(`${API_BASE_URL}/analytics`);
    if (!response.ok) throw new Error('Failed to fetch analytics');
    return response.json();
  },

  async exportLeads(leadIds: number[]): Promise<Blob> {
    const response = await fetch(`${API_BASE_URL}/export`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ lead_ids: leadIds }),
    });
    if (!response.ok) throw new Error('Failed to export leads');
    return response.blob();
  },

  async getFilterOptions(): Promise<FilterOptions> {
    const response = await fetch(`${API_BASE_URL}/filters/options`);
    if (!response.ok) throw new Error('Failed to fetch filter options');
    return response.json();
  },
};
