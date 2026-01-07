import { useState, useEffect } from 'react'
import { BarChart3, TrendingUp, Shield, AlertTriangle, Download } from 'lucide-react'
import axios from 'axios'
import { Alert, ThreatData } from '../types'
import {
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
  ResponsiveContainer,
  Area,
  AreaChart
} from 'recharts'

interface AnalyticsPageProps {
  alerts: Alert[]
}

export default function AnalyticsPage({ alerts }: AnalyticsPageProps) {
  const [threatData, setThreatData] = useState<ThreatData | null>(null)
  const [loading, setLoading] = useState(true)
  const [dateRange, setDateRange] = useState('24h')

  useEffect(() => {
    fetchThreatData()
  }, [dateRange])

  const fetchThreatData = async () => {
    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
      const response = await axios.get(`${backendUrl}/api/threats`)
      setThreatData(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching threat data:', error)
      setLoading(false)
    }
  }

  const exportReport = () => {
    const reportData = {
      generated: new Date().toISOString(),
      dateRange,
      totalAlerts: alerts.length,
      threatData,
      alerts: alerts.slice(0, 100)
    }
    
    const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `ids-report-${new Date().toISOString().split('T')[0]}.json`
    a.click()
  }

  const COLORS = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899']

  // Calculate statistics
  const criticalAlerts = alerts.filter(a => a.severity === 'Critical').length
  const highAlerts = alerts.filter(a => a.severity === 'High').length
  const mediumAlerts = alerts.filter(a => a.severity === 'Medium').length
  const lowAlerts = alerts.filter(a => a.severity === 'Low').length

  const blockedCount = alerts.filter(a => a.status === 'Blocked').length
  const activeCount = alerts.filter(a => a.status === 'Active').length

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-3">
            <BarChart3 className="w-8 h-8 text-primary" />
            Analytics & Reports
          </h1>
          <p className="text-muted-foreground mt-1">
            Comprehensive threat analysis and insights
          </p>
        </div>
        
        <div className="flex items-center gap-3">
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="px-4 py-2 bg-card border border-border rounded-lg text-foreground"
          >
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>
          
          <button
            onClick={exportReport}
            className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg transition-colors"
          >
            <Download className="w-4 h-4" />
            Export Report
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total Alerts</p>
              <p className="text-3xl font-bold text-foreground mt-1">{alerts.length}</p>
            </div>
            <AlertTriangle className="w-10 h-10 text-blue-500" />
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Critical Threats</p>
              <p className="text-3xl font-bold text-red-500 mt-1">{criticalAlerts}</p>
            </div>
            <Shield className="w-10 h-10 text-red-500" />
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Blocked</p>
              <p className="text-3xl font-bold text-green-500 mt-1">{blockedCount}</p>
            </div>
            <Shield className="w-10 h-10 text-green-500" />
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Active Threats</p>
              <p className="text-3xl font-bold text-orange-500 mt-1">{activeCount}</p>
            </div>
            <TrendingUp className="w-10 h-10 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Hourly Threat Trend */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Threat Trend (24h)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={threatData?.hourly_stats || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                labelStyle={{ color: '#f3f4f6' }}
              />
              <Legend />
              <Area type="monotone" dataKey="threats" stackId="1" stroke="#ef4444" fill="#ef4444" />
              <Area type="monotone" dataKey="blocked" stackId="1" stroke="#10b981" fill="#10b981" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Threat Distribution */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Threat Type Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={threatData?.threat_distribution || []}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {(threatData?.threat_distribution || []).map((_entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Severity Breakdown */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Severity Breakdown</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={[
              { name: 'Critical', value: criticalAlerts, fill: '#ef4444' },
              { name: 'High', value: highAlerts, fill: '#f59e0b' },
              { name: 'Medium', value: mediumAlerts, fill: '#3b82f6' },
              { name: 'Low', value: lowAlerts, fill: '#10b981' }
            ]}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                labelStyle={{ color: '#f3f4f6' }}
              />
              <Bar dataKey="value" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Protocol Distribution */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Protocol Distribution</h3>
          <div className="space-y-4">
            {['TCP', 'UDP', 'HTTP', 'HTTPS', 'ICMP'].map((protocol) => {
              const count = alerts.filter(a => a.protocol === protocol).length
              const percentage = alerts.length > 0 ? (count / alerts.length) * 100 : 0
              
              return (
                <div key={protocol}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-foreground">{protocol}</span>
                    <span className="text-muted-foreground">{count} ({percentage.toFixed(1)}%)</span>
                  </div>
                  <div className="w-full bg-secondary rounded-full h-2">
                    <div
                      className="bg-primary h-2 rounded-full transition-all"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Top Threat Sources */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Top Threat Sources</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 text-muted-foreground font-medium">Source IP</th>
                <th className="text-left py-3 px-4 text-muted-foreground font-medium">Threat Count</th>
                <th className="text-left py-3 px-4 text-muted-foreground font-medium">Most Common Type</th>
                <th className="text-left py-3 px-4 text-muted-foreground font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(
                alerts.reduce((acc, alert) => {
                  if (!acc[alert.source_ip]) {
                    acc[alert.source_ip] = { count: 0, types: {}, status: alert.status }
                  }
                  acc[alert.source_ip].count++
                  acc[alert.source_ip].types[alert.threat_type] = 
                    (acc[alert.source_ip].types[alert.threat_type] || 0) + 1
                  return acc
                }, {} as Record<string, { count: number; types: Record<string, number>; status: string }>)
              )
                .sort(([, a], [, b]) => b.count - a.count)
                .slice(0, 10)
                .map(([ip, data]) => {
                  const mostCommonType = Object.entries(data.types)
                    .sort(([, a], [, b]) => b - a)[0][0]
                  
                  return (
                    <tr key={ip} className="border-b border-border hover:bg-accent/50">
                      <td className="py-3 px-4 text-foreground font-mono text-sm">{ip}</td>
                      <td className="py-3 px-4 text-foreground">{data.count}</td>
                      <td className="py-3 px-4 text-foreground">{mostCommonType}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          data.status === 'Blocked' ? 'bg-green-500/20 text-green-400' :
                          data.status === 'Active' ? 'bg-red-500/20 text-red-400' :
                          'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {data.status}
                        </span>
                      </td>
                    </tr>
                  )
                })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
