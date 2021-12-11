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
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    keyword = _fetchKeyword();
  }

  Future<Keyword> _fetchKeyword() async {
    final res = await http.get(Uri.parse(
        'http://110.13.200.51:5000/recommendation/' + widget.searchKeyword));

    if (res.statusCode == 200) {
      setState(() {
        isLoading = true;
      });
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

    return SafeArea(
        child: Scaffold(
            appBar: AppBar(
                title: const Text("My Test APP"),
                backgroundColor: Colors.deepPurple,
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
                        margin: EdgeInsets.fromLTRB(
                            10, height * 0.35, 10, height * 0.05),
                        height: 50,
                        child: ListView.separated(
                          scrollDirection: Axis.horizontal,
                          itemBuilder: (context, index) {
                            if (!selectedKeyword.contains(index)) {
                              return Container(
                                margin:
                                    const EdgeInsets.fromLTRB(10, 10, 10, 10),
                                child: ElevatedButton(
                                    style: ButtonStyle(backgroundColor:
                                        MaterialStateProperty.resolveWith(
                                            (states) {
                                      return Colors.deepPurple;
                                    })),
                                    onPressed: () {
                                      setState(() {
                                        selectedKeyword.add(index);
                                      });
                                    },
                                    child: Text(snapshot.data!.keywords[index]
                                        .toString())),
                              );
                            }
                            return Container();
                          },
                          itemCount: snapshot.data!.keywords.length,
                          separatorBuilder: (BuildContext context, int index) =>
                              const Divider(),
                        )),
                    IconButton(
                        onPressed: () {
                          List<String> keywords_ = [];
                          selectedKeyword.map((index) {
                            keywords_.add(oriKeyword.keywords[index]);
                          });
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => ProductScreen(
                                      keywords: keywords_,
                                      books: oriKeyword.books)));
                        },
                        icon: const Icon(Icons.skip_next)),
                    Container(
                        margin: const EdgeInsets.fromLTRB(10, 0, 10, 0),
                        height: 50,
                        child: ListView.separated(
                          scrollDirection: Axis.horizontal,
                          itemBuilder: (context, index) {
                            if (selectedKeyword.contains(index)) {
                              return Container(
                                margin:
                                    const EdgeInsets.fromLTRB(10, 10, 10, 10),
                                child: ElevatedButton(
                                    style: ButtonStyle(backgroundColor:
                                        MaterialStateProperty.resolveWith(
                                            (states) {
                                      return Colors.blue;
                                    })),
                                    onPressed: () {
                                      setState(() {
                                        selectedKeyword.remove(index);
                                      });
                                    },
                                    child: Text(
                                        oriKeyword.keywords[index].toString())),
                              );
                            }
                            return Container();
                          },
                          itemCount: oriKeyword.keywords.length,
                          separatorBuilder: (BuildContext context, int index) =>
                              const Divider(),
                        ))
                  ]);
                } else if (snapshot.hasError) {
                  return Text("${snapshot.error}");
                }

                return const CircularProgressIndicator(
                  color: Colors.deepPurple,
                );
              },
            )),
            floatingActionButton: FloatingActionButton(
              onPressed: () {
                Navigator.push(context,
                    MaterialPageRoute(builder: (context) => HomeScreen()));
              },
              child: const Icon(Icons.arrow_back),
              backgroundColor: Colors.purple,
            )));
  }
}
