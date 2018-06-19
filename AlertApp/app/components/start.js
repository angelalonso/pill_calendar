import React, { Component } from 'react';
import {  
  StyleSheet,
  Text,   
  View,   
} from 'react-native';

import { connect } from 'react-redux'; 

class Start extends Component {
  constructor(props) {
    super(props);

    this.state = {};

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
                <Text style={[styles.text]}>
                  Save
                </Text>
              </View>
          );
      }
  }
};
 
//Connect everything
export default connect()(Start);
 
const styles = StyleSheet.create({                                                                                                                                                                    
    container:{
        flex:1,
        backgroundColor: '#F5F5F5'
    },
    text:{
        fontWeight: "500",
        backgroundColor: '#F5F5F5'
    },
});
