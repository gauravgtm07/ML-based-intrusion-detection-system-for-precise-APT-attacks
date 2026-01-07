import { useState, useEffect } from 'react'
import { Settings, Bell, Shield, User, Save, RefreshCw } from 'lucide-react'
import { notificationService } from '../services/notificationService'

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    // Alert Settings
    enableNotifications: true,
    emailAlerts: true,
    criticalOnly: false,
    alertSound: true,
    
    // Detection Settings
    portScanThreshold: 10,
    ddosThreshold: 100,
    autoBlock: true,
    blockDuration: 3600,
    
    // System Settings
    refreshInterval: 5,
    maxAlerts: 1000,
    logLevel: 'info',
    
    // User Settings
    theme: 'dark',
    timezone: 'UTC',
  })

  const [whitelistIP, setWhitelistIP] = useState('')
  const [blacklistIP, setBlacklistIP] = useState('')
  const [whitelist, setWhitelist] = useState<string[]>(['192.168.1.1', '10.0.0.1'])
  const [blacklist, setBlacklist] = useState<string[]>(['203.0.113.0', '198.51.100.0'])
  const [saved, setSaved] = useState(false)
  const [permissionGranted, setPermissionGranted] = useState(false)

  // Define applyTheme function before useEffect
  const applyTheme = (theme: string) => {
    console.log('🎨 Applying theme:', theme)
    
    // Apply theme to document (if your CSS supports it)
    if (theme === 'light') {
      console.log('Switching to LIGHT mode')
      document.documentElement.classList.remove('dark')
      document.documentElement.classList.add('light')
      document.body.style.backgroundColor = '#ffffff'
      document.body.style.color = '#000000'
    } else if (theme === 'dark') {
      console.log('Switching to DARK mode')
      document.documentElement.classList.remove('light')
      document.documentElement.classList.add('dark')
      document.body.style.backgroundColor = ''
      document.body.style.color = ''
    } else {
      console.log('Switching to AUTO mode')
      // Auto mode - check system preference
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('dark')
        document.body.style.backgroundColor = ''
        document.body.style.color = ''
      } else {
        document.documentElement.classList.remove('dark')
        document.body.style.backgroundColor = '#ffffff'
        document.body.style.color = '#000000'
      }
    }
  }

  // Load settings on mount
  useEffect(() => {
    const loadedSettings = notificationService.loadSettings()
    setSettings(prev => ({ ...prev, ...loadedSettings }))
    
    // Check notification permission
    if ('Notification' in window) {
      setPermissionGranted(Notification.permission === 'granted')
    }
    
    // Load and apply theme
    const savedTheme = localStorage.getItem('ids_theme') || 'dark'
    setSettings(prev => ({ ...prev, theme: savedTheme }))
    applyTheme(savedTheme)
    
    // Load timezone
    const savedTimezone = localStorage.getItem('ids_timezone') || 'UTC'
    setSettings(prev => ({ ...prev, timezone: savedTimezone }))
  }, [])

  const handleSave = () => {
    // Settings are already saved immediately when toggled
    // This just saves other settings to localStorage
    localStorage.setItem('ids_settings', JSON.stringify(settings))
    
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  const requestNotificationPermission = async () => {
    const granted = await notificationService.requestPermission()
    setPermissionGranted(granted)
    if (granted) {
      alert('✅ Notification permission granted! You will now receive alerts.')
    } else {
      alert('❌ Notification permission denied. Please enable it in your browser settings.')
    }
  }

  const testNotification = () => {
    notificationService.handleAlert({
      threat_type: 'Test Alert',
      severity: 'High',
      source_ip: '192.168.1.100',
      description: 'This is a test notification to verify your settings work correctly.',
    })
  }

  const clearAllAlerts = () => {
    if (confirm('⚠️ Are you sure you want to clear all alerts? This action cannot be undone.')) {
      // In a real app, this would call backend API
      localStorage.removeItem('ids_alerts')
      alert('✅ All alerts have been cleared!')
      window.location.reload()
    }
  }

  const resetToDefaults = () => {
    if (confirm('⚠️ Are you sure you want to reset all settings to defaults? This action cannot be undone.')) {
      const defaultSettings = {
        enableNotifications: true,
        emailAlerts: true,
        criticalOnly: false,
        alertSound: true,
        portScanThreshold: 10,
        ddosThreshold: 100,
        autoBlock: true,
        blockDuration: 3600,
        refreshInterval: 5,
        maxAlerts: 1000,
        logLevel: 'info',
        theme: 'dark',
        timezone: 'UTC',
      }
      
      setSettings(defaultSettings)
      notificationService.updateSettings({
        enableNotifications: true,
        emailAlerts: true,
        criticalOnly: false,
        alertSound: true,
      })
      localStorage.setItem('ids_settings', JSON.stringify(defaultSettings))
      alert('✅ Settings have been reset to defaults!')
    }
  }

  const clearBlacklist = () => {
    if (confirm('⚠️ Are you sure you want to clear the entire blacklist?')) {
      setBlacklist([])
      alert('✅ Blacklist has been cleared!')
    }
  }

  const addToWhitelist = () => {
    if (whitelistIP && !whitelist.includes(whitelistIP)) {
      setWhitelist([...whitelist, whitelistIP])
      setWhitelistIP('')
    }
  }

  const addToBlacklist = () => {
    if (blacklistIP && !blacklist.includes(blacklistIP)) {
      setBlacklist([...blacklist, blacklistIP])
      setBlacklistIP('')
    }
  }

  const removeFromWhitelist = (ip: string) => {
    setWhitelist(whitelist.filter(i => i !== ip))
  }

  const removeFromBlacklist = (ip: string) => {
    setBlacklist(blacklist.filter(i => i !== ip))
  }

  return (
    <div className="container mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-3">
            <Settings className="w-8 h-8 text-primary" />
            Settings & Configuration
          </h1>
          <p className="text-muted-foreground mt-1">
            Customize your intrusion detection system
          </p>
        </div>
        
        <button
          onClick={handleSave}
          className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-all ${
            saved 
              ? 'bg-green-500 text-white' 
              : 'bg-primary hover:bg-primary/90 text-primary-foreground'
          }`}
        >
          {saved ? (
            <>
              <RefreshCw className="w-4 h-4" />
              Saved!
            </>
          ) : (
            <>
              <Save className="w-4 h-4" />
              Save Changes
            </>
          )}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Alert Settings */}
        <div className="bg-card border border-border rounded-lg p-6 space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <Bell className="w-5 h-5 text-primary" />
            <h2 className="text-xl font-semibold text-foreground">Alert Settings</h2>
          </div>

          {/* Notification Permission Status */}
          {!permissionGranted && (
            <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-4 mb-4">
              <p className="text-yellow-400 text-sm mb-2">
                ⚠️ Browser notifications are not enabled
              </p>
              <button
                onClick={requestNotificationPermission}
                className="px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg text-sm transition-colors"
              >
                Enable Notifications
              </button>
            </div>
          )}

          {permissionGranted && (
            <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4 mb-4">
              <p className="text-green-400 text-sm mb-2">
                ✅ Browser notifications are enabled
              </p>
              <button
                onClick={testNotification}
                className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg text-sm transition-colors"
              >
                Test Notification
              </button>
            </div>
          )}

          <div className="space-y-4">
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3 mb-4">
              <p className="text-blue-400 text-xs">
                ℹ️ Alert settings are applied immediately when toggled
              </p>
            </div>

            <div className="flex items-center justify-between">
              <label className="text-foreground">Enable Notifications</label>
              <input
                type="checkbox"
                checked={settings.enableNotifications}
                onChange={(e) => {
                  const newValue = e.target.checked
                  setSettings({ ...settings, enableNotifications: newValue })
                  notificationService.updateSettings({ enableNotifications: newValue })
                }}
                className="w-5 h-5 rounded border-border"
              />
            </div>

            <div className="flex items-center justify-between">
              <label className="text-foreground">Email Alerts</label>
              <input
                type="checkbox"
                checked={settings.emailAlerts}
                onChange={(e) => {
                  const newValue = e.target.checked
                  setSettings({ ...settings, emailAlerts: newValue })
                  notificationService.updateSettings({ emailAlerts: newValue })
                }}
                className="w-5 h-5 rounded border-border"
              />
            </div>

            <div className="flex items-center justify-between">
              <label className="text-foreground">Critical Alerts Only</label>
              <input
                type="checkbox"
                checked={settings.criticalOnly}
                onChange={(e) => {
                  const newValue = e.target.checked
                  setSettings({ ...settings, criticalOnly: newValue })
                  notificationService.updateSettings({ criticalOnly: newValue })
                }}
                className="w-5 h-5 rounded border-border"
              />
            </div>

            <div className="flex items-center justify-between">
              <label className="text-foreground">Alert Sound</label>
              <input
                type="checkbox"
                checked={settings.alertSound}
                onChange={(e) => {
                  const newValue = e.target.checked
                  setSettings({ ...settings, alertSound: newValue })
                  notificationService.updateSettings({ alertSound: newValue })
                }}
                className="w-5 h-5 rounded border-border"
              />
            </div>
          </div>
        </div>

        {/* Detection Settings */}
        <div className="bg-card border border-border rounded-lg p-6 space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <Shield className="w-5 h-5 text-primary" />
            <h2 className="text-xl font-semibold text-foreground">Detection Settings</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-foreground block mb-2">Port Scan Threshold</label>
              <input
                type="number"
                value={settings.portScanThreshold}
                onChange={(e) => setSettings({ ...settings, portScanThreshold: parseInt(e.target.value) })}
                className="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground"
              />
              <p className="text-xs text-muted-foreground mt-1">Number of ports before triggering alert</p>
            </div>

            <div>
              <label className="text-foreground block mb-2">DDoS Threshold (packets/sec)</label>
              <input
                type="number"
                value={settings.ddosThreshold}
                onChange={(e) => setSettings({ ...settings, ddosThreshold: parseInt(e.target.value) })}
                className="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground"
              />
              <p className="text-xs text-muted-foreground mt-1">Packets per second before DDoS alert</p>
            </div>

            <div className="flex items-center justify-between">
              <label className="text-foreground">Auto-Block Threats</label>
              <input
                type="checkbox"
                checked={settings.autoBlock}
                onChange={(e) => setSettings({ ...settings, autoBlock: e.target.checked })}
                className="w-5 h-5 rounded border-border"
              />
            </div>

            <div>
              <label className="text-foreground block mb-2">Block Duration (seconds)</label>
              <input
                type="number"
                value={settings.blockDuration}
                onChange={(e) => setSettings({ ...settings, blockDuration: parseInt(e.target.value) })}
                className="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground"
              />
            </div>
          </div>
        </div>

        {/* IP Whitelist */}
        <div className="bg-card border border-border rounded-lg p-6 space-y-4">
          <h2 className="text-xl font-semibold text-foreground">IP Whitelist</h2>
          <p className="text-sm text-muted-foreground">Trusted IPs that will never be blocked</p>

          <div className="flex gap-2">
            <input
              type="text"
              value={whitelistIP}
              onChange={(e) => setWhitelistIP(e.target.value)}
              placeholder="Enter IP address"
              className="flex-1 px-3 py-2 bg-background border border-border rounded-lg text-foreground"
            />
            <button
              onClick={addToWhitelist}
              className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
            >
              Add
            </button>
          </div>

          <div className="space-y-2 max-h-48 overflow-y-auto">
            {whitelist.map((ip) => (
              <div key={ip} className="flex items-center justify-between p-3 bg-background rounded-lg">
                <span className="text-foreground font-mono text-sm">{ip}</span>
                <button
                  onClick={() => removeFromWhitelist(ip)}
                  className="text-red-400 hover:text-red-300 text-sm"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* IP Blacklist */}
        <div className="bg-card border border-border rounded-lg p-6 space-y-4">
          <h2 className="text-xl font-semibold text-foreground">IP Blacklist</h2>
          <p className="text-sm text-muted-foreground">IPs that are permanently blocked</p>

          <div className="flex gap-2">
            <input
              type="text"
              value={blacklistIP}
              onChange={(e) => setBlacklistIP(e.target.value)}
              placeholder="Enter IP address"
              className="flex-1 px-3 py-2 bg-background border border-border rounded-lg text-foreground"
            />
            <button
              onClick={addToBlacklist}
              className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
            >
              Add
            </button>
          </div>

          <div className="space-y-2 max-h-48 overflow-y-auto">
            {blacklist.map((ip) => (
              <div key={ip} className="flex items-center justify-between p-3 bg-background rounded-lg">
                <span className="text-foreground font-mono text-sm">{ip}</span>
                <button
                  onClick={() => removeFromBlacklist(ip)}
                  className="text-red-400 hover:text-red-300 text-sm"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* System Settings */}
        <div className="bg-card border border-border rounded-lg p-6 space-y-4">
          <h2 className="text-xl font-semibold text-foreground">System Settings</h2>

          <div>
            <label className="text-foreground block mb-2">Refresh Interval (seconds)</label>
            <input
              type="number"
              value={settings.refreshInterval}
              onChange={(e) => setSettings({ ...settings, refreshInterval: parseInt(e.target.value) })}
              className="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground"
            />
          </div>

          <div>
            <label className="text-foreground block mb-2">Max Alerts to Display</label>
            <input
              type="number"
              value={settings.maxAlerts}
              onChange={(e) => setSettings({ ...settings, maxAlerts: parseInt(e.target.value) })}
              className="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground"
            />
          </div>

          <div>
            <label className="text-foreground block mb-2">Log Level</label>
            <select
              value={settings.logLevel}
              onChange={(e) => setSettings({ ...settings, logLevel: e.target.value })}
              className="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground"
            >
              <option value="debug">Debug</option>
              <option value="info">Info</option>
              <option value="warning">Warning</option>
              <option value="error">Error</option>
            </select>
          </div>
        </div>

        {/* User Preferences */}
        <div className="bg-card border border-border rounded-lg p-6 space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <User className="w-5 h-5 text-primary" />
            <h2 className="text-xl font-semibold text-foreground">User Preferences</h2>
          </div>

          <div>
            <label className="text-foreground block mb-2">Theme</label>
            <select
              value={settings.theme}
              onChange={(e) => {
                const newTheme = e.target.value
                setSettings({ ...settings, theme: newTheme })
                applyTheme(newTheme)
                localStorage.setItem('ids_theme', newTheme)
              }}
              className="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground"
            >
              <option value="dark">Dark</option>
              <option value="light">Light</option>
              <option value="auto">Auto</option>
            </select>
            <p className="text-xs text-muted-foreground mt-1">Changes apply immediately</p>
          </div>

          <div>
            <label className="text-foreground block mb-2">Timezone</label>
            <select
              value={settings.timezone}
              onChange={(e) => {
                const newTimezone = e.target.value
                console.log('🌍 Changing timezone to:', newTimezone)
                setSettings({ ...settings, timezone: newTimezone })
                localStorage.setItem('ids_timezone', newTimezone)
              }}
              className="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground"
            >
              <option value="UTC">UTC</option>
              <option value="America/New_York">Eastern Time</option>
              <option value="America/Chicago">Central Time</option>
              <option value="America/Denver">Mountain Time</option>
              <option value="America/Los_Angeles">Pacific Time</option>
              <option value="Europe/London">London</option>
              <option value="Asia/Tokyo">Tokyo</option>
              <option value="Asia/Kolkata">India (IST)</option>
            </select>
            <p className="text-xs text-muted-foreground mt-1">Used for timestamp display</p>
          </div>
        </div>
      </div>

      {/* Danger Zone */}
      <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-red-400 mb-4">Danger Zone</h2>
        <p className="text-sm text-muted-foreground mb-4">
          These actions are permanent and cannot be undone. Use with caution.
        </p>
        <div className="space-y-3">
          <button 
            onClick={clearAllAlerts}
            className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors"
          >
            Clear All Alerts
          </button>
          <button 
            onClick={resetToDefaults}
            className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors ml-3"
          >
            Reset to Defaults
          </button>
          <button 
            onClick={clearBlacklist}
            className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors ml-3"
          >
            Clear Blacklist
          </button>
        </div>
      </div>
    </div>
  )
}
