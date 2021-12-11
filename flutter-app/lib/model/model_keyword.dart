class Keyword {
  List<String> keywords;
  List<String> books;

  Keyword({required this.keywords, required this.books});

  factory Keyword.fromJson(Map<String, dynamic> json) {
    try {
      return Keyword(
          keywords: json['keywords'].cast<String>(),
          books: json['books'].cast<String>());
    } on Error catch (_, ex) {
      return Keyword(keywords: [], books: []);
    }
  }
}
