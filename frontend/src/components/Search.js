/* eslint-disable react/prop-types, react/jsx-handler-names */

import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { withStyles } from '@material-ui/core/styles';
import { books } from '../books';
import TitlebarGridList from './TitlebarGridList';
import { Row, Col, Form, FormGroup } from 'reactstrap';

const suggestions = books.map(book => ({
  author: book.author,
  label: book.title,
  value: book.title,
  imgLink: process.env.PUBLIC_URL+book.imageLink,
}));

const styles = theme => ({
});

class Search extends React.Component {
  state = {
    single: null,
    firstNovel: null,
    secondNovel: null,
    collections: suggestions,
  };

  componentDidMount() {
  }

  handleChange = name => value => {
    this.setState({
      [name]: value,
      collections: this.state.collections.filter((c) => {
        return c !== value;
      }),
    });
  };

  submit = () => {
    if (this.state.firstNovel && this.state.secondNovel && this.state.firstNovel!==this.state.secondNovel) {
      this.props.changeFirstNovel(this.state.firstNovel);
      this.props.changeSecondNovel(this.state.secondNovel);
      this.props.changeActiveStep(1);
    } else if (!this.state.firstNovel) {
      alert("Please select first novel!");
    } else if (!this.state.secondNovel) {
      alert("Please select second novel!");
    } else {
      alert("Please select two different novels!");
    }
  }

  render() {
    const { classes, theme } = this.props;

    const selectStyles = {
      input: base => ({
        ...base,
        color: theme.palette.text.primary,
        '& input': {
          font: 'inherit',
        },
      }),
      
    };

    return (
        <Form>
          <FormGroup>
            <Row>
              <Col>
                <Select
                  key="firstSelect"
                  classes={classes}
                  styles={selectStyles}
                  options={suggestions}
                  isClearable={true}
                  onChange={this.handleChange('firstNovel')}
                  placeholder="Select first novel"
                />
              </Col>
              <Col>
                <Select
                  key="secondSelect"
                  classes={classes}
                  styles={selectStyles}
                  options={suggestions}
                  isClearable={true}
                  onChange={this.handleChange('secondNovel')}
                  placeholder="Select second novel"
                />
              </Col>
            </Row>

            <Row>
              <Col></Col>
              <Col><TitlebarGridList suggestions={suggestions}></TitlebarGridList></Col>
              <Col></Col>
            </Row>
          </FormGroup>

          <FormGroup>
            <Row>
              <Col sm="5"></Col>
              <Col>
                <button type="button" 
                      onClick = {this.submit}
                      className="btn btn-primary btn-block">
                  Submit
                </button>
              </Col>
              <Col sm="5"></Col>
            </Row>
          </FormGroup>
        </Form>
    );
  }
}

Search.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(Search);
