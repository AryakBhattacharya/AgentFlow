const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function checkBackendHealth() {
  const response = await fetch(`${API_URL}/health`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Backend connection failed");
  }

  return response.json();
}