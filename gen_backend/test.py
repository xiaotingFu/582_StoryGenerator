
def get_book_pairs():
    """
    select story from database make sure all combinition has more than three titles

    get the book combinition that has the most stories

    return a list of books    
    """
    import collections
    import sqlite3
    conn = sqlite3.connect('../db/db.sqlite3')
    sql = "select book1, book2, count(*) from Story group by book1, book2 HAVING count(*)> 5 ORDER BY count(*) DESC;"
    cursor = conn.execute(sql)
    # build a graph for book pairs
    # bookpairs = collections.defaultdict(list)
    print("Top 10 books")
    count = 0
    books= []
    for row in cursor: 
            book1, book2, occ = row[0], row[1], str(row[2])
            # print(book1 + " : " + book2 + " appears " + occ + " times")
            pair = [book1, book2]
            pair.sort()
            books.append(pair)
            count += 1 
    print(len(books))

    conn.close()
    return books
get_book_pairs()
