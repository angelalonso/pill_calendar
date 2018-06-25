'use strict'
import React, { Component } from 'react';                                                                                                                                                             
import {
    View,
    StyleSheet,
    Text,
    ActivityIndicator, 
    TouchableHighlight, ActionSheetIOS, FlatList, 
} from 'react-native';
 
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Actions } from 'react-native-router-flux'

import * as ReduxActions from '../actions'; //Import your actions 

class Home extends Component {
  constructor(props) {
    super(props);

    this.state = {};

    this.getMyText = this.getMyText.bind(this);
    this.getStateText = this.getStateText.bind(this);

  }

  componentDidMount() {
    this.props.getAlarms(); //call our action
  }        

  getMyText() {
    return "Text from getMyText";
  }
    
  getStateText() {
    let value = this.props.alarms[0].hour + ":" + this.props.alarms[0].minutes + " - " + this.props.alarms[0].id;
    return value;
  }
    
    render() {
        if (this.props.loading) {
            return (
                <View style={styles.activityIndicatorContainer}>
                    <ActivityIndicator animating={true}/>
                </View>
            );
        } else {
            return (
                <View style={styles.container}>
                    <Text style={styles.text}
                    >
                    Manual text
                    </Text>  
                    <Text style={styles.text}
                    >
                    {this.getMyText()}
                    </Text>  
                    <Text style={styles.text}
                    >
                    {this.getStateText()}
                    </Text>  
                </View>
            );
        }
    }
};
 
// The function takes data from the app current state,
// and insert/links it into the props of our component.
// This function makes Redux know that this component needs to be passed a piece of the state
function mapStateToProps(state, props) {
    return {
        loading: state.dataReducer.loading,
        alarms: state.dataReducer.alarms
    }
}
 
// Doing this merges our actions into the component’s props,
// while wrapping them in dispatch() so that they immediately dispatch an Action.
// Just by doing this, we will have access to the actions defined in out actions file (action/home.js)
function mapDispatchToProps(dispatch) {
    return bindActionCreators(ReduxActions, dispatch);
}
 
//Connect everything
export default connect(mapStateToProps, mapDispatchToProps)(Home);

const styles = StyleSheet.create({
 
  container:{
      flex:1,
      backgroundColor: '#F5F5F5'
  },

  text:{
      fontSize: 14,
      fontWeight: "600",
      marginTop: 8 * 2
  },
});
