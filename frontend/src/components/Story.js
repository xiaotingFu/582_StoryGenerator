import React from 'react';
import { Form, FormGroup, Label, Input } from 'reactstrap';

export default class Story extends React.Component {
    render() {
      return (
        <Form>
          <FormGroup>
            <Label for="exampleText">Your Story</Label>
            <Input type="textarea" name="text" id="exampleText" />
          </FormGroup>
        </Form>
      );
    }
  }