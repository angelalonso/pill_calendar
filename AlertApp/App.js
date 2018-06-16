'use strict';                                                                                                                                                                                         

import {
  StyleSheet,
} from 'react-native';
import {
  StackNavigator,
} from 'react-navigation';
import NoConfigMsg from './NoConfigMsg';
import GetTime from './GetTime';
 
const App = StackNavigator({
  Home: { screen: NoConfigMsg },
  GetTime: { screen: GetTime },
});
export default App;
 
