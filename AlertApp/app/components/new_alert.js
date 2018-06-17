import React, {Component} from 'react';
import {
  Dimensions, 
  Picker,
  StyleSheet, 
  Text, 
  TextInput, 
  TouchableOpacity,
  View, 
} from 'react-native';

import { connect } from 'react-redux';
import { addAlert, updateAlert } from '../actions'
import { Actions } from 'react-native-router-flux';
import KeyboardSpacer from 'react-native-keyboard-spacer';

const {width: windowWidth, height: windowHeight} = Dimensions.get('window');
const MAX_HOURS = 23;
const MAX_MINUTES = 59;

class NewAlert extends Component {

    constructor(props) {
        super(props);

        this.state = {
            hour: (props.edit) ? props.alertitem.hour : "",
            minutes: (props.edit) ? props.alertitem.minutes : "",
            alertstatus: (props.edit) ? props.alertitem.aertstatus : ""
        };

        this.generateID = this.generateID.bind(this);
        this.addAlert = this.addAlert.bind(this);
    }

    generateID() {
        let d = new Date().getTime();
        let id = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            let r = (d + Math.random() * 16) % 16 | 0;
            d = Math.floor(d / 16);
            return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(5);
        });

        return id;
    }

    addAlert() {
        if (this.props.edit){
            let alertitem = this.props.alertitem;
            alertitem['hour'] = this.state.hour;
            alertitem['minutes'] = this.state.minutes;
            alertitem['alertstatus'] = this.state.alertstatus;
            this.props.updateAlert(alertitem);
        }else{
            let id = this.generateID();
            let alertitem = {"id": id, "hour": this.state.hour, "minutes": this.state.minutes, "alertstatus": this.state.alertstatus};
            this.props.addAlert(alertitem);
        }

        Actions.pop();
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

    render() {
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
                      <Picker.Item label = "ON" value = "ON" />
                      <Picker.Item label = "OFF" value = "OFF" />
                    </Picker>
                </View>
                <TouchableOpacity style={[styles.saveBtn]}
                                  // DOESNT WORK, WHY?
                                  //disabled={(this.state.hour.length > 0 && this.state.minutes.length > 0) ? false : true}
                                  onPress={this.addAlert}>
                    <Text style={[styles.buttonText,
                        {
                            color: (this.state.hour.length > 0 && this.state.minutes.length > 0) ? "#FFF" : "rgba(255,255,255,.5)"
                        }]}>
                        Save
                    </Text>
                </TouchableOpacity>
                <KeyboardSpacer />
            </View>
        );
    }

}

//Connect everything
export default connect(null, {addAlert, updateAlert})(NewAlert);

var styles = StyleSheet.create({
    saveBtn:{
        width: windowWidth,
        height: 44,
        justifyContent: "center",
        alignItems: 'center',
        backgroundColor:"#6B9EFA"
    },

    buttonText:{
        fontWeight: "500",
    },

    alertitem: {
        fontSize: 17,
        lineHeight: 38,
        color: "#333333",
        padding: 16,
        paddingLeft:0,
        flex:1,
        height: 200,
        marginBottom:50,
        borderTopWidth: 1,
        borderColor: "rgba(212,211,211, 0.3)",
    },

    title: {
        fontWeight: "400",
        lineHeight: 22,
        fontSize: 16,
        height:25+32,
        padding: 16,
        paddingLeft:0
    },
});
