import { MapPin, ImageIcon } from "lucide-react";

export default function CountryCard({ country, count, isActive, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all duration-200 cursor-pointer ${
        isActive
          ? "bg-accent/15 border border-accent/30 shadow-[0_0_20px_rgba(139,92,246,0.15)]"
          : "hover:bg-bg-card-hover border border-transparent"
      }`}
    >
      <div
        className={`flex items-center justify-center w-9 h-9 rounded-lg ${
          isActive ? "bg-accent/20" : "bg-bg-card"
        }`}
      >
        <MapPin
          size={16}
          className={isActive ? "text-accent" : "text-text-muted"}
        />
      </div>
      <div className="flex-1 min-w-0">
        <p
          className={`text-sm font-medium truncate ${
            isActive ? "text-text-primary" : "text-text-secondary"
          }`}
        >
          {country}
        </p>
      </div>
      <div className="flex items-center gap-1 text-xs text-text-muted">
        <ImageIcon size={12} />
        <span>{count?.toLocaleString()}</span>
      </div>
    </button>
  );
}
