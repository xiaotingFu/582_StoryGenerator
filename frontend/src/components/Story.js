import React from 'react';
import { Button, Form, FormGroup, Label, Input, FormText } from 'reactstrap';

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