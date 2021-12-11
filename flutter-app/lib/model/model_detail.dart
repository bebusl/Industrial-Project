class Detail {
  String title;
  String intro;
  String contents;
  String author;
  String price;

  Detail(
      {required this.title,
      required this.intro,
      required this.contents,
      required this.author,
      required this.price});

  factory Detail.fromJson(Map<String, dynamic> json) {
    var intro = "";
    var contents = "";

    try {
      intro = json['intro'];
    } on Error catch (_, err) {}

    try {
      contents = json['contents'];
    } on Error catch (_, err) {}

    return Detail(
        title: json['title'],
        intro: intro,
        contents: contents,
        author: json['author'],
        price: json['price']);
  }
}
