import streamlit as st
import json
import random
from pathlib import Path

st.set_page_config(
    page_title="PSD Quiz Trainer",
    page_icon=":dart:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
    .block-container { padding-top: 2rem; max-width: 800px; }

    div.stButton > button {
        text-align: left;
        padding: 0.85rem 1.2rem;
        border-radius: 0.6rem;
        font-size: 1rem;
        transition: transform 0.1s ease, box-shadow 0.15s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(100, 100, 255, 0.15);
    }

    .option-neutral {
        padding: 0.75rem 1rem;
        margin: 0.35rem 0;
        border-radius: 0.5rem;
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.18);
        opacity: 0.45;
        font-size: 0.97rem;
    }

    .grade-ring {
        display: flex; align-items: center; justify-content: center;
        width: 120px; height: 120px; border-radius: 50%;
        font-size: 2.4rem; font-weight: 700; margin: 0 auto 0.5rem;
    }
    .grade-a  { border: 5px solid #22c55e; color: #22c55e; }
    .grade-b  { border: 5px solid #3b82f6; color: #3b82f6; }
    .grade-c  { border: 5px solid #f59e0b; color: #f59e0b; }
    .grade-f  { border: 5px solid #ef4444; color: #ef4444; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Load question bank
# ---------------------------------------------------------------------------
QUESTIONS_FILE = Path(__file__).parent / "questions.json"


@st.cache_data
def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


data = load_questions()

# ---------------------------------------------------------------------------
# Session-state defaults
# ---------------------------------------------------------------------------
_DEFAULTS = {
    "page": "dashboard",
    "current_topic": None,
    "questions": [],
    "q_idx": 0,
    "score": 0,
    "answered": False,
    "selected": None,
    "is_correct": None,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

def _start_quiz(topic_key: str):
    if topic_key == "full_mock":
        pool = []
        for t in data["topics"].values():
            pool.extend(t["questions"])
    else:
        pool = list(data["topics"][topic_key]["questions"])
    random.shuffle(pool)
    st.session_state.update(
        page="quiz",
        current_topic=topic_key,
        questions=pool,
        q_idx=0,
        score=0,
        answered=False,
        selected=None,
        is_correct=None,
    )


def _select_answer(option_idx: int, correct_idx: int):
    st.session_state.answered = True
    st.session_state.selected = option_idx
    st.session_state.is_correct = option_idx == correct_idx
    if st.session_state.is_correct:
        st.session_state.score += 1


def _next_question():
    st.session_state.q_idx += 1
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.is_correct = None


def _go_results():
    st.session_state.page = "results"


def _go_dashboard():
    st.session_state.update(**_DEFAULTS)


# ---------------------------------------------------------------------------
# PAGE: Dashboard
# ---------------------------------------------------------------------------

def _render_dashboard():
    st.markdown(
        "<h1 style='text-align:center; margin-bottom:0;'>"
        "&#127919; PSD Quiz Trainer</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; opacity:0.6; margin-top:0;'>"
        "Professional Software Development &mdash; MCQ Revision</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    main_col, qr_col = st.columns([3, 2])

    with main_col:
        topic_keys = list(data["topics"].keys())
        col1, col2 = st.columns(2)
        columns = [col1, col2, col1, col2]

        for i, key in enumerate(topic_keys):
            t = data["topics"][key]
            count = len(t["questions"])
            label = f"{t['icon']}  {t['name']}"
            sub = f"{count} question{'s' if count != 1 else ''}" if count else "Coming soon"
            with columns[i]:
                st.button(
                    f"{label}\n{sub}",
                    key=f"dash_{key}",
                    on_click=_start_quiz,
                    args=(key,),
                    use_container_width=True,
                    disabled=count == 0,
                )

        st.divider()

        total_q = sum(len(t["questions"]) for t in data["topics"].values())
        st.button(
            f"[*] Full Mock Exam\n{total_q} questions across all topics",
            key="dash_full",
            on_click=_start_quiz,
            args=("full_mock",),
            use_container_width=True,
            disabled=total_q == 0,
        )

    with qr_col:
        qr_path = Path(__file__).parent / "donation_qr.jpg"
        st.image(str(qr_path), use_container_width=True)
        st.markdown(
            "<p style='text-align:center; font-size:0.9rem; opacity:0.75;'>"
            "your donation plays a part for my wingstop</p>",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# PAGE: Quiz
# ---------------------------------------------------------------------------

def _render_quiz():
    questions = st.session_state.questions
    idx = st.session_state.q_idx
    total = len(questions)
    q = questions[idx]
    correct_idx = q["correct"]

    topic_label = "Full Mock Exam"
    if st.session_state.current_topic != "full_mock":
        topic_label = data["topics"][st.session_state.current_topic]["name"]

    hdr1, hdr2 = st.columns([4, 1])
    with hdr1:
        st.markdown(f"### {topic_label}")
    with hdr2:
        st.button("X  Quit", on_click=_go_dashboard, type="secondary")

    progress_value = (idx + 1) / total
    st.progress(progress_value, text=f"Question {idx + 1} of {total}")

    answered_so_far = idx + (1 if st.session_state.answered else 0)
    st.caption(f"Score: **{st.session_state.score} / {answered_so_far}**")

    st.markdown(f"**Q{idx + 1}.** {q['question']}")
    st.divider()

    letters = "ABCD"
    if not st.session_state.answered:
        for i, opt in enumerate(q["options"]):
            st.button(
                f"{letters[i]})  {opt}",
                key=f"opt_{idx}_{i}",
                on_click=_select_answer,
                args=(i, correct_idx),
                use_container_width=True,
            )
    else:
        for i, opt in enumerate(q["options"]):
            label = f"{letters[i]})  {opt}"
            if i == correct_idx:
                st.success(f"Correct:  {label}")
            elif i == st.session_state.selected:
                st.error(f"Wrong:  {label}")
            else:
                st.markdown(
                    f'<div class="option-neutral">{label}</div>',
                    unsafe_allow_html=True,
                )

        st.divider()
        if st.session_state.is_correct:
            st.markdown("#### Correct!")
        else:
            st.markdown("#### Incorrect")

        st.info(f"**Rationale:** {q['rationale']}")

        if idx + 1 < total:
            st.button(
                "Next Question  >>",
                on_click=_next_question,
                type="primary",
                use_container_width=True,
            )
        else:
            st.button(
                "See Results  >>",
                on_click=_go_results,
                type="primary",
                use_container_width=True,
            )


# ---------------------------------------------------------------------------
# PAGE: Results
# ---------------------------------------------------------------------------

def _render_results():
    score = st.session_state.score
    total = len(st.session_state.questions)
    pct = (score / total * 100) if total else 0

    st.markdown(
        "<h1 style='text-align:center;'>&#128202; Quiz Complete!</h1>",
        unsafe_allow_html=True,
    )
    st.divider()

    if pct >= 80:
        grade, css = "A", "grade-a"
    elif pct >= 70:
        grade, css = "B", "grade-b"
    elif pct >= 60:
        grade, css = "C", "grade-c"
    else:
        grade, css = "F", "grade-f"

    st.markdown(
        f'<div class="grade-ring {css}">{grade}</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Score", f"{score} / {total}")
    m2.metric("Percentage", f"{pct:.1f}%")
    m3.metric("Grade", grade)

    st.divider()

    if pct >= 80:
        st.success("Excellent work! You have a strong grasp of this topic.")
    elif pct >= 60:
        st.warning("Good effort! Review the questions you missed and try again.")
    else:
        st.error("Keep studying! Go through the lecture notes and retry.")

    c1, c2 = st.columns(2)
    with c1:
        st.button(
            "Retry",
            on_click=_start_quiz,
            args=(st.session_state.current_topic,),
            use_container_width=True,
        )
    with c2:
        st.button(
            "Dashboard",
            on_click=_go_dashboard,
            use_container_width=True,
        )


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

_PAGES = {
    "dashboard": _render_dashboard,
    "quiz": _render_quiz,
    "results": _render_results,
}
_PAGES[st.session_state.page]()
