import 'dart:async';
import 'package:app/model/model_keyword.dart';
import 'package:app/screen/screen_home.dart';
import 'package:app/screen/screen_product.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class KeywordScreen extends StatefulWidget {
  String searchKeyword;
  KeywordScreen({required this.searchKeyword});

  @override
  _KeywordScreen createState() => _KeywordScreen();
}

class _KeywordScreen extends State<KeywordScreen> {
  List<int> selectedKeyword = [];
  late Future<Keyword> keyword;
  late Keyword oriKeyword;

  @override
  void initState() {
    super.initState();
    keyword = _fetchKeyword();
  }

  Future<Keyword> _fetchKeyword() async {
    final res = await http.get(Uri.parse(
        'http://110.13.200.51:5000/recommendation/' + widget.searchKeyword));

    if (res.statusCode == 200) {
      var result = Keyword.fromJson(json.decode(utf8.decode(res.bodyBytes)));
      oriKeyword = result;
      if (oriKeyword.books.isEmpty) {
        Timer(const Duration(milliseconds: 2000), () {
          Navigator.push(
              context, MaterialPageRoute(builder: (context) => HomeScreen()));
        });
      }
      return result;
    } else {
      throw Exception('Failed to load post');
    }
  }

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double width = screenSize.width;
    double height = screenSize.height;

    return WillPopScope(
        onWillPop: () {
          return Future(() => false);
        },
        child: SafeArea(
            child: Scaffold(
                appBar: AppBar(
                    title: const Text("키북키북"),
                    backgroundColor: const Color.fromRGBO(0x78, 0x5D, 0x12, 1),
                    leading: Container()),
                body: Center(
                    child: FutureBuilder<Keyword>(
                  future: keyword,
                  builder: (context, snapshot) {
                    if (snapshot.hasData) {
                      if (snapshot.data!.books.isEmpty) {
                        return const Text("결과가 존재하지 않습니다.");
                      }
                      return Column(children: [
                        Container(
                            margin: const EdgeInsets.all(10),
                            child: const Text(
                              "선택된 키워드",
                              style: TextStyle(fontSize: 20),
                            )),
                        SizedBox(
                            //margin: const EdgeInsets.fromLTRB(10, 0, 10, 0),
                            height: 50,
                            child: ListView.separated(
                              scrollDirection: Axis.horizontal,
                              itemBuilder: (context, index) {
                                if (selectedKeyword.contains(index)) {
                                  return Container(
                                    margin: const EdgeInsets.fromLTRB(
                                        10, 10, 10, 10),
                                    child: ElevatedButton(
                                        style: ButtonStyle(backgroundColor:
                                            MaterialStateProperty.resolveWith(
                                                (states) {
                                          return const Color.fromRGBO(
                                              0x78, 0x5D, 0x12, 1);
                                        })),
                                        onPressed: () {
                                          setState(() {
                                            selectedKeyword.remove(index);
                                          });
                                        },
                                        child: Text(oriKeyword.keywords[index]
                                            .toString())),
                                  );
                                }
                                return const SizedBox.shrink();
                              },
                              itemCount: oriKeyword.keywords.length,
                              separatorBuilder:
                                  (BuildContext context, int index) =>
                                      const Divider(),
                            )),
                        SizedBox(
                            height: height * 0.65,
                            child: ListView.separated(
                                addRepaintBoundaries: false,
                                itemBuilder: (context, index) {
                                  if (!selectedKeyword.contains(index)) {
                                    return ElevatedButton(
                                        style: ButtonStyle(backgroundColor:
                                            MaterialStateProperty.resolveWith(
                                                (states) {
                                          return Colors.white;
                                        })),
                                        onPressed: () {
                                          setState(() {
                                            selectedKeyword.add(index);
                                          });
                                        },
                                        child: Text(
                                            snapshot.data!.keywords[index]
                                                .toString(),
                                            style: const TextStyle(
                                                color: Color.fromRGBO(
                                                    138, 138, 138, 1))));
                                  }
                                  return Visibility(
                                    child: Container(),
                                    visible: false,
                                  );
                                },
                                itemCount: snapshot.data!.keywords.length,
                                separatorBuilder:
                                    (BuildContext context, int index) {
                                  if (selectedKeyword.contains(index)) {
                                    return Visibility(
                                      child: Container(),
                                      visible: false,
                                    );
                                  }
                                  return const Divider(
                                    color: Colors.white,
                                  );
                                })),
                        Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              SizedBox(
                                width: width * 0.35,
                                child: ElevatedButton(
                                    style: ButtonStyle(backgroundColor:
                                        MaterialStateProperty.resolveWith(
                                            (states) {
                                      return Colors.white;
                                    })),
                                    onPressed: () {
                                      setState(() {
                                        selectedKeyword.clear();
                                      });
                                    },
                                    child: const Text(
                                      "초기화",
                                      style: TextStyle(
                                          color: Color.fromRGBO(
                                              0x78, 0x5D, 0x12, 1)),
                                    )),
                              ),
                              const Padding(padding: EdgeInsets.all(10)),
                              SizedBox(
                                  width: width * 0.35,
                                  child: ElevatedButton(
                                      style: ButtonStyle(backgroundColor:
                                          MaterialStateProperty.resolveWith(
                                              (states) {
                                        return const Color.fromRGBO(
                                            0x78, 0x5D, 0x12, 1);
                                      })),
                                      onPressed: () {
                                        List<String> keywords_ = [];
                                        for (int i = 0;
                                            i < selectedKeyword.length;
                                            i++) {
                                          keywords_.add(oriKeyword
                                              .keywords[selectedKeyword[i]]);
                                        }
                                        Navigator.push(
                                            context,
                                            MaterialPageRoute(
                                                builder: (context) =>
                                                    ProductScreen(
                                                        keywords: keywords_,
                                                        books:
                                                            oriKeyword.books)));
                                      },
                                      child: Text("결과보기")))
                            ])
                      ]);
                    } else if (snapshot.hasError) {
                      return Text("${snapshot.error}");
                    }

                    return const CircularProgressIndicator(
                      color: Color.fromRGBO(0x78, 0x5D, 0x12, 1),
                    );
                  },
                )),
                floatingActionButton: FloatingActionButton(
                  onPressed: () {
                    Navigator.push(context,
                        MaterialPageRoute(builder: (context) => HomeScreen()));
                  },
                  child: const Icon(Icons.arrow_back),
                  backgroundColor: const Color.fromRGBO(0x78, 0x5D, 0x12, 1),
                ))));
  }
}
