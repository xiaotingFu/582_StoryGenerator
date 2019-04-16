import React from 'react';
import { Row, Col, Button, Form, FormGroup, Label, Input } from 'reactstrap';

export default class Setting extends React.Component {
  render() {
    return (
      <Form>
        <FormGroup>
          <Row form>
            <Col md={6}>
              <Label for="romanceRating">Romance Rating</Label>
              <Input type="range" name="romance" id="romanceRating"/>
            </Col>
            <Col md={6}>
              <Label for="horrorRating">Horror Rating</Label>
              <Input type="range" name="horror" id="horrorRating"/>
            </Col>
          </Row>
        </FormGroup>
        <FormGroup>
          <Row form>
            <Col md={6}>
              <Label for="clicheRating">Cliche Rating</Label>
              <Input type="range" name="cliche" id="clicheRating"/>
            </Col>
            <Col md={6}>
              <Label for="violenceRating">Violence Rating</Label>
              <Input type="range" name="violence" id="violenceRating"/>
            </Col>
          </Row>
        </FormGroup>
        <FormGroup>
          <Row form>
            <Col md={6}>
              <Label for="boringRating">Boring Rating</Label>
              <Input type="range" name="boring" id="boringRating"/>
            </Col>
          </Row>
        </FormGroup>
        <FormGroup>
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
        </FormGroup>
      </Form>
    );
  }
}