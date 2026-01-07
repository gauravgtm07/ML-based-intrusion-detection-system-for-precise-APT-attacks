import { useState } from 'react'
import { Download } from 'lucide-react'
import axios from 'axios'

export default function ExportButton() {
  const [downloading, setDownloading] = useState(false)
  const [error, setError] = useState('')

  const handleDownloadCSV = async () => {
    setDownloading(true)
    setError('')
    
    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
      const response = await axios.get(`${backendUrl}/api/alerts/export`, {
        responseType: 'blob'
      })

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `alerts_${new Date().toISOString().split('T')[0]}.csv`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Error downloading CSV:', err)
      setError('Failed to download CSV file')
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div className="flex flex-col gap-2">
      <button
        onClick={handleDownloadCSV}
        disabled={downloading}
        className="px-4 py-2 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg font-medium transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Download className="w-4 h-4" />
        {downloading ? 'Downloading...' : 'Export Alerts to CSV'}
      </button>
      
      {error && (
        <div className="p-2 bg-red-500/10 border border-red-500/30 rounded text-red-500 text-sm">
          {error}
        </div>
      )}
    </div>
  )
}
