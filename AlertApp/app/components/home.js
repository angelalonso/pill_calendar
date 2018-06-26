'use strict'
import React, { Component } from 'react';                                                                                                                                                             
import {
    ActivityIndicator, 
    Button,
    StyleSheet,
    Text,
    View,
} from 'react-native';
 
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Actions } from 'react-native-router-flux'

import * as ReduxActions from '../actions'; //Import your actions 

class Home extends Component {
  constructor(props) {
    super(props);

    this.state = {};

    console.log("constructor");
    this.getDataState = this.getDataState.bind(this);
    //INFO: this.props is here not yet loaded

  }

  componentWillReceiveProps(nextProps){
    console.log("nextprops")
    console.log(nextProps.alarms[0].hour)
    if(nextProps.alarms[0] !== this.props.alarms[0]){
      this.setState({
        hour: nextProps.alarms[0].hour,
        minutes: nextProps.alarms[0].minutes,
        alertstatus: nextProps.alarms[0].alertstatus
      });
    }
  }
  componentDidMount() {
    this.props.getAlarms(); //call our action
  }        

  getDataState() {
    //TODO: change to alarmstatus, and OFF, everywhere
    console.log("home>getDataState " + this.props.alarms[0].hour + " - " + this.props.alarms[0].alertstatus);
    let value = this.props.alarms[0].hour + ":" + this.props.alarms[0].minutes + " - " + this.props.alarms[0].alertstatus;
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
                    {this.getDataState()}
                    </Text>  
                    <Button
                      onPress={() => Actions.config()}
                      style={[styles.button]}
                      title="Config"
                      >
                    </Button>

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
  button:{
    fontWeight: "500",
    backgroundColor: '#F5F5F5'
  },

});
