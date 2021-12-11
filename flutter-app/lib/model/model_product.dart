class Product {
  String id;
  String title;
  String cover;
  String author;
  String price;

  Product(
      {required this.id,
      required this.title,
      required this.cover,
      required this.author,
      required this.price});

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
        id: json["_id"],
        title: json['title'],
        cover: json['cover'],
        author: json['author'],
        price: json['price']);
  }
}
