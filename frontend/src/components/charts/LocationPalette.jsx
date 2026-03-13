import React from "react";
import { Palette, MapPin } from "lucide-react";

// Define the standard order for the rows
const SWATCH_TYPES = [
  "vibrant",
  "light_vibrant",
  "dark_vibrant",
  "muted",
  "light_muted",
  "dark_muted",
];

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

  // Assuming item.palette is now the dict of arrays: { vibrant: ["#hex1", "#hex2", "#hex3"], ... }
  const item = data[0];

  return (
    <div className="glass-card p-5 flex flex-col gap-6 group hover:border-accent/30 transition-all duration-500 overflow-hidden relative">
      {/* Ambient background glow */}
      <div className="absolute top-0 right-0 p-8 bg-accent/5 blur-[80px] rounded-full -mr-16 -mt-16 pointer-events-none" />
      
      {/* Header */}
      <div className="flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-accent/10 text-accent">
            <Palette size={20} />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-text-primary flex items-center gap-1.5">
              Location Signature
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

      {/* Top 3 Color Grid */}
      <div className="flex flex-col gap-3 z-10 w-full">
        {SWATCH_TYPES.map((swatch) => {
          // Grab the array of top colors, default to empty array
          const colors = item.palette[swatch] || [];
          
          return (
            <div key={swatch} className="flex items-center gap-4">
              {/* Swatch Category Label */}
              <div className="w-24 text-[10px] font-semibold tracking-wider text-text-muted uppercase">
                {swatch.replace('_', ' ')}
              </div>

              {/* The 3 Rank Slots */}
              <div className="flex-1 flex gap-2 h-7">
                {[0, 1, 2].map((idx) => {
                  const hexCode = colors[idx];

                  return hexCode ? (
                    // Populated Color Rank
                    <div
                      key={`${swatch}-${idx}`}
                      className="group/color relative flex-1 rounded shadow-sm transition-all duration-300 hover:scale-105 hover:z-20 cursor-pointer border border-border/20"
                      style={{ backgroundColor: hexCode }}
                    >
                      {/* Built-in Tooltip using your styling variables */}
                      <div className="absolute -top-9 left-1/2 -translate-x-1/2 opacity-0 group-hover/color:opacity-100 transition-all duration-300 bg-bg-card border border-border px-2 py-1 rounded-lg text-[10px] font-mono text-text-primary pointer-events-none whitespace-nowrap shadow-xl z-30">
                        Rank {idx + 1}: {hexCode}
                      </div>
                    </div>
                  ) : (
                    // Empty/Dashed State for unused ranks
                    <div
                      key={`empty-${swatch}-${idx}`}
                      className="flex-1 rounded border border-dashed border-border/60 bg-bg-card/30 flex items-center justify-center pointer-events-none"
                    >
                      <span className="text-text-muted/40 text-[10px] font-medium">—</span>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default LocationPalette;