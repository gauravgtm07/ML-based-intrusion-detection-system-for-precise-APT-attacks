import { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import Login from './Login'
import Signup from './Signup'

interface AuthWrapperProps {
  children: React.ReactNode
}

export default function AuthWrapper({ children }: AuthWrapperProps) {
  const { user, loading } = useAuth()
  const [showLogin, setShowLogin] = useState(true)

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
          <p className="mt-4 text-slate-300">Loading...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return showLogin ? (
      <Login onSwitchToSignup={() => setShowLogin(false)} />
    ) : (
      <Signup onSwitchToLogin={() => setShowLogin(true)} />
    )
  }

  return <>{children}</>
}
