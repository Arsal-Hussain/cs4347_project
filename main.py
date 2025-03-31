from lib.search import search_books

results = search_books("will")

if not results:
    print("No results found.")
else:
    for i, row in enumerate(results, 1):
        print(f"{i:02}. {row['Isbn']} | {row['Title']} | {row['Authors']} | {row['Status']}")
