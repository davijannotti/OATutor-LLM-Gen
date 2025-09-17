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

        # ------------ UI to ADD Learning Objectives ------------
        st.markdown("### 1. Add Learning Objectives")
        col1, col2, col3 = st.columns([4, 2, 1.5])
        with col1:
            selected_lo = st.selectbox("Select from existing", options=skills_list, key="selected_lo_suggestion")
        with col2:
            new_weight = st.number_input("Weight", min_value=0.0, max_value=1.0, value=0.85, step=0.05, key="new_lo_weight")
        with col3:
            st.text("") # Adds a single empty line
            st.text("") # Adds another empty line
            add_lo_button = st.button("➕ Add LO")

        if add_lo_button and selected_lo:
            st.session_state.learningObjectives[selected_lo] = new_weight

        # Display the list of currently added LOs
        if st.session_state.learningObjectives:
            st.write("Current Learning Objectives for the new lesson:")
            for k, v in st.session_state.learningObjectives.items():
                st.write(f"- **{k}** (Weight: {v})")
            if st.button("Clear All LOs"):
                st.session_state.learningObjectives = {}
        st.divider()

        # ------------ Lesson Details & Live Preview ------------
        st.markdown("### 2. Enter Lesson Details")

        selected_course = st.selectbox("Select Course", options=course_names)
        lesson_id = st.text_input("Lesson ID (slug)", value="lesson1")
        lesson_name = st.text_input("Lesson Name", value="Lesson 1.1")
        lesson_topics = st.text_input("Lesson Topics", value="Introduction")

        # Add the checkbox for allowRecycle
        allow_recycle = st.checkbox("Allow problem recycling in this lesson", value=True)

        # Build the lesson object with the current values from the widgets
        lesson_obj = {
            "id": lesson_id,
            "name": lesson_name,
            "topics": lesson_topics,
            "allowRecycle": allow_recycle,
            "learningObjectives": st.session_state.learningObjectives
        }

        st.subheader("Live Preview of Lesson JSON")
        st.json(lesson_obj)
        st.divider()

        # ---------- Main Form (for submission only) ----------
        st.markdown("### 3. Save Lesson")
        with st.form("new_lesson_form"):
            # The form is now just a container for the submit button
            submitted = st.form_submit_button("💾 Create and Save Lesson")
            if submitted:
                # Validation
                if not st.session_state.learningObjectives:
                    st.error("Please add at least one Learning Objective.")
                elif not lesson_id or not lesson_name:
                    st.error("Lesson ID and Lesson Name are required.")
                else:
                    # Find the correct course and append the lesson
                    for course in course_plans:
                        if course["courseName"] == selected_course:
                            course["lessons"].append(lesson_obj)

                    # Save the updated course plans
                    save_json(COURSE_PLANS_FILE, course_plans)
                    st.success(f"✅ Lesson '{lesson_name}' added to course '{selected_course}'!")

                    # Clear the learning objectives for the next lesson
                    st.session_state.learningObjectives = {}

# ----------------- PROBLEMS (ATUALIZADO) ----------------- #
with tab_problems:
    st.header("📝 Problems Management")

    # Load data
    course_plans = load_json(COURSE_PLANS_FILE, default=[])
    skill_model = load_json(SKILL_MODEL_FILE, default={})
    bkt_params = load_json(BKT_PARAMS_FILE, default={})

    course_names = [c["courseName"] for c in course_plans]
    learning_objectives = list(bkt_params.keys())

    st.subheader("Problem Association")
    selected_course_name = st.selectbox("Course", options=course_names if course_names else ["<none>"])

    selected_course_obj = next((c for c in course_plans if c.get("courseName") == selected_course_name), None)

    lessons_in_course = []
    default_oer = ""
    default_license = ""

    if selected_course_obj:
        lessons_in_course = [l["id"] for l in selected_course_obj.get("lessons", [])]
        default_oer = selected_course_obj.get("courseOER", "")
        default_license = selected_course_obj.get("courseLicense", "")

    selected_lesson = st.selectbox(
        "Lesson ID",
        options=lessons_in_course if lessons_in_course else ["<none>"]
    )
    st.divider()

    st.subheader("Problem Info")
    problem_title = st.text_input("Problem Title")
    problem_body = st.text_area("Problem Body (supports LaTeX with $$...$$)")

    problem_oer = st.text_input("Problem OER (URL)", value=default_oer)
    problem_license = st.text_input("Problem License", value=default_license)

    problem_type = st.selectbox("Problem Type", ["TextBox", "MultipleChoice"])
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
            computed_answer_type = "MultipleSelect" if len(step_answer) > 1 else "string or MultipleChoice"
            st.caption(f"Suggested answerType: {computed_answer_type}")
            answer_type = st.radio(
                "Answer Type (override)",
                options=["string", "MultipleChoice", "MultipleSelect"],
                index=0 if computed_answer_type == "string" else 1
            )
    elif problem_type == "TextBox":
        st.subheader("TextBox Settings")
        answer_input = st.text_input("Correct Answer")
        step_answer = [answer_input] if answer_input else []
        answer_type = st.selectbox("Answer Type", ["algebraic", "string", "numeric"])

    # --- HINTS ---
    st.subheader("Hints")
    num_hints = st.number_input("Number of hints", min_value=0, max_value=10, value=2)
    hints = []
    hint_ids = []

    for i in range(num_hints):
        st.markdown(f"--- \n#### Hint {i+1}")
        hint_title = st.text_input(f"Hint {i+1} Title", key=f"hint_title_{i}")
        hint_text = st.text_area(f"Hint {i+1} Text", key=f"hint_text_{i}")

        is_scaffold = st.checkbox(f"Is this a scaffold hint?", key=f"is_scaffold_{i}")

        hint_answer_val = None
        answer_type_hint = "arithmetic"

        if is_scaffold:
            col1, col2 = st.columns(2)
            with col1:
                answer_input = st.text_input("Hint answer", key=f"hint_answer_{i}")
                if answer_input:
                    hint_answer_val = [answer_input]
            with col2:
                answer_type_hint = st.selectbox(
                    "Type of answer",
                    ["arithmetic", "string", "algebraic"],
                    key=f"hint_answer_type_{i}"
                )

        if hint_text:
            hint_id = f"{slugify(problem_title)}-h{i+1}"
            hint_ids.append(hint_id)

            dependencies = []
            if i > 0 and hint_ids:
                dependencies.append(hint_ids[i-1])

            hint_obj = {
                "id": hint_id,
                "dependencies": dependencies,
                "title": hint_title,
                "text": hint_text,
                "variabilization": {},
                "oer": problem_oer,
                "license": problem_license
            }

            if is_scaffold and hint_answer_val:
                hint_obj["type"] = "scaffold"
                hint_obj["problemType"] = "TextBox"
                hint_obj["answerType"] = answer_type_hint
                hint_obj["hintAnswer"] = hint_answer_val
            else:
                hint_obj["type"] = "hint" if i < (num_hints - 1) else "solution"

            hints.append(hint_obj)

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
        "oer": problem_oer,
        "license": problem_license,
        "lesson": selected_lesson,
        "courseName": selected_course_name
    }
    step_obj = {
        "id": problem_id,
        "problemType": problem_type,
        "stepTitle": step_title,
        "stepBody": "",
        "stepAnswer": step_answer,
        "answerType": answer_type,
        "choices": choices if problem_type == "MultipleChoice" else [],
        "variabilization": {},
        "oer": problem_oer,
        "license": problem_license,
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
