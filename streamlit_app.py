import streamlit as st
import uuid
from datetime import datetime

# Session State Init
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Helper to go to next step
def next_step():
    st.session_state.step += 1

def reset():
    st.session_state.step = 1
    st.session_state.form_data = {}

# Step 1: Welcome
def step_1():
    st.title("🏙️ NYC LL144 Compliance Assistant")
    st.markdown("Turn complex compliance into a guided audit. Let's see if you're ready for NYC's AI Hiring Law.")
    if st.button("Start My Audit →"):
        next_step()

# Step 2: Confirm AEDT Use
def step_2():
    st.header("Step 1: Do You Use an Automated Hiring Tool?")
    st.markdown("NYC LL144 applies to tools that automate candidate assessment or decision-making.")

    use_aedt = st.radio("Do you use an Automated Employment Decision Tool (AEDT)?", ["Yes", "No", "Unsure"])
    st.session_state.form_data['uses_aedt'] = use_aedt

    if st.button("Continue →"):
        if use_aedt == "No":
            st.warning("LL144 may not apply to your company. You're free to continue if you still want an audit.")
        next_step()

# Step 3: Job Role Impact
def step_3():
    st.header("Step 2: Which Roles Are Affected?")
    roles = st.multiselect("Select impacted job categories:", 
                           ["Engineering", "Sales", "Customer Support", "HR", "Operations", "Marketing", "Other"])
    hiring_volume = st.slider("Roughly how many people do you hire per year using AEDTs?", 0, 500, 10)

    st.session_state.form_data['roles'] = roles
    st.session_state.form_data['hiring_volume'] = hiring_volume

    if st.button("Continue →"):
        next_step()

# Step 4: Upload Bias Audit
def step_4():
    st.header("Step 3: Upload Your Most Recent Bias Audit")
    uploaded_file = st.file_uploader("PDF or JSON audit file", type=['pdf', 'json'])
    st.session_state.form_data['uploaded_audit'] = uploaded_file.name if uploaded_file else None

    if uploaded_file:
        st.success("File received: " + uploaded_file.name)

    if st.button("Continue →", disabled=not uploaded_file):
        next_step()

# Step 5: Public Disclosure Link
def step_5():
    st.header("Step 4: Link to Your Public Audit Summary")
    public_url = st.text_input("Paste the public URL where this audit is accessible:")
    st.session_state.form_data['audit_url'] = public_url

    if st.button("Continue →", disabled=not public_url.startswith("http")):
        next_step()

# Step 6: Candidate Notice
def step_6():
    st.header("Step 5: Did You Notify Candidates?")
    notice = st.radio("Did your candidates receive notice 10+ business days in advance?", ["Yes", "No"])
    st.session_state.form_data['notice_given'] = notice

    if st.button("Continue →"):
        next_step()

# Step 7: Summary + Placeholder Score
def step_7():
    st.header("🧾 Audit Summary")

    form_data = st.session_state.form_data
    st.write("### Your Inputs:")
    st.json(form_data)

    # Placeholder score
    score = 80 if form_data.get('uses_aedt') == "Yes" else 50
    st.write(f"### Preliminary Compliance Score: **{score}/100**")
    
    if score >= 75:
        st.success("You're mostly compliant. Download a summary or request full certification.")
    else:
        st.warning("Compliance gaps detected. Recommend next steps and remediation.")

    if st.button("🔄 Start Over"):
        reset()

# Routing logic
if st.session_state.step == 1:
    step_1()
elif st.session_state.step == 2:
    step_2()
elif st.session_state.step == 3:
    step_3()
elif st.session_state.step == 4:
    step_4()
elif st.session_state.step == 5:
    step_5()
elif st.session_state.step == 6:
    step_6()
elif st.session_state.step == 7:
    step_7()
