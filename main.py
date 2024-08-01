import re


def get_sentence_lists(text):
  sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
  sentences = [
      re.findall(r'\b\w+\b', sentence.lower()) for sentence in sentences
  ]
  return sentences


def get_sentence_lists_from_files(filenames):
  sentences = []
  for filename in filenames:
    with open(filename, 'r') as file:
      sentences += get_sentence_lists(file.read())  #concatenate sentences

  return sentences


def build_semantic_descriptors(sentences):
  cooccur = {}
  for sentence in sentences:
    for word in sentence:
      if word:
        if word not in cooccur:
          cooccur[word] = {}
        for other_word in sentence:
          if other_word != word:
            cooccur[word][other_word] = cooccur[word].get(other_word, 0) + 1
  return cooccur


def most_similar_word(word, choices, semantic_descriptors):
  max_count = 0
  most_similar = "none"
  if word in semantic_descriptors:
    word_cooccur = semantic_descriptors[word]
    for choice in choices:
      if choice in word_cooccur and word_cooccur[choice] > max_count:
        max_count = word_cooccur[choice]
        most_similar = choice
  return most_similar


def run_similarity_test(filename, semantic_descriptors):
  with open(filename, 'r') as file:
    lines = file.readlines()

  correct_count = 0
  total = 0

  for line in lines:
    words = line.strip().split(",")
    word = words[0]
    correct = words[1]
    choices = words[2:]  # get 2nd element up to last for choices
    choices = [choice.strip() for choice in choices]  # cleanup choices
    answer = most_similar_word(word, choices, semantic_descriptors)
    total += 1
    if (answer == correct):
      correct_count += 1
      print(f"{word}: {answer}, correct!")
    else:
      print(f"{word}: {answer}, incorrect!")

  return correct_count / total


def main():

  # train the program by making it read through text
  sentence_list = get_sentence_lists_from_files(
      ['thesaurus.txt', 'langley.txt', 'constitution.txt'])
  #build a nested dictionary with count of word co-occurrences
  semantic_descriptors = build_semantic_descriptors(sentence_list)
  result = run_similarity_test("test.txt", semantic_descriptors)
  print(f"Your score is: {(result * 100.0):.2f}%")


main()
