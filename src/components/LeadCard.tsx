import { Building2, Mail, MapPin, Users, TrendingUp, Briefcase, DollarSign, CheckCircle2, ExternalLink } from 'lucide-react';
import { Lead } from '../types/lead';

interface LeadCardProps {
  lead: Lead;
  isSelected: boolean;
  onToggleSelect: (id: number) => void;
}

export function LeadCard({ lead, isSelected, onToggleSelect }: LeadCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50';
    if (score >= 60) return 'text-blue-600 bg-blue-50';
    return 'text-gray-600 bg-gray-50';
  };

  const getScoreBadge = (score: number) => {
    if (score >= 80) return 'High Priority';
    if (score >= 60) return 'Medium Priority';
    return 'Low Priority';
  };

  return (
    <div
      className={`bg-white rounded-lg shadow-sm border-2 transition-all hover:shadow-md ${
        isSelected ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-200'
      }`}
    >
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <input
                type="checkbox"
                checked={isSelected}
                onChange={() => onToggleSelect(lead.id)}
                className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
              />
              <h3 className="text-xl font-semibold text-gray-900">{lead.company}</h3>
            </div>
            <div className="flex items-center gap-2 text-gray-700 ml-7">
              <Briefcase className="w-4 h-4" />
              <span className="font-medium">{lead.contact_name}</span>
              <span className="text-gray-400">•</span>
              <span className="text-sm">{lead.role}</span>
            </div>
          </div>
          <div className="flex flex-col items-end gap-2">
            <div className={`px-3 py-1 rounded-full text-sm font-semibold ${getScoreColor(lead.score || 0)}`}>
              <div className="flex items-center gap-1">
                <TrendingUp className="w-4 h-4" />
                {lead.score || 0}
              </div>
            </div>
            <span className="text-xs font-medium text-gray-500">
              {getScoreBadge(lead.score || 0)}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div className="flex items-center gap-2 text-gray-700">
            <Mail className="w-4 h-4 text-gray-400" />
            <a
              href={`mailto:${lead.email}`}
              className="text-blue-600 hover:text-blue-700 hover:underline text-sm"
            >
              {lead.email}
            </a>
            {lead.email_valid && (
              <CheckCircle2 className="w-4 h-4 text-green-500" />
            )}
          </div>

          <div className="flex items-center gap-2 text-gray-700">
            <MapPin className="w-4 h-4 text-gray-400" />
            <span className="text-sm">{lead.location}</span>
          </div>

          <div className="flex items-center gap-2 text-gray-700">
            <Users className="w-4 h-4 text-gray-400" />
            <span className="text-sm">{lead.company_size} employees</span>
          </div>

          <div className="flex items-center gap-2 text-gray-700">
            <DollarSign className="w-4 h-4 text-gray-400" />
            <span className="text-sm">{lead.funding_stage}</span>
          </div>

          <div className="flex items-center gap-2 text-gray-700">
            <Building2 className="w-4 h-4 text-gray-400" />
            <span className="text-sm">{lead.industry}</span>
          </div>

          <div className="flex items-center gap-2 text-gray-700">
            <ExternalLink className="w-4 h-4 text-gray-400" />
            <a
              href={`https://${lead.linkedin_url}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-700 hover:underline text-sm"
            >
              LinkedIn Profile
            </a>
          </div>
        </div>

        <div className="border-t border-gray-100 pt-4">
          <div className="flex flex-wrap gap-2">
            <span className="text-xs font-medium text-gray-500">Tech Stack:</span>
            {lead.tech_stack.map((tech) => (
              <span
                key={tech}
                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
              >
                {tech}
              </span>
            ))}
          </div>
          <div className="mt-2 text-xs text-gray-500">
            Last Activity: {new Date(lead.last_activity).toLocaleDateString()}
          </div>
        </div>
      </div>
    </div>
  );
}
