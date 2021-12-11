import 'package:app/model/model_product.dart';
import 'package:app/screen/screen_detail.dart';
import 'package:app/screen/screen_home.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ProductScreen extends StatefulWidget {
  List<String> books;
  List<String> keywords;
  ProductScreen({required this.books, required this.keywords});

  @override
  _ProductScreen createState() => _ProductScreen();
}

class _ProductScreen extends State<ProductScreen> {
  late Future<List<Product>> products;

  @override
  void initState() {
    super.initState();
    products = _fetchProducts();
  }

  Future<List<Product>> _fetchProducts() async {
    Map data = {"keywords": widget.keywords, "books": widget.books};
    var body = json.encode(data);

    final res = await http.post(
        Uri.parse('http://110.13.200.51:5000/recommendation/keywords'),
        headers: {"Content-Type": "application/json"},
        body: body);

    if (res.statusCode == 200) {
      final parsed = json
          .decode(utf8.decode(res.bodyBytes))['data']
          .cast<Map<String, dynamic>>();
      var result =
          parsed.map<Product>((json) => Product.fromJson(json)).toList();
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
                backgroundColor: const Color.fromRGBO(0xF8, 0xFF, 0xEA, 1),
                appBar: AppBar(
                    title: const Text("My Test APP"),
                    backgroundColor: Colors.blue,
                    leading: Container()),
                body: Center(
                    child: FutureBuilder<List<Product>>(
                  future: products,
                  builder: (context, snapshot) {
                    if (snapshot.hasData) {
                      return Column(children: [
                        Container(
                            alignment: Alignment.centerLeft,
                            margin: const EdgeInsets.fromLTRB(30, 15, 15, 15),
                            child: const Text("추천 도서",
                                style: TextStyle(
                                  color: Colors.black,
                                  fontWeight: FontWeight.w500,
                                  fontSize: 35,
                                ))),
                        Expanded(
                          child: ListView.separated(
                            itemBuilder: (context, index) {
                              return GestureDetector(
                                  onTap: () {
                                    Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                            builder: (context) => DetailScreen(
                                                  bookId:
                                                      snapshot.data![index].id,
                                                  tempCover: snapshot
                                                      .data![index].cover
                                                      .toString(),
                                                )));
                                  },
                                  child: Container(
                                      margin: const EdgeInsets.fromLTRB(
                                          10, 10, 10, 10),
                                      child: Row(children: <Widget>[
                                        SizedBox(
                                            width: width * 0.3,
                                            //height: height * 0.10,
                                            child: Image.network(snapshot
                                                .data![index].cover
                                                .toString())),
                                        Container(
                                            height: height * 0.15,
                                            margin: EdgeInsets.fromLTRB(
                                                width * 0.05,
                                                height * 0.01,
                                                0,
                                                0),
                                            width: width * 0.5,
                                            child: Column(children: [
                                              Container(
                                                  alignment:
                                                      Alignment.centerLeft,
                                                  child: Text(
                                                      snapshot
                                                          .data![index].title
                                                          .toString(),
                                                      style: const TextStyle(
                                                          fontSize: 15,
                                                          fontWeight: FontWeight
                                                              .bold))),
                                              Container(
                                                  alignment:
                                                      Alignment.centerLeft,
                                                  margin: EdgeInsets.fromLTRB(
                                                      0,
                                                      height * 0.01,
                                                      0,
                                                      height * 0.01),
                                                  child: Text(
                                                      snapshot
                                                          .data![index].author
                                                          .toString(),
                                                      style: const TextStyle(
                                                          fontSize: 15))),
                                              Container(
                                                  alignment:
                                                      Alignment.centerLeft,
                                                  child: Text(
                                                      snapshot.data![index]
                                                              .price
                                                              .toString() +
                                                          "원",
                                                      style: const TextStyle(
                                                          fontSize: 15)))
                                            ]))
                                      ])));
                            },
                            itemCount: snapshot.data!.length,
                            separatorBuilder:
                                (BuildContext context, int index) =>
                                    const Divider(),
                          ),
                        )
                      ]);
                    } else if (snapshot.hasError) {
                      return Text("${snapshot.error}");
                    }

                    return const CircularProgressIndicator(
                      color: Colors.blue,
                    );
                  },
                )),
                floatingActionButton: FloatingActionButton(
                  onPressed: () {
                    Navigator.push(context,
                        MaterialPageRoute(builder: (context) => HomeScreen()));
                  },
                  child: const Icon(Icons.arrow_back),
                  backgroundColor: Colors.blue,
                ))));
  }
}
