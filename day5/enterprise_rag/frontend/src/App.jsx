import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';

const suggestions = [
  { icon: '◷', title: 'Annual leave', prompt: 'How many days of annual leave are available each year?' },
  { icon: '⌂', title: 'Company policies', prompt: 'What are the key company policies I should know?' },
  { icon: '⌘', title: 'Technical docs', prompt: 'Summarize the technical documentation.' },
];

function makeSessionId() {
  return globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function Icon({ name, size = 18 }) {
  const paths = {
    spark: <><path d="m12 3 1.9 5.8L20 11l-6.1 2.2L12 19l-2-5.8L4 11l6-2.2L12 3Z" /><path d="m19 14 .9 2.1L22 17l-2.1.9L19 20l-.9-2.1L16 17l2.1-.9L19 14Z" /></>,
    plus: <><path d="M12 5v14M5 12h14" /></>,
    send: <><path d="m22 2-7 20-4-9-9-4Z" /><path d="M22 2 11 13" /></>,
    book: <><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v17H6.5A2.5 2.5 0 0 1 4 17.5Z" /><path d="M4 16.5A2.5 2.5 0 0 1 6.5 14H20M8 7h8" /></>,
    shield: <><path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11Z" /><path d="m9 12 2 2 4-4" /></>,
    chevron: <path d="m9 18 6-6-6-6" />,
    file: <><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z" /><path d="M14 2v6h6M8 13h8M8 17h8" /></>,
    menu: <><path d="M4 6h16M4 12h16M4 18h16" /></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name]}</svg>;
}

function App() {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(makeSessionId);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiReady, setApiReady] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    fetch('/api/health')
      .then((response) => setApiReady(response.ok))
      .catch(() => setApiReady(false));
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [messages, loading]);

  function startNewChat() {
    fetch(`/api/chat/${sessionId}`, { method: 'DELETE' }).catch(() => {});
    setMessages([]);
    setInput('');
    setSessionId(makeSessionId());
    setSidebarOpen(false);
    inputRef.current?.focus();
  }

  async function sendMessage(value = input) {
    const message = value.trim();
    if (!message || loading) return;

    setInput('');
    setSidebarOpen(false);
    setMessages((current) => [...current, { role: 'user', content: message }]);
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, message }),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.detail || 'The assistant could not answer. Check that the API server is running.');
      setMessages((current) => [...current, {
        role: 'assistant',
        content: data.answer || 'I could not find an answer in the documents.',
        sources: data.sources || [],
      }]);
    } catch (error) {
      setMessages((current) => [...current, {
        role: 'error',
        content: error.message || 'Could not connect to the assistant. Make sure the API is running.',
      }]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  const hasConversation = messages.length > 0;

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? 'sidebar--open' : ''}`}>
        <a className="brand" href="#top" aria-label="Northstar home">
          <span className="brand-mark"><Icon name="spark" size={19} /></span>
          <span>northstar<span className="brand-dot">.</span></span>
        </a>

        <button className="new-chat-button" onClick={startNewChat}>
          <Icon name="plus" size={17} /> <span>New conversation</span>
          <kbd>⌘ K</kbd>
        </button>

        <div className="sidebar-section">
          <div className="sidebar-label">Your workspace</div>
          <div className="workspace-card">
            <span className="workspace-icon"><Icon name="book" size={17} /></span>
            <span className="workspace-copy"><strong>Enterprise knowledge</strong><small>Private company library</small></span>
            <span className="workspace-status" title="Workspace ready" />
          </div>
        </div>

        <div className="sidebar-section sources-section">
          <div className="sidebar-label">Connected sources <span>3</span></div>
          <div className="source-item"><span className="source-icon source-icon--peach"><Icon name="file" size={15} /></span><span>HR policy</span><i>PDF</i></div>
          <div className="source-item"><span className="source-icon source-icon--blue"><Icon name="file" size={15} /></span><span>Company policy</span><i>PDF</i></div>
          <div className="source-item"><span className="source-icon source-icon--green"><Icon name="file" size={15} /></span><span>Technical docs</span><i>PDF</i></div>
        </div>

        <div className="sidebar-spacer" />
        <div className="privacy-card">
          <span className="privacy-icon"><Icon name="shield" size={17} /></span>
          <div><strong>Your data stays yours</strong><p>Answers are grounded in your private workspace documents.</p></div>
        </div>
        <div className="profile-row"><span className="avatar">N</span><span><strong>Knowledge assistant</strong><small>Enterprise workspace</small></span><span className="profile-more">···</span></div>
      </aside>

      <main className="main-panel" id="top">
        <header className="topbar">
          <button className="mobile-menu icon-button" onClick={() => setSidebarOpen((open) => !open)} aria-label="Toggle menu"><Icon name="menu" /></button>
          <div className="breadcrumb"><span>Workspace</span><Icon name="chevron" size={14} /><strong>Ask anything</strong></div>
          <div className={`connection ${apiReady === false ? 'connection--offline' : ''}`}>
            <span className="connection-dot" />{apiReady === null ? 'Connecting' : apiReady ? 'Systems operational' : 'API unavailable'}
          </div>
        </header>

        <section className={`conversation ${hasConversation ? 'conversation--active' : ''}`}>
          {!hasConversation ? (
            <div className="welcome">
              <div className="welcome-badge"><Icon name="spark" size={15} /> YOUR COMPANY KNOWLEDGE, CONNECTED</div>
              <h1>Good work starts<br />with <span>good answers.</span></h1>
              <p className="welcome-copy">Ask a question across your policies and technical docs.<br className="desktop-break" /> Get a clear answer, with the source to back it up.</p>
              <div className="suggestion-grid">
                {suggestions.map((item) => (
                  <button className="suggestion-card" key={item.title} onClick={() => sendMessage(item.prompt)}>
                    <span className="suggestion-icon">{item.icon}</span>
                    <span className="suggestion-title">{item.title}</span>
                    <span className="suggestion-prompt">{item.prompt}</span>
                    <span className="suggestion-arrow"><Icon name="chevron" size={16} /></span>
                  </button>
                ))}
              </div>
              <div className="trust-note"><span className="trust-check">✓</span> Responses are generated from your workspace documents</div>
            </div>
          ) : (
            <div className="message-list">
              {messages.map((message, index) => (
                <article className={`message message--${message.role}`} key={`${index}-${message.role}`}>
                  <div className={`message-avatar ${message.role === 'user' ? 'message-avatar--user' : ''}`}>
                    {message.role === 'user' ? 'Y' : message.role === 'error' ? '!' : <Icon name="spark" size={16} />}
                  </div>
                  <div className="message-content">
                    <div className="message-author">{message.role === 'user' ? 'You' : message.role === 'error' ? 'Connection issue' : 'Northstar'}<span>{message.role === 'assistant' ? '· grounded answer' : ''}</span></div>
                    <div className="message-text">
                      {message.role === 'assistant' ? <ReactMarkdown>{message.content}</ReactMarkdown> : message.content}
                    </div>
                    {message.sources?.length > 0 && <div className="source-chips">{message.sources.map((source) => <span className="source-chip" key={source}><Icon name="file" size={13} />{source}</span>)}</div>}
                  </div>
                </article>
              ))}
              {loading && <article className="message message--assistant"><div className="message-avatar"><Icon name="spark" size={16} /></div><div className="message-content"><div className="message-author">Northstar<span>· searching your sources</span></div><div className="typing"><i /><i /><i /></div></div></article>}
              <div ref={bottomRef} />
            </div>
          )}
        </section>

        <footer className="composer-wrap">
          <form className="composer" onSubmit={(event) => { event.preventDefault(); sendMessage(); }}>
            <textarea
              ref={inputRef}
              rows="1"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter' && !event.shiftKey) {
                  event.preventDefault();
                  sendMessage();
                }
              }}
              placeholder="Ask a question about your company…"
              aria-label="Your question"
              disabled={loading}
            />
            <div className="composer-bottom"><span><kbd>↵</kbd> to send <span className="composer-separator">·</span> <kbd>⇧ ↵</kbd> for a new line</span><button className="send-button" type="submit" disabled={!input.trim() || loading} aria-label="Send question"><Icon name="send" size={17} /></button></div>
          </form>
          <div className="disclaimer">AI can make mistakes. Check important details in the original source.</div>
        </footer>
      </main>
    </div>
  );
}

export default App;
