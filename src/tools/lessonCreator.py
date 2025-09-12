import streamlit as st
import json
from pathlib import Path

# ----------------- Helpers ----------------- #
def load_json(file_path, default=None):
    path = Path(file_path)
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return default if default is not None else {}

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def slugify(text):
    return text.lower().replace(" ", "_").replace(".", "").replace(",", "")

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# ----------------- Paths ----------------- #
BASE_DIR = Path("../content-sources/oatutor")
COURSE_PLANS_FILE = BASE_DIR / "coursePlans.json"
SKILL_MODEL_FILE = BASE_DIR / "skillModel.json"
BKT_PARAMS_FILE = BASE_DIR / "bkt-params" / "defaultBKTParams.json"
CONTENT_POOL = BASE_DIR / "content-pool"

# ----------------- Streamlit UI ----------------- #
st.set_page_config(page_title="OATutor Content Creator", layout="wide")
st.title("📘 OATutor Content Creator")

tab_courses, tab_lessons, tab_problems, tab_skills = st.tabs(
    ["📘 Courses", "📖 Lessons", "📝 Problems", "⚙️ Skills"]
)

# ----------------- COURSES ----------------- #
with tab_courses:
    st.header("📘 Courses Management")
    course_plans = load_json(COURSE_PLANS_FILE, default=[])

    # Form to add a new course
    with st.form("new_course_form"):
        course_name = st.text_input("Course Name")
        course_oer = st.text_input("Course OER (URL)")
        course_license = st.text_input("Course License")
        submitted = st.form_submit_button("➕ Add Course")
        if submitted:
            if not course_name:
                st.error("Course Name is required!")
            else:
                new_course = {
                    "courseName": course_name,
                    "courseOER": course_oer,
                    "courseLicense": course_license,
                    "lessons": []
                }
                course_plans.append(new_course)
                save_json(COURSE_PLANS_FILE, course_plans)
                st.success(f"✅ Course '{course_name}' added!")

    st.subheader("Existing Courses")
    if course_plans:
        for course in course_plans:
            st.write(f"- {course['courseName']} ({len(course['lessons'])} lessons)")
    else:
        st.info("No courses yet.")

# ----------------- LESSONS -----------------
with tab_lessons:
    st.header("📖 Create Lessons")

    course_plans = load_json(COURSE_PLANS_FILE, default=[])
    course_names = [c["courseName"] for c in course_plans]

    bkt_params = load_json(BKT_PARAMS_FILE, default={})
    skills_list = list(bkt_params.keys())

    if not course_names:
        st.warning("⚠️ No courses found. Please create a course first.")
    else:
        if "learningObjectives" not in st.session_state:
            st.session_state.learningObjectives = {}

        # ------------ UI to ADD Learning Objectives (OUTSIDE the form) ------------
        st.markdown("### 1. Add Learning Objectives")
        col1, col2, col3 = st.columns([4, 2, 1])
        with col1:
            new_lo_input = st.text_input("Search/Add Learning Objective", key="new_lo_text")
            suggestions = [s for s in skills_list if new_lo_input.lower() in s.lower()] if new_lo_input else skills_list
            selected_lo = st.selectbox("Select from existing or type new", options=suggestions, key="selected_lo_suggestion")

        with col2:
            new_weight = st.number_input("Weight", min_value=0.0, max_value=1.0, value=0.85, step=0.05, key="new_lo_weight")
        with col3:
            st.write("&#8203;") # Espaço em branco para alinhar verticalmente
            add_lo_button = st.button("➕ Add LO")

        if add_lo_button and selected_lo:
            st.session_state.learningObjectives[selected_lo] = new_weight

        if st.session_state.learningObjectives:
            st.write("Current Learning Objectives for the new lesson:")
            for k, v in st.session_state.learningObjectives.items():
                st.write(f"- **{k}** (Weight: {v})")
            if st.button("Clear All LOs"):
                 st.session_state.learningObjectives = {}
                 st.rerun()
        st.divider()

        # ---------- Main Form ----------
        st.markdown("### 2. Enter Lesson Details and Save")
        with st.form("new_lesson_form"):
            selected_course = st.selectbox("Select Course", options=course_names)

            lesson_id = st.text_input("Lesson ID (slug)", value="lesson1")
            lesson_name = st.text_input("Lesson Name", value="Lesson 1.1")
            lesson_topics = st.text_input("Lesson Topics", value="Introduction")

            # ---------- Preview JSON ----------
            lesson_obj = {
                "id": lesson_id,
                "name": lesson_name,
                "topics": lesson_topics,
                "allowRecycle": True,
                "learningObjectives": st.session_state.learningObjectives
            }
            st.subheader("Preview Lesson JSON")
            st.json(lesson_obj)

            # ---------- Submit button form ----------
            submitted = st.form_submit_button("💾 Create and Save Lesson")
            if submitted:
                if not st.session_state.learningObjectives:
                    st.error("Please add at least one Learning Objective.")
                elif not lesson_id or not lesson_name:
                    st.error("Lesson ID and Lesson Name are required.")
                else:
                    for course in course_plans:
                        if course["courseName"] == selected_course:
                            course["lessons"].append(lesson_obj)
                    save_json(COURSE_PLANS_FILE, course_plans)
                    st.success(f"✅ Lesson '{lesson_name}' added to course '{selected_course}'!")
                    st.session_state.learningObjectives = {}
                    # st.rerun() # Rerun to clean UI

# ----------------- PROBLEMS ----------------- #
with tab_problems:
    st.header("📝 Problems Management")

    # Load data
    course_plans = load_json(COURSE_PLANS_FILE, default=[])
    skill_model = load_json(SKILL_MODEL_FILE, default={})
    bkt_params = load_json(BKT_PARAMS_FILE, default={})

    course_names = [c["courseName"] for c in course_plans]
    lessons = [l for c in course_plans for l in c.get("lessons", [])]
    lesson_map = {l["id"]: l for l in lessons}
    lesson_ids = [l["id"] for l in lessons]
    learning_objectives = list(bkt_params.keys())

    st.subheader("Problem Info")
    problem_title = st.text_input("Problem Title")
    problem_body = st.text_area("Problem Body (supports LaTeX with $$...$$)")
    problem_type = st.selectbox("Problem Type", ["TextBox", "MultipleChoice"])

    selected_course = st.selectbox("Course", options=course_names if course_names else ["<none>"])
    selected_lesson = st.selectbox("Lesson ID", options=[l["id"] for l in lessons if l["id"]], index=0 if lesson_ids else 0)

    step_title = st.text_input("Step Title")

    # Choices + AnswerType dynamically
    step_answer = []
    choices = []
    answer_type = "string"
    if problem_type == "MultipleChoice":
        st.subheader("Choices (one per line)")
        choices_input = st.text_area("Enter choices", placeholder="Choice 1\nChoice 2\nChoice 3")
        choices = [c.strip() for c in choices_input.splitlines() if c.strip()]

        if choices:
            st.subheader("Correct Answers")
            step_answer = st.multiselect("Select correct answers", options=choices)
            computed_answer_type = "MultipleSelect" if len(step_answer) > 1 else "string"
            st.caption(f"Suggested answerType: {computed_answer_type}")
            answer_type = st.radio(
                "Answer Type (override)",
                options=["string", "MultipleSelect"],
                index=0 if computed_answer_type == "string" else 1
            )
    elif problem_type == "TextBox":
        st.subheader("TextBox Settings")
        answer_input = st.text_input("Correct Answer")
        step_answer = [answer_input] if answer_input else []
        answer_type = st.selectbox("Answer Type", ["algebraic", "string", "numeric"])

    # Hints
    st.subheader("Hints")
    num_hints = st.number_input("Number of hints", min_value=0, max_value=10, value=2)
    hints = []
    for i in range(num_hints):
        hint_text = st.text_area(f"Hint {i+1} Text")
        if hint_text:
            hint_type = "hint" if i < (num_hints - 1) else "solution"
            hints.append({
                "id": f"{slugify(problem_title)}-h{i+1}",
                "title": f"Hint {i+1}",
                "text": hint_text,
                "type": hint_type,
                "dependencies": [i-1] if i > 0 else [],
                "variabilization": {},
                "oer": "",
                "license": ""
            })

    # Skills
    st.subheader("Learning Objectives")
    selected_skills = st.multiselect("Select Learning Objectives", options=learning_objectives)

    # ----------------- Preview ----------------- #
    st.subheader("Preview Problem JSON")
    problem_id = slugify(problem_title) if problem_title else "<problem_id>"
    step_id = f"{problem_id}a"
    problem_obj = {
        "id": problem_id,
        "title": problem_title,
        "body": problem_body,
        "variabilization": {},
        "oer": "",
        "license": "",
        "lesson": selected_lesson,
        "courseName": selected_course
    }
    step_obj = {
        "id": problem_id,
        "problemType": problem_type,
        "stepTitle": step_title,
        "stepBody": problem_body,
        "stepAnswer": step_answer,
        "answerType": answer_type,
        "choices": choices if problem_type == "MultipleChoice" else None,
        "variabilization": {},
        "oer": "",
        "license": "",
        "lesson": selected_lesson
    }
    st.json({"problem": problem_obj, "step": step_obj, "hints": hints})

    # ----------------- Save ----------------- #
    if st.button("➕ Create Problem"):
        # Validate
        if not problem_title:
            st.error("Problem Title is required.")
        elif problem_type == "MultipleChoice" and len(choices) < 2:
            st.error("MultipleChoice requires at least 2 choices.")
        elif problem_type == "MultipleChoice" and len(step_answer) < 1:
            st.error("Select at least one correct answer.")
        else:
            problem_path = CONTENT_POOL / problem_id
            steps_path = problem_path / "steps"
            step_path = steps_path / step_id
            tutoring_path = step_path / "tutoring"
            ensure_dir(tutoring_path)

            save_json(problem_path / f"{problem_id}.json", problem_obj)
            save_json(step_path / f"{step_id}.json", step_obj)
            save_json(tutoring_path / f"{step_id}DefaultPathway.json", hints)

            if selected_skills:
                skill_model[problem_id] = selected_skills
                save_json(SKILL_MODEL_FILE, skill_model)
            st.success(f"✅ Problem '{problem_id}' created successfully!")

# ----------------- SKILLS ----------------- #
with tab_skills:
    st.header("⚙️ Skills Management")
    bkt_params = load_json(BKT_PARAMS_FILE, default={})

    with st.form("new_skill_form"):
        skill_name = st.text_input("Skill ID (e.g., find_factors)")
        prob_mastery = st.number_input("probMastery", min_value=0.0, max_value=1.0, value=0.1)
        prob_transit = st.number_input("probTransit", min_value=0.0, max_value=1.0, value=0.1)
        prob_slip = st.number_input("probSlip", min_value=0.0, max_value=1.0, value=0.1)
        prob_guess = st.number_input("probGuess", min_value=0.0, max_value=1.0, value=0.1)

        skill_submitted = st.form_submit_button("➕ Add Skill")
        if skill_submitted:
            bkt_params[skill_name] = {
                "probMastery": prob_mastery,
                "probTransit": prob_transit,
                "probSlip": prob_slip,
                "probGuess": prob_guess
            }
            save_json(BKT_PARAMS_FILE, bkt_params)
            st.success(f"✅ Skill '{skill_name}' added!")

    st.subheader("Existing Skills")
    for skill, params in bkt_params.items():
        st.write(f"- **{skill}** → {params}")
