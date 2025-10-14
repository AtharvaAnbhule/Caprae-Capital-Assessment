import { TrendingUp, Users, CheckCircle2, Target, BarChart3 } from 'lucide-react';
import { Analytics } from '../types/lead';

interface AnalyticsDashboardProps {
  analytics: Analytics | null;
}

export function AnalyticsDashboard({ analytics }: AnalyticsDashboardProps) {
  if (!analytics) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-6">
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-4">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    );
  }

  const stats = [
    {
      label: 'Total Leads',
      value: analytics.total_leads,
      icon: Users,
      color: 'bg-blue-500',
    },
    {
      label: 'Valid Emails',
      value: analytics.valid_emails,
      icon: CheckCircle2,
      color: 'bg-green-500',
    },
    {
      label: 'High Quality Leads',
      value: analytics.high_quality_leads,
      icon: Target,
      color: 'bg-orange-500',
    },
    {
      label: 'Avg Lead Score',
      value: analytics.avg_score.toFixed(1),
      icon: TrendingUp,
      color: 'bg-cyan-500',
    },
  ];

  return (
    <div className="mb-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div
              key={stat.label}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">
                    {stat.label}
                  </p>
                  <p className="text-3xl font-bold text-gray-900">
                    {stat.value}
                  </p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="w-5 h-5 text-gray-600" />
            <h3 className="text-lg font-semibold text-gray-900">
              Top Technologies
            </h3>
          </div>
          <div className="space-y-3">
            {analytics.top_technologies.map((tech) => (
              <div key={tech.name} className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">
                  {tech.name}
                </span>
                <div className="flex items-center gap-2">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{
                        width: `${(tech.count / analytics.total_leads) * 100}%`,
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold text-gray-900 w-8 text-right">
                    {tech.count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="w-5 h-5 text-gray-600" />
            <h3 className="text-lg font-semibold text-gray-900">
              Industries
            </h3>
          </div>
          <div className="space-y-3">
            {analytics.industries.slice(0, 5).map((industry) => (
              <div
                key={industry.name}
                className="flex items-center justify-between"
              >
                <span className="text-sm font-medium text-gray-700">
                  {industry.name}
                </span>
                <div className="flex items-center gap-2">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-green-600 h-2 rounded-full transition-all"
                      style={{
                        width: `${(industry.count / analytics.total_leads) * 100}%`,
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold text-gray-900 w-8 text-right">
                    {industry.count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
