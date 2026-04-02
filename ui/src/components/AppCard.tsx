interface Metric {
  label: string
  value: string | number
}

interface AppCardProps {
  name: string
  icon: string
  href: string
  metrics: Metric[]
  available: boolean
}

export default function AppCard({ name, icon, href, metrics, available }: AppCardProps) {
  return (
    <a
      href={href}
      className="block bg-bg-card border border-border rounded-lg p-5 hover:shadow-md hover:border-accent/30 transition-all group"
    >
      <div className="flex items-center gap-3 mb-4">
        <span className="text-2xl">{icon}</span>
        <h2 className="text-lg font-semibold text-text-primary group-hover:text-accent transition-colors">
          {name}
        </h2>
      </div>
      {available ? (
        <div className="space-y-2">
          {metrics.map((m) => (
            <div key={m.label} className="flex justify-between items-baseline">
              <span className="text-sm text-text-secondary">{m.label}</span>
              <span className="text-sm font-medium text-text-primary">{m.value}</span>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-text-secondary italic">Unavailable</p>
      )}
    </a>
  )
}
