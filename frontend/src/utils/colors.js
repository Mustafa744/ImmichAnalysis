export const CHART_COLORS = [
  "#8b5cf6", // purple
  "#22b8cf", // cyan
  "#ff922b", // orange
  "#51cf66", // green
  "#fcc419", // yellow
  "#ff6b6b", // red
  "#339af0", // blue
  "#cc5de8", // violet
  "#20c997", // teal
];

export function getChartColor(index) {
  return CHART_COLORS[index % CHART_COLORS.length];
}
