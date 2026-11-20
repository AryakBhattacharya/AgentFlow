"use client";

import { useEffect, useState } from "react";
import { checkBackendHealth } from "@/lib/api";

export default function Home() {
  const [status, setStatus] = useState("Checking backend...");

  useEffect(() => {
    checkBackendHealth()
      .then(() => setStatus("Backend connected"))
      .catch(() => setStatus("Backend unavailable"));
  }, []);

  return (
    <main className="min-h-screen bg-[#0B0F19] text-white flex flex-col items-center justify-center">
      <h1 className="text-5xl font-bold tracking-tight">
        AgentFlow
      </h1>

      <p className="mt-4 text-gray-400">
        AI Agent Workflow Orchestration Platform
      </p>

      <div className="mt-8 rounded-xl border border-gray-700 p-5">
        <p className="text-sm text-gray-400">
          Backend connectivity
        </p>

        <p className="mt-2 font-semibold">
          {status}
        </p>
      </div>
    </main>
  );
}