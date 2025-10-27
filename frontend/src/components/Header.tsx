import { Shield, Activity, LogOut } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

interface HeaderProps {
  isConnected: boolean
}

export default function Header({ isConnected }: HeaderProps) {
  const { signOut, user } = useAuth()
  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Shield className="w-8 h-8 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">
                Intrusion Detection System
              </h1>
              <p className="text-sm text-muted-foreground">
                Real-time Network Security Monitoring
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className={`flex items-center gap-2 px-4 py-2 rounded-lg border ${
              isConnected 
                ? 'bg-green-500/10 border-green-500/20 text-green-500' 
                : 'bg-red-500/10 border-red-500/20 text-red-500'
            }`}>
              <Activity className={`w-4 h-4 ${isConnected ? 'animate-pulse' : ''}`} />
              <span className="text-sm font-medium">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
            
            <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-700/50 border border-slate-600">
              <span className="text-sm text-slate-300">{user?.email}</span>
            </div>
            
            <button
              onClick={() => signOut()}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 border border-red-500/20 hover:border-red-500/30 text-red-400 hover:text-red-300 transition-colors"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
              <span className="text-sm font-medium">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
