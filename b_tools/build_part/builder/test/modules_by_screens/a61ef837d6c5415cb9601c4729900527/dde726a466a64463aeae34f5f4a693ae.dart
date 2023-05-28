import 'package:flutter/material.dart';

class dde726a466a64463aeae34f5f4a693ae extends StatelessWidget implements PreferredSizeWidget{
  const dde726a466a64463aeae34f5f4a693ae({super.key});

  @override 
  final Size preferredSize = const Size.fromHeight(50); 

  @override
  Widget build(BuildContext context){
    return AppBar(
      title:
Container(
    padding: const EdgeInsets.only(left: 0.0, top: 0.0, right: 0.0, bottom: 0.0),
    margin: const EdgeInsets.only(left: 0.0, top: 0.0, right: 0.0, bottom: 0.0),
    alignment: Alignment.center,
    child: const Text("Settings",
        style: TextStyle(
            fontSize: 24
        ),),
),       backgroundColor: Color(0xffffffff),
      foregroundColor: Color(0xff000000)
    ); 
  }
}