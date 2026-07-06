import React from "react";
import { Construction } from "lucide-react";

export default function AdminPlaceholder({ section, description }) {
  return (
    <div
      className="max-w-3xl mx-auto"
      data-testid={`admin-placeholder-${section}`}
    >
      <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
        Admin Portal · {section}
      </div>
      <div className="mt-6 rounded-2xl border border-equinesync-graphite/10 bg-white p-10 text-center">
        <div
          className="w-14 h-14 mx-auto rounded-full bg-equinesync-lilac/20 flex items-center justify-center"
          aria-hidden="true"
        >
          <Construction className="w-6 h-6 text-equinesync-slate" strokeWidth={1.4} />
        </div>
        <h1 className="mt-5 font-display text-2xl text-equinesync-graphite font-light">
          {section} access is read-only here.
        </h1>
        {description && (
          <p className="mt-3 text-[13.5px] text-equinesync-graphite/65 leading-relaxed max-w-md mx-auto">
            {description}
          </p>
        )}
        <p className="mt-4 text-[11.5px] tracking-wide uppercase text-equinesync-graphite/45">
          Settings changes remain restricted until an approved workflow is connected.
        </p>
      </div>
    </div>
  );
}
