import { useState, useEffect } from 'react'
import { io, Socket } from 'socket.io-client'
import Dashboard from './components/Dashboard'
import Header from './components/Header'
import LandingPage from './components/LandingPage'
import { Alert, NetworkStats } from './types'
import AuthWrapper from './components/Auth/AuthWrapper'

function App() {
  const [showDashboard, setShowDashboard] = useState(false)
  const [socket, setSocket] = useState<Socket | null>(null)
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [stats, setStats] = useState<NetworkStats>({
    total_packets: 0,
    threats_detected: 0,
    blocked_ips: 0,
    active_connections: 0
  })
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    // Only initialize socket when dashboard is shown
    if (!showDashboard) return

    // Initialize Socket.IO connection with better error handling
    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
    const newSocket = io(backendUrl, {
      transports: ['polling', 'websocket'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5
    })

    newSocket.on('connect', () => {
      console.log('✅ Connected to IDS Backend')
      setIsConnected(true)
    })

    newSocket.on('disconnect', () => {
      console.log('❌ Disconnected from server')
      setIsConnected(false)
    })

    newSocket.on('connect_error', (error) => {
      console.log('⚠️ Connection error:', error.message)
      setIsConnected(false)
    })

    newSocket.on('new_alert', (alert: Alert) => {
      setAlerts(prev => [alert, ...prev].slice(0, 50))
    })

    newSocket.on('stats_update', (newStats: NetworkStats) => {
      setStats(newStats)
    })

    setSocket(newSocket)

    return () => {
      newSocket.close()
    }
  }, [showDashboard])

  return (
    <AuthWrapper>
      {!showDashboard ? (
        <LandingPage onEnterDashboard={() => setShowDashboard(true)} />
      ) : (
        <div className="min-h-screen bg-background">
          <Header isConnected={isConnected} />
          <Dashboard 
            alerts={alerts} 
            stats={stats}
            socket={socket}
          />
        </div>
      )}
    </AuthWrapper>
  )
}

export default App
