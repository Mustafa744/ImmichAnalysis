export default function Card({
  title,
  icon: Icon,
  children,
  className = "",
  noPadding = false,
}) {
  return (
    <div className={`glass-card ${className}`}>
      {title && (
        <div className="flex items-center gap-2.5 px-5 pt-5 pb-0">
          {Icon && <Icon size={18} className="text-accent" />}
          <h3 className="text-sm font-semibold tracking-wide uppercase text-text-secondary">
            {title}
          </h3>
        </div>
      )}
      <div className={noPadding ? "" : "p-5"}>{children}</div>
    </div>
  );
}
