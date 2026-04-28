import streamlit as st
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Causal Inference — Step-by-Step Guide",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; }

.stApp { background: #f5f2ec; color: #1a1a1a; }

div[data-testid="stSidebar"] {
    background: #1a1a2e !important;
    border-right: 3px solid #e63946 !important;
}
div[data-testid="stSidebar"] * { color: #e8e8e8 !important; }
div[data-testid="stSidebar"] .stRadio label { color: #e8e8e8 !important; }
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3 { color: #ffffff !important; }

/* Progress tracker */
.progress-track {
    display: flex; align-items: center; gap: 0; margin: 1rem 0 2rem 0;
    overflow-x: auto; padding-bottom: 4px;
    background: white; border-radius: 12px; padding: 1rem 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.prog-step {
    display: flex; flex-direction: column; align-items: center; gap: 4px;
    min-width: 80px;
}
.prog-dot {
    width: 38px; height: 38px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.85rem;
    border: 2px solid #d4cfc5;
    background: #f5f2ec; color: #aaa;
}
.prog-dot.active  { background: #e63946; color: white; border-color: #e63946; }
.prog-dot.done    { background: #2d6a4f; color: white; border-color: #2d6a4f; }
.prog-label { font-size: 0.66rem; color: #888; text-align: center; max-width: 72px; line-height: 1.2; }
.prog-line  { flex: 1; height: 2px; background: #d4cfc5; min-width: 18px; margin-top: -20px; }
.prog-line.done { background: #2d6a4f; }

/* Step header */
.step-header {
    background: #1a1a2e;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 1.2rem;
}
.step-number {
    background: #e63946; color: white;
    width: 50px; height: 50px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.2rem;
    flex-shrink: 0;
}
.step-title    { color: white; font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; margin: 0 0 0.2rem 0; }
.step-subtitle { color: #a0a8c8; margin: 0; font-size: 0.9rem; }

/* Concept cards */
.concept-card {
    background: white; border-radius: 10px; padding: 1.2rem 1.5rem;
    margin: 0.8rem 0; border-left: 4px solid #e63946;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.concept-card.blue  { border-left-color: #2563eb; }
.concept-card.green { border-left-color: #2d6a4f; }
.concept-card.amber { border-left-color: #d97706; }
.concept-card h4 { margin: 0 0 0.5rem 0; font-size: 1rem; color: #1a1a2e; font-family: 'Syne', sans-serif; }
.concept-card p  { margin: 0; color: #444; font-size: 0.93rem; line-height: 1.6; }

/* Formula block */
.formula {
    background: #1a1a2e; border-radius: 8px;
    padding: 1rem 1.4rem;
    font-family: 'Courier New', monospace;
    color: #93c5fd; font-size: 0.9rem;
    margin: 0.8rem 0; line-height: 1.8;
}

/* Hint box */
.hint-box {
    background: #fff8e1; border: 1px solid #fbbf24;
    border-radius: 8px; padding: 0.9rem 1.2rem; margin: 0.8rem 0;
    font-size: 0.9rem; color: #78350f; line-height: 1.5;
}

/* Feedback boxes */
.reveal-correct   { background: #f0fdf4; border: 1.5px solid #4ade80; border-radius: 10px; padding: 1.2rem 1.5rem; margin: 1rem 0; }
.reveal-incorrect { background: #fff1f2; border: 1.5px solid #fb7185; border-radius: 10px; padding: 1.2rem 1.5rem; margin: 1rem 0; }
.reveal-partial   { background: #fffbeb; border: 1.5px solid #fbbf24; border-radius: 10px; padding: 1.2rem 1.5rem; margin: 1rem 0; }
.reveal-neutral   { background: #eef2ff; border: 1.5px solid #818cf8; border-radius: 10px; padding: 1.2rem 1.5rem; margin: 1rem 0; }
.reveal-correct h4   { color: #16a34a; margin: 0 0 0.5rem 0; font-family: 'Syne', sans-serif; }
.reveal-incorrect h4 { color: #dc2626; margin: 0 0 0.5rem 0; font-family: 'Syne', sans-serif; }
.reveal-partial h4   { color: #d97706; margin: 0 0 0.5rem 0; font-family: 'Syne', sans-serif; }
.reveal-neutral h4   { color: #4338ca; margin: 0 0 0.5rem 0; font-family: 'Syne', sans-serif; }

/* Data table */
.data-table-wrap { background: white; border-radius: 10px; padding: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin: 1rem 0; }

/* DAG */
.dag-box {
    background: #1a1a2e; border-radius: 12px; padding: 2rem;
    text-align: center; font-family: 'Courier New', monospace;
    color: #93c5fd; font-size: 1rem; line-height: 2.4; margin: 1rem 0;
}

/* Buttons */
.stButton > button {
    background: #e63946 !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
    padding: 0.55rem 1.6rem !important; font-size: 0.95rem !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTextArea textarea, .stTextInput input {
    border: 2px solid #d4cfc5 !important; border-radius: 8px !important;
    background: white !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important; color: #1a1a1a !important;
}
.stTextArea textarea:focus, .stTextInput input:focus { border-color: #e63946 !important; }

.scorecard {
    background: #1a1a2e; border-radius: 14px; padding: 2rem;
    text-align: center; margin: 1rem 0; border: 1px solid #e63946;
}
.scorecard .big { font-family: 'Syne', sans-serif; font-size: 3.5rem; font-weight: 800; color: #e63946; }
.scorecard .sub { color: #a0a8c8; font-size: 0.95rem; margin-top: 0.3rem; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
STEPS = [
    "Introduction & Data",
    "Q1 — P(Med | Female)",
    "Q2 — P(Remission | Med, F)",
    "Q3 — Identifying the Confounder",
    "Q4 — Causal Impact (ATE)",
    "Q5 — DAG / Causal Network",
    "Final Review",
]

GRADE_MSG = {
    "correct":   ("✅ Correct!", "reveal-correct"),
    "partial":   ("⚠️ Partially Correct — almost there!", "reveal-partial"),
    "incorrect": ("❌ Not quite yet — review the hints above and try again.", "reveal-incorrect"),
}

# ── Session state init ────────────────────────────────────────────────────────
defaults = {
    "step": 0,
    "q1_ans": "", "q1_grade": "", "q1_graded": False,
    "q2_ans": "", "q2_grade": "", "q2_graded": False,
    "q3_ans": "", "q3_grade": "", "q3_graded": False,
    "q4_ans": "", "q4_grade": "", "q4_graded": False,
    "visited": {0},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go(n):
    st.session_state.step = n
    st.session_state.visited.add(n)

# ── Graders ───────────────────────────────────────────────────────────────────
def grade_q1(raw):
    s = raw.strip().lower().replace(",", ".").replace("%", "").replace("=", "").replace("approx","").strip()
    # Try to extract a number
    import re
    nums = re.findall(r'\d+\.?\d*', s)
    for n in nums:
        v = float(n)
        if abs(v - 0.7667) < 0.015 or abs(v - 76.67) < 1.5:
            return "correct"
        if abs(v - 0.7667) < 0.06 or abs(v - 76.67) < 6:
            return "partial"
    if "263" in s and "343" in s:
        return "correct"
    if "263" in s or "343" in s:
        return "partial"
    return "incorrect"

def grade_q2(raw):
    s = raw.strip().lower().replace(",", ".").replace("%", "")
    import re
    nums = re.findall(r'\d+\.?\d*', s)
    for n in nums:
        v = float(n)
        if abs(v - 0.7300) < 0.015 or abs(v - 73.0) < 1.5:
            return "correct"
        if abs(v - 0.7300) < 0.06 or abs(v - 73.0) < 6:
            return "partial"
    if "192" in s and "263" in s:
        return "correct"
    if "192" in s or "263" in s:
        return "partial"
    return "incorrect"

def grade_q3(raw):
    s = raw.lower()
    if any(w in s for w in ["gender", "sex", "confound", "simpson"]):
        return "correct"
    if any(w in s for w in ["bias", "selection", "covariate", "third", "variable"]):
        return "partial"
    return "incorrect"

def grade_q4(raw):
    s = raw.lower()
    if any(w in s for w in ["0.054", "0.053", "0.052", "5.4", "5.3", "5.2", "positive", "benefit", "helps", "increase"]):
        return "correct"
    if any(w in s for w in ["standardis", "standardiz", "backdoor", "do(", "ate", "adjustment", "control", "gender"]):
        return "partial"
    return "incorrect"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 Causal Inference")
    st.markdown("#### Step-by-Step Assignment")
    st.markdown("---")
    for i, name in enumerate(STEPS):
        done   = i in st.session_state.visited and i < st.session_state.step
        active = i == st.session_state.step
        icon = "✅" if done else ("▶️" if active else "⬜")
        if st.button(f"{icon} {name}", key=f"nav_{i}", use_container_width=True):
            go(i); st.rerun()
    st.markdown("---")
    grades = [st.session_state.q1_grade, st.session_state.q2_grade,
              st.session_state.q3_grade, st.session_state.q4_grade]
    correct_count = sum(g == "correct" for g in grades)
    answered = sum(g != "" for g in grades)
    st.markdown(f"**Progress:** {answered}/4 answered")
    st.markdown(f"**Score:** {correct_count}/4 correct")
    st.markdown("---")
    st.caption("📚 Pearl, Glymour & Jewell\n*Causal Inference in Statistics: A Primer* — Example 1.2.1")

# ── Progress tracker ──────────────────────────────────────────────────────────
step = st.session_state.step
visited = st.session_state.visited

dots = ""
for i, name in enumerate(STEPS):
    is_done   = i in visited and i < step
    is_active = i == step
    cls = "done" if is_done else ("active" if is_active else "")
    short = name.split("—")[0].split("Q")[0].strip() if "—" not in name else "Q" + name.split("Q")[1].split("—")[0].strip()
    dots += f'<div class="prog-step"><div class="prog-dot {cls}">{i+1}</div><div class="prog-label">{short[:12]}</div></div>'
    if i < len(STEPS) - 1:
        dots += f'<div class="prog-line {"done" if is_done else ""}"></div>'

st.markdown(f'<div class="progress-track">{dots}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 0 — Introduction & Data
# ══════════════════════════════════════════════════════════════════════════════
if step == 0:
    st.markdown("""
    <div class="step-header">
        <div class="step-number">📖</div>
        <div>
            <p class="step-title">Introduction & Data</p>
            <p class="step-subtitle">Read carefully before answering any questions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="concept-card green">
        <h4>🎯 What is this assignment about?</h4>
        <p>This problem is based on <strong>Example 1.2.1</strong> from <em>Causal Inference in Statistics: A Primer</em>
        (Pearl, Glymour & Jewell). You will explore <strong>Simpson's Paradox</strong> — a phenomenon where a
        trend in grouped data reverses when groups are combined — and learn how <strong>causal reasoning</strong>
        reveals the true effect of a medication even in the presence of confounding.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 The Data — Recovery Rates of 700 Patients")
    st.markdown("""
    <div class="concept-card blue">
        <h4>📋 How to read this table</h4>
        <p>700 patients were prescribed a drug. Exactly <strong>350 took it</strong> and 350 did not.
        Numbers show how many <strong>recovered</strong> and the total <strong>n</strong> per subgroup.
        For example, "81 (n=87)" means 81 out of 87 men who took medication recovered.</p>
    </div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame({
        "Group":              ["Men",    "Women",  "Total"],
        "Recovered (Med)":    ["81",     "192",    "273"],
        "n — took Med":       ["87",     "263",    "350"],
        "Rate (Med)":         ["93.1%",  "73.0%",  "78.0%"],
        "Recovered (No Med)": ["234",    "55",     "289"],
        "n — No Med":         ["270",    "80",     "350"],
        "Rate (No Med)":      ["86.7%",  "68.8%",  "82.6%"],
    })
    st.markdown('<div class="data-table-wrap">', unsafe_allow_html=True)
    st.dataframe(df.set_index("Group"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="hint-box">
        <strong>💡 Notice something strange?</strong>
        The <em>Total row</em> shows No-Med patients recovering at a <em>higher</em> rate (82.6%) than Med patients (78.0%).
        Does that mean the drug is <em>harmful</em>? That is the paradox we will unravel — step by step!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔑 Key Concepts You Will Need")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="concept-card blue">
            <h4>📐 Conditional Probability</h4>
            <p><strong>P(A | B)</strong> = "probability of A <em>given</em> B has occurred."<br><br>
            Formula: <code>P(A|B) = count(A and B) / count(B)</code><br><br>
            Example: out of all women, how many took the medication?</p>
        </div>
        <div class="concept-card">
            <h4>🔀 Confounding Variable</h4>
            <p>A variable that influences <strong>both</strong> who receives the treatment
            <strong>and</strong> the outcome, creating a misleading association between them.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="concept-card green">
            <h4>⚖️ Simpson's Paradox</h4>
            <p>A trend can <strong>reverse</strong> when groups are combined. This happens when a
            confounding variable is distributed unevenly across groups, distorting the overall picture.</p>
        </div>
        <div class="concept-card amber">
            <h4>🎯 Causal Effect — do(X)</h4>
            <p>To find the <em>true</em> causal effect we imagine an <strong>intervention</strong>
            written as <strong>do(Med=1)</strong>. This removes the confounder's influence on who
            receives treatment, isolating the drug's real impact.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Begin Question 1 →"):
        go(1); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Q1
# ══════════════════════════════════════════════════════════════════════════════
elif step == 1:
    st.markdown("""
    <div class="step-header">
        <div class="step-number">1</div>
        <div>
            <p class="step-title">Question 1 — Probability of Taking Medication Given Female</p>
            <p class="step-subtitle">P(Medication = Yes | Gender = Female)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="concept-card">
        <h4>❓ The Question</h4>
        <p style="font-size:1.05rem;color:#1a1a2e;">
        What is the <strong>probability of taking medication given that the person is female</strong>?
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📘 Guided Solution — Follow These Steps")

    with st.expander("📌 Step A — Recall the conditional probability formula", expanded=True):
        st.markdown("""
        We want **P(Med | Female)**. The conditional probability formula tells us:
        """)
        st.markdown("""
        <div class="formula">
P(Med | Female) = (Number of females who TOOK medication)
                  ─────────────────────────────────────────
                       (Total number of females)
        </div>
        """, unsafe_allow_html=True)
        st.markdown("We are restricting our sample to **only females** and asking: within that group, what fraction took the medication?")

    with st.expander("📌 Step B — Find the numerator", expanded=True):
        st.markdown("Look at the **Women row** in the data table.")
        st.markdown("""
        <div class="hint-box">
        <strong>Numerator = Women who took medication</strong><br>
        From the table: "n — took Med" for Women = <strong>263</strong>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 Step C — Find the denominator", expanded=True):
        st.markdown("Total women = women who took Med **+** women who did NOT take Med")
        st.markdown("""
        <div class="hint-box">
        <strong>Denominator = Total women</strong><br>
        263 (took Med) + 80 (did NOT take Med) = <strong>343</strong>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 Step D — Compute the result", expanded=True):
        st.markdown("""
        <div class="formula">
P(Med | Female) = 263 / 343 = ?
        </div>
        """, unsafe_allow_html=True)
        st.markdown("Divide 263 by 343 and round to 4 decimal places.")

    st.markdown("### ✏️ Your Answer")
    st.markdown("Enter your answer as a decimal (e.g. `0.7667`) or a fraction (e.g. `263/343`):")
    ans = st.text_input("P(Med | Female) =", value=st.session_state.q1_ans,
                        key="q1_in", placeholder="Type your answer…")

    col_a, col_b = st.columns([1, 4])
    with col_a:
        if st.button("✔ Check Answer", key="chk1"):
            st.session_state.q1_ans = ans
            st.session_state.q1_grade = grade_q1(ans)
            st.session_state.q1_graded = True

    if st.session_state.q1_graded:
        g = st.session_state.q1_grade
        msg, css = GRADE_MSG[g]
        explanation = {
            "correct":   "Well done! 263 women took medication out of 343 total women.",
            "partial":   "You were close. Make sure numerator = 263 (women who took Med) and denominator = 343 (263 + 80).",
            "incorrect": "Hint: Numerator = 263 (women who took Med). Denominator = 263 + 80 = 343 (all women). Divide them.",
        }[g]
        st.markdown(f"""
        <div class="{css}">
            <h4>{msg}</h4>
            <p><strong>Correct answer:</strong> 263 / 343 ≈ <strong>0.7667</strong> (76.67%)</p>
            <p>{explanation}</p>
        </div>
        """, unsafe_allow_html=True)
        if g in ("correct", "partial"):
            st.markdown("""
            <div class="reveal-neutral">
                <h4>💡 What does this mean?</h4>
                <p>About <strong>77% of women</strong> chose to take the medication — much higher than men
                (87 / 357 ≈ 24%). This unequal uptake by gender is the seed of Simpson's Paradox and
                will become crucial when we estimate the drug's true causal effect in Q4.</p>
            </div>
            """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Introduction"):
            go(0); st.rerun()
    with col2:
        if st.button("Next: Question 2 →"):
            go(2); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Q2
# ══════════════════════════════════════════════════════════════════════════════
elif step == 2:
    st.markdown("""
    <div class="step-header">
        <div class="step-number">2</div>
        <div>
            <p class="step-title">Question 2 — Probability of Remission</p>
            <p class="step-subtitle">P(Remission | Medication = Yes, Gender = Female)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="concept-card">
        <h4>❓ The Question</h4>
        <p style="font-size:1.05rem;color:#1a1a2e;">
        What is the <strong>probability of remission of symptoms</strong> given that the person
        has <strong>taken their medication AND is female</strong>?
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📘 Guided Solution — Follow These Steps")

    with st.expander("📌 Step A — Two conditions = narrower sample", expanded=True):
        st.markdown("""
        We now condition on **two** things simultaneously: the person is **(1) Female** and **(2) took Medication**.
        That means we work *only* within the **Women + Med** cell of the table.
        """)
        st.markdown("""
        <div class="formula">
P(Remission | Med=Yes, Female) =
    (Women who TOOK medication AND recovered)
    ──────────────────────────────────────────
          (Total women who TOOK medication)
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 Step B — Find the numerator", expanded=True):
        st.markdown("""
        <div class="hint-box">
        <strong>Numerator = Women who took Med AND recovered</strong><br>
        "Recovered (Med)" for Women row = <strong>192</strong>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 Step C — Find the denominator", expanded=True):
        st.markdown("""
        <div class="hint-box">
        <strong>Denominator = Total women who took medication</strong><br>
        "n — took Med" for Women row = <strong>263</strong><br>
        (This is the same number we found in Q1!)
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 Step D — Compute", expanded=True):
        st.markdown("""
        <div class="formula">
P(Remission | Med, Female) = 192 / 263 = ?
        </div>
        """, unsafe_allow_html=True)
        st.markdown("Divide 192 by 263 and round to 4 decimal places.")

    st.markdown("### ✏️ Your Answer")
    ans = st.text_input("P(Remission | Med, Female) =", value=st.session_state.q2_ans,
                        key="q2_in", placeholder="Type your answer…")

    col_a, _ = st.columns([1, 4])
    with col_a:
        if st.button("✔ Check Answer", key="chk2"):
            st.session_state.q2_ans = ans
            st.session_state.q2_grade = grade_q2(ans)
            st.session_state.q2_graded = True

    if st.session_state.q2_graded:
        g = st.session_state.q2_grade
        msg, css = GRADE_MSG[g]
        explanation = {
            "correct":   "Great work! 192 out of 263 women who took medication recovered.",
            "partial":   "Almost! Use 192 as numerator (recovered women on Med) and 263 as denominator (all women who took Med).",
            "incorrect": "Hint: Among the 263 women who took medication, 192 recovered. Divide 192 by 263.",
        }[g]
        st.markdown(f"""
        <div class="{css}">
            <h4>{msg}</h4>
            <p><strong>Correct answer:</strong> 192 / 263 ≈ <strong>0.7300</strong> (73.0%)</p>
            <p>{explanation}</p>
        </div>
        """, unsafe_allow_html=True)
        if g in ("correct", "partial"):
            st.markdown("""
            <div class="reveal-neutral">
                <h4>💡 Interpretation</h4>
                <p>Among women who took the medication, <strong>73%</strong> recovered.
                Compare this to women who did NOT take it: 55/80 ≈ <strong>68.75%</strong>.
                Within the female group, the drug appears to <em>help</em> by ~4.3 percentage points.
                We'll see this pattern for men too in Q4!</p>
            </div>
            """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Q1"):
            go(1); st.rerun()
    with col2:
        if st.button("Next: Question 3 →"):
            go(3); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Q3
# ══════════════════════════════════════════════════════════════════════════════
elif step == 3:
    st.markdown("""
    <div class="step-header">
        <div class="step-number">3</div>
        <div>
            <p class="step-title">Question 3 — Identifying the Confounder (Selection Bias)</p>
            <p class="step-subtitle">Which variable distorts our estimate of the drug's effect?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="concept-card">
        <h4>❓ The Question</h4>
        <p style="font-size:1.05rem;color:#1a1a2e;">
        If we had observational data on <strong>Gender, Medication, and Remission</strong>,
        which variable is leading to <strong>selection bias</strong> when we try to measure
        the impact of taking the medication?
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📘 Guided Reasoning — Follow These Steps")

    with st.expander("📌 Step A — What does a confounder look like?", expanded=True):
        st.markdown("A variable is a confounder if it satisfies **both** of these conditions:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="concept-card green">
                <h4>Condition 1 — Affects Treatment</h4>
                <p>It influences who takes the medication (i.e., it predicts treatment choice).</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="concept-card green">
                <h4>Condition 2 — Affects Outcome</h4>
                <p>It independently influences recovery, <em>regardless</em> of medication.</p>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("📌 Step B — Check: Does Gender affect Medication uptake?", expanded=True):
        st.markdown("""
        <div class="hint-box">
        <strong>Women:</strong> 263 / 343 ≈ 77% took medication (from Q1)<br>
        <strong>Men:</strong> 87 / 357 ≈ 24% took medication<br><br>
        ✅ <strong>Yes — Gender strongly predicts who takes the drug.</strong>
        Women are 3× more likely to take the medication than men.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 Step C — Check: Does Gender affect Recovery independently?", expanded=True):
        st.markdown("Look at **No-Med** recovery rates (no drug influence here):")
        st.markdown("""
        <div class="hint-box">
        <strong>Men (no med):</strong> 234 / 270 ≈ 86.7% recovered naturally<br>
        <strong>Women (no med):</strong> 55 / 80 ≈ 68.8% recovered naturally<br><br>
        ✅ <strong>Yes — Men recover more easily even without the drug.</strong>
        Gender directly affects the outcome independent of medication.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 Step D — Why does this cause Simpson's Paradox?", expanded=True):
        st.markdown("""
        <div class="concept-card">
            <h4>The confounding mechanism</h4>
            <p>
            Women (who have <em>lower natural recovery</em>) disproportionately took the drug.<br>
            So the drug group is <strong>loaded with harder-to-treat patients</strong>.<br><br>
            When we aggregate, the drug looks less effective — not because it's bad, but because
            sicker/harder-to-recover patients happened to take it more. This is called
            <strong>confounding by indication</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="formula">
Confounding path:  Medication ← Gender → Remission

Gender causes BOTH medication uptake AND recovery outcome.
This "backdoor path" creates a spurious negative correlation
between medication and recovery in the raw data.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ✏️ Your Answer")
    st.markdown("Name the confounding variable and briefly explain why it causes selection bias:")
    ans = st.text_area("Your answer:", value=st.session_state.q3_ans, height=110,
                       key="q3_in", placeholder="e.g. 'Gender is the confounder because it affects both who takes the medication and recovery rates…'")

    col_a, _ = st.columns([1, 4])
    with col_a:
        if st.button("✔ Check Answer", key="chk3"):
            st.session_state.q3_ans = ans
            st.session_state.q3_grade = grade_q3(ans)
            st.session_state.q3_graded = True

    if st.session_state.q3_graded:
        g = st.session_state.q3_grade
        msg, css = GRADE_MSG[g]
        explanation = {
            "correct":   "Excellent! Gender is the confounder — it causes both treatment selection and the outcome, creating Simpson's Paradox.",
            "partial":   "You're on the right track! Be more specific: the variable is 'Gender', and it is a confounder because it satisfies both conditions above.",
            "incorrect": "The answer is Gender. It causes: (1) women to take medication far more than men, and (2) lower natural recovery in women regardless of medication.",
        }[g]
        st.markdown(f"""
        <div class="{css}">
            <h4>{msg}</h4>
            <p><strong>Correct answer:</strong> <strong>Gender</strong> is the confounding variable.
            It affects both treatment selection (women take meds 3× more) and recovery outcome
            (men recover more naturally), creating Simpson's Paradox in the raw data.</p>
            <p>{explanation}</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Q2"):
            go(2); st.rerun()
    with col2:
        if st.button("Next: Question 4 →"):
            go(4); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Q4
# ══════════════════════════════════════════════════════════════════════════════
elif step == 4:
    st.markdown("""
    <div class="step-header">
        <div class="step-number">4</div>
        <div>
            <p class="step-title">Question 4 — The True Causal Impact of Medication</p>
            <p class="step-subtitle">Backdoor Adjustment / Standardisation Formula</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="concept-card">
        <h4>❓ The Question</h4>
        <p style="font-size:1.05rem;color:#1a1a2e;">
        What is the <strong>causal impact</strong> of taking the medication on recovery?
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📘 Guided Solution — The Backdoor Adjustment")

    with st.expander("📌 Step A — Why the raw comparison is wrong", expanded=True):
        st.markdown("""
        The overall rates are: Med group = **78.0%** recovered, No-Med group = **82.6%** recovered.
        That naïvely suggests the drug *harms* patients — but this is the Simpson's Paradox trap!

        The comparison is polluted by Gender confounding. We need a method that
        **controls for gender** to isolate the drug's real effect.
        """)

    with st.expander("📌 Step B — The Backdoor Adjustment Formula", expanded=True):
        st.markdown("""
        We use **do-calculus**: we imagine assigning *everyone* the same medication status (do(Med=1)
        or do(Med=0)) while keeping the natural gender proportions of the population.
        """)
        st.markdown("""
        <div class="formula">
P(Recover | do(Med = m)) =
    Σ over Gender  [ P(Recover | Med=m, Gender=g) × P(Gender=g) ]

Where:
  P(Recover | Med=m, Gender=g) = within-group recovery rate (from table)
  P(Gender=g) = fraction of the total population of that gender
        </div>
        """, unsafe_allow_html=True)
        st.markdown("This formula **re-weights** the gender-specific rates by the population's actual gender mix, removing the confounding.")

    with st.expander("📌 Step C — Compute gender proportions (N = 700)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="hint-box">
            <strong>Total Men</strong> = 87 (took Med) + 270 (no Med) = 357<br>
            P(Male) = 357 / 700 ≈ <strong>0.5100</strong>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="hint-box">
            <strong>Total Women</strong> = 263 + 80 = 343<br>
            P(Female) = 343 / 700 ≈ <strong>0.4900</strong>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("📌 Step D — Compute P(Recover | do(Med = 1))", expanded=True):
        st.markdown("""
        <div class="formula">
Within-gender recovery rates IF taking medication:
  P(Recover | Med=1, Men)   = 81 / 87   ≈ 0.9310
  P(Recover | Med=1, Women) = 192 / 263 ≈ 0.7300

P(Recover | do(Med=1)) = 0.9310 × 0.5100  +  0.7300 × 0.4900
                       = 0.4748            +  0.3577
                       ≈ 0.8325
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 Step E — Compute P(Recover | do(Med = 0))", expanded=True):
        st.markdown("""
        <div class="formula">
Within-gender recovery rates if NOT taking medication:
  P(Recover | Med=0, Men)   = 234 / 270 ≈ 0.8667
  P(Recover | Med=0, Women) = 55 / 80   ≈ 0.6875

P(Recover | do(Med=0)) = 0.8667 × 0.5100  +  0.6875 × 0.4900
                       = 0.4420            +  0.3369
                       ≈ 0.7789
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 Step F — Average Treatment Effect (ATE)", expanded=True):
        st.markdown("""
        <div class="formula">
ATE = P(Recover | do(Med=1))  −  P(Recover | do(Med=0))
    = 0.8325                  −  0.7789
    ≈ +0.054

→ The medication INCREASES recovery probability by ~5.4 percentage points.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="concept-card green">
            <h4>🎉 The drug genuinely helps!</h4>
            <p>After controlling for Gender, the medication has a <strong>positive causal effect
            of ~5.4 percentage points</strong>. The raw data made it look harmful — but that was
            entirely an illusion created by confounding (sicker patients — women — happened to take
            the drug more). Once we standardise by gender, the truth emerges.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ✏️ Your Answer")
    st.markdown("Describe the causal impact — include whether it is positive/negative and the approximate magnitude:")
    ans = st.text_area("Your answer:", value=st.session_state.q4_ans, height=110,
                       key="q4_in",
                       placeholder="e.g. 'The medication has a positive causal effect of approximately 0.054 (5.4 percentage points), calculated using the backdoor adjustment formula controlling for gender.'")

    col_a, _ = st.columns([1, 4])
    with col_a:
        if st.button("✔ Check Answer", key="chk4"):
            st.session_state.q4_ans = ans
            st.session_state.q4_grade = grade_q4(ans)
            st.session_state.q4_graded = True

    if st.session_state.q4_graded:
        g = st.session_state.q4_grade
        msg, css = GRADE_MSG[g]
        explanation = {
            "correct":   "Correct! You correctly identified the positive ATE ≈ +0.054 using gender-adjusted standardisation.",
            "partial":   "Good thinking! Make sure to mention the direction (positive) and ideally the magnitude (~5.4 pp or 0.054), computed by the backdoor adjustment controlling for gender.",
            "incorrect": "Use the backdoor formula: standardise within-gender recovery rates by population gender proportions. ATE = P(R|do(Med=1)) − P(R|do(Med=0)) ≈ 0.8325 − 0.7789 = +0.054.",
        }[g]
        st.markdown(f"""
        <div class="{css}">
            <h4>{msg}</h4>
            <p><strong>Correct answer:</strong> ATE ≈ <strong>+0.054</strong> — the medication has a
            <strong>positive causal effect</strong>, increasing recovery by ~5.4 percentage points
            after controlling for gender via the backdoor adjustment formula.</p>
            <p>{explanation}</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Q3"):
            go(3); st.rerun()
    with col2:
        if st.button("Next: Question 5 (DAG) →"):
            go(5); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Q5 DAG
# ══════════════════════════════════════════════════════════════════════════════
elif step == 5:
    st.markdown("""
    <div class="step-header">
        <div class="step-number">5</div>
        <div>
            <p class="step-title">Question 5 — Causal Network (DAG)</p>
            <p class="step-subtitle">Draw & interpret the Directed Acyclic Graph for this problem</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="concept-card">
        <h4>❓ The Question</h4>
        <p style="font-size:1.05rem;color:#1a1a2e;">
        Draw and explain the <strong>causal network (DAG)</strong> representing the
        relationships among <strong>Gender, Medication, and Remission</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📘 What is a DAG?")
    with st.expander("📌 DAG Explained — Directed Acyclic Graph", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="concept-card blue">
                <h4>What each element means</h4>
                <p>
                <strong>Nodes</strong> = variables (Gender, Medication, Remission)<br><br>
                <strong>Arrows →</strong> = causal relationships ("X causes Y")<br><br>
                <strong>Acyclic</strong> = no feedback loops; causes flow in one direction only
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="concept-card amber">
                <h4>Why DAGs matter</h4>
                <p>A DAG lets us identify which paths carry <em>causal</em> information
                and which carry <em>spurious</em> associations. We can then
                decide what to control for to get an unbiased estimate.</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 🕸️ The DAG for This Problem")
    st.markdown("""
    <div class="dag-box">
        <span style="font-size:0.85rem;color:#fbbf24;letter-spacing:0.15em;">CONFOUNDER</span><br>
        <span style="font-size:1.3rem;font-weight:bold;color:#fbbf24;">GENDER</span><br>
        <span style="font-size:1.4rem;color:#93c5fd;">&nbsp;&nbsp;&nbsp;↙&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↘</span><br>
        <span style="font-size:1.1rem;">
        &nbsp;&nbsp;&nbsp;<span style="color:#f87171;">MEDICATION</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <span style="color:#6ee7b7;">REMISSION</span>
        </span><br>
        <span style="font-size:1.4rem;color:#93c5fd;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↘&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↗</span><br>
        <span style="font-size:0.8rem;color:#6b7280;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(direct causal path)</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 Interpreting Each Arrow")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="concept-card">
            <h4>Arrow 1<br>Gender → Medication</h4>
            <p>Women take medication at ~77%, men at ~24%. Gender <strong>causes treatment selection</strong>
            — a real-world selection effect (perhaps women had more access to or trust in this drug).</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="concept-card amber">
            <h4>Arrow 2<br>Gender → Remission</h4>
            <p>Even without medication, men recover at 86.7% vs women at 68.8%. Gender
            <strong>directly affects recovery</strong> — making it a true confounder
            (it independently affects the outcome).</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="concept-card green">
            <h4>Arrow 3<br>Medication → Remission</h4>
            <p>This is the <strong>causal path we want to estimate</strong>. The backdoor adjustment
            (Q4) isolated this effect by blocking the spurious path through Gender.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 The Backdoor Path & How to Block It", expanded=True):
        st.markdown("""
        <div class="formula">
Backdoor (confounding) path:  Medication ← Gender → Remission

This path creates a SPURIOUS association between Medication and Remission
that has nothing to do with the drug's actual effect.

To block it: condition on Gender (stratify your analysis by gender).
This is exactly what the backdoor adjustment formula in Q4 did.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="concept-card green">
            <h4>The key insight</h4>
            <p>Once we condition on Gender, the only remaining path from Medication to Remission
            is the <strong>direct causal arrow</strong>. The backdoor path is blocked, and we recover
            the true ATE ≈ +0.054 — the drug genuinely helps by ~5.4 percentage points.</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Q4"):
            go(4); st.rerun()
    with col2:
        if st.button("Go to Final Review →"):
            go(6); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — Final Review
# ══════════════════════════════════════════════════════════════════════════════
elif step == 6:
    st.markdown("""
    <div class="step-header">
        <div class="step-number">🏁</div>
        <div>
            <p class="step-title">Final Review — Your Complete Assignment</p>
            <p class="step-subtitle">Your answers, scores, and key takeaways</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    grades = {
        "q1": st.session_state.q1_grade,
        "q2": st.session_state.q2_grade,
        "q3": st.session_state.q3_grade,
        "q4": st.session_state.q4_grade,
    }
    correct_n  = sum(g == "correct" for g in grades.values())
    partial_n  = sum(g == "partial"  for g in grades.values())
    answered_n = sum(g != ""         for g in grades.values())
    score_pct  = int(((correct_n + 0.5 * partial_n) / 4) * 100)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="scorecard">
            <div class="big">{correct_n}/4</div>
            <div class="sub">Fully Correct</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="scorecard" style="border-color:#fbbf24;">
            <div class="big" style="color:#fbbf24;">{partial_n}</div>
            <div class="sub">Partial Credit</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        colour = "#4ade80" if score_pct >= 75 else ("#fbbf24" if score_pct >= 50 else "#fb7185")
        st.markdown(f"""
        <div class="scorecard" style="border-color:{colour};">
            <div class="big" style="color:{colour};">{score_pct}%</div>
            <div class="sub">Weighted Score</div>
        </div>""", unsafe_allow_html=True)

    if answered_n < 4:
        st.warning(f"⚠️ You have only answered {answered_n}/4 questions. Go back and complete the remaining ones for a full score.")

    st.markdown("---")
    st.markdown("### 📋 Answer Comparison")

    review = [
        ("Q1", "P(Med | Female)",             st.session_state.q1_ans, "263 / 343 ≈ **0.7667** (76.67%)",         st.session_state.q1_grade),
        ("Q2", "P(Remission | Med, Female)",  st.session_state.q2_ans, "192 / 263 ≈ **0.7300** (73.00%)",         st.session_state.q2_grade),
        ("Q3", "Confounding variable",         st.session_state.q3_ans, "**Gender** — confounder (Simpson's Paradox)", st.session_state.q3_grade),
        ("Q4", "Causal impact (ATE)",          st.session_state.q4_ans, "ATE ≈ **+0.054** — positive, ~5.4 pp benefit", st.session_state.q4_grade),
    ]

    for qid, qname, user_ans, correct_ans, grade in review:
        icon = {"correct": "✅", "partial": "⚠️", "incorrect": "❌", "": "⬜"}[grade]
        with st.expander(f"{icon}  {qid} — {qname}", expanded=(grade not in ("correct","partial"))):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Your answer:**")
                st.info(user_ans.strip() if user_ans.strip() else "_Not answered_")
            with col2:
                st.markdown("**Correct answer:**")
                st.success(correct_ans)

    st.markdown("---")
    st.markdown("### 💡 Three Key Lessons from This Problem")

    st.markdown("""
    <div class="concept-card green">
        <h4>Lesson 1 — Simpson's Paradox is real and dangerous</h4>
        <p>Raw aggregate data showed the drug looked harmful (78% vs 82.6%). But within every
        gender subgroup, the drug <em>helped</em>. Aggregating without accounting for confounders
        can completely reverse the apparent direction of an effect. Always look at subgroups!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="concept-card blue">
        <h4>Lesson 2 — Observational data requires causal thinking</h4>
        <p>In this study, patients chose whether to take the medication — a classic observational
        setup. This means who takes the drug is <em>not random</em>; it is driven by other factors
        (like gender) that also affect outcomes. Naïve comparisons are biased. We need explicit
        causal models (DAGs) to think clearly about what to control for.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="concept-card">
        <h4>Lesson 3 — The backdoor adjustment recovers the truth</h4>
        <p>By <strong>stratifying within gender</strong> and then averaging with correct population
        weights, we blocked the confounding path and found the true ATE ≈ +0.054.
        This is the do-calculus in action: <em>P(R | do(Med=1)) − P(R | do(Med=0)) ≈ +5.4 pp</em>.
        The drug genuinely helps. Causal reasoning saved us from a false conclusion.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Restart Assignment from Beginning"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
