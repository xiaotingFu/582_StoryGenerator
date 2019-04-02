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
      query: '',
    };
  }

  componentDidMount() {

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
        <CustomStepper></CustomStepper>
        <div className="row ">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
            <div className="card p-3">
                <Search></Search>
            </div>
            <div className="card p-3">
              <Setting></Setting>
            </div>
            <div className="card p-3">
              <Story></Story>
            </div>
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
