import os
import math
import re
import operator

def extract_corpus(corpus_dir = "articles"):
    """
    Returns a corpus of articles from the given directory.

    Args:
        corpus_dir (str): The location of the corpus.

    Returns:
        dict: A dictionary with key = title of the article,
              value = list of words in the article
    """
    corpus = {}
    num_documents = 0
    for filename in os.listdir(corpus_dir):
        with open(os.path.join(corpus_dir, filename)) as f:
            corpus[filename] = re.sub("[^\w]", " ",  f.read()).split()
    return corpus

class SearchEngine(object):
    """
    Represents an instance of a search engine. Instances of the search engine are
    initialized with a corpus.

    Args:
        corpus (dict): A dictionary of (article title, article text) pairs.
    """
    def __init__(self, corpus):
        # The corpus of (article title, article text) pairs.
        self.corpus = corpus
        # Has The Document name as key and value as a Dict containing words and their frequency
        self.count = {}
        # counts number of documents a word appears in key is word value is the count of documents
        df = {}
        self.num_docs = len(corpus)
        self.idf = {}
        for doc in corpus.keys():
            cnt = {}
            for word in corpus[doc]:
                word = word.lower()
                if word in cnt:
                    cnt[word] = cnt[word] + 1
                else:
                    df.setdefault(word, 0)
                    df[word] += 1
                    cnt[word] = 1
            self.count[doc] = cnt

        for word in df:
            self.idf[word] = math.log(self.num_docs/df[word])

    def inner_product(self, title, doc, count, flagidf):
        scr = 0
        commonwords = (set(self.count.get(title).keys()) & set(self.count.get(doc).keys()))
        for word in commonwords:
            inprod = 0
            inprod = inprod + (self.count.get(title).get(word) * self.count.get(doc).get(word))
            if (flagidf == True):
                # Need to multiply inverse 2 times because we are using two count frequency vectors so twice inverse
                inprod = inprod * (self.idf.get(word))**2
            scr = scr + inprod
        return scr

    def distance(self, title, count, flagidf):
        score = {}
        for doc in corpus.keys():
            if (doc != title):
                numerator = self.inner_product(title, doc, self.count, flagidf)
                deno1 = self.inner_product(doc, doc, self.count, flagidf)
                deno2 = self.inner_product(title, title, self.count, flagidf)
                score[doc] = math.acos(min(numerator / (math.sqrt(deno1 * deno2)), 1))

        sortedscore = sorted(score.items(), key=operator.itemgetter(1))
        return sortedscore

    def get_relevant_articles_doc_dist(self, title, k):
        """
        Returns the articles most relevant to a given document, limited to at most
        k results. Uses the normal document distance score.

        Args:
            title (str): The title of the article being queried (assume it exists).


        Returns:
            An array of the k most relevant (article title, document distance) pairs, ordered
            by decreasing relevance.

            Specifications:
                * Case is ignored entirely
                * If two articles have the same distance, titles should be in alphabetical order
        """
        # TODO: Implement this for part (a)
        sortedscore = self.distance(title, self.count, False)
        print(sortedscore)
        return sortedscore[:k]

    def get_relevant_articles_tf_idf(self, title, k):
        """
        Returns the articles most relevant to a given document, limited to at most
        k results. Uses the document distance with TF-IDF scores.

        Args:
            title (str): The title of the article being queried (assume it exists).

        Returns:
            An array of the k most relevant (article title, document distance) pairs, ordered
            by decreasing relevance.

            Specifications:
                * Case is ignored entirely
                * If two articles have the same distance, titles should be in alphabetical order
        """
        # TODO: Implement this for part (b)
        sortedscore = self.distance(title, self.count, True)
        print(sortedscore)
        return sortedscore[:k]


    def search(self, query, k):
        """
        Returns the articles most relevant to a given query, limited to at most
        k results.

        Args:
            query (str): The query for the search engine. Doesn't contain any special characters.

        Returns:
            An array of the k best (article title, tf-idf score) pairs, ordered by decreasing score.

            Specifications:
                * Only consider articles with a positive tf-idf score.
                * If there are fewer than k results with a positive tf-idf score, return those results.
                  If there are more, return only the k best results.
                * If two articles have the same score, titles should be in alphabetical order
        """
        # TODO: Implement this for part (c)
        score = {}

        for doc in corpus:
            scr = 0
            for queryword in set(query.lower().split()):
                idf = self.idf.get(queryword, 0)
                termfreq = self.count.get(doc).get(queryword, 0)
                scr =scr + idf*termfreq
            score[doc] = scr

        sortedscore = sorted(score.items(), key=operator.itemgetter(1))
        print(sortedscore)
        if(len(sortedscore)<k):
            return sortedscore
        else:
            return sortedscore[len(sortedscore)-k:len(sortedscore)][::-1]


if __name__ == '__main__':
    corpus = extract_corpus()
    e = SearchEngine(corpus)
    print("Welcome to 6006LE! We hope you have a wonderful experience. To exit, type 'exit.'")
    print("\nSuggested searches: the yummiest fruit in the world, child prodigy, operating system, red tree, coolest algorithm....")
    while True:
        query = input('\nEnter query here: ').strip()
        if query == "exit":
            print("Good bye!")
            break

        results = e.search(query, 5)
        if len(results) == 0:
            print("There are no results for that query. :(")
        else:
            print("Top results: ")
            for title, score in results:
                print("    - %s (score %f)" % (title, score))
