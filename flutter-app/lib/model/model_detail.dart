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
    return Detail(
        title: json['title'],
        intro: json['intro'],
        contents: json['contents'],
        author: json['author'],
        price: json['price']);
  }
}
