export default function Loader({ rows = 3, className = "" }) {
  return (
    <div className={`space-y-3 ${className}`}>
      {Array.from({ length: rows }).map((_, i) => (
        <div
          key={i}
          className="animate-shimmer rounded-xl"
          style={{ height: i === 0 ? "2rem" : "1rem", opacity: 1 - i * 0.15 }}
        />
      ))}
    </div>
  );
}
