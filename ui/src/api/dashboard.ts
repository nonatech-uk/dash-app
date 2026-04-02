import { apiFetch } from './client'

export type DashboardData = Record<string, Record<string, unknown> | null>

export function fetchDashboard(): Promise<DashboardData> {
  return apiFetch('/dashboard')
}
