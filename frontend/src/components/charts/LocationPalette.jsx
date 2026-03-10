import React from "react";
import { Palette, MapPin } from "lucide-react";

const LocationPalette = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="glass-card p-5 animate-pulse">
        <div className="h-4 w-32 bg-border rounded mb-4" />
        <div className="h-10 w-full bg-border rounded-xl" />
      </div>
    );
  }

  if (!data || data.length === 0) return null;

  // We only show the first one if it's filtered, or a list if it's a general overview.
  // But based on the dashboard flow, it's usually 1 country or 1 city active.
  const item = data[0];

  return (
    <div className="glass-card p-5 flex flex-col gap-4 group hover:border-accent/30 transition-all duration-500 overflow-hidden relative">
      <div className="absolute top-0 right-0 p-8 bg-accent/5 blur-[80px] rounded-full -mr-16 -mt-16 pointer-events-none" />
      
      <div className="flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-accent/10 text-accent">
            <Palette size={20} />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-text-primary flex items-center gap-1.5">
              Location Color Palette
            </h3>
            <p className="text-xs text-text-muted flex items-center gap-1 mt-0.5">
              <MapPin size={12} />
              {item.city ? `${item.city}, ${item.country}` : item.country}
              <span className="mx-1">•</span>
              {item.count} photos
            </p>
          </div>
        </div>
      </div>

      <div className="relative h-12 flex w-full rounded-2xl overflow-hidden shadow-sm border border-border/50 z-10">
        {item.palette.map((color, idx) => (
          <div
            key={idx}
            className="h-full relative group/color transition-all duration-300 hover:scale-[1.02] hover:z-20 first:rounded-l-2xl last:rounded-r-2xl"
            style={{ 
              backgroundColor: color.hex, 
              width: `${color.proportion}%` 
            }}
          >
            <div className="absolute inset-0 opacity-0 group-color/color:opacity-100 bg-white/10 transition-opacity pointer-events-none" />
            <div className="absolute -bottom-10 left-1/2 -translate-x-1/2 opacity-0 group-hover/color:opacity-100 transition-all duration-300 bg-bg-card border border-border px-2 py-1 rounded-lg text-[10px] font-medium pointer-events-none whitespace-nowrap shadow-xl z-30">
              {color.hex} • {color.proportion}%
            </div>
          </div>
        ))}
      </div>
      
      <div className="grid grid-cols-5 gap-2 z-10">
        {item.palette.map((color, idx) => (
          <div key={idx} className="flex flex-col items-center gap-1">
            <div 
              className="w-full h-1.5 rounded-full" 
              style={{ backgroundColor: color.hex }}
            />
            <span className="text-[10px] font-mono text-text-muted uppercase">
              {color.hex.replace('#', '')}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LocationPalette;
