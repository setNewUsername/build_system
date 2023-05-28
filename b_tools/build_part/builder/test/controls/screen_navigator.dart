import 'package:flutter/material.dart';

class ScreenNavigator{
  Map<String, Function> screensIds = <String, Function>{};
  final String startScreenId = "afdfe2e077ae43f8afda3c993d728484";

  ScreenNavigator();

  void addScreen(String newScreen, Function screenGetFunction){
    screensIds[newScreen] = screenGetFunction;
  }

  Widget? getScreen(String targetScreenId){
      return screensIds[targetScreenId] == null ? null : screensIds[targetScreenId]!.call();
  }

  Widget getStartScreen(){
    return screensIds[startScreenId] == null ? null : screensIds[startScreenId]!.call(); 
  }
}