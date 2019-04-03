import React from 'react';
import { Button, Form, FormGroup, Label, Input, FormText } from 'reactstrap';

export default class Setting extends React.Component {
    render() {
      return (
        <Form>
          <FormGroup>
            <Label for="exampleEmail">Setting 1</Label>
            <Input type="email" name="email" id="exampleEmail" placeholder="with a placeholder" />
          </FormGroup>
          <FormGroup>
            <Label for="examplePassword">Setting 2</Label>
            <Input type="password" name="password" id="examplePassword" placeholder="password placeholder" />
          </FormGroup>
          <FormGroup>
            <Label for="exampleText">Text Area</Label>
            <Input type="textarea" name="text" id="exampleText" />
          </FormGroup>
          <div style={{textAlign: "center"}}>
            <Button type="button" 
                    onClick = {() => this.props.changeActiveStep(2)}
                    className="btn"
                    style={{width: "20%",
                            position: "absolute",
                            bottom: "0",
                            left: "20%"}}>
              Submit
            </Button>
            <Button type="button" 
                    onClick = {() => this.props.changeActiveStep(0)}
                    className="btn"
                    style={{width: "20%",
                            position: "absolute",
                            bottom: "0",
                            right: "20%"}}>
              Cancel
            </Button>
          </div>
        </Form>
      );
    }
  }