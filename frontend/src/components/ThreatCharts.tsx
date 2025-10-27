import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'
import { ThreatData } from '../types'
import { BarChart3, PieChart as PieChartIcon, TrendingUp } from 'lucide-react'

interface ThreatChartsProps {
  threatData: ThreatData
}

const COLORS = ['#3b82f6', '#ef4444', '#f59e0b', '#10b981', '#8b5cf6', '#ec4899']

export default function ThreatCharts({ threatData }: ThreatChartsProps) {
  return (
    <div className="space-y-6">
      {/* Hourly Threats Chart */}
      <div className="bg-card border border-border rounded-lg p-6">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-5 h-5 text-primary" />
          <h2 className="text-lg font-semibold text-foreground">Hourly Threat Activity</h2>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={threatData.hourly_stats}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="time" 
              stroke="#9ca3af"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              stroke="#9ca3af"
              style={{ fontSize: '12px' }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1f2937', 
                border: '1px solid #374151',
                borderRadius: '8px'
              }}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="threats" 
              stroke="#ef4444" 
              strokeWidth={2}
              name="Threats"
            />
            <Line 
              type="monotone" 
              dataKey="blocked" 
              stroke="#10b981" 
              strokeWidth={2}
              name="Blocked"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Threat Distribution */}
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-2 mb-4">
            <PieChartIcon className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">Threat Distribution</h2>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={threatData.threat_distribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {threatData.threat_distribution.map((_entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: '1px solid #374151',
                  borderRadius: '8px'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Severity Breakdown */}
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">Severity Breakdown</h2>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart 
              data={[
                { name: 'Low', value: threatData.severity_breakdown.Low, fill: '#3b82f6' },
                { name: 'Medium', value: threatData.severity_breakdown.Medium, fill: '#f59e0b' },
                { name: 'High', value: threatData.severity_breakdown.High, fill: '#ef4444' },
                { name: 'Critical', value: threatData.severity_breakdown.Critical, fill: '#dc2626' }
              ]}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis 
                dataKey="name" 
                stroke="#9ca3af"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="#9ca3af"
                style={{ fontSize: '12px' }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: '1px solid #374151',
                  borderRadius: '8px'
                }}
              />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {[
                  { name: 'Low', value: threatData.severity_breakdown.Low, fill: '#3b82f6' },
                  { name: 'Medium', value: threatData.severity_breakdown.Medium, fill: '#f59e0b' },
                  { name: 'High', value: threatData.severity_breakdown.High, fill: '#ef4444' },
                  { name: 'Critical', value: threatData.severity_breakdown.Critical, fill: '#dc2626' }
                ].map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
