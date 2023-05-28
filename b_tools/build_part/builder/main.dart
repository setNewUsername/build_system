import 'package:flutter/material.dart';

import 'package:test/controls/screen_navigator.dart';
import 'package:test/commons/root_widget.dart';
import 'package:test/controls/screen_handler.dart';

void main() => runApp(ScreenRootInheritedWidget(scrnNav: ScreenNavigator(), child: const MyApp()));

class MyApp extends StatelessWidget{
  static ScreenHandler scrHand = const ScreenHandler();

  const MyApp({super.key});

  @override
  Widget build(BuildContext context){
    
ScreenRootInheritedWidget.of(context).scrnNav.addScreen("afdfe2e077ae43f8afda3c993d728484", scrHand.getafdfe2e077ae43f8afda3c993d728484Screen);
ScreenRootInheritedWidget.of(context).scrnNav.addScreen("a61ef837d6c5415cb9601c4729900527", scrHand.geta61ef837d6c5415cb9601c4729900527Screen);
ScreenRootInheritedWidget.of(context).scrnNav.addScreen("a1575d76ec854a819d4f875cee900047", scrHand.geta1575d76ec854a819d4f875cee900047Screen);
 
    return MaterialApp(
      title: 'Test app',
      home: ScreenRootInheritedWidget.of(context).scrnNav.getStartScreen(),
    );
  }
}