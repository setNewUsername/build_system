import 'package:flutter/material.dart';

import 'package:test/modules_by_screens/a61ef837d6c5415cb9601c4729900527/fa62a4b1e1b34cc6992d3f6365b3db11.dart';
import 'package:test/modules_by_screens/a61ef837d6c5415cb9601c4729900527/dde726a466a64463aeae34f5f4a693ae.dart';
import 'package:test/modules_by_screens/a61ef837d6c5415cb9601c4729900527/a8c85f92b8e04b5eb0511111d87277ad.dart';

class a61ef837d6c5415cb9601c4729900527 extends StatelessWidget{
  static String screenId = 'a61ef837d6c5415cb9601c4729900527';

  const a61ef837d6c5415cb9601c4729900527({super.key});

  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: const dde726a466a64463aeae34f5f4a693ae(),
      bottomNavigationBar: a8c85f92b8e04b5eb0511111d87277ad(footerParentScreenId: screenId),
      body: const fa62a4b1e1b34cc6992d3f6365b3db11()
    );
  }
}