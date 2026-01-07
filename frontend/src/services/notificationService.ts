// Notification Service for IDS
// Handles browser notifications, sounds, and email alerts

export interface NotificationSettings {
  enableNotifications: boolean
  emailAlerts: boolean
  criticalOnly: boolean
  alertSound: boolean
}

class NotificationService {
  private settings: NotificationSettings = {
    enableNotifications: true,
    emailAlerts: true,
    criticalOnly: false,
    alertSound: true,
  }

  private audioContext: AudioContext | null = null

  constructor() {
    // Request notification permission on initialization
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission()
    }
  }

  // Update settings
  updateSettings(newSettings: Partial<NotificationSettings>) {
    this.settings = { ...this.settings, ...newSettings }
    localStorage.setItem('ids_notification_settings', JSON.stringify(this.settings))
  }

  // Load settings from localStorage
  loadSettings(): NotificationSettings {
    const saved = localStorage.getItem('ids_notification_settings')
    if (saved) {
      this.settings = JSON.parse(saved)
    }
    return this.settings
  }

  // Get current settings
  getSettings(): NotificationSettings {
    return this.settings
  }

  // Play alert sound
  playAlertSound(severity: string) {
    if (!this.settings.alertSound) return

    try {
      // Create audio context if not exists
      if (!this.audioContext) {
        this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
      }

      const ctx = this.audioContext
      const oscillator = ctx.createOscillator()
      const gainNode = ctx.createGain()

      oscillator.connect(gainNode)
      gainNode.connect(ctx.destination)

      // Different frequencies for different severities
      const frequencies: Record<string, number> = {
        Critical: 880,  // High pitch
        High: 660,
        Medium: 440,
        Low: 330,       // Low pitch
      }

      oscillator.frequency.value = frequencies[severity] || 440
      oscillator.type = 'sine'

      // Volume envelope
      gainNode.gain.setValueAtTime(0.3, ctx.currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5)

      oscillator.start(ctx.currentTime)
      oscillator.stop(ctx.currentTime + 0.5)
    } catch (error) {
      console.error('Error playing alert sound:', error)
    }
  }

  // Show browser notification
  showNotification(title: string, body: string, severity: string) {
    if (!this.settings.enableNotifications) return

    // Check if we should only show critical alerts
    if (this.settings.criticalOnly && severity !== 'Critical') return

    // Check browser notification permission
    if ('Notification' in window && Notification.permission === 'granted') {
      const icon = this.getSeverityIcon(severity)
      
      const notification = new Notification(title, {
        body,
        icon,
        badge: icon,
        tag: 'ids-alert',
        requireInteraction: severity === 'Critical',
        silent: !this.settings.alertSound,
      })

      // Auto-close after 10 seconds (except critical)
      if (severity !== 'Critical') {
        setTimeout(() => notification.close(), 10000)
      }

      notification.onclick = () => {
        window.focus()
        notification.close()
      }
    } else if (Notification.permission === 'default') {
      // Request permission
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          this.showNotification(title, body, severity)
        }
      })
    }
  }

  // Send email alert (via backend)
  async sendEmailAlert(alertData: any) {
    if (!this.settings.emailAlerts) return

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
      await fetch(`${backendUrl}/api/send-email-alert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(alertData),
      })
    } catch (error) {
      console.error('Error sending email alert:', error)
    }
  }

  // Handle new alert
  handleAlert(alert: any) {
    const { threat_type, severity, source_ip, description } = alert

    // Play sound
    if (this.settings.alertSound) {
      this.playAlertSound(severity)
    }

    // Show browser notification
    if (this.settings.enableNotifications) {
      const title = `🚨 ${severity} Threat Detected`
      const body = `${threat_type} from ${source_ip}\n${description}`
      this.showNotification(title, body, severity)
    }

    // Send email alert
    if (this.settings.emailAlerts) {
      this.sendEmailAlert(alert)
    }
  }

  // Get severity icon
  private getSeverityIcon(severity: string): string {
    const icons: Record<string, string> = {
      Critical: '🔴',
      High: '🟠',
      Medium: '🟡',
      Low: '🟢',
    }
    return icons[severity] || '⚠️'
  }

  // Request notification permission
  async requestPermission(): Promise<boolean> {
    if (!('Notification' in window)) {
      console.warn('This browser does not support notifications')
      return false
    }

    if (Notification.permission === 'granted') {
      return true
    }

    if (Notification.permission !== 'denied') {
      const permission = await Notification.requestPermission()
      return permission === 'granted'
    }

    return false
  }
}

// Export singleton instance
export const notificationService = new NotificationService()
