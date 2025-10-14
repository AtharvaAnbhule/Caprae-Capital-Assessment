import { useState, useEffect, useCallback } from "react";
import { Download, Zap, CheckSquare, Square } from "lucide-react";
import { LeadCard } from "./components/LeadCard";
import { FilterBar } from "./components/FilterBar";
import { AnalyticsDashboard } from "./components/AnalyticsDashboard";
import { api } from "./services/api";
import { Lead, FilterOptions, Analytics } from "./types/lead";
import isEqual from "lodash.isequal";

function App() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    tech_stacks: [],
    locations: [],
    company_sizes: [],
    roles: [],
    industries: [],
  });
  const [selectedLeads, setSelectedLeads] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);
  const [filters, setFilters] = useState<Record<string, any>>({});

  // Load analytics & filter options once
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [analyticsData, options] = await Promise.all([
          api.getAnalytics(),
          api.getFilterOptions(),
        ]);
        setAnalytics(analyticsData);
        setFilterOptions(options);
      } catch (error) {
        console.error("Error loading initial data:", error);
      }
    };

    loadInitialData();
  }, []);

  // Load leads whenever filters change (debounced)
  useEffect(() => {
    let timeout: NodeJS.Timeout;
    const fetchLeads = async () => {
      setLoading(true);
      try {
        const data = await api.getLeads(filters);
        setLeads(data.leads);
      } catch (error) {
        console.error("Error loading leads:", error);
      } finally {
        setLoading(false);
      }
    };

    timeout = setTimeout(fetchLeads, 300); // 300ms debounce

    return () => clearTimeout(timeout);
  }, [filters]);

  // Only update filters if values actually changed
  const handleFilterChange = useCallback((newFilters: Record<string, any>) => {
    setFilters((prev) => (isEqual(prev, newFilters) ? prev : newFilters));
  }, []);

  const handleToggleSelect = (id: number) => {
    setSelectedLeads((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) newSet.delete(id);
      else newSet.add(id);
      return newSet;
    });
  };

  const handleSelectAll = () => {
    if (selectedLeads.size === leads.length) setSelectedLeads(new Set());
    else setSelectedLeads(new Set(leads.map((lead) => lead.id)));
  };

  const handleExport = async () => {
    if (selectedLeads.size === 0) {
      alert("Please select at least one lead to export");
      return;
    }

    setExporting(true);
    try {
      const blob = await api.exportLeads(Array.from(selectedLeads));
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `leads_export_${new Date().toISOString().split("T")[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Error exporting leads:", error);
      alert("Failed to export leads");
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-blue-600 to-cyan-500 p-2 rounded-lg">
              <Zap className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                LeadSquatch Pro
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Intelligent Lead Generation & Filtering Platform
              </p>
            </div>
          </div>

          <button
            onClick={handleExport}
            disabled={selectedLeads.size === 0 || exporting}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              selectedLeads.size === 0
                ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                : "bg-gradient-to-r from-blue-600 to-cyan-500 text-white hover:from-blue-700 hover:to-cyan-600 shadow-md hover:shadow-lg"
            }`}>
            <Download className="w-5 h-5" />
            {exporting ? "Exporting..." : `Export (${selectedLeads.size})`}
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <AnalyticsDashboard analytics={analytics} />

        <FilterBar
          onFilterChange={handleFilterChange}
          filterOptions={filterOptions}
        />

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={handleSelectAll}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors">
              {selectedLeads.size === leads.length && leads.length > 0 ? (
                <CheckSquare className="w-5 h-5 text-blue-600" />
              ) : (
                <Square className="w-5 h-5" />
              )}
              {selectedLeads.size === leads.length && leads.length > 0
                ? "Deselect All"
                : "Select All"}
            </button>
            {selectedLeads.size > 0 && (
              <div className="text-sm text-gray-600">
                <span className="font-medium text-blue-600">
                  {selectedLeads.size} selected
                </span>
              </div>
            )}
          </div>
          <div className="text-sm font-medium text-gray-700">
            Showing {leads.length} lead{leads.length !== 1 ? "s" : ""}
          </div>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 gap-6">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        ) : leads.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
            <div className="text-gray-400 mb-4">
              <Zap className="w-16 h-16 mx-auto" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No leads found
            </h3>
            <p className="text-gray-600">
              Try adjusting your filters to see more results
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {leads.map((lead) => (
              <LeadCard
                key={lead.id}
                lead={lead}
                isSelected={selectedLeads.has(lead.id)}
                onToggleSelect={handleToggleSelect}
              />
            ))}
          </div>
        )}
      </main>

      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-600">
            LeadSquatch Pro - Professional Lead Generation & Filtering Tool
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
