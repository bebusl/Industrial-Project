import 'package:app/screen/screen_keyword.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String searchKeyword = "";

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double width = screenSize.width;
    double height = screenSize.height;

    return SafeArea(
        child: Scaffold(
            appBar: AppBar(
                title: Text("My Test APP"),
                backgroundColor: Colors.deepPurple,
                leading: Container()),
            body: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: <Widget>[
                  Container(
                      margin: EdgeInsets.fromLTRB(0, 0, 0, height * 0.15),
                      child: const Center(
                          child: Text("찾고싶은 책의 키워드를 입력하세요.",
                              style: TextStyle(
                                fontSize: 30,
                                fontWeight: FontWeight.bold,
                              )))),
                  Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                    Container(
                      margin: EdgeInsets.fromLTRB(0, 0, width * 0.05, 0),
                      width: width * 0.7,
                      child: TextField(
                        onChanged: (text) {
                          setState(() {
                            searchKeyword = text;
                          });
                        },
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: '검색어',
                        ),
                      ),
                    ),
                    IconButton(
                        onPressed: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => KeywordScreen(
                                        searchKeyword: searchKeyword,
                                      )));
                        },
                        icon: const Icon(Icons.search)),
                  ]),
                  Padding(
                    padding: EdgeInsets.fromLTRB(0, 0, 0, height * 0.1),
                  )
                ])));
  }
}
