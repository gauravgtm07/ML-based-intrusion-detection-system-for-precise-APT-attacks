export interface Alert {
  id: number
  timestamp: string
  source_ip: string
  destination_ip: string
  threat_type: string
  severity: 'Low' | 'Medium' | 'High' | 'Critical'
  status: 'Active' | 'Blocked' | 'Investigating'
  description: string
  port: number
  protocol: string
}

export interface NetworkStats {
  total_packets: number
  threats_detected: number
  blocked_ips: number
  active_connections: number
}

export interface ThreatData {
  hourly_stats: HourlyStat[]
  threat_distribution: ThreatDistribution[]
  severity_breakdown: SeverityBreakdown
}

export interface HourlyStat {
  time: string
  threats: number
  blocked: number
  allowed: number
}

export interface ThreatDistribution {
  name: string
  value: number
}

export interface SeverityBreakdown {
  Low: number
  Medium: number
  High: number
  Critical: number
}
