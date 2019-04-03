import React from 'react';
import { Row, Col, Button, Form, FormGroup, Label, Input } from 'reactstrap';

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
          <Row>
            <Col sm="3"></Col>
            <Col sm="2">
              <Button type="button"
                color="primary"
                onClick={() => this.props.changeActiveStep(2)}
                className="btn btn-primary btn-block">
                Submit
              </Button>
            </Col>
            <Col sm="2"></Col>
            <Col sm="2">
              <Button type="button"
                onClick={() => this.props.changeActiveStep(0)}
                className="btn btn-block">
                Cancel
              </Button>
            </Col>
            <Col sm="3"></Col>
          </Row>
      </Form>
    );
  }
}