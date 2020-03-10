import sys, time, threading, nltk, json
from nltk import word_tokenize
from nltk.corpus import wordnet

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            #for cursor in '|/-\\': yield cursor
            for cursor in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)
        
def remove_stop_words(line):
    tokens = word_tokenize(line)
    print("Actual text:", tokens)
    # Remove stop words
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    words = [w for w in tokens if not w in stop_words]
    print("Relevant text:", words)
    return words

def write_significant_terms_json(file_name, passed_list):
    import os
    #check if the file already exists
    #exists = os.path.isfile('/path/to/file')
    exists = os.path.isfile('./json_data/'+file_name+'.json')
    if exists: # Json file already exists
        print("Saving significant terms to an existing file "+file_name+".json...")
        #load existing dictionary and add new values to it
        with open('./json_data/'+file_name+'.json') as f:
            dic = json.load(f)
            f.close
            final_dic =  list(set(dic + passed_list))
            #print("Final->", final_dic)
            #print("Writing new data to file...")
            with open('./json_data/'+file_name+'.json', 'w') as f:
                json.dump(final_dic, f)
    else: # write dictionary into a json object
        print("Saving significant terms to a new file "+file_name+".json...")
        with open('./json_data/'+file_name+'.json', 'w') as f:
            json.dump(passed_list, f)

list1, list2, = [], []
def remove_insignificant_words(list1, list2):
    similar_list = []
    for word1 in list1:
        for word2 in list2:
            wordFromList1 = wordnet.synsets(word1)
            wordFromList2 = wordnet.synsets(word2)
            if wordFromList1 and wordFromList2: 
                s = wordFromList1[0].wup_similarity(wordFromList2[0])
                if s != None:
                    if s >= 0.8:
                        #print("High similarity found->", wordFromList1[0], "and", wordFromList2[0], "=", s)
                        similar_list.append(word2)
    return similar_list

def find_similar_words(x):
    for i in range(0, len(x)):
        list1, list2 = [], []
        list1.append(x[i])
        y = word_vectors.most_similar(x[i])
        #print("\nf. Writing tokens to Malik_Adeel1.txt file...", end=' ')
        print("\nSimilar words for", (x[i]),":")
        for j in range(0, len(y)):
            print(y[j][0], end=", ")#pick first part only, 2nd is value
            list2.append(y[j][0])
        significant_list = remove_insignificant_words(list1, list2)
        print()
        print("Most significant words for", x[i], "->", significant_list)
        # write dictionary into a json object
        write_significant_terms_json(x[i], significant_list)
        #with open(x[i]+'.json', 'w') as f:
        #    json.dump(sl, f)
    print("--------------------------------------------------------------------")
    print()

spinner = Spinner()
#spinner.start()
# ... some long-running operations
#time.sleep(5) 
#spinner.stop()

#conda install -c anaconda gensim
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
# Load data from bin to text file fir the first time.

print("Loading Google word2vec...")
spinner.start()
word_vectors = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary= True)
spinner.stop()
print("...Loaded!!")
#word_vectors.save_word2vec_format('GoogleNews.txt', binary=False)
#model = Word2Vec.load("GoogleNews.txt")

print("\nProcessing words...")
line = "Husky sleeping on the grass"
x = remove_stop_words(line)
#x = ['Husky sleeping on the grass','Husky','Sleeping','on', 'the']
find_similar_words(x)

line = "Assassin bug on the leaf"
x = remove_stop_words(line)
find_similar_words(x)

line = "Black bear fishing"
x = remove_stop_words(line)
find_similar_words(x)

line = "Running dog"
x = remove_stop_words(line)
find_similar_words(x)
#load JSON into dictionary
#with open('my_dict.json') as f:
#    my_dict = json.load(f)
