import { useState } from 'react'
import { Calendar, Download, Search } from 'lucide-react'
import { Alert } from '../types'
import axios from 'axios'

interface TimeFilterProps {
  onFilterResults: (alerts: Alert[]) => void
  onClearFilter: () => void
}

export default function TimeFilter({ onFilterResults, onClearFilter }: TimeFilterProps) {
  const [startTime, setStartTime] = useState('')
  const [endTime, setEndTime] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [filteredCount, setFilteredCount] = useState<number | null>(null)

  const handleFilter = async () => {
    if (!startTime || !endTime) {
      setError('Please select both start and end times')
      return
    }

    setLoading(true)
    setError('')

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
      const response = await axios.get(`${backendUrl}/api/alerts/filter-by-time`, {
        params: {
          start_time: new Date(startTime).toISOString(),
          end_time: new Date(endTime).toISOString()
        }
      })

      onFilterResults(response.data.alerts)
      setFilteredCount(response.data.total)
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to filter alerts')
      console.error('Error filtering alerts:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleClearFilter = () => {
    setStartTime('')
    setEndTime('')
    setError('')
    setFilteredCount(null)
    onClearFilter()
  }

  const handleDownloadCSV = async () => {
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
    }
  }

  return (
    <div className="bg-card border border-border rounded-lg p-4 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Calendar className="w-5 h-5 text-primary" />
          <h2 className="text-lg font-semibold text-foreground">Filter by Time Period</h2>
        </div>
        <button
          onClick={handleDownloadCSV}
          className="px-3 py-2 bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
        >
          <Download className="w-4 h-4" />
          Export CSV
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-muted-foreground mb-2">
            Start Time
          </label>
          <input
            type="datetime-local"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            className="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-muted-foreground mb-2">
            End Time
          </label>
          <input
            type="datetime-local"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
            className="w-full px-3 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
          />
        </div>
      </div>

      <div className="flex gap-2">
        <button
          onClick={handleFilter}
          disabled={loading || !startTime || !endTime}
          className="flex-1 px-4 py-2 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg font-medium transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Search className="w-4 h-4" />
          {loading ? 'Filtering...' : 'Filter Alerts'}
        </button>

        <button
          onClick={handleClearFilter}
          className="px-4 py-2 bg-muted hover:bg-muted/80 text-foreground rounded-lg font-medium transition-colors"
        >
          Clear Filter
        </button>
      </div>

      {error && (
        <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-500 text-sm">
          {error}
        </div>
      )}

      {filteredCount !== null && (
        <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg text-green-500 text-sm">
          Found {filteredCount} alert{filteredCount !== 1 ? 's' : ''} in the selected time period
        </div>
      )}
    </div>
  )
}
