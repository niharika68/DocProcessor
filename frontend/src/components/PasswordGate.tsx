import { useState } from "react";

const CORRECT_PASSWORD = import.meta.env.VITE_APP_PASSWORD as string | undefined;
const SESSION_KEY = "doc_processor_auth";

function isUnlocked(): boolean {
  return sessionStorage.getItem(SESSION_KEY) === "true";
}

interface Props {
  children: React.ReactNode;
}

export default function PasswordGate({ children }: Props) {
  const [unlocked, setUnlocked] = useState(isUnlocked);
  const [input, setInput] = useState("");
  const [error, setError] = useState(false);

  // If no password is configured, show the app directly
  if (!CORRECT_PASSWORD) return <>{children}</>;

  if (unlocked) return <>{children}</>;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (input === CORRECT_PASSWORD) {
      sessionStorage.setItem(SESSION_KEY, "true");
      setUnlocked(true);
    } else {
      setError(true);
      setInput("");
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: "#f8f9fa",
      fontFamily: "system-ui, sans-serif",
    }}>
      <div style={{
        background: "white",
        borderRadius: 12,
        padding: "40px 48px",
        boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
        width: 340,
        textAlign: "center",
      }}>
        <h1 style={{ margin: "0 0 6px", fontSize: 20, fontWeight: 700, color: "#1e293b" }}>
          Document Processor
        </h1>
        <p style={{ margin: "0 0 28px", color: "#64748b", fontSize: 14 }}>
          Enter the password to continue
        </p>
        <form onSubmit={handleSubmit}>
          <input
            type="password"
            value={input}
            onChange={(e) => { setInput(e.target.value); setError(false); }}
            placeholder="Password"
            autoFocus
            style={{
              width: "100%",
              padding: "10px 14px",
              fontSize: 15,
              border: `1.5px solid ${error ? "#f87171" : "#e2e8f0"}`,
              borderRadius: 8,
              outline: "none",
              boxSizing: "border-box",
              marginBottom: 8,
              background: error ? "#fff5f5" : "white",
            }}
          />
          {error && (
            <p style={{ margin: "0 0 10px", color: "#ef4444", fontSize: 13 }}>
              Incorrect password. Please try again.
            </p>
          )}
          <button
            type="submit"
            style={{
              width: "100%",
              padding: "10px",
              background: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: 8,
              fontSize: 15,
              fontWeight: 600,
              cursor: "pointer",
              marginTop: 4,
            }}
          >
            Enter
          </button>
        </form>
      </div>
    </div>
  );
}
