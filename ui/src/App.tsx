import { useQuery } from '@tanstack/react-query'
import { fetchDashboard, DashboardData } from './api/dashboard'
import AppCard from './components/AppCard'

function fmt(v: unknown): string {
  if (v == null) return '-'
  if (typeof v === 'number') return v.toLocaleString()
  return String(v)
}

function fmtDate(v: unknown): string {
  if (!v || typeof v !== 'string') return '-'
  return new Date(v).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}

function g(obj: Record<string, unknown> | null | undefined, key: string): unknown {
  return obj ? obj[key] : undefined
}

function buildCards(data: DashboardData | undefined) {
  const j = data?.journal
  const f = data?.finance
  const w = data?.wine
  const p = data?.pipeline
  const m = data?.music
  const l = data?.locations

  return [
    {
      name: 'Journal',
      icon: '\u25EB',
      href: 'https://journal.mees.st',
      available: !!j,
      metrics: j
        ? [
            { label: 'Entries', value: fmt(g(j, 'total_entries')) },
            { label: 'Photos', value: fmt(g(j, 'total_photos')) },
            { label: 'Latest', value: fmtDate(g(j, 'date_range_end')) },
          ]
        : [],
    },
    {
      name: 'Finance',
      icon: '\u00A3',
      href: 'https://finance.mees.st',
      available: !!f,
      metrics: f
        ? [
            { label: 'Accounts', value: fmt(g(f, 'active_accounts')) },
            { label: 'Transactions', value: fmt(g(f, 'active_transactions')) },
            { label: 'Categorised', value: `${g(f, 'category_coverage_pct') ?? '-'}%` },
          ]
        : [],
    },
    {
      name: 'Wine',
      icon: '\uD83C\uDF77',
      href: 'https://wine.mees.st',
      available: !!w,
      metrics: w
        ? [
            { label: 'In cellar', value: fmt(g(w, 'cellar_bottles')) },
            { label: 'Tastings', value: fmt(g(w, 'total_tastings')) },
            { label: 'Avg rating', value: fmt(g(w, 'avg_rating')) },
          ]
        : [],
    },
    {
      name: 'Pipeline',
      icon: '\u25B6',
      href: 'https://pipeline.mees.st',
      available: !!p,
      metrics: p
        ? [
            { label: 'Processed today', value: fmt(g(p, 'processed_today')) },
            { label: 'Exceptions', value: fmt(g(p, 'exceptions_pending')) },
            { label: 'Last processed', value: fmtDate(g(p, 'last_processed')) },
          ]
        : [],
    },
    {
      name: 'Music',
      icon: '\u266B',
      href: 'https://music.mees.st',
      available: !!m,
      metrics: m
        ? [
            { label: 'Tracks', value: fmt(g(m, 'total_tracks')) },
            { label: 'Artists', value: fmt(g(m, 'total_artists')) },
            { label: 'Today', value: fmt(g(m, 'scrobbles_today')) },
          ]
        : [],
    },
    {
      name: 'Locations',
      icon: '\u25CE',
      href: 'https://locations.mees.st',
      available: !!l,
      metrics: l
        ? [
            { label: 'GPS points', value: fmt(g(l, 'gps_points')) },
            { label: 'Ski days', value: fmt(g(l, 'skiing_days')) },
          ]
        : [],
    },
    {
      name: 'Links',
      icon: '\uD83D\uDD17',
      href: 'https://links.mees.st',
      available: true,
      metrics: [],
    },
  ]
}

export default function App() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: fetchDashboard,
  })

  const cards = buildCards(data)

  return (
    <div className="max-w-5xl mx-auto px-4 py-6 md:px-6 md:py-10">
      <h1 className="text-2xl font-bold text-text-primary mb-8">Dashboard</h1>
      {isLoading && <p className="text-text-secondary">Loading...</p>}
      {error && <p className="text-expense">Failed to load dashboard data.</p>}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {cards.map((card) => (
          <AppCard key={card.name} {...card} />
        ))}
      </div>
    </div>
  )
}
