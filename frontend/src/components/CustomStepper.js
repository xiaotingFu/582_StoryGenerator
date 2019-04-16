import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';

const styles = theme => ({
  instructions: {
    marginTop: theme.spacing.unit,
    marginBottom: theme.spacing.unit,
  },
});

function getSteps() {
  return ['Select original novels', 'Adjust your settings', 'Get your own story!'];
}

class CustomStepper extends React.Component {
  state = {
    activeStep: 0,
  };

  handleNext = () => {
    this.setState({
      activeStep: this.state.activeStep + 1,
    });
  };

  handleBack = () => {
    this.setState(state => ({
      activeStep: state.activeStep - 1,
    }));
  };

  handleReset = () => {
    this.setState({
      activeStep: 0,
    });
  };

  render() {
    const { classes } = this.props;
    const steps = getSteps();

    return (
      <div className={classes.root}>
        <Stepper activeStep={this.props.activeStep}>
          {steps.map((label, index) => {
            return (
              <Step key={label} onClick={() => {this.setState({
                    activeStep: index,
                  });
                  this.props.changeActiveStep(index);
                }}>
                <StepLabel>{label}</StepLabel>
              </Step>
            );
          })}
        </Stepper>
      </div>
    );
  }
}

CustomStepper.propTypes = {
  classes: PropTypes.object,
};

export default withStyles(styles)(CustomStepper);
