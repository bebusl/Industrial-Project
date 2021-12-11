class Detail {
  String title;
  String intro;
  String contents;
  String author;
  String price;
  List<Map<String, dynamic>> reveiws;

  Detail(
      {required this.title,
      required this.intro,
      required this.contents,
      required this.author,
      required this.price,
      required this.reveiws});

  factory Detail.fromJson(Map<String, dynamic> json) {
    var intro = "";
    var contents = "";
    var bookInfo = json['book_info'];
    List<Map<String, dynamic>> reviews =
        json['reviews'].cast<Map<String, dynamic>>();

    try {
      intro = bookInfo['intro'];
    } on Error catch (_, err) {}

    try {
      contents = bookInfo['contents'];
    } on Error catch (_, err) {}

    return Detail(
        title: bookInfo['title'],
        intro: intro,
        contents: contents,
        author: bookInfo['author'],
        price: bookInfo['price'],
        reveiws: reviews);
  }
}
