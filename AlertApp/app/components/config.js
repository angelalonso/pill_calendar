'use strict'
import React, { Component } from 'react';                                                                                                                                                             
import {
    ActivityIndicator, 
    Button,
    Picker,
    StyleSheet,
    Text,
    View,
} from 'react-native';
 
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Actions } from 'react-native-router-flux'

import * as ReduxActions from '../actions'; //Import your actions 
import { updateAlarm } from '../actions'


const MAX_HOURS = 23;
const MAX_MINUTES = 59;


class Config extends Component {
  constructor(props) {
    super(props);

    this.state = {                     
      hour: props.alarms[0].hour,
      minutes: props.alarms[0].minutes,
      alertstatus: props.alarms[0].alertstatus
    };     
    //console.log("hello" + this.state.hour);

    this.updateAlarm = this.updateAlarm.bind(this);
  }

  componentDidMount() {
    this.props.getAlarms(); //call our action
  }        


  // copied from react-native-simple-time-picker 
  getHoursItems = () => { 
    const items = []; 
    for (let i = 0; i <= MAX_HOURS; i++) { 
      items.push( 
        <Picker.Item key={i} value={i} label={`${i.toString()}`} />, 
      ); 
    } 
    return items; 
  } 
  getMinutesItems = () => {
    const items = [];
    for (let i = 0; i <= MAX_MINUTES; i++) {
      items.push(
        <Picker.Item key={i} value={i} label={`${i.toString()}`} />,
      );
    }
    return items;
  }

  updateAlarm() {

    console.log(this.props.alarms[0]);
    let alarm = this.props.alarms[0];
    alarm['hour'] = this.state.hour;
    alarm['minutes'] = this.state.minutes;
    alarm['alertstatus'] = this.state.alertstatus;
    this.props.updateAlarm(alarm); 
    console.log(alarm['hour']);
    //Actions.home();
    Actions.reset('home');
    //Actions.popTo('home');
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
            <View style={{flex: 1, backgroundColor: '#fff'}}>
                <View style={{flex:1, paddingLeft:10, paddingRight:10}}>
                    <Picker selectedValue = {this.state.hour} onValueChange = {(text) => this.setState({hour: text})}>
                      {this.getHoursItems()}  
                    </Picker>
                    <Picker selectedValue = {this.state.minutes} onValueChange = {(text) => this.setState({minutes: text})}>
                      {this.getMinutesItems()}  
                    </Picker>
                    <Picker selectedValue = {this.state.alertstatus} onValueChange = {(text) => this.setState({alertstatus: text})}>
                      <Picker.Item label = "ON" value = "on" />
                      <Picker.Item label = "OFF" value = "off" />
                    </Picker>
                </View>
                  <Button
										onPress={this.updateAlarm}
                    //onPress={() => Actions.home()}
                    style={[styles.button]}
                    title="Save"
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
export default connect(mapStateToProps, mapDispatchToProps)(Config);

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
    backgroundColor: '#F50505'
  },

});
