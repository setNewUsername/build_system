import 'package:flutter/material.dart';

class a94cfdcf8f4f452db88bf4fc3c17371f extends StatelessWidget implements PreferredSizeWidget{
  const a94cfdcf8f4f452db88bf4fc3c17371f({super.key});

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
    child: const Text("Main menu",
        style: TextStyle(
            fontSize: 24
        ),),
),       backgroundColor: Color(0xffffffff),
      foregroundColor: Color(0xff000000)
    ); 
  }
}