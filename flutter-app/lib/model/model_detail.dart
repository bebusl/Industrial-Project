class Detail {
  String title;
  String author;
  String price;

  Detail({required this.title, required this.author, required this.price});

  factory Detail.fromJson(Map<String, dynamic> json) {
    return Detail(
        title: json['title'], author: json['author'], price: json['price']);
  }
}
