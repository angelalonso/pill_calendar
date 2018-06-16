import React, { Component } from 'react';
import { StyleSheet, View, Text, AsyncStorage } from 'react-native';
 
import TimePicker from 'react-native-simple-time-picker';
 
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
 
export default class GetTime extends Component {
  constructor(props) {
    super(props);
    this.state = {
        myKey: null
    }
    this.onChange = this.changeTime.bind(this);
  }
  async getKey() {
    try {
      const value = await AsyncStorage.getItem('@MySuperStore:key');
      this.setState({myKey: value});
    } catch (error) {
      console.log("Error retrieving data" + error);
    }
  }

  async saveKey(value) {
    try {
      await AsyncStorage.setItem('@MySuperStore:key', value);
    } catch (error) {
      console.log("Error saving data" + error);
    }
  }

  async resetKey() {
    try {
      await AsyncStorage.removeItem('@MySuperStore:key');
      const value = await AsyncStorage.getItem('@MySuperStore:key');
      this.setState({myKey: value});
    } catch (error) {
      console.log("Error resetting data" + error);
    }
  }

  state = {
    selectedHours: 0,
    selectedMinutes: 0,
  }

  changeTime(hours, minutes) {
    this.saveKey(minutes.toString());
    this.setState({ selectedHours: hours, selectedMinutes: minutes });
    console.log(this.state);

  }
 
  render() {
    const { selectedHours, selectedMinutes } = this.state;
    return (
      <View style={styles.container}>
        <Text>{selectedHours}:{selectedMinutes}</Text>
        <TimePicker
          selectedHours={selectedHours}
          selectedMinutes={selectedMinutes}
          onChange={
            (hours, minutes) => this.changeTime(hours, minutes)
          }
        />
      </View>
    );
  }
}
