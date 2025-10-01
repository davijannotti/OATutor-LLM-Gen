# Documentation: OATutor Content Creator Tool

This documentation details how to use the content creation tool for the OATutor platform, developed with Streamlit. The tool is designed to simplify the process of creating courses, lessons, problems, and skills in a structured and intuitive way.

## 1. Requirements

Before running the application, ensure that your environment meets the following requirements:

* **Python:** You must have **Python version 3.11** installed.
* **Python Libraries:** Install the `streamlit` library via pip.
    ```bash
    pip install streamlit
    ```
* **Directory Structure:** The tool depends on a specific folder and file structure to function correctly. Create the following structure in the parent directory of where the `contentCreator.py` script is located:

    ```
    .
    ├── content-sources/
    │   └── oatutor/
    │       ├── bkt-params/
    │       │   └── defaultBKTParams.json  (Can start as an empty JSON file: {})
    │       ├── content-pool/              (Will be populated by the tool)
    │       ├── coursePlans.json           (Can start as an empty JSON array: [])
    │       └── skillModel.json            (Can start as an empty JSON file: {})
    └── your_project_folder/
        └── contentCreator.py
    ```

## 2. How to Run the Tool

1.  Open a terminal or command prompt.
2.  Navigate to the folder where the `contentCreator.py` script is located.
3.  Run the following command:

    ```bash
    streamlit run contentCreator.py
    ```
4.  Your web browser will automatically open with the application interface.

## 3. Recommended Workflow

For a cohesive content creation process, follow the order of the tabs from left to right, as there are dependencies between them:

1.  **⚙️ Skills:** First, define all the skills that will be tracked on the platform. They are the foundation for the learning objectives of lessons and problems.
2.  **📘 Courses:** Create the main structure of your course.
3.  **📖 Lessons:** Add lessons to the courses you've created, associating them with the learning objectives (skills) defined in step 1.
4.  **📝 Problems:** Create the problems and associate them with a specific lesson and the skills it assesses.

## 4. Features by Tab

The tool is organized into four main tabs.

### ⚙️ Skills Tab

On this tab, you manage the skills that the tutor system will use to track student knowledge, based on the BKT (Bayesian Knowledge Tracing) model.

* **Skill ID:** A unique identifier for the skill (e.g., `solve_linear_equations`). Use a "slug" format (lowercase, no spaces, using `_`).
* **BKT Parameters:**
    * `probMastery` (Initial Mastery Probability): The probability that the student already knows the skill before the first interaction.
    * `probTransit` (Transition Probability): The probability that the student will learn the skill after an opportunity to practice.
    * `probSlip` (Slip Probability): The probability that a student who masters the skill will make a mistake.
    * `probGuess` (Guess Probability): The probability that a student who does not master the skill will guess the correct answer.

After filling out the fields, click **"➕ Add Skill"** to save the new skill to the `defaultBKTParams.json` file.

### 📘 Courses Tab

This tab allows you to create the general structure of the courses.

* **Course Name:** The full name of the course (e.g., "Algebra for Beginners").
* **Course OER (URL):** Optional. A link to the original Open Educational Resource for the course, if applicable.
* **Course License:** Optional. The license under which the course content is distributed (e.g., "CC BY-SA 4.0").

Click **"➕ Add Course"** to add the course. It will be saved in the `coursePlans.json` file.

### 📖 Lessons Tab

Here you create the lessons that make up a course and define their learning objectives.

The process is divided into 3 steps:

1.  **Add Learning Objectives:**
    * Select a previously registered skill from the "Select from existing" list.
    * Set a "Weight" for this skill in the lesson (a value between 0.0 and 1.0).
    * Click **"➕ Add LO"** to add it to the current lesson. You can add multiple objectives.

2.  **Enter Lesson Details:**
    * **Select Course:** Choose which course this lesson belongs to.
    * **Lesson ID (slug):** A unique identifier for the lesson (e.g., `introduction_to_variables`).
    * **Lesson Name:** The full name of the lesson (e.g., "Lesson 1.1: Introduction to Variables").
    * **Lesson Topics:** Keywords or topics covered (e.g., "variables, expressions").
    * **Allow problem recycling:** Check this box if you want problems from this lesson to be presented to the student again.
    * Below the fields, a **"Live Preview of Lesson JSON"** shows how the data will be saved.

3.  **Save the Lesson:**
    * After filling everything out, click the **"💾 Create and Save Lesson"** button. The lesson will be added to the selected course in the `coursePlans.json` file.

### 📝 Problems Tab

This is the most complex tab, where interactive problems are created.

1.  **Association:**
    * First, select the **Course** and **Lesson ID** to which this problem belongs.

2.  **Problem Information:**
    * **Problem Title:** A descriptive title for the problem. The problem ID will be automatically generated from this title.
    * **Problem Body:** The problem statement. **Supports LaTeX** for mathematical formulas, which should be enclosed in `$$...$$`.
    * **Problem OER / License:** Inherited from the course but can be overridden.

3.  **Problem Type and Answer:**
    * **Problem Type:** Choose between `TextBox` or `MultipleChoice`.
    * **Step Title:** A title for the main step of the problem (e.g., "Calculate the value of x").
    * **Answer Configuration:**
        * If **MultipleChoice**: Enter the options in the "Choices" text area, one per line. Then, select the correct answer(s) in "Correct Answers". The `answerType` will be suggested but can be changed.
        * If **TextBox**: Enter the correct answer in the "Correct Answer" field and select the appropriate `answerType` (`algebraic`, `string`, `numeric`).

4.  **Hints:**
    * **Number of hints:** Set how many hints the problem will have. The last hint is usually considered the solution.
    * For each hint:
        * Fill in the **Title** and **Text**.
        * **Is this a scaffold hint?**: Check this option if the hint is a supporting question that requires an answer from the student to proceed. When checked, new fields will appear to define the answer and answer type for this sub-question.

5.  **Learning Objectives:**
    * Select the **skills** that this problem helps to assess.

6.  **Preview and Saving:**
    * A complete JSON preview for the problem, step, and hints is displayed at the bottom.
    * Click **"➕ Create Problem"** to save. The tool will automatically generate the necessary folder structure and JSON files within `content-sources/oatutor/content-pool/`.

---