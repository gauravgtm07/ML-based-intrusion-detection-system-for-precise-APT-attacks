import { Shield, Activity, Bell, BarChart3, Lock, Zap, Eye, Network, ChevronRight, Github, Play } from 'lucide-react'
import { useState, useEffect } from 'react'

interface LandingPageProps {
  onEnterDashboard: () => void
}

export default function LandingPage({ onEnterDashboard }: LandingPageProps) {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  const features = [
    {
      icon: <Activity className="w-8 h-8" />,
      title: "Real-time Monitoring",
      description: "Live network traffic analysis with instant threat detection and WebSocket updates",
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Advanced Protection",
      description: "Detect port scans, DDoS attacks, SQL injection, XSS, and malicious payloads",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: <Bell className="w-8 h-8" />,
      title: "Smart Alerts",
      description: "Instant notifications with severity classification and detailed threat analysis",
      color: "from-orange-500 to-red-500"
    },
    {
      icon: <BarChart3 className="w-8 h-8" />,
      title: "Analytics Dashboard",
      description: "Comprehensive visualizations with charts, graphs, and historical data",
      color: "from-green-500 to-emerald-500"
    },
    {
      icon: <Network className="w-8 h-8" />,
      title: "Packet Capture",
      description: "Analyze live network packets from your system using Scapy integration",
      color: "from-indigo-500 to-blue-500"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "High Performance",
      description: "Optimized for speed with efficient packet processing and minimal overhead",
      color: "from-yellow-500 to-orange-500"
    }
  ]

  const stats = [
    { value: "99.9%", label: "Detection Rate" },
    { value: "<50ms", label: "Response Time" },
    { value: "10K+", label: "Packets/sec" },
    { value: "24/7", label: "Monitoring" }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse delay-2000"></div>
      </div>

      {/* Navigation */}
      <nav className="relative z-10 px-6 py-4 border-b border-slate-800/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
              <Shield className="w-6 h-6" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              SecureWatch IDS
            </span>
          </div>
          <div className="flex items-center gap-4">
            <a href="#features" className="text-slate-300 hover:text-white transition-colors">Features</a>
            <a href="#demo" className="text-slate-300 hover:text-white transition-colors">Demo</a>
            <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-slate-300 hover:text-white transition-colors">
              <Github className="w-5 h-5" />
            </a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 px-6 py-20 md:py-32">
        <div className={`max-w-7xl mx-auto text-center transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full mb-8">
            <Zap className="w-4 h-4 text-blue-400" />
            <span className="text-sm text-blue-300">Real-time Network Security</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            Protect Your Network
            <br />
            <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              In Real-Time
            </span>
          </h1>
          
          <p className="text-xl text-slate-400 mb-12 max-w-3xl mx-auto leading-relaxed">
            Advanced intrusion detection system with live packet capture, intelligent threat analysis, 
            and instant alerts. Monitor your network security with military-grade precision.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button 
              onClick={onEnterDashboard}
              className="group px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl font-semibold text-lg hover:shadow-2xl hover:shadow-blue-500/50 transition-all duration-300 flex items-center gap-2"
            >
              <Play className="w-5 h-5" />
              Launch Dashboard
              <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
            <a 
              href="#demo"
              className="px-8 py-4 bg-slate-800/50 border border-slate-700 rounded-xl font-semibold text-lg hover:bg-slate-800 transition-all duration-300 flex items-center gap-2"
            >
              <Eye className="w-5 h-5" />
              Watch Demo
            </a>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-20 max-w-4xl mx-auto">
            {stats.map((stat, index) => (
              <div 
                key={index}
                className="p-6 bg-slate-800/30 border border-slate-700/50 rounded-xl backdrop-blur-sm hover:bg-slate-800/50 transition-all duration-300"
              >
                <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                  {stat.value}
                </div>
                <div className="text-slate-400 text-sm">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative z-10 px-6 py-20 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Powerful <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Features</span>
            </h2>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              Everything you need to secure your network infrastructure
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group p-8 bg-slate-800/30 border border-slate-700/50 rounded-2xl backdrop-blur-sm hover:bg-slate-800/50 hover:border-slate-600 transition-all duration-300 hover:scale-105"
              >
                <div className={`inline-flex p-4 bg-gradient-to-br ${feature.color} rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold mb-3">{feature.title}</h3>
                <p className="text-slate-400 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="relative z-10 px-6 py-20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Built with <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Modern Tech</span>
            </h2>
            <p className="text-xl text-slate-400">
              Leveraging cutting-edge technologies for maximum performance
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="p-8 bg-slate-800/30 border border-slate-700/50 rounded-2xl backdrop-blur-sm">
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                <div className="p-2 bg-blue-500/20 rounded-lg">
                  <Lock className="w-6 h-6 text-blue-400" />
                </div>
                Backend
              </h3>
              <ul className="space-y-3 text-slate-300">
                <li className="flex items-center gap-2">
                  <ChevronRight className="w-4 h-4 text-blue-400" />
                  Flask & Python 3.9+ for robust API
                </li>
                <li className="flex items-center gap-2">
                  <ChevronRight className="w-4 h-4 text-blue-400" />
                  Scapy for advanced packet analysis
                </li>
                <li className="flex items-center gap-2">
                  <ChevronRight className="w-4 h-4 text-blue-400" />
                  WebSocket for real-time communication
                </li>
                <li className="flex items-center gap-2">
                  <ChevronRight className="w-4 h-4 text-blue-400" />
                  SQLite for efficient data storage
                </li>
              </ul>
            </div>

            <div className="p-8 bg-slate-800/30 border border-slate-700/50 rounded-2xl backdrop-blur-sm">
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                <div className="p-2 bg-purple-500/20 rounded-lg">
                  <Activity className="w-6 h-6 text-purple-400" />
                </div>
                Frontend
              </h3>
              <ul className="space-y-3 text-slate-300">
                <li className="flex items-center gap-2">
                  <ChevronRight className="w-4 h-4 text-purple-400" />
                  React 18 with TypeScript
                </li>
                <li className="flex items-center gap-2">
                  <ChevronRight className="w-4 h-4 text-purple-400" />
                  TailwindCSS for beautiful UI
                </li>
                <li className="flex items-center gap-2">
                  <ChevronRight className="w-4 h-4 text-purple-400" />
                  Recharts for data visualization
                </li>
                <li className="flex items-center gap-2">
                  <ChevronRight className="w-4 h-4 text-purple-400" />
                  Lucide React for modern icons
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section id="demo" className="relative z-10 px-6 py-20 bg-gradient-to-r from-blue-600/20 to-purple-600/20 border-y border-slate-700/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Secure Your Network?
          </h2>
          <p className="text-xl text-slate-300 mb-10">
            Start monitoring threats in real-time with our powerful intrusion detection system
          </p>
          <button 
            onClick={onEnterDashboard}
            className="group px-10 py-5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl font-bold text-xl hover:shadow-2xl hover:shadow-blue-500/50 transition-all duration-300 flex items-center gap-3 mx-auto"
          >
            <Shield className="w-6 h-6" />
            Get Started Now
            <ChevronRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 px-6 py-12 border-t border-slate-800/50">
        <div className="max-w-7xl mx-auto text-center text-slate-400">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
              <Shield className="w-5 h-5" />
            </div>
            <span className="text-lg font-bold text-white">SecureWatch IDS</span>
          </div>
          <p className="mb-4">
            Advanced Network Security Monitoring & Intrusion Detection
          </p>
          <p className="text-sm">
            Built with ❤️ for network security professionals
          </p>
        </div>
      </footer>
    </div>
  )
}
