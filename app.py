from PIL import Image
import streamlit as st

# -----------------------------
# Assets (avatars / header)
# -----------------------------
ALEX_AVATAR = Image.open("assets/alex.png")
SAM_AVATAR = Image.open("assets/sam.png")
MED_AVATAR = Image.open("assets/mediator.png")

# -----------------------------
# Scenario data
# -----------------------------
SCENARIO = {
    "title": "Demo Deadline Conflict",
    "initial_state": {"turn": 0, "tension": 50, "trust_alex": 55, "trust_sam": 55},
    "scoring": {
        "best":   {"tension": -15, "trust_alex": 10, "trust_sam": 10},
        "medium": {"tension": -5,  "trust_alex": 3,  "trust_sam": 3},
        "bad":    {"tension": 10,  "trust_alex": -5, "trust_sam": -5},
    },
    "end_conditions": {
        "win":  {"tension_max": 20, "trust_min": 70},
        "lose": {"tension_min": 85, "trust_min": 20},
    },
    "turns": [
        {
            "alex": "Sam, you ignored the delivery date again. I promised the dashboard demo today.",
            "sam": "Because your requirements changed three times. I’m not shipping something broken.",
            "choices": [
                {"id": "A", "text": "Let’s pause. Alex, what exactly must be shown today? Sam, what’s the minimum safe demo you can support?", "grade": "best"},
                {"id": "B", "text": "Both of you need to calm down and be professional.", "grade": "medium"},
                {"id": "C", "text": "Sam, you should’ve followed the deadline. Alex’s promise matters.", "grade": "bad"},
            ],
        },
        {
            "alex": "We need the KPI tiles + one trend chart, that’s it.",
            "sam": "Those KPIs depend on a data pipeline that still fails sometimes.",
            "choices": [
                {"id": "A", "text": "So the goal is a stable demo of KPI tiles + trend chart. Sam, what failure risk remains? Alex, what can we drop if needed?", "grade": "best"},
                {"id": "B", "text": "Sam, just hardcode the numbers for now.", "grade": "bad"},
                {"id": "C", "text": "Alex, stop changing scope.", "grade": "medium"},
            ],
        },
        {
            "alex": "Stakeholders don’t care about perfect accuracy today.",
            "sam": "They’ll absolutely notice if numbers don’t match last week’s report.",
            "choices": [
                {"id": "A", "text": "Let’s align on ‘demo quality’: consistent with last report, clearly labeled as preliminary, and no crashes. Agree?", "grade": "best"},
                {"id": "B", "text": "Accuracy doesn’t matter in demos.", "grade": "bad"},
                {"id": "C", "text": "Sam, you’re overthinking it.", "grade": "bad"},
            ],
        },
        {
            "alex": "You didn’t tell me the pipeline was unstable until last night.",
            "sam": "I did—on Slack—two weeks ago.",
            "choices": [
                {"id": "A", "text": "Sounds like a communication gap. Can each of you show what you sent/received, then we define one ‘single source’ for status updates?", "grade": "best"},
                {"id": "B", "text": "Slack is messy. Use email next time.", "grade": "medium"},
                {"id": "C", "text": "Alex, you must’ve missed it. Pay attention.", "grade": "bad"},
            ],
        },
        {
            "alex": "I need predictability.",
            "sam": "I need requirements that don’t move mid-sprint.",
            "choices": [
                {"id": "A", "text": "Let’s set a rule: Alex freezes demo scope by today 6pm; Sam commits to a demo build by tomorrow 10am. Changes after freeze go to a backlog.", "grade": "best"},
                {"id": "B", "text": "Both of you should try harder to be flexible.", "grade": "medium"},
                {"id": "C", "text": "No more changes, Alex. Ever.", "grade": "bad"},
            ],
        },
        {
            "alex": "Okay, but what exactly are we showing?",
            "sam": "If it’s only 2 KPIs + 1 chart, I can make it stable.",
            "choices": [
                {"id": "A", "text": "Great. Confirm: 2 KPIs, 1 trend chart, data from last validated snapshot, and we add a footer ‘Demo — preliminary’. Deal?", "grade": "best"},
                {"id": "B", "text": "Show everything, but warn them it might crash.", "grade": "bad"},
                {"id": "C", "text": "Keep it simple. Just do something.", "grade": "medium"},
            ],
        },
        {
            "alex": "I’m still frustrated about being surprised.",
            "sam": "I’m still frustrated about being blamed.",
            "choices": [
                {"id": "A", "text": "Before we close: Alex, say one thing you’ll do differently (status check rhythm). Sam, say one thing you’ll do differently (raise risks earlier + clearer).", "grade": "best"},
                {"id": "B", "text": "Let’s not talk about feelings—just work.", "grade": "medium"},
                {"id": "C", "text": "You’re both equally at fault, so move on.", "grade": "bad"},
            ],
        },
        {
            "alex": "I’ll run a 10-min daily demo check-in and confirm scope in writing.",
            "sam": "I’ll flag pipeline risk with a clear impact + options, not just a message.",
            "choices": [
                {"id": "A", "text": "Awesome. I’ll summarize: scope, deadline, quality bar, and comms rule. If anything changes, we escalate within 1 hour.", "grade": "best"},
                {"id": "B", "text": "Good, let’s hope it works now.", "grade": "medium"},
                {"id": "C", "text": "Finally. That wasn’t so hard, right?", "grade": "bad"},
            ],
        },
    ],
}

# -----------------------------
# Helpers (define BEFORE usage)
# -----------------------------
def clamp(x):
    return max(0, min(100, x))

def reset():
    init = SCENARIO["initial_state"]
    st.session_state.turn = init["turn"]
    st.session_state.tension = init["tension"]
    st.session_state.trust_alex = init["trust_alex"]
    st.session_state.trust_sam = init["trust_sam"]
    st.session_state.log = []
    st.session_state.dialogue_added = False
    st.session_state.finished = False
    st.session_state.finish_reason = None

def check_end():
    win = SCENARIO["end_conditions"]["win"]
    lose = SCENARIO["end_conditions"]["lose"]
    if (
        st.session_state.tension <= win["tension_max"]
        and st.session_state.trust_alex >= win["trust_min"]
        and st.session_state.trust_sam >= win["trust_min"]
    ):
        return "win"
    if (
        st.session_state.tension >= lose["tension_min"]
        or st.session_state.trust_alex <= lose["trust_min"]
        or st.session_state.trust_sam <= lose["trust_min"]
    ):
        return "lose"
    return None

# -----------------------------
# Init session
# -----------------------------
if "turn" not in st.session_state:
    reset()

# -----------------------------
# UI header + controls
# -----------------------------
st.set_page_config(page_title=SCENARIO["title"], layout="centered")
st.title(SCENARIO["title"])
st.image("assets/header.png", use_container_width=True)

controls = st.columns([1, 1, 3])
with controls[0]:
    st.button("🔄 Restart", on_click=reset)

with controls[1]:
    if st.button("⏹️ Finish game"):
        st.session_state.finished = True
        st.session_state.finish_reason = "Player ended the game early."
        st.rerun()

# Finished screen
if st.session_state.finished:
    st.info(f"Game finished. Reason: {st.session_state.finish_reason}")
    st.write(
        f"**Final stats** — Tension: {st.session_state.tension}, "
        f"Trust(Alex): {st.session_state.trust_alex}, Trust(Sam): {st.session_state.trust_sam}"
    )
    st.stop()

# -----------------------------
# Stats + meters
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Turn", f"{st.session_state.turn+1}/{len(SCENARIO['turns'])}")
col2.metric("Tension", st.session_state.tension)
col3.metric("Trust (Alex)", st.session_state.trust_alex)
col4.metric("Trust (Sam)", st.session_state.trust_sam)

st.subheader("Conflict level")
st.progress(st.session_state.tension / 100)

st.subheader("Trust meters")
st.write("Alex")
st.progress(st.session_state.trust_alex / 100)
st.write("Sam")
st.progress(st.session_state.trust_sam / 100)

st.divider()

# -----------------------------
# Current turn: add Alex/Sam once, then render transcript once
# -----------------------------
turn_data = SCENARIO["turns"][st.session_state.turn]

if not st.session_state.dialogue_added:
    st.session_state.log.append(("Alex", turn_data["alex"]))
    st.session_state.log.append(("Sam", turn_data["sam"]))
    st.session_state.dialogue_added = True

# Transcript (render ONCE, with avatars)
for speaker, msg in st.session_state.log:
    if speaker == "Alex":
        with st.chat_message("assistant", avatar=ALEX_AVATAR):
            st.markdown(msg)
    elif speaker == "Sam":
        with st.chat_message("assistant", avatar=SAM_AVATAR):
            st.markdown(msg)
    else:
        with st.chat_message("user", avatar=MED_AVATAR):
            st.markdown(msg)

st.divider()

# -----------------------------
# Choices
# -----------------------------
st.markdown("### Choose your mediation message:")
chosen = None
for i, ch in enumerate(turn_data["choices"]):
    if st.button(f"{ch['id']}) {ch['text']}", key=f"choice_{st.session_state.turn}_{i}"):
        chosen = ch

if chosen:
    st.session_state.log.append(("Mediator", chosen["text"]))

    delta = SCENARIO["scoring"][chosen["grade"]]
    st.session_state.tension = clamp(st.session_state.tension + delta["tension"])
    st.session_state.trust_alex = clamp(st.session_state.trust_alex + delta["trust_alex"])
    st.session_state.trust_sam = clamp(st.session_state.trust_sam + delta["trust_sam"])

    outcome = check_end()
    if outcome == "win":
        st.success("✅ Conflict managed! Tension is low and trust is high.")
        st.stop()
    if outcome == "lose":
        st.error("❌ Conflict escalated. Try different mediation choices.")
        st.stop()

    # Next turn or finish
    if st.session_state.turn < len(SCENARIO["turns"]) - 1:
        st.session_state.turn += 1
        st.session_state.dialogue_added = False
        st.rerun()
    else:
        st.session_state.finished = True
        st.session_state.finish_reason = "Completed all questions."
        st.rerun()



