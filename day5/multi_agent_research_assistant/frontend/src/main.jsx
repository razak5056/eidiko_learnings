import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { ArrowUpRight, Check, ChevronRight, FileText, LoaderCircle, RotateCcw, ShieldCheck, Sparkles } from "lucide-react";
import "./styles.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const stages = [
  ["manager", "Planning", "Build a research brief"],
  ["technical_research", "Technical", "Map the foundations"],
  ["business_research", "Business", "Measure the impact"],
  ["trends_research", "Trends", "Find applications and signals"],
  ["summarizer", "Synthesis", "Shape the narrative"],
  ["reviewer", "Review", "Stress-test the findings"],
  ["approval", "Approval", "Your final decision"],
];

function App() {
  const [topic, setTopic] = useState("");
  const [run, setRun] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const completed = new Set((run?.events || []).flatMap((event) => Object.keys(event)));
  const currentIndex = stages.findIndex(([id]) => !completed.has(id));
  const progress = run ? Math.round((completed.size / stages.length) * 100) : 0;

  useEffect(() => {
    if (!run?.thread_id || !run.running) return undefined;
    const timer = window.setInterval(async () => {
      try {
        const response = await fetch(`${API_URL}/research/${run.thread_id}`);
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Unable to read research status.");
        setRun(data);
        if (data.error) setError(data.error);
      } catch (requestError) {
        setError(requestError.message);
      }
    }, 1200);
    return () => window.clearInterval(timer);
  }, [run?.thread_id, run?.running]);

  async function startResearch(event) {
    event.preventDefault();
    if (!topic.trim()) return;
    setBusy(true);
    setError("");
    try {
      const response = await fetch(`${API_URL}/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topic.trim() }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "The research run could not start.");
      setRun(data);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  async function decide(decision) {
    setBusy(true);
    setError("");
    try {
      const response = await fetch(`${API_URL}/research/${run.thread_id}/approval`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ decision }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "The decision could not be submitted.");
      setRun(data);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  function reset() {
    setRun(null);
    setTopic("");
    setError("");
  }

  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand"><span className="brand-mark">RD</span><span>Research Desk</span></div>
        <div className="topbar-meta"><span className="live-dot" /> PostgreSQL checkpointed <span className="topbar-divider" /> LangGraph workflow</div>
        <button className="icon-button" onClick={reset} title="Start a new brief"><RotateCcw size={17} /></button>
      </header>

      <main>
        <section className="hero-grid">
          <div className="hero-copy">
            <p className="eyebrow">Multi-agent intelligence studio</p>
            <h1>From open question<br /><em>to trusted brief.</em></h1>
            <p className="hero-text">A coordinated research team that thinks in parallel, challenges its own work, and waits for your sign-off.</p>
          </div>
          <div className="hero-note">
            <Sparkles size={20} />
            <div><strong>Three perspectives, one report.</strong><span>Technical foundations, business impact, and future signals are investigated together.</span></div>
          </div>
        </section>

        <section className="workspace">
          <aside className="composer panel">
            <div className="panel-heading"><span className="section-number">01</span><div><p className="eyebrow">Research brief</p><h2>What should we investigate?</h2></div></div>
            <form onSubmit={startResearch}>
              <textarea value={topic} onChange={(event) => setTopic(event.target.value)} disabled={busy || Boolean(run)} placeholder="e.g. The future of clean energy in India" />
              <div className="form-footer"><span>{topic.length}/500</span><button className="primary-button" disabled={busy || Boolean(run) || !topic.trim()}>{busy ? <LoaderCircle className="spin" size={16} /> : <ArrowUpRight size={16} />} Begin research</button></div>
            </form>
            {run && <div className="brief-chip"><FileText size={15} /><span>{topic}</span></div>}
            {error && <div className="error-box">{error}</div>}
          </aside>

          <section className="process panel">
            <div className="process-header"><div className="panel-heading"><span className="section-number">02</span><div><p className="eyebrow">Live orchestration</p><h2>Research in motion</h2></div></div><span className="progress-label">{progress}%</span></div>
            <div className="progress-track"><div style={{ width: `${progress}%` }} /></div>
            <div className="stage-list">
              {stages.map(([id, label, description], index) => {
                const done = completed.has(id);
                const active = run && !done && index === currentIndex;
                return <div className={`stage ${done ? "done" : ""} ${active ? "active" : ""}`} key={id}><div className="stage-icon">{done ? <Check size={15} /> : active ? <LoaderCircle className="spin" size={15} /> : <span>{String(index + 1).padStart(2, "0")}</span>}</div><div className="stage-copy"><strong>{label}</strong><span>{description}</span></div>{done && <ChevronRight size={16} className="stage-arrow" />}</div>;
              })}
            </div>
          </section>
        </section>

        {run?.pending_approval && <section className="approval-card"><div className="approval-icon"><ShieldCheck size={23} /></div><div className="approval-copy"><p className="eyebrow">Human review required</p><h2>The report is ready for your judgment.</h2><p>The automated reviewer has completed its pass. Approve this brief or send it back for one more revision.</p></div><div className="approval-actions"><button className="secondary-button" disabled={busy} onClick={() => decide("no")}>Request revision</button><button className="primary-button" disabled={busy} onClick={() => decide("yes")}>{busy ? <LoaderCircle className="spin" size={16} /> : <Check size={16} />} Approve report</button></div></section>}

        {run?.report && !run.pending_approval && !run.running && <section className="report-section"><div className="report-heading"><div><p className="eyebrow">Approved research brief</p><h2>{topic}</h2></div><button className="secondary-button" onClick={() => downloadReport(run.report, topic)}><FileText size={16} /> Download .md</button></div><article className="report-card">{run.report.split("\n").map((line, index) => line.startsWith("#") ? <h3 key={index}>{line.replace(/^#+\s*/, "")}</h3> : <p key={index}>{line || "\u00a0"}</p>)}</article></section>}

        {run?.review_feedback && <details className="review-details"><summary>Open reviewer notes</summary><p>{run.review_feedback}</p></details>}
      </main>
      <footer><span>Research Desk</span><span>Designed for careful decisions.</span></footer>
    </div>
  );
}

function downloadReport(report, topic) {
  const blob = new Blob([report], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${topic.toLowerCase().replace(/[^a-z0-9]+/g, "-") || "research-report"}.md`;
  link.click();
  URL.revokeObjectURL(url);
}

createRoot(document.getElementById("root")).render(<App />);
