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
      activeStep: 2,
      response: null,
      firstNovel: null,
      secondNovel: null,
      finalNovel: null,
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

  setFinalNovel(finalNovel) {
    this.setState({finalNovel});
  }

  setResponse(response) {
    this.setState(response);
  }

  renderByActiveStep(step) {
    switch (step) {
      case 0:
        return <Search changeFirstNovel={(firstNovel)=>this.changeFirstNovel(firstNovel)} 
                      changeSecondNovel={(secondNovel)=>this.changeSecondNovel(secondNovel)} 
                      changeActiveStep={step=>this.changeActiveStep(step)}
                      setResponse={res=>this.setResponse(res)}></Search>;
      case 1:
        return <Setting changeActiveStep={step=>this.changeActiveStep(step)}
                      firstNovel={this.state.firstNovel}
                      secondNovel={this.state.secondNovel}
                      setFinalNovel={novel=>this.setFinalNovel(novel)}></Setting>;
      case 2:
        return <Story firstNovel={this.state.firstNovel} 
                      secondNovel={this.state.secondNovel}
                      finalNovel={this.state.finalNovel}
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
