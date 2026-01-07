import { useState } from 'react'
import { AlertTriangle, Clock, MapPin, Ban } from 'lucide-react'
import { Socket } from 'socket.io-client'
import { Alert } from '../types'
import { formatTimestamp, getSeverityColor, getStatusColor } from '../lib/utils'
import axios from 'axios'

interface AlertsListProps {
  alerts: Alert[]
  socket: Socket | null
}

export default function AlertsList({ alerts, socket }: AlertsListProps) {
  const [blockingIps, setBlockingIps] = useState<Set<number>>(new Set())
  const [blockedAlerts, setBlockedAlerts] = useState<Set<number>>(new Set())

  const handleBlockIP = async (alert: Alert) => {
    if (blockedAlerts.has(alert.id) || blockingIps.has(alert.id)) return

    setBlockingIps(prev => new Set(prev).add(alert.id))

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
      await axios.post(`${backendUrl}/api/block-ip`, {
        ip: alert.source_ip,
        alert_id: alert.id
      })

      setBlockedAlerts(prev => new Set(prev).add(alert.id))
      alert.status = 'Blocked'
      
      // Request stats update from server
      if (socket) {
        socket.emit('request_stats')
      }
    } catch (error) {
      console.error('Error blocking IP:', error)
    } finally {
      setBlockingIps(prev => {
        const newSet = new Set(prev)
        newSet.delete(alert.id)
        return newSet
      })
    }
  }
  return (
    <div className="bg-card border border-border rounded-lg h-[600px] flex flex-col">
      <div className="p-4 border-b border-border">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-primary" />
          <h2 className="text-lg font-semibold text-foreground">Live Alerts</h2>
          <span className="ml-auto text-sm text-muted-foreground">
            {alerts.length} alerts
          </span>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {alerts.length === 0 ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <p>No alerts detected</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className="bg-background border border-border rounded-lg p-4 hover:border-primary/50 transition-colors"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-1 rounded text-xs font-medium border ${getSeverityColor(alert.severity)}`}>
                    {alert.severity}
                  </span>
                  <span className={`px-2 py-1 rounded text-xs font-medium border ${getStatusColor(alert.status)}`}>
                    {alert.status}
                  </span>
                </div>
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Clock className="w-3 h-3" />
                  {formatTimestamp(alert.timestamp)}
                </div>
              </div>
              
              <h3 className="font-semibold text-foreground mb-2">
                {alert.threat_type}
              </h3>
              
              <p className="text-sm text-muted-foreground mb-3">
                {alert.description}
              </p>
              
              <div className="grid grid-cols-2 gap-2 text-xs mb-3">
                <div className="flex items-center gap-1 text-muted-foreground">
                  <MapPin className="w-3 h-3" />
                  <span>Source: {alert.source_ip}</span>
                </div>
                <div className="flex items-center gap-1 text-muted-foreground">
                  <MapPin className="w-3 h-3" />
                  <span>Dest: {alert.destination_ip}</span>
                </div>
                <div className="text-muted-foreground">
                  Port: {alert.port}
                </div>
                <div className="text-muted-foreground">
                  Protocol: {alert.protocol}
                </div>
              </div>
              
              {alert.status !== 'Blocked' && !blockedAlerts.has(alert.id) && (
                <button
                  onClick={() => handleBlockIP(alert)}
                  disabled={blockingIps.has(alert.id)}
                  className="w-full mt-2 px-3 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-500 border border-red-500/30 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Ban className="w-4 h-4" />
                  {blockingIps.has(alert.id) ? 'Blocking...' : 'Block IP Address'}
                </button>
              )}
              
              {(alert.status === 'Blocked' || blockedAlerts.has(alert.id)) && (
                <div className="w-full mt-2 px-3 py-2 bg-green-500/10 text-green-500 border border-green-500/30 rounded-lg text-sm font-medium text-center">
                  ✓ IP Blocked Successfully
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
