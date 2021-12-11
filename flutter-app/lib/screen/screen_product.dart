import 'package:app/model/model_product.dart';
import 'package:app/screen/screen_detail.dart';
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

    return SafeArea(
        child: Scaffold(
            appBar: AppBar(
                title: const Text("My Test APP"),
                backgroundColor: Colors.deepPurple,
                leading: Container()),
            body: Center(
                child: FutureBuilder<List<Product>>(
              future: products,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  return Column(children: [
                    Container(
                        margin: const EdgeInsets.all(15),
                        child: const Text("추천 도서",
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 40,
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
                                            bookId: snapshot.data![index].id)));
                              },
                              child: Container(
                                  margin:
                                      const EdgeInsets.fromLTRB(10, 10, 10, 10),
                                  child: Column(children: <Widget>[
                                    SizedBox(
                                        width: width * 0.4,
                                        child: Image.network(snapshot
                                            .data![index].cover
                                            .toString())),
                                    Container(
                                        margin: const EdgeInsets.fromLTRB(
                                            10, 10, 10, 10),
                                        child: Text(
                                            snapshot.data![index].title
                                                .toString(),
                                            style:
                                                const TextStyle(fontSize: 30))),
                                    Container(
                                        margin: const EdgeInsets.fromLTRB(
                                            5, 5, 5, 5),
                                        child: Text(
                                            snapshot.data![index].author
                                                .toString(),
                                            style:
                                                const TextStyle(fontSize: 20))),
                                    Container(
                                        margin: const EdgeInsets.fromLTRB(
                                            5, 5, 5, 5),
                                        child: Text(
                                            snapshot.data![index].price
                                                    .toString() +
                                                "원",
                                            style:
                                                const TextStyle(fontSize: 20))),
                                  ])));
                        },
                        itemCount: snapshot.data!.length,
                        separatorBuilder: (BuildContext context, int index) =>
                            const Divider(),
                      ),
                    )
                  ]);
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
