export default function HorseshoeIcon({ className = "", strokeWidth = 1.5, ...props }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
      {...props}
    >
      <path d="M7 3.5v7.2a5 5 0 0 0 10 0V3.5" />
      <path d="M7 3.5h3" />
      <path d="M14 3.5h3" />
      <path d="M7 8h2" />
      <path d="M15 8h2" />
      <path d="M8 14.5h2" />
      <path d="M14 14.5h2" />
      <path d="M5.5 20.5h4" />
      <path d="M14.5 20.5h4" />
    </svg>
  );
}
