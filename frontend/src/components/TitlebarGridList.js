import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import IconButton from '@material-ui/core/IconButton';

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper,
    margin: '50px 0px',
  },
  gridList: {
    height: "500px",
    width: "600px",
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)',
  },
});

/**
 * The example data is structured as follows:
 *
 * import image from 'path/to/image.jpg';
 * [etc...]
 *
 * const tileData = [
 *   {
 *     img: image,
 *     title: 'Image',
 *     author: 'author',
 *   },
 *   {
 *     [etc...]
 *   },
 * ];
 */
class TitlebarGridList extends React.Component {

  state = {

  };

  render() {
    const { classes } = this.props;

    return (
      <div className={classes.root}>
        <GridList cellHeight={"auto"} className={classes.gridList}>
          {this.props.suggestions.map(title => (
            <GridListTile key={title.label}>
              <img src={title.imgLink} alt={title.label} />
              <GridListTileBar
                title={title.label}
                subtitle={<span>by: {title.author}</span>}
                actionIcon={
                  <IconButton className={classes.icon}>
                  </IconButton>
                }
              />
            </GridListTile>
          ))}
        </GridList>
      </div>
    ); 
  }
}

TitlebarGridList.propTypes = {
  classes: PropTypes.object,
};

export default withStyles(styles)(TitlebarGridList);
