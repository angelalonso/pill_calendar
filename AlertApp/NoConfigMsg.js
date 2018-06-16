'use strict';

import React, { Component } from 'react';
import {
  Button,
  StyleSheet,
  Text,
  View,
} from 'react-native';


export default class NoConfigMsg extends Component<{}> { 
  _onGoPressed = () => { 
    this.props.navigation.navigate('GetTime');
  }; 

  render() {
    return (
      <View  style={styles.container}>
        <Text style={styles.description}>
          Hola! Parece que no tienes nada configurado todavia. Haz Click para empezar.
        </Text> 
        <Button
          onPress={this._onGoPressed}
          color='#48BBEC'
          title='Empezar'
        />
      </View>
    )
  }
};

const styles = StyleSheet.create({
  description: {
    marginBottom: 20,
    fontSize: 18,
    textAlign: 'center',
    color: '#656565'
  },
  container: {
    padding: 30,
    marginTop: 65,
    alignItems: 'center'
  },
 
});                      
