/* eslint-disable react/prop-types, react/jsx-handler-names */

import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { withStyles } from '@material-ui/core/styles';
import { books } from '../books';
import { Config } from '../config';
import TitlebarGridList from './TitlebarGridList';
import { Row, Col, Form, FormGroup, Collapse} from 'reactstrap';
import { Button, Card, CardActionArea, CardActions,
        CardContent, CardMedia, Typography} from '@material-ui/core';
import { ExpandMore, ExpandLess } from '@material-ui/icons';

const suggestions = books.map(book => ({
  value: book.title,
  label: book.title,
}));

const styles = theme => ({
  icon: {
    margin: theme.spacing.unit,
    fontSize: 32,
  },
  media: {
    height: 140,
  },
  card: {
    height: 320,
  },
  content: {
    height: 120,
  },
});

class Search extends React.Component {

  state = {
    single: null,
    firstNovel: null,
    secondNovel: null,
    collapse: false,
    secondOptions: [],
    secondSelectPlaceholder: "Select your first novel first",
    fetchedBooks: []
  }

  componentDidMount() {
  }

  handleChange = name => value => {
    this.setState({
      [name]: value,
    });
    if (value) {
      console.log("not empty");
      this.loadNovelFromServer(name, value.label);
    } else if(name==="firstNovel"){
      console.log("1 is empty");
      this.setState({
        secondNovel: null,
        secondOptions: [],
        secondSelectPlaceholder: "Select your first novel first",
      });
    } else if(name==="secondNovel"){
      console.log("2 is empty");
      this.setState({
        secondOptions: this.state.fetchedBooks,
      })
    }
  }

  toggle = () => {
    this.setState({
      collapse: !this.state.collapse
    })
  }

  submit = () => {
    if (this.state.firstNovel && this.state.secondNovel && 
      this.state.firstNovel.label!==this.state.secondNovel.label) {
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

  renderByCollapse = (classes) => {
    return this.state.collapse ?
            <Button variant="contained" 
                  color="primary" 
                  className={classes.button+" btn-block"}
                  onClick={this.toggle}>
                  Library
                  <ExpandLess className={classes.rightIcon} />
            </Button>:
            <Button variant="contained" 
                  color="primary" 
                  className={classes.button+" btn-block"}
                  onClick={this.toggle}>
                  Library
                  <ExpandMore className={classes.rightIcon} />
            </Button>;
  }

  loadNovelFromServer = (whichNovel, bookName) => {
    fetch('https://www.googleapis.com/books/v1/volumes?q='+bookName)
      .then((response) => {
        if (response.status !== 200) {
          console.log('Looks like there was a problem. Status Code: ' +
            response.status);
          return;
        }
        // Examine the text in the response
        response.json().then((data) => {
          const book = data.items[0];
          console.log(book);
          this.setState({[whichNovel]:{
            author: (book.volumeInfo.authors&&book.volumeInfo.authors.length>0)?
                    book.volumeInfo.authors[0]:"Unknown",
            label: bookName,
            value: bookName,
            description: book.volumeInfo.description?
                        book.volumeInfo.description:
                        "No description available",
            imgLink: book.volumeInfo.imageLinks?
                    book.volumeInfo.imageLinks.thumbnail:
                    "https://placeholdit.imgix.net/~text?txtsize=33&txt=318%C3%97180&w=318&h=180",
          }});
        });
      })
      .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });

      let url = Config.url+"/booknames";

      let params = {
        bookname: bookName,
        // storylength: this.state.storylength,
      }

      console.log(params);
      let paramsArray = [];
      Object.keys(params).forEach(key => paramsArray.push(key + '=' + params[key]))
      if (url.search(/\?/) === -1) {
          url += '?' + paramsArray.join('&')
      } else {
          url += '&' + paramsArray.join('&')
      }
      
      // fetch generated story
      fetch(url, {
        method: 'GET',
        headers: new Headers({
          'Content-Type': 'application/json',
        }),
        mode: 'cors'
      })
      .then((resp) => resp.json())
      .catch((error)=>{console.log(error)})
      .then((response) => {
        if (!response) {
          // alert('Ooops, there is something wrong with your network!');
          return;
        }   
        if(whichNovel==="firstNovel"){     
          console.log(response);
          this.setState({
            secondSelectPlaceholder: "Select second novel",
            secondOptions: response.map(book => ({
              value: book,
              label: book,
            })),
            fetchedBooks: this.state.secondOptions,
          });
        }
      });
          

  }

  learnMore(n) {
    if (n===1) {
      alert(this.state.firstNovel?this.state.firstNovel.description:"Description of Novel I");
    } else {
      alert(this.state.secondNovel?this.state.secondNovel.description:"Description of Novel II");
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
              <Col sm="1"></Col>
              <Col sm="4">
                <Select
                  key="firstSelect"
                  classes={classes}
                  styles={selectStyles}
                  options={suggestions}
                  isClearable={true}
                  onChange={this.handleChange('firstNovel')}
                  placeholder="Select first novel"
                  value={this.state.firstNovel}
                />
              </Col>
              <Col sm="2">
                  {/* {this.renderByCollapse(classes)} */}
              </Col>
              <Col sm="4">
                <Select
                  key="secondSelect"
                  classes={classes}
                  styles={selectStyles}
                  options={this.state.secondOptions}
                  isClearable={true}
                  onChange={this.handleChange('secondNovel')}
                  placeholder= {this.state.secondSelectPlaceholder}
                  value={this.state.secondNovel}
                />
              </Col>
              <Col sm="1"></Col>
            </Row>
          </FormGroup>
          
          <Collapse isOpen={this.state.collapse}>
            <FormGroup>
              <Row>
                <Col></Col>
                <Col>
                  <TitlebarGridList suggestions={suggestions}></TitlebarGridList>
                </Col>
                <Col></Col>
              </Row>
            </FormGroup>
          </Collapse>
          
          <FormGroup>
            <Row>
              <Col sm="1"></Col>
              <Col>
                <Card className={classes.card}>
                  <CardActionArea>
                    <CardMedia
                      className={classes.media}
                      image={this.state.firstNovel?
                        this.state.firstNovel.imgLink:
                        "https://placeholdit.imgix.net/~text?txtsize=33&txt=318%C3%97180&w=318&h=180"}
                      title="Contemplative Reptile"
                    />
                    <CardContent className={classes.content}>
                      <Typography gutterBottom variant="h5" component="h3">
                        {!this.state.firstNovel?"Novel I":this.state.firstNovel.label}
                      </Typography>
                      <Typography component="p">
                        {this.state.firstNovel && this.state.firstNovel.description?
                          this.state.firstNovel.description.substring(0, 100).trim()+"...":
                          "Description of Novel I"}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                  <CardActions>
                    <Button size="small" color="primary"
                            onClick={()=>this.learnMore(1)}>
                      Learn More
                    </Button>
                  </CardActions>
                </Card>
              </Col>
              <Col sm="2"></Col>
              <Col>
                <Card className={classes.card}>
                  <CardActionArea>
                    <CardMedia
                      className={classes.media}
                      image={this.state.secondNovel?
                        this.state.secondNovel.imgLink:
                        "https://placeholdit.imgix.net/~text?txtsize=33&txt=318%C3%97180&w=318&h=180"}
                      title="Contemplative Reptile"
                    />
                    <CardContent className={classes.content}>
                      <Typography gutterBottom variant="h5" component="h3">
                        {!this.state.secondNovel?"Novel II":this.state.secondNovel.label}
                      </Typography>
                      <Typography component="p">
                        {this.state.secondNovel && this.state.secondNovel.description?
                          this.state.secondNovel.description.substring(0, 100).trim()+"...":
                          "Description of Novel II"}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                  <CardActions>
                    <Button size="small" color="primary"
                            onClick={()=>this.learnMore(2)}>
                      Learn More
                    </Button>
                  </CardActions>
                </Card>
              </Col>
              <Col sm="1"></Col>
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
