"use client";
import { useEffect, useState } from "react";
export default function Home() {
  const [health, setHealth] = useState("Checking...");
  useEffect(() => {
    const run = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/healthz`);
        const data = await res.json();
        setHealth(data?.status === "ok" ? "✅ Backend OK" : "⚠️ Backend issue");
      } catch {
        setHealth("❌ Backend unreachable");
      }
    };
    run();
  }, []);
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 text-center p-6">
      <h1 className="text-4xl font-bold mb-2">D1FY — Your Game. Your Proof.</h1>
      <p className="text-lg text-gray-600 mb-6">Day 1: Wiring the stack.</p>
      <div className="text-xl"><span className="font-medium">Backend Health: </span>{health}</div>
    </main>
  );
}
