// frontend/src/App.js

import React, { Component } from "react";
import Modal from "./components/Modal";
import CustomNavbar from "./components/CustomNavbar";
import CustomStepper from "./components/CustomStepper";
import Search from "./components/Search";
import Setting from "./components/Setting";
import Story from "./components/Story";
import axios from "axios";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      activeStep: 0,
    };
  }

  componentDidMount() {

  }

  changeActiveStep(activeStep) {
    this.setState({activeStep});
  }

  renderByActiveStep(step) {
    switch (step) {
      case 0:
        return <Search changeActiveStep={step=>this.changeActiveStep(step)}></Search>;
        break;
      case 1:
        return <Setting changeActiveStep={step=>this.changeActiveStep(step)}></Setting>;
        break;
      case 2:
        return <Story changeActiveStep={step=>this.changeActiveStep(step)}></Story>;
        break;
      default:
        break;
    }
  }

  handleInputChange = () => {
    this.setState({
      query: this.search.value
    });
  }

  render() {
    return (
      <main className="content">
        <CustomNavbar></CustomNavbar>
        <CustomStepper activeStep={this.state.activeStep} 
          changeActiveStep={step=>this.changeActiveStep(step)}>
        </CustomStepper>
        <div className="container">
          {/* <div className="col-md-6 col-sm-10 mx-auto p-0"> */}
            <div className="card h-100 p-3" style={{height: "100%"}}>
                {this.renderByActiveStep(this.state.activeStep)}
            {/* </div> */}
          </div>
        </div>
        {this.state.modal ? (
          <Modal
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            onSave={this.handleSubmit}
          />
        ) : null}
      </main>
    );
  }
}
export default App;
