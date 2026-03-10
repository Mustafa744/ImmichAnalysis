import { Navigation, Calendar, ImageIcon } from "lucide-react";
import Card from "../ui/Card";

function TripCard({ trip }) {
  const startDate = new Date(trip.start).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
  const endDate = new Date(trip.end).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
  const days = Math.max(
    1,
    Math.ceil(
      (new Date(trip.end) - new Date(trip.start)) / (1000 * 60 * 60 * 24),
    ),
  );

  return (
    <div className="glass-card glass-card-hover p-4 flex items-start gap-3">
      <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-accent/10 shrink-0">
        <Navigation size={18} className="text-accent" />
      </div>
      <div className="flex-1 min-w-0 space-y-1">
        <div className="flex items-center gap-2">
          <h4 className="text-sm font-semibold text-text-primary truncate">
            {trip.city || trip.country || `Trip #${trip.id}`}
          </h4>
          {trip.country && trip.city && (
            <span className="text-xs text-text-muted">· {trip.country}</span>
          )}
        </div>
        <div className="flex items-center gap-4 text-xs text-text-muted">
          <span className="flex items-center gap-1">
            <Calendar size={11} />
            {startDate} — {endDate}
          </span>
          <span>
            {days} day{days !== 1 ? "s" : ""}
          </span>
          <span className="flex items-center gap-1">
            <ImageIcon size={11} />
            {trip.photos_count}
          </span>
        </div>
      </div>
    </div>
  );
}

export default function TripsList({ data }) {
  if (!data?.length) return null;

  return (
    <Card title="Detected Trips" icon={Navigation}>
      <div className="space-y-3 max-h-80 overflow-y-auto stagger-children">
        {data.map((trip) => (
          <TripCard key={trip.id} trip={trip} />
        ))}
      </div>
    </Card>
  );
}
