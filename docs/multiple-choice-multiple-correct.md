# Multiple-Correct Multiple-Choice Questions

This document outlines how to create multiple-choice questions that have multiple correct answers.

## Overview

The system now supports multiple-correct multiple-choice questions. This feature allows you to create questions where a user can select multiple options, and the submission is only considered correct if all the correct options are selected.

## JSON Configuration

To create a multiple-correct multiple-choice question, you need to configure the problem's JSON file with the following properties:

- `problemType`: Set this to `"MultipleChoice"`.
- `answerType`: Set this to `"MultipleSelect"`.
- `stepAnswer`: This must be an array containing all the correct answers. The order of the answers in the array does not matter.
- `choices`: This must be an array containing all the possible choices to be displayed to the user. This includes both correct and incorrect answers.

## Example

Here is an example of a JSON object for a multiple-correct multiple-choice question:

```json
{
    "id": "example-multi-select-problem",
    "stepAnswer": [
        "Apple",
        "Banana"
    ],
    "problemType": "MultipleChoice",
    "answerType": "MultipleSelect",
    "stepTitle": "Select all the fruits.",
    "stepBody": "",
    "choices": [
        "Apple",
        "Banana",
        "Carrot",
        "Broccoli"
    ],
    "variabilization": {}
}
```

In this example:
- The user will be presented with four options: "Apple", "Banana", "Carrot", and "Broccoli".
- The user must select both "Apple" and "Banana" to get the answer correct.
- Selecting only one correct answer, or any incorrect answers, will result in the answer being marked as incorrect.
