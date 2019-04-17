import React from 'react';
import { Row, Col, Button, Form, FormGroup, InputGroup, 
        InputGroupAddon, Label, Input } from 'reactstrap';

export default class Setting extends React.Component {
  submit() {
    this.props.changeActiveStep(2);
  }

  render() {
    return (
      <Form>
        <FormGroup>
          <Row form>
            <Col md={6}>
              <Label for="romanceRating">Romance Rating</Label>
              <Input type="select" name="select" id="romanceRating">
                <option value="0" label="Lowest"/>
                <option value="25" label="Low"/>
                <option value="50" label="Middle"/>
                <option value="75" label="High"/>
                <option value="100" label="Highest"/>
              </Input>
            </Col>
            <Col md={6}>
              <Label for="horrorRating">Horror Rating</Label>
              <Input type="select" name="horror" id="horrorRating">
                <option value="0" label="Lowest"/>
                <option value="25" label="Low"/>
                <option value="50" label="Middle"/>
                <option value="75" label="High"/>
                <option value="100" label="Highest"/>
              </Input>
            </Col>
          </Row>
        </FormGroup>
        <FormGroup>
          <Row form>
            <Col md={6}>
              <Label for="clicheRating">Cliche Rating</Label>
              <Input type="select" name="cliche" id="clicheRating">
                <option value="0" label="Lowest"/>
                <option value="25" label="Low"/>
                <option value="50" label="Middle"/>
                <option value="75" label="High"/>
                <option value="100" label="Highest"/>
              </Input>
            </Col>
            <Col md={6}>
              <Label for="violenceRating">Violence Rating</Label>
              <Input type="select" name="violence" id="violenceRating">
                <option value="0" label="Lowest"/>
                <option value="25" label="Low"/>
                <option value="50" label="Middle"/>
                <option value="75" label="High"/>
                <option value="100" label="Highest"/>
              </Input>
            </Col>
          </Row>
        </FormGroup>
        <FormGroup>
          <Row form>
            <Col md={6}>
              <Label for="boringRating">Boring Rating</Label>
              <Input type="select" name="boring" id="boringRating">
                <option value="0" label="Lowest"/>
                <option value="25" label="Low"/>
                <option value="50" label="Middle"/>
                <option value="75" label="High"/>
                <option value="100" label="Highest"/>
              </Input>
            </Col>
          </Row>
        </FormGroup>
        <FormGroup>
          <Row>
            <Col sm="3"></Col>
            <Col sm="2">
              <Button type="button"
                color="primary"
                onClick={this.submit}
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