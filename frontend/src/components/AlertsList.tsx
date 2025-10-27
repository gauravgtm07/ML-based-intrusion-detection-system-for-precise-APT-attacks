import { AlertTriangle, Clock, MapPin } from 'lucide-react'
import { Alert } from '../types'
import { formatTimestamp, getSeverityColor, getStatusColor } from '../lib/utils'

interface AlertsListProps {
  alerts: Alert[]
}

export default function AlertsList({ alerts }: AlertsListProps) {
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
              
              <div className="grid grid-cols-2 gap-2 text-xs">
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
            </div>
          ))
        )}
      </div>
    </div>
  )
}
