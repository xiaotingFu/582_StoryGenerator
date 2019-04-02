import React from "react";
import { books } from "../books";

const suggestions = books.map((book) => {
  return { label: book.title };
});

export default class Search extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      suggestions: [],
    }
  }

  componentDidMount() {
    
  }

  render() {
    return (
      <div>
        {suggestions.map((suggestion)=>{
          return <p>{suggestion.label}</p>;
        })}
      </div>
    );
  }
}
