import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatTimestamp(timestamp: string): string {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

export function formatDate(timestamp: string): string {
  const date = new Date(timestamp)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

export function getSeverityColor(severity: string): string {
  switch (severity) {
    case 'Critical':
      return 'text-red-500 bg-red-500/10 border-red-500/20'
    case 'High':
      return 'text-orange-500 bg-orange-500/10 border-orange-500/20'
    case 'Medium':
      return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20'
    case 'Low':
      return 'text-blue-500 bg-blue-500/10 border-blue-500/20'
    default:
      return 'text-gray-500 bg-gray-500/10 border-gray-500/20'
  }
}

export function getStatusColor(status: string): string {
  switch (status) {
    case 'Blocked':
      return 'text-green-500 bg-green-500/10 border-green-500/20'
    case 'Active':
      return 'text-red-500 bg-red-500/10 border-red-500/20'
    case 'Investigating':
      return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20'
    default:
      return 'text-gray-500 bg-gray-500/10 border-gray-500/20'
  }
}
