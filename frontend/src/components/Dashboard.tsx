import { useState, useEffect } from 'react'
import { Socket } from 'socket.io-client'
import axios from 'axios'
import StatsCards from './StatsCards'
import AlertsList from './AlertsList'
import ThreatCharts from './ThreatCharts'
import { Alert, NetworkStats, ThreatData } from '../types'

interface DashboardProps {
  alerts: Alert[]
  stats: NetworkStats
  socket: Socket | null
}

export default function Dashboard({ alerts, stats, socket }: DashboardProps) {
  const [threatData, setThreatData] = useState<ThreatData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchThreatData()
    const interval = setInterval(fetchThreatData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchThreatData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/threats')
      setThreatData(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching threat data:', error)
      setLoading(false)
    }
  }

  return (
    <main className="container mx-auto px-4 py-6 space-y-6">
      <StatsCards stats={stats} />
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          {!loading && threatData && (
            <ThreatCharts threatData={threatData} />
          )}
        </div>
        
        <div className="lg:col-span-1">
          <AlertsList alerts={alerts} />
        </div>
      </div>
    </main>
  )
}
