import { Activity, Shield, Ban, Network } from 'lucide-react'
import { NetworkStats } from '../types'

interface StatsCardsProps {
  stats: NetworkStats
}

export default function StatsCards({ stats }: StatsCardsProps) {
  const cards = [
    {
      title: 'Total Packets',
      value: stats.total_packets.toLocaleString(),
      icon: Activity,
      color: 'text-blue-500',
      bgColor: 'bg-blue-500/10',
      borderColor: 'border-blue-500/20'
    },
    {
      title: 'Threats Detected',
      value: stats.threats_detected.toLocaleString(),
      icon: Shield,
      color: 'text-red-500',
      bgColor: 'bg-red-500/10',
      borderColor: 'border-red-500/20'
    },
    {
      title: 'Blocked IPs',
      value: stats.blocked_ips.toLocaleString(),
      icon: Ban,
      color: 'text-orange-500',
      bgColor: 'bg-orange-500/10',
      borderColor: 'border-orange-500/20'
    },
    {
      title: 'Active Connections',
      value: stats.active_connections.toLocaleString(),
      icon: Network,
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
      borderColor: 'border-green-500/20'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, index) => {
        const Icon = card.icon
        return (
          <div
            key={index}
            className={`bg-card border ${card.borderColor} rounded-lg p-6 hover:shadow-lg transition-shadow`}
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 ${card.bgColor} rounded-lg`}>
                <Icon className={`w-6 h-6 ${card.color}`} />
              </div>
            </div>
            <div>
              <p className="text-sm text-muted-foreground mb-1">{card.title}</p>
              <p className="text-3xl font-bold text-foreground">{card.value}</p>
            </div>
          </div>
        )
      })}
    </div>
  )
}
