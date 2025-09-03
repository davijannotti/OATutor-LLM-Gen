import React from 'react';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormGroup from '@material-ui/core/FormGroup';
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import { renderText } from '../../platform-logic/renderText.js';
import { ThemeContext } from "../../config/config";

class MultipleChoice extends React.Component {
    static contextType = ThemeContext;

    constructor(props) {
        super(props);
        this.state = {
            value: props.defaultValue || (this.props.allowMultiple ? [] : null),
        };
    }

    handleChange = (event) => {
        this.setState({ value: event.target.value });
        this.props.onChange(event);
    };

    handleCheckboxChange = (event) => {
        const { value } = this.state;
        const { value: selectedValue } = event.target;
        const newValue = value.includes(selectedValue)
            ? value.filter((v) => v !== selectedValue)
            : [...value, selectedValue];

        this.setState({ value: newValue });
        this.props.onChange({ target: { value: newValue } });
    };

    render() {
        let { choices: _choices = [], variabilization, allowMultiple } = this.props;

        const choices = []
        if (Array.isArray(_choices)) {
            [...new Set(_choices)].forEach(choice => {
                if (choice.includes(" above")) {
                    choices.push(choice);
                } else {
                    choices.unshift(choice);
                }
            })
        }

        return (
            <div style={{ marginRight: "5%", textAlign: "center" }}>
                <FormControl>
                    {allowMultiple ? (
                        <FormGroup>
                            {choices.length > 0
                                ? choices.map((choice, i) =>
                                    <FormControlLabel
                                        control={<Checkbox checked={this.state.value.includes(choice)} onChange={this.handleCheckboxChange} value={choice} />}
                                        label={renderText(choice, null, variabilization, this.context)}
                                        key={choice} />)
                                : "Error: This problem has no answer choices. Please submit feedback."}
                        </FormGroup>
                    ) : (
                        <RadioGroup value={this.state.value} onChange={this.handleChange}>
                            {choices.length > 0
                                ? choices.map((choice, i) =>
                                    <FormControlLabel value={choice} control={<Radio />}
                                        label={renderText(choice, null, variabilization, this.context)}
                                        key={choice} />)
                                : "Error: This problem has no answer choices. Please submit feedback."}
                        </RadioGroup>
                    )}
                </FormControl>
            </div>
        );
    }
}

export default MultipleChoice;
