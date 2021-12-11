import 'package:app/model/model_detail.dart';
import 'package:app/model/model_product.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class DetailScreen extends StatefulWidget {
  late String bookId;
  String tempCover;
  DetailScreen({required this.bookId, required this.tempCover});

  @override
  _DetailScreen createState() => _DetailScreen();
}

class _DetailScreen extends State<DetailScreen> {
  late Future<Detail> detail;

  @override
  void initState() {
    super.initState();
    detail = _fetchDetail();
  }

  Future<Detail> _fetchDetail() async {
    final res = await http
        .get(Uri.parse('http://110.13.200.51:5000/book/' + widget.bookId));

    if (res.statusCode == 200) {
      var result = Detail.fromJson(
          json.decode(utf8.decode(res.bodyBytes))['data']['book_info']);
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
                child: FutureBuilder<Detail>(
              future: detail,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  return Container(
                      margin: EdgeInsets.fromLTRB(
                          width * 0.05, height * 0.05, width * 0.05, 0),
                      child: Column(children: [
                        SizedBox(
                            width: width * 0.6,
                            child: Image.network(widget.tempCover)),
                        Padding(padding: EdgeInsets.all(height * 0.02)),
                        Container(
                            margin: const EdgeInsets.fromLTRB(10, 10, 10, 10),
                            child: Text(snapshot.data!.title.toString(),
                                style: const TextStyle(fontSize: 30))),
                        Container(
                            margin: const EdgeInsets.fromLTRB(10, 10, 10, 10),
                            child: Text(
                                snapshot.data!.intro.isEmpty
                                    ? "책 소개가 존재하지 않습니다."
                                    : snapshot.data!.intro.toString(),
                                style: const TextStyle(fontSize: 20))),
                        Container(
                            margin: const EdgeInsets.fromLTRB(5, 5, 5, 5),
                            child: Text(snapshot.data!.author.toString(),
                                style: const TextStyle(fontSize: 25))),
                        Container(
                            margin: const EdgeInsets.fromLTRB(5, 5, 5, 5),
                            child: Text(snapshot.data!.price.toString() + "원",
                                style: const TextStyle(fontSize: 25))),
                      ]));
                } else if (snapshot.hasError) {
                  return Text("${snapshot.error}");
                }

                return const CircularProgressIndicator(
                  color: Colors.deepPurple,
                );
              },
            ))));
  }
}
