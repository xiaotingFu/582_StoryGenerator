// frontend/src/App.js

import React, { Component } from "react";
import CustomNavbar from "./components/CustomNavbar";
import CustomStepper from "./components/CustomStepper";
import Search from "./components/Search";
import Setting from "./components/Setting";
import Story from "./components/Story";

import { Row, Col, Card } from 'reactstrap';




class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      activeStep: 0,
      firstNovel: null,
      secondNovel: null
    };
  }

  componentDidMount() {

  }

  componentDidUpdate() {
    console.log(this.state);
  }

  changeActiveStep(activeStep) {
    this.setState({activeStep});
  }

  changeFirstNovel(firstNovel) {
    this.setState({firstNovel});
  }

  changeSecondNovel(secondNovel) {
    this.setState({secondNovel});
  }

  renderByActiveStep(step) {
    switch (step) {
      case 0:
        return <Search changeFirstNovel={(firstNovel)=>this.changeFirstNovel(firstNovel)} 
                      changeSecondNovel={(secondNovel)=>this.changeSecondNovel(secondNovel)} 
                      changeActiveStep={step=>this.changeActiveStep(step)}></Search>;
                      // function(step) {
                      //   this.changeActiveStep(step);
                      // }
      case 1:
        return <Setting changeActiveStep={step=>this.changeActiveStep(step)}></Setting>;
      case 2:
        return <Story firstNovel={this.state.firstNovel} 
                      secondNovel={this.state.secondNovel}
                      changeActiveStep={step=>this.changeActiveStep(step)}></Story>;
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
        <Row>
          <Col sm="1"></Col>
          <Col sm="10">
            <Card className="h-100 p-3" 
              style={{ backgroundImage: "url(texture/vintage-concrete.png)" }}>
              {this.renderByActiveStep(this.state.activeStep)}
            </Card>
          </Col>
          <Col sm="1"></Col>
        </Row>
      </main>
    );
  }
}
export default App;
