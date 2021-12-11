import 'package:app/screen/screen_keyword.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String searchKeyword = "";

  Future<bool> _onWillPop() async {
    return (await showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Are you sure?'),
            content: const Text('Do you want to exit an App'),
            actions: <Widget>[
              TextButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: const Text('No'),
              ),
              TextButton(
                onPressed: () =>
                    SystemChannels.platform.invokeMethod('SystemNavigator.pop'),
                child: const Text('Yes'),
              ),
            ],
          ),
        )) ??
        false;
  }

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double width = screenSize.width;
    double height = screenSize.height;

    return WillPopScope(
        onWillPop: _onWillPop,
        child: SafeArea(
            child: Scaffold(
          backgroundColor: const Color.fromRGBO(0xF8, 0xFF, 0xEA, 1),
          appBar: AppBar(
              title: const Text("My Test APP"),
              backgroundColor: Colors.blue,
              leading: Container()),
          body: Center(
              child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: <Widget>[
                Container(
                    margin: EdgeInsets.fromLTRB(0, 0, 0, height * 0.03),
                    child: const Center(
                        child: Text("책 추천 받아라.",
                            style: TextStyle(
                              fontSize: 40,
                              fontWeight: FontWeight.bold,
                            )))),
                Container(
                    margin: EdgeInsets.fromLTRB(0, 0, 0, height * 0.1),
                    child: const Center(
                        child: Text("키워드 기반 책 추천 서비스.",
                            style:
                                TextStyle(fontSize: 15, color: Colors.grey)))),
                SizedBox(
                  width: width * 0.8,
                  child: TextField(
                    onChanged: (text) {
                      setState(() {
                        searchKeyword = text;
                      });
                    },
                    decoration: const InputDecoration(
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10.0)),
                        borderSide: BorderSide(color: Colors.grey),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10.0)),
                        borderSide: BorderSide(color: Colors.blue),
                      ),
                      border: OutlineInputBorder(),
                      labelText: '찾고싶은 책의 키워드를 입력하세요.',
                    ),
                  ),
                ),
                SizedBox(
                    width: width * 0.8,
                    child: ElevatedButton.icon(
                      style: ButtonStyle(
                        shape:
                            MaterialStateProperty.all<RoundedRectangleBorder>(
                                RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10.0),
                        )),
                      ),
                      onPressed: () {
                        Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => KeywordScreen(
                                      searchKeyword: searchKeyword,
                                    )));
                      },
                      icon: const Icon(Icons.search, size: 18),
                      label: const Text("책 추천 받기"),
                    )),
                Padding(
                  padding: EdgeInsets.fromLTRB(0, 0, 0, height * 0.1),
                )
              ])),
        )));
  }
}
