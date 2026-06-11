import React from "react";
import { ShieldAlert } from "lucide-react";
import { Card, PageHeader } from "../components/Primitives";

export default function Forbidden() {
  return (
    <div data-testid="forbidden-page">
      <PageHeader
        eyebrow="Access"
        title="Permission needed"
        subtitle="This workspace is limited to roles with the right barn permissions."
      />
      <Card hover={false} className="text-center py-14">
        <ShieldAlert className="w-8 h-8 mx-auto mb-4 text-equine-clay" />
        <div className="font-display text-2xl text-equine-ink mb-2">This page is not available for your role.</div>
        <div className="text-[13px] text-equine-inkMuted">Use the sidebar to continue with the tools available to you.</div>
      </Card>
    </div>
  );
}
