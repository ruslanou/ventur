import { useState, useEffect, useRef } from "react";
import "./App.css";

const API_BASE = "http://localhost:8000";
const USER_ID = "demo_user";

// ── API ──────────────────────────────────────────────────────────────────────
async function apiFetchPlaces() {
  const res = await fetch(`${API_BASE}/places`);
  const data = await res.json();
  return data.places || [];
}

async function apiStamp(placeId) {
  const res = await fetch(`${API_BASE}/stamp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: USER_ID, place_id: placeId }),
  });
  return res.json();
}

async function apiChat(message) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, user_id: USER_ID }),
  });
  const data = await res.json();
  return data.response;
}

async function apiFetchProfile() {
  const res = await fetch(`${API_BASE}/profile/${USER_ID}`);
  return res.json();
}

// ── Theme ────────────────────────────────────────────────────────────────────
const GH = {
  bg: "#0f0f1a",
  modalBg: "#16213e",
};

const CATEGORY_EMOJI = {
  Restaurant: "🍽️",
  Bar: "🍺",
  Attraction: "🏛️",
  Hotel: "🏨",
};

const CATEGORY_COLOR = {
  Restaurant: "#10B981",
  Bar: "#F59E0B",
  Attraction: "#8B5CF6",
  Hotel: "#06B6D4",
};

const LEVELS = [
  { name: "Explorer", min: 0, max: 499, icon: "🌱", color: "#84CC16" },
  { name: "Adventurer", min: 500, max: 999, icon: "⚡", color: "#F59E0B" },
  { name: "Pathfinder", min: 1000, max: 1999, icon: "🔥", color: "#F97316" },
  { name: "Legend", min: 2000, max: 9999, icon: "👑", color: "#8B5CF6" },
];

function normalizePlace(p) {
  return {
    id: p.id,
    name: p.name,
    category: p.category,
    emoji: CATEGORY_EMOJI[p.category] || "📍",
    color: CATEGORY_COLOR[p.category] || "#F59E0B",
    points: p.points,
    address: p.address,
    description: p.description,
    stamped: false,
  };
}

export default function Ventur() {
  const [screen, setScreen] = useState("onboarding");
  const [onboardStep, setOnboardStep] = useState(0);
  const [activeTab, setActiveTab] = useState("passport");
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hey explorer! 🌟 I'm your Ventur guide for Montgomery, Alabama!\n\nAsk me about bars, restaurants, or attractions to discover and earn stamps!" }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [scanning, setScanning] = useState(false);
  const [justStamped, setJustStamped] = useState(null);
  const [places, setPlaces] = useState([]);
  const [profile, setProfile] = useState(null);
  const [loadingPlaces, setLoadingPlaces] = useState(true);
  const [exploreFilter, setExploreFilter] = useState("All");
  const chatBottomRef = useRef(null);

  useEffect(() => {
    apiFetchPlaces().then((raw) => {
      setPlaces(raw.map(normalizePlace));
      setLoadingPlaces(false);
    }).catch(() => setLoadingPlaces(false));
  }, []);

  useEffect(() => {
    if (screen === "home") {
      apiFetchProfile().then((p) => {
        setProfile(p);
        const stampedIds = new Set((p.stamped_places || []).map((sp) => sp.id));
        setPlaces((prev) => prev.map((pl) => ({ ...pl, stamped: stampedIds.has(pl.id) })));
      });
    }
  }, [screen]);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const totalPoints = profile?.points ?? places.filter(p => p.stamped).reduce((s, p) => s + p.points, 0);
  const stampsCollected = profile?.stamps_collected ?? places.filter(p => p.stamped).length;
  const currentLevel = LEVELS.find(l => totalPoints >= l.min && totalPoints <= l.max) || LEVELS[0];
  const nextLevel = LEVELS[LEVELS.indexOf(currentLevel) + 1];
  const progress = nextLevel ? ((totalPoints - currentLevel.min) / (nextLevel.min - currentLevel.min)) * 100 : 100;

  const sendMessage = async (text) => {
    const msg = text || input;
    if (!msg.trim()) return;
    setMessages(prev => [...prev, { from: "user", text: msg }]);
    setInput("");
    setIsTyping(true);
    try {
      const reply = await apiChat(msg);
      setMessages(prev => [...prev, { from: "bot", text: reply }]);
    } catch {
      setMessages(prev => [...prev, { from: "bot", text: "Something went wrong. Try again!" }]);
    }
    setIsTyping(false);
  };

  const simulateScan = async (place) => {
    setScanning(true);
    try {
      const [result] = await Promise.all([
        apiStamp(place.id),
        new Promise(r => setTimeout(r, 3000)),
      ]);
      setScanning(false);
      setPlaces(prev => prev.map(p => p.id === place.id ? { ...p, stamped: true } : p));
      if (result.success) {
        setJustStamped({ ...place, points: result.points_earned });
        apiFetchProfile().then(setProfile);
      } else {
        setJustStamped({ ...place, points: 0, alreadyStamped: true });
      }
      setTimeout(() => setJustStamped(null), 3000);
    } catch {
      setScanning(false);
    }
    setSelectedPlace(null);
  };

  const onboardSteps = [
    { bg: "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)", emoji: "✈️", title: "Welcome to Ventur", subtitle: "Your city is your passport", desc: "Explore Montgomery's best restaurants, bars, and attractions. Collect stamps. Level up. Earn rewards." },
    { bg: "linear-gradient(135deg, #0f3460 0%, #533483 50%, #e94560 100%)", emoji: "📖", title: "Collect Stamps", subtitle: "Visit. Scan. Stamp.", desc: "Scan QR codes at participating venues to collect unique stamps in your digital passport book." },
    { bg: "linear-gradient(135deg, #f59e0b 0%, #ef4444 50%, #8b5cf6 100%)", emoji: "👑", title: "Level Up & Win", subtitle: "Explorer → Legend", desc: "Earn points with every stamp. Level up from Explorer to Legend and unlock exclusive rewards from local businesses." },
  ];

  if (screen === "onboarding") {
    const s = onboardSteps[onboardStep];
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", background: "#0a0a0a", fontFamily: "'Georgia', serif" }}>
        <div style={{ width: 390, height: 780, borderRadius: 40, boxShadow: "0 30px 80px rgba(0,0,0,0.8)", position: "relative", background: s.bg, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "60px 40px 48px" }}>
          <div style={{ position: "absolute", inset: 0, borderRadius: 40, background: "radial-gradient(circle at 20% 20%, rgba(255,255,255,0.05) 0%, transparent 50%)", pointerEvents: "none" }} />
          <div style={{ position: "absolute", top: 40, right: 40, width: 100, height: 100, borderRadius: "50%", border: "2px dashed rgba(255,255,255,0.1)", pointerEvents: "none" }} />
          <div style={{ position: "absolute", bottom: 100, left: 30, width: 70, height: 70, borderRadius: "50%", border: "2px dashed rgba(255,255,255,0.1)", pointerEvents: "none" }} />
          <div style={{ fontSize: 90, marginBottom: 24, filter: "drop-shadow(0 0 20px rgba(255,255,255,0.3))", position: "relative", zIndex: 1 }}>{s.emoji}</div>
          <div style={{ color: "rgba(255,255,255,0.6)", fontSize: 11, letterSpacing: 4, textTransform: "uppercase", marginBottom: 8, fontFamily: "monospace", position: "relative", zIndex: 1 }}>{s.subtitle}</div>
          <h1 style={{ color: "#fff", fontSize: 30, fontWeight: 700, margin: "0 0 14px", textAlign: "center", lineHeight: 1.2, position: "relative", zIndex: 1 }}>{s.title}</h1>
          <p style={{ color: "rgba(255,255,255,0.7)", fontSize: 14, lineHeight: 1.7, textAlign: "center", margin: "0 0 36px", position: "relative", zIndex: 1 }}>{s.desc}</p>
          <div style={{ display: "flex", gap: 8, marginBottom: 28, position: "relative", zIndex: 1 }}>
            {onboardSteps.map((_, i) => (
              <div key={i} style={{ width: i === onboardStep ? 28 : 8, height: 8, borderRadius: 4, background: i === onboardStep ? "#fff" : "rgba(255,255,255,0.3)", transition: "all 0.4s" }} />
            ))}
          </div>
          <button onClick={() => onboardStep < 2 ? setOnboardStep(onboardStep + 1) : setScreen("home")} style={{ background: "#fff", color: "#1a1a2e", border: "none", borderRadius: 20, padding: "16px 48px", fontSize: 16, fontWeight: 700, cursor: "pointer", letterSpacing: 1, position: "relative", zIndex: 10 }}>
            {onboardStep < 2 ? "NEXT →" : "START EXPLORING"}
          </button>
          {onboardStep < 2 && (
            <button onClick={() => setScreen("home")} style={{ background: "none", border: "none", color: "rgba(255,255,255,0.5)", fontSize: 13, cursor: "pointer", marginTop: 16, position: "relative", zIndex: 10 }}>Skip</button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", background: "#0a0a0a", fontFamily: "'Georgia', serif" }}>
      <div style={{ width: 390, height: 780, borderRadius: 40, overflow: "hidden", boxShadow: "0 30px 80px rgba(0,0,0,0.8)", display: "flex", flexDirection: "column", background: GH.bg, position: "relative" }}>

        {justStamped && (
          <div className="toast-banner" style={{ position: "absolute", top: 20, left: 20, right: 20, background: justStamped.alreadyStamped ? "linear-gradient(135deg, #374151, #1f2937)" : "linear-gradient(135deg, #10b981, #059669)", borderRadius: 16, padding: "16px 20px", zIndex: 100, display: "flex", alignItems: "center", gap: 12, boxShadow: "0 10px 30px rgba(16,185,129,0.4)" }}>
            <span style={{ fontSize: 30 }}>{justStamped.alreadyStamped ? "📖" : "🎉"}</span>
            <div>
              <div style={{ color: "#fff", fontWeight: 700, fontSize: 14 }}>{justStamped.alreadyStamped ? "Already Stamped!" : "Stamp Collected!"}</div>
              <div style={{ color: "rgba(255,255,255,0.85)", fontSize: 12 }}>{justStamped.name}{!justStamped.alreadyStamped && ` • +${justStamped.points} pts`}</div>
            </div>
          </div>
        )}

        {/* HEADER */}
        <div style={{ background: "linear-gradient(135deg, #1a1a2e, #16213e)", padding: "44px 24px 20px", position: "relative", overflow: "hidden" }}>
          <div style={{ position: "absolute", top: -20, right: -20, width: 100, height: 100, borderRadius: "50%", border: "1px dashed rgba(255,255,255,0.1)" }} />
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <div>
              <div style={{ color: "rgba(255,255,255,0.5)", fontSize: 10, letterSpacing: 3, textTransform: "uppercase", fontFamily: "monospace" }}>Montgomery, AL</div>
              <div style={{ color: "#fff", fontSize: 26, fontWeight: 700, letterSpacing: -0.5 }}>Ventur</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ color: currentLevel.color, fontSize: 11, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", fontFamily: "monospace" }}>{currentLevel.icon} {currentLevel.name}</div>
              <div style={{ color: "#fff", fontSize: 22, fontWeight: 700 }}>{totalPoints.toLocaleString()} pts</div>
            </div>
          </div>
          <div style={{ marginTop: 16 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <span style={{ color: "rgba(255,255,255,0.5)", fontSize: 10, fontFamily: "monospace" }}>{stampsCollected}/{places.length} stamps</span>
              {nextLevel && <span style={{ color: "rgba(255,255,255,0.5)", fontSize: 10, fontFamily: "monospace" }}>{nextLevel.name} at {nextLevel.min}pts</span>}
            </div>
            <div style={{ height: 6, background: "rgba(255,255,255,0.1)", borderRadius: 3, overflow: "hidden" }}>
              <div style={{ height: "100%", width: `${progress}%`, background: `linear-gradient(90deg, ${currentLevel.color}, ${nextLevel?.color || currentLevel.color})`, borderRadius: 3, transition: "width 0.5s" }} />
            </div>
          </div>
        </div>

        {/* CONTENT */}
        <div className="no-scrollbar" style={{ flex: 1, overflow: activeTab === "chat" ? "hidden" : "auto", background: "#0f0f1a" }}>

          {activeTab === "passport" && (
            <div style={{ padding: "20px 20px 100px" }}>
              <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, letterSpacing: 3, textTransform: "uppercase", fontFamily: "monospace", marginBottom: 16 }}>Your Passport Book</div>
              {loadingPlaces ? (
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                  {Array.from({ length: 8 }).map((_, i) => (
                    <div key={i} style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 20, padding: "16px 14px" }}>
                      <div className="skeleton" style={{ width: 36, height: 36, borderRadius: 10, marginBottom: 12 }} />
                      <div className="skeleton" style={{ width: "80%", height: 12, marginBottom: 8 }} />
                      <div className="skeleton" style={{ width: "50%", height: 10, marginBottom: 14 }} />
                      <div className="skeleton" style={{ width: "60%", height: 22, borderRadius: 10 }} />
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                  {places.map(place => (
                    <button key={place.id} onClick={() => setSelectedPlace(place)} className="place-card" style={{ background: place.stamped ? `linear-gradient(135deg, ${place.color}22, ${place.color}11)` : "rgba(255,255,255,0.03)", border: `1px solid ${place.stamped ? place.color + "44" : "rgba(255,255,255,0.08)"}`, borderRadius: 20, padding: "16px 14px", cursor: "pointer", textAlign: "left", position: "relative", overflow: "hidden" }}>
                      {place.stamped && <div style={{ position: "absolute", top: -16, right: -16, width: 60, height: 60, borderRadius: "50%", border: `2px dashed ${place.color}55` }} />}
                      <div style={{ fontSize: 28, marginBottom: 8 }}>{place.emoji}</div>
                      <div style={{ color: place.stamped ? "#fff" : "rgba(255,255,255,0.5)", fontSize: 12, fontWeight: 700, marginBottom: 4, lineHeight: 1.3, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{place.name}</div>
                      <div style={{ color: place.stamped ? place.color : "rgba(255,255,255,0.25)", fontSize: 10, fontFamily: "monospace", letterSpacing: 1 }}>{place.category.toUpperCase()}</div>
                      {place.stamped ? (
                        <div style={{ marginTop: 10, display: "inline-flex", alignItems: "center", gap: 4, background: place.color + "22", borderRadius: 10, padding: "4px 10px" }}>
                          <span style={{ fontSize: 10 }}>✅</span>
                          <span style={{ color: place.color, fontSize: 10, fontWeight: 700, fontFamily: "monospace" }}>STAMPED</span>
                        </div>
                      ) : (
                        <div style={{ marginTop: 10, display: "inline-flex", alignItems: "center", gap: 4, background: "rgba(255,255,255,0.05)", borderRadius: 10, padding: "4px 10px" }}>
                          <span style={{ color: "rgba(255,255,255,0.3)", fontSize: 10, fontFamily: "monospace" }}>+{place.points}pts</span>
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === "explore" && (
            <div style={{ padding: "20px 0 100px" }}>
              <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, letterSpacing: 3, textTransform: "uppercase", fontFamily: "monospace", marginBottom: 14, paddingLeft: 20 }}>Discover Montgomery</div>
              {/* Filter chips */}
              <div className="filter-chips" style={{ display: "flex", gap: 8, marginBottom: 20, overflowX: "auto", paddingLeft: 20, paddingRight: 20 }}>
                {["All", "Restaurant", "Bar", "Attraction", "Hotel"].map(cat => {
                  const active = exploreFilter === cat;
                  return (
                    <button key={cat} onClick={() => setExploreFilter(cat)} style={{ flexShrink: 0, background: active ? "#f59e0b" : "rgba(255,255,255,0.06)", border: active ? "none" : "1px solid rgba(255,255,255,0.1)", borderRadius: 20, padding: "6px 14px", color: active ? "#000" : "rgba(255,255,255,0.6)", fontSize: 12, fontWeight: active ? 700 : 400, cursor: "pointer", transition: "all 0.15s" }}>
                      {cat}
                    </button>
                  );
                })}
              </div>
              {/* Place list */}
              {(exploreFilter === "All"
                ? ["Restaurant", "Bar", "Attraction", "Hotel"]
                : [exploreFilter]
              ).map(cat => {
                const catPlaces = places.filter(p => p.category === cat);
                if (catPlaces.length === 0) return null;
                return (
                  <div key={cat} style={{ marginBottom: 24, paddingLeft: 20, paddingRight: 20 }}>
                    {exploreFilter === "All" && (
                      <div style={{ color: "rgba(255,255,255,0.6)", fontSize: 11, letterSpacing: 2, fontFamily: "monospace", marginBottom: 12 }}>— {cat.toUpperCase()}S</div>
                    )}
                    {catPlaces.map(place => (
                      <button key={place.id} onClick={() => setSelectedPlace(place)} style={{ width: "100%", background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 16, padding: "14px 16px", marginBottom: 8, display: "flex", alignItems: "center", gap: 14, cursor: "pointer", textAlign: "left" }}>
                        <div style={{ width: 48, height: 48, borderRadius: 14, background: place.color + "22", overflow: "hidden", flexShrink: 0, position: "relative", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 22 }}>
                          <span style={{ position: "absolute" }}>{place.emoji}</span>
                          <img
                            src={`http://localhost:8000/place-photo/${place.id}?maxwidth=200`}
                            alt={place.name}
                            style={{ width: "100%", height: "100%", objectFit: "cover", position: "relative", zIndex: 1 }}
                            onError={e => { e.target.style.display = "none"; }}
                          />
                        </div>
                        <div style={{ flex: 1 }}>
                          <div style={{ color: "#fff", fontSize: 13, fontWeight: 700 }}>{place.name}</div>
                          <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 11, marginTop: 2 }}>{place.address}</div>
                        </div>
                        <div style={{ textAlign: "right" }}>
                          {place.stamped ? <div style={{ color: "#10b981", fontSize: 16 }}>✅</div> : <div style={{ color: place.color, fontSize: 11, fontFamily: "monospace" }}>+{place.points}</div>}
                        </div>
                      </button>
                    ))}
                  </div>
                );
              })}
            </div>
          )}

          {activeTab === "chat" && (
            <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
              {/* Chat header */}
              <div style={{ padding: "14px 20px 10px", borderBottom: "1px solid rgba(255,255,255,0.06)", display: "flex", alignItems: "center", gap: 12, flexShrink: 0 }}>
                <div style={{ width: 36, height: 36, borderRadius: "50%", background: "linear-gradient(135deg, #f59e0b, #ef4444)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, flexShrink: 0 }}>✈️</div>
                <div>
                  <div style={{ color: "#fff", fontSize: 13, fontWeight: 700 }}>Ventur AI Guide</div>
                  <div style={{ color: "#10b981", fontSize: 10, fontFamily: "monospace", display: "flex", alignItems: "center", gap: 4 }}>
                    <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#10b981", display: "inline-block" }} />
                    Online — powered by Gemini
                  </div>
                </div>
              </div>

              {/* Messages */}
              <div style={{ flex: 1, padding: "16px 16px 8px", overflowY: "auto", display: "flex", flexDirection: "column", gap: 14 }}>
                {messages.map((msg, i) => (
                  <div key={i} style={{ display: "flex", justifyContent: msg.from === "user" ? "flex-end" : "flex-start", gap: 8, alignItems: "flex-end" }}>
                    {msg.from === "bot" && (
                      <div style={{ width: 28, height: 28, borderRadius: "50%", background: "linear-gradient(135deg, #f59e0b, #ef4444)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, flexShrink: 0 }}>✈️</div>
                    )}
                    <div style={{ maxWidth: "78%", background: msg.from === "user" ? "linear-gradient(135deg, #533483, #e94560)" : "rgba(255,255,255,0.07)", borderRadius: msg.from === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px", padding: "11px 15px", border: msg.from === "bot" ? "1px solid rgba(255,255,255,0.06)" : "none" }}>
                      {msg.text.split("\n").map((line, j) => (
                        <p key={j} style={{ margin: "2px 0", color: "#fff", fontSize: 13, lineHeight: 1.55 }}>{line || " "}</p>
                      ))}
                    </div>
                  </div>
                ))}
                {isTyping && (
                  <div style={{ display: "flex", gap: 8, alignItems: "flex-end" }}>
                    <div style={{ width: 28, height: 28, borderRadius: "50%", background: "linear-gradient(135deg, #f59e0b, #ef4444)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12 }}>✈️</div>
                    <div style={{ background: "rgba(255,255,255,0.07)", border: "1px solid rgba(255,255,255,0.06)", borderRadius: "18px 18px 18px 4px", padding: "14px 18px" }}>
                      <div style={{ display: "flex", gap: 4 }}>
                        {[0,1,2].map(i => <div key={i} className="typing-dot" />)}
                      </div>
                    </div>
                  </div>
                )}
                <div ref={chatBottomRef} />
              </div>

              {/* Quick suggestions */}
              <div style={{ padding: "8px 16px 6px", display: "flex", gap: 8, overflowX: "auto", flexShrink: 0 }}>
                {["Best bars 🍺", "Top restaurants 🍽️", "Must-see attractions 🏛️", "Hidden gems ✨"].map((q, i) => (
                  <button key={i} onClick={() => sendMessage(q.replace(/ [🀀-🿿]|[☀-⟿]/gu, "").trim())} style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 20, padding: "7px 14px", color: "rgba(255,255,255,0.75)", fontSize: 11, cursor: "pointer", whiteSpace: "nowrap", fontFamily: "monospace", flexShrink: 0 }}>{q}</button>
                ))}
              </div>

              {/* Input bar */}
              <div style={{ padding: "8px 16px 96px", display: "flex", gap: 10, alignItems: "center", flexShrink: 0 }}>
                <input
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={e => e.key === "Enter" && sendMessage()}
                  placeholder="Ask about places to explore..."
                  style={{ flex: 1, background: "rgba(255,255,255,0.07)", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 24, padding: "13px 20px", color: "#fff", fontSize: 13, outline: "none", fontFamily: "Georgia, serif" }}
                />
                <button
                  onClick={() => sendMessage()}
                  disabled={!input.trim() || isTyping}
                  style={{ width: 44, height: 44, borderRadius: "50%", background: input.trim() && !isTyping ? "linear-gradient(135deg, #f59e0b, #ef4444)" : "rgba(255,255,255,0.08)", border: "none", color: "#fff", fontSize: 16, cursor: input.trim() && !isTyping ? "pointer" : "default", transition: "background 0.2s", flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>➤</button>
              </div>
            </div>
          )}

          {activeTab === "profile" && (
            <div style={{ padding: "20px 20px 100px" }}>
              <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, letterSpacing: 3, textTransform: "uppercase", fontFamily: "monospace", marginBottom: 20 }}>Explorer Profile</div>
              <div style={{ background: `linear-gradient(135deg, ${currentLevel.color}22, ${currentLevel.color}11)`, border: `1px solid ${currentLevel.color}33`, borderRadius: 24, padding: 24, marginBottom: 20, textAlign: "center" }}>
                <div style={{ fontSize: 60, marginBottom: 8 }}>{currentLevel.icon}</div>
                <div style={{ color: currentLevel.color, fontSize: 11, letterSpacing: 3, fontFamily: "monospace" }}>RANK</div>
                <div style={{ color: "#fff", fontSize: 28, fontWeight: 700 }}>{currentLevel.name}</div>
                <div style={{ color: "rgba(255,255,255,0.5)", fontSize: 13, marginTop: 4 }}>{totalPoints} total points</div>
              </div>
              {/* Stamp progress ring */}
              {(() => {
                const total = places.length || 1;
                const r = 54;
                const circ = 2 * Math.PI * r;
                const offset = circ * (1 - stampsCollected / total);
                return (
                  <div style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 24, padding: "24px 16px", marginBottom: 12, display: "flex", alignItems: "center", gap: 20 }}>
                    <svg width={130} height={130} style={{ flexShrink: 0 }}>
                      <circle cx={65} cy={65} r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth={10} />
                      <circle cx={65} cy={65} r={r} fill="none" stroke={currentLevel.color} strokeWidth={10}
                        strokeDasharray={circ} strokeDashoffset={offset}
                        strokeLinecap="round"
                        transform="rotate(-90 65 65)"
                        style={{ transition: "stroke-dashoffset 0.8s ease" }}
                      />
                      <text x={65} y={60} textAnchor="middle" fill="#fff" fontSize={26} fontWeight={700} fontFamily="monospace">{stampsCollected}</text>
                      <text x={65} y={78} textAnchor="middle" fill="rgba(255,255,255,0.35)" fontSize={11} fontFamily="monospace">of {places.length}</text>
                    </svg>
                    <div style={{ flex: 1 }}>
                      <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, letterSpacing: 2, fontFamily: "monospace", marginBottom: 6 }}>STAMPS COLLECTED</div>
                      <div style={{ color: "#fff", fontSize: 22, fontWeight: 700, marginBottom: 4 }}>{stampsCollected} <span style={{ color: "rgba(255,255,255,0.3)", fontSize: 14, fontWeight: 400 }}>/ {places.length}</span></div>
                      <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 12 }}>{places.length - stampsCollected} left to explore</div>
                      <div style={{ marginTop: 10, height: 4, background: "rgba(255,255,255,0.08)", borderRadius: 2, overflow: "hidden" }}>
                        <div style={{ height: "100%", width: `${(stampsCollected / (places.length || 1)) * 100}%`, background: currentLevel.color, borderRadius: 2, transition: "width 0.8s ease" }} />
                      </div>
                    </div>
                  </div>
                );
              })()}
              {/* Mini passport emoji grid */}
              <div style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 24, padding: "16px", marginBottom: 20 }}>
                <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, letterSpacing: 2, fontFamily: "monospace", marginBottom: 12 }}>PASSPORT COLLECTION</div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                  {places.map(place => (
                    <div key={place.id} title={place.name} style={{ width: 40, height: 40, borderRadius: 12, background: place.stamped ? place.color + "33" : "rgba(255,255,255,0.04)", border: `1px solid ${place.stamped ? place.color + "66" : "rgba(255,255,255,0.08)"}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20, opacity: place.stamped ? 1 : 0.3, transition: "all 0.3s" }}>
                      {place.emoji}
                    </div>
                  ))}
                </div>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 20 }}>
                {[
                  { label: "Points", value: totalPoints, icon: "⭐" },
                  { label: "Rank", value: currentLevel.name, icon: "👑" },
                ].map((stat, i) => (
                  <div key={i} style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 16, padding: "16px", textAlign: "center" }}>
                    <div style={{ fontSize: 24, marginBottom: 4 }}>{stat.icon}</div>
                    <div style={{ color: "#fff", fontSize: 20, fontWeight: 700 }}>{stat.value}</div>
                    <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, fontFamily: "monospace", letterSpacing: 1 }}>{stat.label.toUpperCase()}</div>
                  </div>
                ))}
              </div>
              <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, letterSpacing: 3, fontFamily: "monospace", marginBottom: 12 }}>LEVEL PROGRESSION</div>
              {LEVELS.map((level, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12, opacity: totalPoints >= level.min ? 1 : 0.3 }}>
                  <div style={{ width: 36, height: 36, borderRadius: "50%", background: level.color + "22", border: `1px solid ${level.color}44`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }}>{level.icon}</div>
                  <div style={{ flex: 1 }}>
                    <div style={{ color: "#fff", fontSize: 13, fontWeight: 600 }}>{level.name}</div>
                    <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, fontFamily: "monospace" }}>{level.min} pts required</div>
                  </div>
                  {totalPoints >= level.min && <div style={{ color: level.color, fontSize: 14 }}>✓</div>}
                </div>
              ))}
              {profile?.stamped_places?.length > 0 && (
                <>
                  <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10, letterSpacing: 3, fontFamily: "monospace", margin: "20px 0 12px" }}>PLACES VISITED</div>
                  {profile.stamped_places.map(place => (
                    <div key={place.id} style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 10, background: "rgba(255,255,255,0.03)", borderRadius: 12, padding: "10px 14px" }}>
                      <div style={{ fontSize: 20 }}>{CATEGORY_EMOJI[place.category] || "📍"}</div>
                      <div>
                        <div style={{ color: "#fff", fontSize: 13, fontWeight: 600 }}>{place.name}</div>
                        <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 11 }}>{place.points} pts · {place.neighborhood}</div>
                      </div>
                    </div>
                  ))}
                </>
              )}
            </div>
          )}
        </div>

        {/* BOTTOM NAV */}
        <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, zIndex: 20, background: "rgba(15,15,26,0.95)", backdropFilter: "blur(20px)", borderTop: "1px solid rgba(255,255,255,0.06)", padding: "12px 0 24px", display: "flex", justifyContent: "space-around" }}>
          {[
            { id: "passport", icon: "📖", label: "Passport" },
            { id: "explore", icon: "🗺️", label: "Explore" },
            { id: "chat", icon: "💬", label: "Guide" },
            { id: "profile", icon: "👤", label: "Profile" },
          ].map(tab => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)} style={{ background: "none", border: "none", display: "flex", flexDirection: "column", alignItems: "center", gap: 4, cursor: "pointer", padding: "0 16px" }}>
              <div style={{ width: 44, height: 44, borderRadius: 14, background: activeTab === tab.id ? "rgba(245,158,11,0.15)" : "transparent", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20, transition: "all 0.2s" }}>{tab.icon}</div>
              <span style={{ fontSize: 9, color: activeTab === tab.id ? "#f59e0b" : "rgba(255,255,255,0.3)", fontFamily: "monospace", letterSpacing: 1 }}>{tab.label.toUpperCase()}</span>
            </button>
          ))}
        </div>

        {/* PLACE MODAL */}
        {selectedPlace && (
          <div style={{ position: "absolute", inset: 0, background: "rgba(0,0,0,0.8)", display: "flex", alignItems: "flex-end", zIndex: 50 }} onClick={() => setSelectedPlace(null)}>
            <div style={{ width: "100%", background: GH.modalBg, borderRadius: "28px 28px 0 0", overflow: "hidden", boxShadow: "0 -8px 40px rgba(0,0,0,0.5)" }} onClick={e => e.stopPropagation()}>
              {/* Photo hero */}
              <div style={{ position: "relative", height: 260, overflow: "hidden", background: selectedPlace.color + "33", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 64 }}>
                <span style={{ position: "relative", zIndex: 0 }}>{selectedPlace.emoji}</span>
                <img
                  src={`${API_BASE}/place-photo/${selectedPlace.id}?maxwidth=600`}
                  alt={selectedPlace.name}
                  style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", objectFit: "cover", zIndex: 1 }}
                  onError={e => { e.target.style.display = "none"; }}
                />
                <div style={{ position: "absolute", top: 0, left: 0, right: 0, bottom: 0, background: "linear-gradient(to bottom, transparent 40%, rgba(22,33,62,0.95))", zIndex: 2 }} />
                <div style={{ position: "absolute", top: 12, left: "50%", transform: "translateX(-50%)", width: 40, height: 4, background: "rgba(255,255,255,0.35)", borderRadius: 2, zIndex: 3 }} />
                <div style={{ position: "absolute", bottom: 16, left: 20, right: 20, zIndex: 3 }}>
                  <div style={{ color: "#fff", fontSize: 18, fontWeight: 700 }}>{selectedPlace.name}</div>
                  <div style={{ color: selectedPlace.color, fontSize: 11, fontFamily: "monospace", letterSpacing: 1 }}>{selectedPlace.category.toUpperCase()} • {selectedPlace.address}</div>
                </div>
              </div>

              {/* Content */}
              <div style={{ padding: "20px 28px 44px" }}>
                <div style={{ color: "rgba(255,255,255,0.6)", fontSize: 13, lineHeight: 1.6, marginBottom: 20 }}>{selectedPlace.description}</div>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: "rgba(255,255,255,0.04)", borderRadius: 16, padding: "14px 18px", marginBottom: 20 }}>
                  <span style={{ color: "rgba(255,255,255,0.6)", fontSize: 13 }}>Stamp Value</span>
                  <span style={{ color: selectedPlace.color, fontSize: 18, fontWeight: 700, fontFamily: "monospace" }}>+{selectedPlace.points} pts</span>
                </div>
                {selectedPlace.stamped ? (
                  <div style={{ background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.3)", borderRadius: 18, padding: "16px", textAlign: "center" }}>
                    <div style={{ color: "#10b981", fontSize: 16, fontWeight: 700 }}>✅ Already Stamped!</div>
                    <div style={{ color: "rgba(255,255,255,0.5)", fontSize: 12, marginTop: 4 }}>You visited this place</div>
                  </div>
                ) : scanning ? (
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12, padding: "8px 0" }}>
                    <div className="qr-scanner">
                      <div className="qr-grid" />
                      <div className="qr-corner qr-corner-tl" />
                      <div className="qr-corner qr-corner-tr" />
                      <div className="qr-corner qr-corner-bl" />
                      <div className="qr-corner qr-corner-br" />
                      <div className="qr-scanline" />
                    </div>
                    <div style={{ color: "#f59e0b", fontSize: 14, fontWeight: 700, letterSpacing: 1 }}>Scanning QR Code...</div>
                    <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 12 }}>Hold steady!</div>
                  </div>
                ) : (
                  <button className="stamp-btn" onClick={() => simulateScan(selectedPlace)} style={{ width: "100%", background: `linear-gradient(135deg, ${selectedPlace.color}, ${selectedPlace.color}99)`, border: "none", borderRadius: 18, padding: "18px", color: "#fff", fontSize: 15, fontWeight: 700, cursor: "pointer", letterSpacing: 1 }}>
                    📷 SCAN QR CODE TO STAMP
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
