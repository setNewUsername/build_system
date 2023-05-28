import 'package:flutter/material.dart';
import 'package:test/commons/root_widget.dart';

class a8c85f92b8e04b5eb0511111d87277ad extends StatelessWidget{
  final String footerParentScreenId; 

  const a8c85f92b8e04b5eb0511111d87277ad({super.key, required this.footerParentScreenId});

  void leedToScreen(context, scrId){
    if(footerParentScreenId != scrId){
        Widget? newScr = ScreenRootInheritedWidget.of(context).scrnNav.getScreen(scrId);
        if(newScr != null){
          Navigator.push(
            context,
          MaterialPageRoute(builder: (context) => newScr),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context){
    return Container(
      height: 60,
      padding: const EdgeInsets.only(left: 0.0, top: 0.0, right: 0.0, bottom: 0.0),
      margin: const EdgeInsets.only(left: 0.0, top: 0.0, right: 0.0, bottom: 0.0),
      color: Color(0xffffffff),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
Container(
    height: 50,
    width: 50,
    margin: const EdgeInsets.only(left: 0.0, top: 0.0, right: 0.0, bottom: 0.0),
    child: ElevatedButton(
    onPressed: (){
        leedToScreen(context, "afdfe2e077ae43f8afda3c993d728484");
    },
    style: ButtonStyle(
        backgroundColor: MaterialStateProperty.all(Color(
            0xff000000
        )),
        side: MaterialStateProperty.all(const BorderSide(color: Color(
            0xff000000
        )))
    ),
    child: Container(
        alignment: Alignment.center,
        child: const Text(
            "M",
            style: TextStyle(
                color: Color(
                    0xffffffff
                ), 
                fontSize: 16
            ))
        )
    ),
),Container(
    height: 50,
    width: 50,
    margin: const EdgeInsets.only(left: 0.0, top: 0.0, right: 0.0, bottom: 0.0),
    child: ElevatedButton(
    onPressed: (){
        leedToScreen(context, "a61ef837d6c5415cb9601c4729900527");
    },
    style: ButtonStyle(
        backgroundColor: MaterialStateProperty.all(Color(
            0xff000000
        )),
        side: MaterialStateProperty.all(const BorderSide(color: Color(
            0xff000000
        )))
    ),
    child: Container(
        alignment: Alignment.center,
        child: const Text(
            "S",
            style: TextStyle(
                color: Color(
                    0xfffdfdfd
                ), 
                fontSize: 16
            ))
        )
    ),
),Container(
    height: 50,
    width: 50,
    margin: const EdgeInsets.only(left: 0.0, top: 0.0, right: 0.0, bottom: 0.0),
    child: ElevatedButton(
    onPressed: (){
        leedToScreen(context, "a1575d76ec854a819d4f875cee900047");
    },
    style: ButtonStyle(
        backgroundColor: MaterialStateProperty.all(Color(
            0xff000000
        )),
        side: MaterialStateProperty.all(const BorderSide(color: Color(
            0xff000000
        )))
    ),
    child: Container(
        alignment: Alignment.center,
        child: const Text(
            "B",
            style: TextStyle(
                color: Color(
                    0xffffffff
                ), 
                fontSize: 16
            ))
        )
    ),
),         ],
      ),
    );
  }
}